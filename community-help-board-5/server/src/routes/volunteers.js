const router = require('express').Router();
const { requireAuth } = require('../middleware/auth');
const VolunteerProfile = require('../models/VolunteerProfile');

router.post('/', requireAuth, async (req, res, next) => {
  try {
    const doc = await VolunteerProfile.findOneAndUpdate(
      { userId: req.user.id },
      { userId: req.user.id, ...req.body },
      { upsert: true, new: true, setDefaultsOnInsert: true }
    );
    res.status(201).json(doc);
  } catch (e) { next(e); }
});

router.get('/:id', async (req, res, next) => {
  try {
    const doc = await VolunteerProfile.findOne({ userId: req.params.id }).populate('userId', 'name city points ratingAvg ratingCount');
    res.json(doc);
  } catch (e) { next(e); }
});

router.patch('/:id', requireAuth, async (req, res, next) => {
  try {
    if (req.params.id !== req.user.id) return res.status(403).json({ error: 'Forbidden' });
    const doc = await VolunteerProfile.findOneAndUpdate({ userId: req.user.id }, req.body, { new: true });
    res.json(doc);
  } catch (e) { next(e); }
});

module.exports = router;
