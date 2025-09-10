const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

const HelpRequestSchema = new Schema({
  requesterId: { type: Types.ObjectId, ref: 'User', required: true, index: true },
  title: { type: String, required: true },
  description: { type: String, required: true },
  category: { type: String, enum: ['food','medicine','shelter','transport','other'], required: true },
  urgency: { type: String, enum: ['low','medium','high','critical'], default: 'medium' },
  media: [{ url: String, kind: { type: String, enum: ['image','video'] } }],
  location: { type: { type: String, enum: ['Point'], default: 'Point' }, coordinates: { type: [Number], required: true } },
  address: String,
  status: { type: String, enum: ['open','in_progress','fulfilled','canceled'], default: 'open', index: true },
  acceptedResponseId: { type: Types.ObjectId, ref: 'Response' },
  respondersCount: { type: Number, default: 0 },
}, { timestamps: true });

HelpRequestSchema.index({ location: '2dsphere' });
HelpRequestSchema.index({ title: 'text', description: 'text' }, { weights: { title: 5, description: 1 } });

module.exports = mongoose.model('HelpRequest', HelpRequestSchema);
