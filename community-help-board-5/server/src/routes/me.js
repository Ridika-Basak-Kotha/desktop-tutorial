const router = require('express').Router();
const { requireAuth } = require('../middleware/auth');
const User = require('../models/User');

router.get('/', requireAuth, async (req, res, next) => {
  try {
    const me = await User.findById(req.user.id).select('-passwordHash');
    res.json(me);
  } catch (e) { next(e); }
});

router.patch('/', requireAuth, async (req, res, next) => {
  try {
    const { name, phone, bio, city, avatarUrl, location } = req.body;
    const updates = { name, phone, bio, city, avatarUrl, location };
    const me = await User.findByIdAndUpdate(req.user.id, updates, { new: true }).select('-passwordHash');
    res.json(me);
  } catch (e) { next(e); }
});

module.exports = router;
