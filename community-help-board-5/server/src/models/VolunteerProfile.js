const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

const VolunteerProfileSchema = new Schema({
  userId: { type: Types.ObjectId, ref: 'User', unique: true, required: true },
  skills: [{ type: String, enum: ['food','medicine','shelter','transport','counseling','first_aid','others'] }],
  availability: { type: String },
  verified: { type: Boolean, default: false },
  govtIdUrl: String,
}, { timestamps: true });

module.exports = mongoose.model('VolunteerProfile', VolunteerProfileSchema);
