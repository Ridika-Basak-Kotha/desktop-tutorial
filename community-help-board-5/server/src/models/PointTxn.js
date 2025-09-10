const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

const PointTxnSchema = new Schema({
  userId: { type: Types.ObjectId, ref: 'User', required: true, index: true },
  points: { type: Number, required: true },
  reason: { type: String, enum: ['offer_accepted','request_fulfilled','5star_bonus','admin_adjust','other'], required: true },
  refType: { type: String, enum: ['HelpRequest','Response','Rating','Other'] },
  refId: Types.ObjectId,
}, { timestamps: true });

module.exports = mongoose.model('PointTxn', PointTxnSchema);
