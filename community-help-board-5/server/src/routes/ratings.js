const router = require('express').Router();
const { requireAuth } = require('../middleware/auth');
const Rating = require('../models/Rating');
const HelpRequest = require('../models/HelpRequest');
const User = require('../models/User');
const { addPoints } = require('../services/points');

router.post('/:volunteerId', requireAuth, async (req, res, next) => {
  try {
    const { requestId, score, comment } = req.body;
    if (!requestId || !score) return res.status(400).json({ error: 'Missing fields' });

    const reqDoc = await HelpRequest.findById(requestId);
    if (!reqDoc) return res.status(404).json({ error: 'Request not found' });
    if (String(reqDoc.requesterId) !== req.user.id) return res.status(403).json({ error: 'Only requester can rate' });
    if (reqDoc.status !== 'fulfilled') return res.status(400).json({ error: 'Rate after fulfilled' });

    const rating = await Rating.create({ volunteerId: req.params.volunteerId, raterId: req.user.id, requestId, score, comment });

    // update volunteer average
    const agg = await Rating.aggregate([
      { $match: { volunteerId: rating.volunteerId } },
      { $group: { _id: '$volunteerId', count: { $sum: 1 }, avg: { $avg: '$score' } } }
    ]);
    if (agg[0]) {
      await User.updateOne({ _id: rating.volunteerId }, { $set: { ratingAvg: agg[0].avg, ratingCount: agg[0].count } });
    }

    // points bonus
    if (score >= 5) await addPoints(rating.volunteerId, 10, '5star_bonus', 'Rating', rating._id);

    res.status(201).json(rating);
  } catch (e) { 
    if (e.code === 11000) return res.status(400).json({ error: 'You already rated for this request' });
    next(e); 
  }
});

router.get('/for/:volunteerId', async (req, res, next) => {
  try {
    const list = await Rating.find({ volunteerId: req.params.volunteerId }).sort({ createdAt: -1 });
    res.json(list);
  } catch (e) { next(e); }
});

module.exports = router;
