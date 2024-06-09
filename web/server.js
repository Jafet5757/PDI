const express = require('express');
const path = require('path');
const multer = require('multer');
const morgan = require('morgan');
const app = express();
const port = 3000;

app.use(morgan('dev'));
app.use(express.static(path.join(__dirname, 'public')));

// Configurar almacenamiento para multer
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, './public/uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

app.get('/', (req, res) => {
  // enviamos index.html
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/loadImage', upload.single('image'), (req, res) => {
  if (!req.file) {
        return res.status(400).send('No image uploaded');
    }

    return res.json({
        message: 'Image uploaded successfully',
        filename: req.file.filename
    });
})

app.listen(port, () => {
  console.log(`El servidor está escuchando en http://localhost:${port}`);
});