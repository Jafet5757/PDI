const prewitButton = document.getElementById('prewit-btn');
const averageButton = document.getElementById('average-btn');
const otsuButton = document.getElementById('otsu-btn');
const ecualizationButton = document.getElementById('ecualization-btn');

prewitButton.addEventListener('click', () => { 
  // procesamos la imagen
  processImage('prewit');
})

averageButton.addEventListener('click', () => { 
  // procesamos la imagen
  processImage('average');
})

otsuButton.addEventListener('click', () => { 
  // procesamos la imagen
  processImage('otsu');
})

ecualizationButton.addEventListener('click', () => { 
  // procesamos la imagen
  processImage('ecualization');
})

function processImage(type) {
  // leemos la imagen
  const image = document.querySelector('#image');
  // vaciamos los contenedores
  imagePrcessedContainer.innerHTML = '';
  imageMaskContainer.innerHTML = '';
  // enviamos la ruta al back para que la procese
  fetch(`/generalProcess?type=${type}&image=${image.src}`)
    .then(response => response.json())
    .then(data => {
      // mostramos la mascara
      const imageMask = new Image();
      imageMask.src = 'images-processed/temp.jpg';
      imageMask.src = updateSrcImage(imageMask.src);
      imageMask.width = 300;
      imageMask.height = 300;
      imageMaskContainer.appendChild(imageMask);
    })
    .catch(err => {
      console.error(err);
      Swal.fire({
        title: 'Error!',
        text: 'No se pudo procesar la imagen',
        icon: 'error'
      })
    });
}