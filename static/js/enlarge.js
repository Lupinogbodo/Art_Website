document.addEventListener('DOMContentLoaded', () => {
    console.log('enlarge.js loaded, attaching lightbox listeners…');
  
    const lightbox  = document.getElementById('lightbox');
    const imgEl     = document.getElementById('lightbox-img');
    const descEl    = document.getElementById('lightbox-desc');
    const closeArea = document.getElementById('lightbox-close');
  
    if (!lightbox) {
      console.error('Lightbox overlay not found!');
      return;
    }
  
    // Clicking any art image
    document.querySelectorAll('.art-card img.art-img').forEach(img => {
      img.addEventListener('click', () => {
        console.log('Image clicked:', img.src);
  
        imgEl.src = img.src;
        imgEl.alt = img.alt;
        descEl.textContent = img.closest('.art-card').querySelector('.art-info p').textContent;
  
        lightbox.classList.add('active');
      });
    });
  
    // Close when clicking the backdrop
    closeArea.addEventListener('click', () => {
      lightbox.classList.remove('active');
    });
  });
  