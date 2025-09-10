const http = require('http');
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const { Server } = require('socket.io');

dotenv.config();

const app = express();
app.use(express.json({ limit: '10mb' }));
app.use(cors({ origin: process.env.CLIENT_URL, credentials: true }));
app.use(morgan('dev'));

// Health
app.get('/health', (req, res) => res.json({ ok: true }));

// Mongo
mongoose.set('strictQuery', true);
mongoose.connect(process.env.MONGO_URI).then(() => {
  console.log('✅ MongoDB connected');
}).catch((e) => {
  console.error('Mongo error:', e.message);
  process.exit(1);
});

// Models (ensure they are registered)
require('./models/User');
require('./models/VolunteerProfile');
require('./models/HelpRequest');
require('./models/Response');
require('./models/Rating');
require('./models/PointTxn');
require('./models/Notification');

// Routes
app.use('/auth', require('./routes/auth'));
app.use('/me', require('./routes/me'));
app.use('/volunteers', require('./routes/volunteers'));
app.use('/requests', require('./routes/requests'));
app.use('/responses', require('./routes/responses'));
app.use('/ratings', require('./routes/ratings'));
app.use('/notifications', require('./routes/notifications'));

// Error handler
app.use(require('./middleware/error'));

// Server & Socket
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.CLIENT_URL,
    methods: ['GET','POST','PATCH','DELETE']
  }
});
app.set('io', io);

io.on('connection', (socket) => {
  // users join personal room after login from the client side if desired
  socket.on('join', (room) => socket.join(room));
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log('🚀 API listening on port', PORT));
