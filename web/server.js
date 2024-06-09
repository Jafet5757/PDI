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

app.get('/generalProcess', (req, res) => { 
  // procesamos la imagen
  const type = req.query.type;
  const image = req.query.image;
  const api_url = 'http://127.0.0.1:8000/'
  // contruimos la url para el servidor de python
  const url = `${api_url}${type}?image_path=${image}`;
  // enviamos la peticion
  fetch(url)
    .then(response => response.json())
    .then(data => {
      console.log('La imagen temp en images-processed/temp.jpg se ha procesado correctamente');
      res.json(data);
    })
    .catch(err => {
      console.error(err);
    });
})

app.listen(port, () => {
  console.log(`El servidor está escuchando en http://localhost:${port}`);
});