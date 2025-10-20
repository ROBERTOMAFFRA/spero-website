/* ======================================================
   SPERO RESTORATION - MAIN JAVASCRIPT
   ====================================================== */

// Smooth scroll for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  });
});

// Mobile menu toggle (future improvement)
const navToggle = document.querySelector(".nav-toggle");
if (navToggle) {
  navToggle.addEventListener("click", () => {
    document.querySelector("nav ul").classList.toggle("open");
  });
}

// Simple contact form validation
const contactForm = document.querySelector("form[action='/send_email']");
if (contactForm) {
  contactForm.addEventListener("submit", (e) => {
    const name = contactForm.querySelector("#name").value.trim();
    const email = contactForm.querySelector("#email").value.trim();
    const message = contactForm.querySelector("#message").value.trim();

    if (!name || !email || !message) {
      alert("Please fill out all required fields before sending.");
      e.preventDefault();
    }
  });
}

// WhatsApp Floating Button Animation
const whatsappBtn = document.querySelector(".whatsapp-float img");
if (whatsappBtn) {
  whatsappBtn.addEventListener("mouseenter", () => {
    whatsappBtn.style.transform = "scale(1.1)";
  });
  whatsappBtn.addEventListener("mouseleave", () => {
    whatsappBtn.style.transform = "scale(1)";
  });
}
