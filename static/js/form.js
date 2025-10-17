// =======================================================
// SPERO RESTORATION CORP - FORM HANDLER (SendGrid Ready)
// =======================================================

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("inspectionForm");
  const responseText = document.getElementById("formResponse");

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    responseText.textContent = "Sending your request...";
    responseText.style.color = "#1c5dff";

    const formData = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      phone: form.phone.value.trim(),
      message: form.message.value.trim(),
    };

    try {
      const res = await fetch("/send_email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok) {
        responseText.textContent = "✅ Your inspection request has been sent successfully!";
        responseText.style.color = "#0a8a00";
        form.reset();
      } else {
        throw new Error(data.error || "Error sending email");
      }
    } catch (error) {
      console.error("Form submission error:", error);
      responseText.textContent =
        "❌ Something went wrong. Please try again or contact us directly at contact@spero-restoration.com.";
      responseText.style.color = "#ff3333";
    }
  });
});
