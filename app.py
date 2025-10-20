<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spero Restoration Corp | Water, Fire & Mold Restoration Orlando</title>
  <meta name="description" content="Spero Restoration Corp — Orlando’s trusted experts for water, fire, and mold damage restoration, and home remodeling. Serving Windermere, Lake Nona, and Winter Garden.">
  <meta name="keywords" content="water damage restoration Orlando, mold remediation, fire repair, home remodeling, Windermere, Lake Nona, Winter Garden, Clermont, Florida restoration services">

  <!-- Open Graph -->
  <meta property="og:title" content="Spero Restoration Corp | Restoration & Remodeling Experts">
  <meta property="og:description" content="Water, fire, and mold restoration experts serving Orlando, Windermere, Lake Nona, and surrounding areas.">
  <meta property="og:image" content="https://spero-restoration.com/static/images/banner.png">
  <meta property="og:url" content="https://spero-restoration.com/">
  <meta property="og:type" content="website">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Spero Restoration Corp">
  <meta name="twitter:description" content="Restoration & Remodeling Experts serving Central Florida.">
  <meta name="twitter:image" content="https://spero-restoration.com/static/images/banner.png">

  <link rel="icon" href="{{ url_for('static', filename='images/favicon.ico') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

  <!-- Structured Data: Local Business -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Spero Restoration Corp",
    "image": "https://spero-restoration.com/static/images/logo.png",
    "@id": "https://spero-restoration.com",
    "url": "https://spero-restoration.com",
    "telephone": "+1-407-724-6310",
    "email": "contact@spero-restoration.com",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Orlando, FL",
      "addressLocality": "Orlando",
      "addressRegion": "FL",
      "postalCode": "32819",
      "addressCountry": "US"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 28.5383,
      "longitude": -81.3792
    },
    "areaServed": ["Orlando", "Windermere", "Lake Nona", "Winter Garden", "Clermont"],
    "priceRange": "$$",
    "sameAs": [
      "https://www.facebook.com/sperorestoration",
      "https://www.instagram.com/sperorestoration"
    ]
  }
  </script>
</head>

<body>
  <!-- HEADER -->
  <header>
    <a href="{{ url_for('index') }}">
      <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Spero Restoration Logo">
    </a>
    <nav>
      <ul>
        <li><a href="{{ url_for('index') }}" class="active">Home</a></li>
        <li><a href="{{ url_for('about') }}">About</a></li>
        <li><a href="{{ url_for('services') }}">Services</a></li>
        <li><a href="{{ url_for('contact') }}">Contact</a></li>
      </ul>
    </nav>
  </header>

  <!-- HERO SECTION -->
  <section class="hero">
    <h1>Restoration & Remodeling Experts</h1>
    <p>Serving Orlando, Windermere, Lake Nona, and Winter Garden</p>
    <a href="{{ url_for('contact') }}" class="btn-primary">Schedule Inspection</a>
  </section>

  <!-- ABOUT SECTION -->
  <section id="about">
    <h2>About Us</h2>
    <p>
      Spero Restoration Corp is a licensed and insured company providing complete restoration and remodeling solutions across Central Florida. 
     We specialize in water, fire, and mold damage restoration - restoring your property and peace of mind.
    </p>
  </section>

  <!-- SERVICES -->
  <section id="services">
    <h2>Our Services</h2>
    <div class="services">
      <div class="service-card">
        <img src="{{ url_for('static', filename='images/water.png') }}" alt="Water Damage Restoration">
        <h3>Water Damage Restoration</h3>
        <p>Rapid response water removal and drying services to protect your home and prevent long-term damage.</p>
      </div>
      <div class="service-card">
        <img src="{{ url_for('static', filename='images/mold.png') }}" alt="Mold Remediation">
        <h3>Mold Remediation</h3>
        <p>Certified mold detection, removal, and air quality improvement services for a healthy home.</p>
      </div>
      <div class="service-card">
        <img src="{{ url_for('static', filename='images/fire.png') }}" alt="Fire & Smoke Repair">
        <h3>Fire & Smoke Repair</h3>
        <p>Professional cleanup, repair, and odor removal to restore your property after fire damage.</p>
      </div>
      <div class="service-card">
        <img src="{{ url_for('static', filename='images/remodel.png') }}" alt="Home Remodeling">
        <h3>Home Remodeling</h3>
        <p>From design to finishing touches, we bring your dream renovation to life with expert craftsmanship.</p>
      </div>
    </div>
  </section>

  <!-- REVIEWS SECTION -->
  <section id="reviews">
    <h2>What Our Clients Say</h2>
    <div class="reviews">
      <div class="review">
        <p>"Spero Restoration exceeded expectations. Fast, professional, and truly cared about our home!"</p>
        <div class="stars">★★★★★</div>
        <h4>- Sarah, Windermere</h4>
      </div>
      <div class="review">
        <p>"Outstanding service! They handled our water damage efficiently and kept us updated throughout."</p>
        <div class="stars">★★★★★</div>
        <h4>- John, Lake Nona</h4>
      </div>
    </div>
  </section>

  <!-- FAQ SECTION -->
  <section id="faq">
    <h2>Frequently Asked Questions</h2>
    <div class="faq-item">
      <h3>How soon can you respond to an emergency?</h3>
      <p>We offer 24/7 emergency restoration response throughout Orlando and Central Florida.</p>
    </div>
    <div class="faq-item">
      <h3>Do you work with insurance companies?</h3>
      <p>Yes, we work directly with all major insurance carriers to simplify your claim process.</p>
    </div>
    <div class="faq-item">
      <h3>What areas do you serve?</h3>
      <p>We proudly serve Orlando, Windermere, Lake Nona, Clermont, and Winter Garden areas.</p>
    </div>
  </section>

  <!-- CALL TO ACTION -->
  <section class="contact-cta">
    <h2>Need Immediate Assistance?</h2>
    <p>Contact us today for 24/7 emergency restoration and expert remodeling support.</p>
    <a href="{{ url_for('contact') }}" class="btn-primary">Request Inspection</a>
  </section>

  <!-- FOOTER -->
  <footer>
    <p>&copy; 2025 Spero Restoration Corp | Orlando, FL | (407) 724-6310</p>
    <p><a href="{{ url_for('privacy') }}">Privacy Policy</a> | <a href="{{ url_for('terms') }}">Terms of Service</a></p>
  </footer>

  <!-- WhatsApp & Call Floating Buttons -->
  <a href="https://wa.me/14077246310" class="whatsapp-float" target="_blank">
    <img src="{{ url_for('static', filename='images/whatsapp-icon.png') }}" alt="Chat on WhatsApp">
  </a>

  <a href="tel:4077246310" class="call-float">
    📞 Call Now
  </a>

</body>
</html>
