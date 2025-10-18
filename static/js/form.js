document.addEventListener("DOMContentLoaded", function() {
  const form = document.querySelector(".form");
  form?.addEventListener("submit", () => {
    alert("Thank you! Your request has been sent.");
  });
});
