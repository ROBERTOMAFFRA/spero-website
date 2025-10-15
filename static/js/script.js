// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});

// Back to top button
const backToTop = document.createElement('button');
backToTop.textContent = "↑";
backToTop.id = "backToTop";
backToTop.style.cssText = `
  position: fixed;
  bottom: 30px;
  left: 20px;
  padding: 10px;
  border: none;
  background: #0056b3;
  color: white;
  font-size: 1.2rem;
  border-radius: 50%;
  display: none;
  cursor: pointer;
`;
document.body.appendChild(backToTop);

window.addEventListener('scroll', () => {
  backToTop.style.display = window.scrollY > 300 ? 'block' : 'none';
});
backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
