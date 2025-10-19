# 🌎 Spero Restoration Corp — Official Website

> Professional restoration and remodeling services website built with **Flask**, optimized for SEO, multilingual content, and dynamic admin control.

---

## ⚙️ Overview

**Spero Restoration Corp** website is a modern, multilingual platform designed for **maximum SEO performance** and **local lead generation** in the Orlando, Florida region.

### 🧩 Tech Stack
- **Framework:** Flask (Python 3.13)
- **Hosting:** Render.com (auto-deploy from GitHub)
- **Email Delivery:** SendGrid API
- **SEO & Analytics:** JSON-LD, Sitemap, Robots.txt
- **Languages:** English 🇺🇸, Spanish 🇪🇸, Portuguese 🇧🇷
- **Design:** Responsive + Optimized for Google Core Web Vitals

---

## 📂 Project Structure


---

## 🔐 Environment Variables (`.env`)

Create a `.env` file in the project root or set them directly in **Render Dashboard → Environment**:

| Variable | Description |
|-----------|--------------|
| `SECRET_KEY` | Flask session secret key |
| `SENDGRID_API_KEY` | API key from SendGrid |
| `SENDER_EMAIL` | contact@spero-restoration.com |
| `ADMIN_USERNAME` | RobertoMaffra |
| `ADMIN_PASSWORD` | spero2025admin |

> 🔒 The `.env.example` file is included as a reference template and safe to commit.

---

## 🚀 Deployment on Render

1. Connect this GitHub repo to **Render.com**.  
2. Add environment variables under **Dashboard → Environment**.  
3. Deploy automatically or manually.

Render detects Flask automatically with the following files:
- `Procfile`
- `requirements.txt`
- `runtime.txt`

**Procfile content:**


---

## 🧑‍💼 Admin Panel

Access:


### 🔑 Login
- **Username:** `RobertoMaffra`
- **Password:** `spero2025admin`

### 📸 Features
- Upload **Before & After** photos → auto-created in `/static/images/uploads`
- Add and manage **Customer Reviews** with star ratings ⭐⭐⭐⭐⭐
- Logout functionality included
- Fully mobile-responsive interface

---

## 💬 Contact Form (SendGrid)

All contact messages are automatically sent to:

- `contact@spero-restoration.com`
- `roberto.maffra@gmail.com`

And a confirmation email is sent back to the customer.

> Uses SendGrid transactional email API (through `send_emails_via_sendgrid()` function in `app.py`).

---

## 🌍 Multilingual System

Supports:
- 🇺🇸 English → `/index?lang=en`
- 🇪🇸 Spanish → `/index?lang=es`
- 🇧🇷 Portuguese → `/index?lang=pt`

JSON files located at:



You can edit these files anytime to update wording or add new sections.

---

## 🧭 SEO & Google Indexation

### Included
- ✅ `robots.txt`  
- ✅ `sitemap.xml`  
- ✅ JSON-LD LocalBusiness Schema  
- ✅ Meta titles & descriptions  
- ✅ Clean URLs  
- ✅ Mobile friendly  
- ✅ SSL active (https)

### Manual Steps
1. Visit [Google Search Console](https://search.google.com/search-console/)
2. Add both domains:
   - `https://spero-restoration.com`
   - `https://www.spero-restoration.com`
3. Submit sitemap:


4. Link your [Google Business Profile](https://www.google.com/business/) with this domain for Local SEO.

---

## 🪣 Uploads & Reviews Storage

| Data | Location | Format |
|------|-----------|--------|
| Photos | `/static/images/uploads` | JPEG / PNG |
| Testimonials | `/data/testimonials.json` | JSON |
| Legacy testimonials | `/data/testimonials.txt` | Fallback |

If you upload images via admin, the system auto-creates the `uploads/` folder.

---

## 🔄 Local Development

```bash
# Clone repo
git clone https://github.com/robertomaffra/spero-restoration.git
cd spero-restoration

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run Flask
python app.py


http://127.0.0.1:5000

Flask==3.0.3
sendgrid==6.11.0
python-dotenv==1.0.1
gunicorn==21.2.0
Werkzeug==3.0.3


---

## ✅ O que este README garante
- Organização profissional para **Render + GitHub**.  
- Clareza sobre **configurações, SEO, admin e multilíngue**.  
- Padronização total para futuras manutenções ou colaboradores.  

---

Quer que eu monte também a **versão curta em português** (para adicionar na descrição do repositório GitHub e no Google Search Console “meta project description”)? Ela melhora o ranqueamento e a credibilidade quando alguém pesquisa “Spero Restoration Corp site oficial”.






