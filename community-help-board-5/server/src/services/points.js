const PointTxn = require('../models/PointTxn');
const User = require('../models/User');

async function addPoints(userId, points, reason, refType, refId) {
  await PointTxn.create({ userId, points, reason, refType, refId });
  await User.updateOne({ _id: userId }, { $inc: { points } });
}

module.exports = { addPoints };
