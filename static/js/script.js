// script.js — interações simples para o site Spero Restoration Corp

// Rolagem suave para seções internas
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Exibe confirmação ao enviar o formulário de contato
const contactForm = document.querySelector('form');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    const name = document.querySelector('input[name="name"]').value;
    if (name.trim() !== "") {
      alert(`Thank you, ${name}! Your message has been sent successfully.`);
    }
  });
}

// Botão “Back to top” dinâmico
const backToTop = document.createElement('button');
backToTop.textContent = "↑";
backToTop.id = "backToTop";

