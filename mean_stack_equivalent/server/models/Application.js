const mongoose = require('mongoose');

const AuditLogSchema = new mongoose.Schema({
  changedBy: { type: String, required: true },
  oldStatus: { type: String, required: true },
  newStatus: { type: String, required: true },
  remarks: { type: String, default: '' },
  timestamp: { type: Date, default: Date.now }
});

const ApplicationSchema = new mongoose.Schema({
  appCode: { type: String, required: true, unique: true },
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  fullName: { type: String, required: true },
  dob: { type: String, required: true },
  contactNumber: { type: String, required: true },
  address: { type: String, required: true },
  class10Marks: { type: Number, required: true, min: 0, max: 100 },
  class10Board: { type: String, required: true },
  class12Marks: { type: Number, required: true, min: 0, max: 100 },
  class12Board: { type: String, required: true },
  passingYear: { type: Number, required: true },
  course: { type: String, required: true },
  // Module 1: Document Upload - file on disk, only a REFERENCE stored in MongoDB
  docReference: {
    filename: { type: String },
    filepath: { type: String },
    mimetype: { type: String },
    size: { type: Number }
  },
  // Module 3: Status Workflow (Draft -> Submitted -> Under Review -> Accepted / Rejected)
  status: {
    type: String,
    enum: ['Draft', 'Submitted', 'Under Review', 'Accepted', 'Rejected'],
    default: 'Draft'
  },
  remarks: { type: String, default: '' },
  submittedAt: { type: Date },
  auditTrail: [AuditLogSchema],
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Application', ApplicationSchema);
