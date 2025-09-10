const router = require('express').Router();
const { requireAuth } = require('../middleware/auth');
const HelpRequest = require('../models/HelpRequest');
const Response = require('../models/Response');
const { notify } = require('../services/notify');

// Create
router.post('/', requireAuth, async (req, res, next) => {
  try {
    const doc = await HelpRequest.create({ ...req.body, requesterId: req.user.id });
    req.app.get('io').emit('request:created', { id: doc._id, title: doc.title, category: doc.category, status: doc.status, createdAt: doc.createdAt });
    res.status(201).json(doc);
  } catch (e) { next(e); }
});

// List with filters
router.get('/', async (req, res, next) => {
  try {
    const { status='open', category, q, lat, lng, radius=10000, sort='latest' } = req.query;
    const filter = {};
    if (status) filter.status = status;
    if (category) filter.category = category;
    if (q) filter.$text = { $search: q };
    let query = HelpRequest.find(filter);

    if (lat && lng) {
      query = query.where('location').near({
        center: { type: 'Point', coordinates: [parseFloat(lng), parseFloat(lat)] },
        maxDistance: parseInt(radius,10)
      });
    }
    if (sort === 'latest') query = query.sort({ createdAt: -1 });
    const docs = await query.limit(50);
    res.json(docs);
  } catch (e) { next(e); }
});

// Get by id
router.get('/:id', async (req, res, next) => {
  try {
    const doc = await HelpRequest.findById(req.params.id);
    res.json(doc);
  } catch (e) { next(e); }
});

// Update
router.patch('/:id', requireAuth, async (req, res, next) => {
  try {
    const doc = await HelpRequest.findById(req.params.id);
    if (!doc) return res.status(404).json({ error: 'Not found' });
    if (String(doc.requesterId) !== req.user.id) return res.status(403).json({ error: 'Forbidden' });
    Object.assign(doc, req.body);
    await doc.save();
    res.json(doc);
  } catch (e) { next(e); }
});

// Change status
router.patch('/:id/status', requireAuth, async (req, res, next) => {
  try {
    const { status } = req.body;
    const doc = await HelpRequest.findById(req.params.id);
    if (!doc) return res.status(404).json({ error: 'Not found' });
    if (String(doc.requesterId) !== req.user.id) return res.status(403).json({ error: 'Forbidden' });
    doc.status = status;
    await doc.save();

    // notify accepted volunteer when fulfilled
    if (status === 'fulfilled' && doc.acceptedResponseId) {
      const resp = await Response.findById(doc.acceptedResponseId);
      if (resp) await notify(req.app, resp.volunteerId, 'status_changed', { requestId: doc._id, status });
    }

    res.json(doc);
  } catch (e) { next(e); }
});

// Delete
router.delete('/:id', requireAuth, async (req, res, next) => {
  try {
    const doc = await HelpRequest.findById(req.params.id);
    if (!doc) return res.status(404).json({ error: 'Not found' });
    if (String(doc.requesterId) !== req.user.id) return res.status(403).json({ error: 'Forbidden' });
    await doc.deleteOne();
    res.json({ ok: true });
  } catch (e) { next(e); }
});

module.exports = router;
