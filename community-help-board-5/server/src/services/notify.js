const Notification = require('../models/Notification');

async function notify(app, userId, type, payload) {
  const note = await Notification.create({ userId, type, payload });
  const io = app.get('io');
  if (io) io.to(`user:${userId}`).emit('notification:new', note);
  return note;
}

module.exports = { notify };
