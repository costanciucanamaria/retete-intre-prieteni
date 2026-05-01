# 🍲 Retete intre Prieteni (Django Project)

O aplicație web construită în Django pentru gestionarea rețetelor între utilizatori.  
Utilizatorii pot adăuga, edita, șterge și vizualiza rețete, pot încărca imagini, comenta și da like.

---

## 🚀 Funcționalități

- Autentificare (login / register / logout)
- CRUD complet pentru rețete
- Upload imagini pentru rețete
- Sistem de comentarii
- Sistem de like / unlike
- Căutare rețete
- Filtrare după categorie
- Sortare (alfabetic, după dată, după utilizator)
- Paginare rezultate
- Vizualizare rețete după utilizator

---

## 📂 Structură proiect

retete_intre_prieteni/
│
├── retete/            # settings, urls principale
├── retetele/          # aplicația principală (rețete)
├── prieteni/          # utilizatori custom
├── media/             # imagini uploadate
├── static/            # CSS / fișiere statice
└── templates/         # template-uri HTML

---

## ⚙️ Instalare

### 1. Clonează proiectul
git clone <link-repository>
cd retete_intre_prieteni

### 2. Creează mediu virtual
python -m venv venv

Activează mediul virtual:

Windows:
venv\Scripts\activate

Linux / Mac:
source venv/bin/activate

---

### 3. Instalează dependențele
pip install django pillow

---

### 4. Migrare bază de date
python manage.py makemigrations
python manage.py migrate

---

### 5. Creează utilizator admin
python manage.py createsuperuser

---

### 6. Rulează serverul
python manage.py runserver

Acces în browser:
http://127.0.0.1:8000/

---

## 📄 Pagini principale

### Public
- / → lista rețetelor
- /cautare → căutare + filtrare
- /login/
- /register/

### Utilizator logat
- /introducere_reteta/ → adăugare rețetă
- /reteta/<id>/modificare_reteta/
- /reteta/<id>/stergere_reteta/
- /reteta/<id>/like/
- /reteta/<id>/comment/

### Utilizatori
- /prieteni/<id>/retete/ → rețetele unui utilizator

---

## 🧠 Modele principale

### Retete
- nume
- ingrediente
- preparare
- timp_pregatire
- timp_gatire
- data_creare
- categorie
- user (autor)
- poza

### Like
- user
- reteta (unique)

### Comment
- user
- reteta
- text
- data_creare

---

## 🎨 Tehnologii folosite

- Django 6
- SQLite
- HTML + CSS
- Django Templates
- Pillow (imagini)

---

## ⚠️ Observații

- Proiectul rulează în DEBUG (nu este production)
- Media files necesită configurare MEDIA_URL și MEDIA_ROOT
- Imaginile sunt salvate local în folderul media/

---

## 🚀 Posibile îmbunătățiri

- AJAX pentru like și comentarii (fără refresh)
- API REST (Django REST Framework)
- UI modern (Bootstrap / Tailwind)
- Sistem de follow între utilizatori
- Notificări pentru like/comment
