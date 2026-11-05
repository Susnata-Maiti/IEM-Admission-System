const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const User = require('../models/User');
const Application = require('../models/Application');

const JWT_SECRET = process.env.JWT_SECRET || 'iem_admission_jwt_secret_token_2026';

// --------------------------------------------------------------------------
// Module 1: Multer Setup (File on disk, reference in MongoDB)
// --------------------------------------------------------------------------
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, `${uniqueSuffix}-${file.originalname}`);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit (FR-05)
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'application/pdf' || file.originalname.toLowerCase().endsWith('.pdf')) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type: Only PDF documents are allowed.'));
    }
  }
});

// --------------------------------------------------------------------------
// Module 2: Auth & RBAC Middleware (JWT + Server-Side Role Check)
// --------------------------------------------------------------------------
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.status(401).json({ detail: 'Access denied. Missing JWT token.' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(401).json({ detail: 'Invalid or expired token.' });
    req.user = user;
    next();
  });
};

const requireRole = (allowedRoles) => {
  return (req, res, next) => {
    if (!req.user || !allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ 
        detail: `Forbidden: Access restricted to roles [${allowedRoles.join(', ')}]. Server-side role guard enforced.` 
      });
    }
    next();
  };
};

// --------------------------------------------------------------------------
// Module 3: Status Transition Business Rules (State Machine)
// --------------------------------------------------------------------------
function validateTransition(currentStatus, newStatus, remarks) {
  if (currentStatus === newStatus) {
    return { valid: false, reason: `Application is already in status '${currentStatus}'` };
  }
  if (currentStatus === 'Draft') {
    if (newStatus === 'Submitted') return { valid: true };
    return { valid: false, reason: "Draft can only transition to 'Submitted'" };
  }
  if (currentStatus === 'Submitted') {
    if (newStatus === 'Under Review') return { valid: true };
    if (newStatus === 'Rejected') {
      if (!remarks || !remarks.trim()) return { valid: false, reason: "Rejection requires remarks." };
      return { valid: true };
    }
    return { valid: false, reason: "Submitted can only transition to 'Under Review' or 'Rejected'" };
  }
  if (currentStatus === 'Under Review') {
    if (['Accepted', 'Rejected'].includes(newStatus)) return { valid: true };
    return { valid: false, reason: "Under Review can only transition to 'Accepted' or 'Rejected'" };
  }
  return { valid: false, reason: `Terminal state '${currentStatus}' cannot be altered.` };
}

// --------------------------------------------------------------------------
// Auth Routes
// --------------------------------------------------------------------------
router.post('/auth/register', async (req, res) => {
  try {
    const { name, email, password } = req.body;
    if (password.length < 8 || !/[A-Z]/.test(password) || !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      return res.status(400).json({ detail: 'Password must be >= 8 chars, contain 1 uppercase and 1 special char.' });
    }
    const existing = await User.findOne({ email });
    if (existing) return res.status(400).json({ detail: 'Email already registered.' });

    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(password, salt);
    const user = new User({ name, email, passwordHash, role: 'student' });
    await user.save();

    const token = jwt.sign({ userId: user._id, email: user.email, role: user.role, name: user.name }, JWT_SECRET, { expiresIn: '24h' });
    res.json({ token, user: { id: user._id, name: user.name, email: user.email, role: user.role } });
  } catch (err) {
    res.status(500).json({ detail: err.message });
  }
});

router.post('/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
      return res.status(401).json({ detail: 'Invalid email or password.' });
    }
    const token = jwt.sign({ userId: user._id, email: user.email, role: user.role, name: user.name }, JWT_SECRET, { expiresIn: '24h' });
    res.json({ token, user: { id: user._id, name: user.name, email: user.email, role: user.role } });
  } catch (err) {
    res.status(500).json({ detail: err.message });
  }
});

// --------------------------------------------------------------------------
// Student Routes (Upload + Submit)
// --------------------------------------------------------------------------
router.post('/student/application/upload', authenticateToken, requireRole(['student']), upload.single('document'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ detail: 'No PDF file uploaded.' });
    let app = await Application.findOne({ userId: req.user.userId });
    if (app && app.status !== 'Draft') {
      return res.status(403).json({ detail: 'Cannot upload files after submission. Application locked.' });
    }
    res.json({
      message: 'File stored on disk, reference captured.',
      reference: {
        filename: req.file.originalname,
        filepath: req.file.path,
        size: req.file.size
      }
    });
  } catch (err) {
    res.status(500).json({ detail: err.message });
  }
});

// --------------------------------------------------------------------------
// Module 4: Admin Dashboard with MongoDB Aggregation Pipeline ($group, $match)
// --------------------------------------------------------------------------
router.get('/admin/metrics', authenticateToken, requireRole(['admin', 'director']), async (req, res) => {
  try {
    // MongoDB Aggregation Pipeline ($match + $group)
    const statusCounts = await Application.aggregate([
      { $match: { status: { $ne: 'Draft' } } },
      { $group: { _id: '$status', count: { $sum: 1 } } }
    ]);

    const deptCounts = await Application.aggregate([
      { $match: { status: { $ne: 'Draft' } } },
      { $group: { _id: '$course', count: { $sum: 1 } } }
    ]);

    const total = await Application.countDocuments({ status: { $ne: 'Draft' } });

    res.json({
      metrics: {
        total,
        statusBreakdown: statusCounts,
        departmentBreakdown: deptCounts
      }
    });
  } catch (err) {
    res.status(500).json({ detail: err.message });
  }
});

module.exports = router;
