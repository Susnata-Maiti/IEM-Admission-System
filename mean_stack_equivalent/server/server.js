const path = require('path');
const os = require('os');
require('dotenv').config({ path: path.join(__dirname, '.env') });
require('dotenv').config({ path: path.join(__dirname, '../../.env') });
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const apiRoutes = require('./routes/api');

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGODB_URI || process.env.MONGO_URI || 'mongodb://localhost:27017/iem_admission';

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve uploaded documents (Use writable /tmp on Vercel, local folder otherwise)
const uploadDir = process.env.VERCEL ? path.join(os.tmpdir(), 'uploads') : path.join(__dirname, 'uploads');
app.use('/uploads', express.static(uploadDir));

// Cache database connection across serverless function invocations
let cachedDb = null;
async function connectToDatabase() {
  if (cachedDb && mongoose.connection.readyState === 1) {
    return cachedDb;
  }
  if (!MONGO_URI) {
    console.warn('MONGODB_URI environment variable is missing.');
    return null;
  }
  cachedDb = await mongoose.connect(MONGO_URI, {
    serverSelectionTimeoutMS: 5000
  });
  console.log('Connected to MongoDB');
  return cachedDb;
}

// Ensure database connection before API requests
app.use(async (req, res, next) => {
  try {
    await connectToDatabase();
    next();
  } catch (err) {
    console.error('MongoDB connection error:', err.message);
    next();
  }
});

// Root endpoint: displays status instead of 404
app.get('/', (req, res) => {
  res.json({
    status: 'online',
    service: 'IEM Admission System - MEAN Stack POC Backend',
    platform: process.env.VERCEL ? 'Vercel Serverless' : 'Local Node.js',
    endpoints: {
      auth_register: 'POST /api/auth/register',
      auth_login: 'POST /api/auth/login',
      admin_metrics: 'GET /api/admin/metrics',
      application_submit: 'POST /api/student/application/submit'
    }
  });
});

// API routes
app.use('/api', apiRoutes);

// Only listen locally, do NOT block Vercel serverless export
if (!process.env.VERCEL) {
  app.listen(PORT, () => {
    console.log(`Express server running on http://localhost:${PORT}`);
  });
}

// Export app for Vercel
module.exports = app;
