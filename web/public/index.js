const imageContainer = document.querySelector('#image-container');
const imagePrcessedContainer = document.querySelector('#image-processed-container');
const imageMaskContainer = document.querySelector('#image-mask-container');
const inputImage = document.querySelector('#input-image');
const startButton = document.querySelector('#start-btn');
const resetButton = document.querySelector('#reset-btn');
const api_url = 'http://127.0.0.1:8000/';

function updateSrcImage(src) {
  // agregamos parametros a la imagen para que no se cachee
  const currentSrc = src;
  const newSrc = currentSrc.split('?')[0] + '?t=' + new Date().getTime();
  return newSrc;
}

inputImage.addEventListener('change', (e) => { 
  // cargamos la imagen en el contenedor
  const file = e.target.files[0];
  // la neviamos al servidor para que la guarde
  const formData = new FormData();
  formData.append('image', file);
  // la enviamos a loadImage des este mismo servidor
  fetch(`/loadImage`, {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // creamos una url para mostrar la imagen
      const imageUrl = `uploads/${data.filename}`;
      // mostramos la imagen en el contenedor
      imageContainer.innerHTML = '';
      const image = new Image();
      image.src = imageUrl;
      image.id = 'image';
      image.width = 300;
      image.height = 300;
      imageContainer.appendChild(image);
    })
    .catch(err => {
      console.error(err);
      Swal.fire({
        title: 'Error!',
        text: 'No se pudo cargar la imagen',
        icon: 'error'
      })
    });
});

resetButton.addEventListener('click', () => { 
  window.location.reload(true);
})

startButton.addEventListener('click', async () => { 
  // Obtenemos la imagen cargada
  const image = document.querySelector('#image');

  try {
    // los agregamos a sus contenedores
    imagePrcessedContainer.innerHTML = '';
    imageMaskContainer.innerHTML = '';

    // Esperamos a que autoDetectApi termine
    const data = await autoDetectApi(image.src);

    // esperamos 2 segundo para que la imagen se guarde en el servidor
    //await new Promise(resolve => setTimeout(resolve, 2000));
    
    // cargamos la imagen temp y temp3 de la carpeta images-processed
    const temp = new Image();
    const temp3 = new Image();
    temp.src = 'images-processed/temp.jpg';
    temp3.src = 'images-processed/temp3.jpg';

    // actualizamos la url de las imagenes
    temp.src = updateSrcImage(temp.src);
    temp3.src = updateSrcImage(temp3.src);
    
    // les agregamos un id
    temp.id = 'temp';
    temp3.id = 'temp3';
    
    // les agregamos un ancho y alto
    temp.width = 300;
    temp.height = 300;
    temp3.width = 300;
    temp3.height = 300;
    
    imagePrcessedContainer.appendChild(temp);
    imageMaskContainer.appendChild(temp3);
  } catch (error) {
    console.error('Error processing image:', error);
    // Manejo de errores adicional si es necesario
  }
});

function autoDetect(imagePath) {
      return new Promise((resolve, reject) => {
        let img = new Image();
        img.src = imagePath;
        img.onload = function() {
          try {
            let src = cv.imread(img);
            
            // Umbralizamos la imagen usando el método de Otsu en el canal rojo
            // Dividimos la imagen en sus tres canales
            let channels = new cv.MatVector();
            cv.split(src, channels);
            let red = channels.get(2);  // El canal rojo
            let threshold = new cv.Mat();
            cv.threshold(red, threshold, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU);
            
            // Aplicamos el filtro media 3 veces
            let median = new cv.Mat();
            cv.medianBlur(threshold, median, 3);
            cv.medianBlur(median, median, 3);
            cv.medianBlur(median, median, 3);
            
            // Aplicamos el filtro min 4 veces
            let min = new cv.Mat();
            cv.erode(median, min, new cv.Mat(), new cv.Point(-1, -1), 4);
            
            // Aplicamos el filtro gaussiano 2 veces
            let gaussian = new cv.Mat();
            cv.GaussianBlur(min, gaussian, new cv.Size(3, 3), 0);
            cv.GaussianBlur(gaussian, gaussian, new cv.Size(3, 3), 0);
            
            // Aplicamos filtro media
            cv.medianBlur(gaussian, median, 3);
            cv.medianBlur(median, median, 3);
            
            // Aplicamos el filtro max 4 veces
            let max = new cv.Mat();
            cv.dilate(median, max, new cv.Mat(), new cv.Point(-1, -1), 4);
            
            // Aplicamos filtro media 3 veces
            cv.medianBlur(max, median, 3);
            cv.medianBlur(median, median, 3);
            cv.medianBlur(median, median, 3);
            
            // Aplicamos Sobel
            let sobely = new cv.Mat();
            cv.Sobel(median, sobely, cv.CV_64F, 0, 1, 3);
            
            // Convertimos sobely a 8 bits
            let absSobely = new cv.Mat();
            cv.convertScaleAbs(sobely, absSobely);
            
            // Creamos una máscara y mostramos los bordes sobre la imagen original
            let mask = new cv.Mat();
            cv.threshold(absSobely, mask, 0, 255, cv.THRESH_BINARY);
            
            let result = new cv.Mat();
            cv.bitwise_and(src, src, result, mask);
            
            // Convertimos las matrices a imágenes base64
            let segmentedImg = new cv.Mat();
            cv.cvtColor(result, segmentedImg, cv.COLOR_RGBA2BGRA);
            let segmentedDataUrl = canvasToDataUrl(segmentedImg);
            let sobelMaskDataUrl = canvasToDataUrl(mask);
            
            // Liberamos los objetos
            src.delete();
            red.delete();
            threshold.delete();
            median.delete();
            min.delete();
            gaussian.delete();
            max.delete();
            sobely.delete();
            absSobely.delete();
            mask.delete();
            result.delete();
            segmentedImg.delete();
            
            // Resolviendo la promesa con los resultados
            resolve({ segmented: segmentedDataUrl, sobelMask: sobelMaskDataUrl });
          } catch (err) {
            reject(err);
          }
        };
        img.onerror = reject;
      });
    }

async function autoDetectApi(imagePath) {
  try {
    // Enviamos la imagen al servidor del API
    const response = await fetch(`${api_url}process_image?image_path=${encodeURI(imagePath)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      mode: 'no-cors'
    });

    // Convertimos la respuesta a JSON
    const data = await response.json();
    console.log(data);
    return data;  // Devolvemos los datos para su uso posterior
  } catch (err) {
    console.error(err);
  }
}

function canvasToDataUrl(mat) {
  let canvas = document.createElement('canvas');
  cv.imshow(canvas, mat);
  return canvas.toDataURL('image/png');
}