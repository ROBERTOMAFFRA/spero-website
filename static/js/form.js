// Handle forms and sendgrid validation feedback
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", () => {
      alert("Submitting your message...");
    });
  }
});
