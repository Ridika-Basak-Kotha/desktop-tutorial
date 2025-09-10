const router = require('express').Router();
const { requireAuth } = require('../middleware/auth');
const Notification = require('../models/Notification');

router.get('/', requireAuth, async (req, res, next) => {
  try {
    const list = await Notification.find({ userId: req.user.id }).sort({ createdAt: -1 }).limit(50);
    res.json(list);
  } catch (e) { next(e); }
});

router.patch('/:id/read', requireAuth, async (req, res, next) => {
  try {
    await Notification.updateOne({ _id: req.params.id, userId: req.user.id }, { $set: { isRead: true } });
    res.json({ ok: true });
  } catch (e) { next(e); }
});

router.patch('/mark-all-read', requireAuth, async (req, res, next) => {
  try {
    await Notification.updateMany({ userId: req.user.id, isRead: false }, { $set: { isRead: true } });
    res.json({ ok: true });
  } catch (e) { next(e); }
});

module.exports = router;
