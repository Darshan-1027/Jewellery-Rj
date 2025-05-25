 let img = document.getElementById("myImage");
  let images = [
    "static/img/poster_02.jpeg",
    "static/img/poster_03.jpeg",
    "static/img/poster_04.jpeg"
  ];
  let i = 0;

  // Auto-change every 1.5 seconds
  let autoSlide = setInterval(nextImage, 6000);

  // Right button click
  document.getElementById("Right").addEventListener("click", function () {
    nextImage();
    resetAutoSlide();
  });

  // Left button click
  document.getElementById("Left").addEventListener("click", function () {
    i = (i - 1 + images.length) % images.length;
    img.src = images[i];
    resetAutoSlide();
  });

  // Next image function
  function nextImage() {
    i = (i + 1) % images.length;
    img.src = images[i];
  }

  // Reset auto-slide timer after manual change
  function resetAutoSlide() {
    clearInterval(autoSlide);
    autoSlide = setInterval(nextImage, 3000);
  }


  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault(); // Stop default jump
      const target = document.querySelector(this.getAttribute('href'));

      if (target) {
        target.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });



