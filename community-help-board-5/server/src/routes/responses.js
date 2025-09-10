const router = require('express').Router({ mergeParams: true });
const { requireAuth } = require('../middleware/auth');
const Response = require('../models/Response');
const HelpRequest = require('../models/HelpRequest');
const { notify } = require('../services/notify');
const { addPoints } = require('../services/points');

// Create response (offer)
router.post('/:requestId', requireAuth, async (req, res, next) => {
  try {
    const request = await HelpRequest.findById(req.params.requestId);
    if (!request) return res.status(404).json({ error: 'Request not found' });
    if (request.status !== 'open') return res.status(400).json({ error: 'Request not open' });

    const resp = await Response.create({
      requestId: request._id,
      volunteerId: req.user.id,
      message: req.body.message || ''
    });

    request.respondersCount += 1;
    await request.save();

    await notify(req.app, request.requesterId, 'new_response', { responseId: resp._id, requestId: request._id });
    res.status(201).json(resp);
  } catch (e) { 
    if (e.code === 11000) return res.status(400).json({ error: 'You already offered' });
    next(e); 
  }
});

// List responses for a request
router.get('/for/:requestId', requireAuth, async (req, res, next) => {
  try {
    const list = await Response.find({ requestId: req.params.requestId }).populate('volunteerId', 'name points');
    res.json(list);
  } catch (e) { next(e); }
});

// Accept / reject / withdraw
router.patch('/:responseId', requireAuth, async (req, res, next) => {
  try {
    const { action } = req.body;
    const response = await Response.findById(req.params.responseId);
    if (!response) return res.status(404).json({ error: 'Not found' });
    const request = await HelpRequest.findById(response.requestId);
    if (!request) return res.status(404).json({ error: 'Request not found' });

    if (action === 'accept') {
      if (String(request.requesterId) !== req.user.id) return res.status(403).json({ error: 'Only requester can accept' });
      request.status = 'in_progress';
      request.acceptedResponseId = response._id;
      await request.save();
      response.status = 'accepted';
      await response.save();
      await notify(req.app, response.volunteerId, 'response_accepted', { requestId: request._id });
      await addPoints(response.volunteerId, 20, 'offer_accepted', 'Response', response._id);
      return res.json(response);
    }

    if (action === 'reject') {
      if (String(request.requesterId) !== req.user.id) return res.status(403).json({ error: 'Only requester can reject' });
      response.status = 'rejected';
      await response.save();
      await notify(req.app, response.volunteerId, 'response_rejected', { requestId: request._id });
      return res.json(response);
    }

    if (action === 'withdraw') {
      if (String(response.volunteerId) !== req.user.id) return res.status(403).json({ error: 'Only volunteer can withdraw' });
      response.status = 'withdrawn';
      await response.save();
      return res.json(response);
    }

    return res.status(400).json({ error: 'Invalid action' });
  } catch (e) { next(e); }
});

module.exports = router;
