const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

const RatingSchema = new Schema({
  volunteerId: { type: Types.ObjectId, ref: 'User', required: true, index: true },
  raterId: { type: Types.ObjectId, ref: 'User', required: true },
  requestId: { type: Types.ObjectId, ref: 'HelpRequest', required: true },
  score: { type: Number, min: 1, max: 5, required: true },
  comment: String,
}, { timestamps: true });

RatingSchema.index({ volunteerId: 1, requestId: 1 }, { unique: true });

module.exports = mongoose.model('Rating', RatingSchema);
