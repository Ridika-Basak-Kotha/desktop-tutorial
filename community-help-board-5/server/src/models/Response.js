const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

const ResponseSchema = new Schema({
  requestId: { type: Types.ObjectId, ref: 'HelpRequest', required: true, index: true },
  volunteerId: { type: Types.ObjectId, ref: 'User', required: true, index: true },
  message: String,
  status: { type: String, enum: ['offered','accepted','rejected','withdrawn'], default: 'offered' },
}, { timestamps: true });

ResponseSchema.index({ requestId: 1, volunteerId: 1 }, { unique: true });

module.exports = mongoose.model('Response', ResponseSchema);
