const express = require('express');
const app = express();
const cors = require('cors');
const mainRouter = require('./routes/main-router');
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use('/v2',mainRouter);
app.all('*', (req, res, next) => {
    next(new Error(`Can't find  ${req.originalUrl} on this server!`, 404));
  });

const port = 5000;
  app.listen(port, () => {
    console.log(`App running on port ${port}...`);
  });