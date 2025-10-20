// Multi-language placeholder (EN/ES/PT)
const languages = {
  en: { welcome: "Welcome to Spero Restoration" },
  es: { welcome: "Bienvenido a Spero Restoration" },
  pt: { welcome: "Bem-vindo à Spero Restoration" }
};

function setLanguage(lang) {
  document.getElementById("welcome-text").innerText = languages[lang].welcome;
}
