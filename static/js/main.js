// 🌟 SPERO RESTORATION CORP - MAIN SCRIPT (v3)

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Lazy load images
document.addEventListener("DOMContentLoaded", function() {
  const images = document.querySelectorAll("img");
  images.forEach(img => {
    img.loading = "lazy";
  });
});

// Analytics (replace IDs with your real ones)
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-XXXXXXXXXX'); // Google Analytics ID

// Facebook Pixel
!function(f,b,e,v,n,t,s){
  if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'XXXXXXXXXXXXXXX'); // Facebook Pixel ID
fbq('track', 'PageView');

// Track WhatsApp clicks
document.querySelectorAll('.whatsapp-float').forEach(btn => {
  btn.addEventListener('click', () => {
    fbq('track', 'Contact');
    gtag('event', 'whatsapp_click');
  });
});
