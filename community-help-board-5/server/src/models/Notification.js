const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

const NotificationSchema = new Schema({
  userId: { type: Types.ObjectId, ref: 'User', index: true },
  type: { type: String, enum: ['new_response','response_accepted','response_rejected','status_changed','new_rating'] },
  payload: Schema.Types.Mixed,
  isRead: { type: Boolean, default: false },
}, { timestamps: true });

module.exports = mongoose.model('Notification', NotificationSchema);
