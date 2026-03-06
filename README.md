# Shaqyru.kz — Той шақыру платформасы

Kazakh wedding invitation platform with audio player.

## Tech Stack

| Layer    | Technology                              |
|----------|-----------------------------------------|
| Frontend | Nuxt 3, Vue 3, TailwindCSS, Pinia       |
| Backend  | Django 6, Django REST Framework         |
| Database | PostgreSQL (SQLite for development)     |

---

## Project Structure

```
NewToi/
├── NewToi/          # Django config (settings, urls)
├── invitations/     # Invitation templates + builder API
├── songs/           # Wedding songs API
├── blog/            # Blog posts API
├── templates/       # Django HTML templates (SPA entry)
├── frontend/        # Nuxt 3 SPA
│   ├── pages/
│   │   ├── index.vue           # Homepage
│   │   ├── templates.vue       # Templates gallery
│   │   ├── songs.vue           # Audio player
│   │   ├── builder.vue         # Invitation builder
│   │   └── invite/[slug].vue   # Public invitation view
│   ├── components/
│   ├── stores/      # Pinia stores
│   └── composables/ # useApi composable
└── manage.py
```

---

## Quick Start (Development)

### 1. Backend

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser

# Seed example data
python manage.py seed_data

# Start Django dev server
python manage.py runserver
# API available at http://localhost:8000/api/
# Admin at http://localhost:8000/admin/
```

### 2. Frontend

```bash
cd frontend

# Copy environment file
cp .env.example .env

# Install dependencies (requires Node.js 18+)
npm install

# Start Nuxt dev server
npm run dev
# Frontend at http://localhost:3000
```

---

## API Endpoints

| Method | Endpoint                                   | Description                  |
|--------|--------------------------------------------|------------------------------|
| GET    | `/api/invitations/templates/`              | List invitation templates    |
| GET    | `/api/invitations/templates/?category=uzatu` | Filter templates by category |
| GET    | `/api/invitations/templates/{id}/`         | Template detail              |
| POST   | `/api/invitations/`                        | Create invitation            |
| GET    | `/api/invitations/{slug}/`                 | Get invitation by slug       |
| POST   | `/api/invitations/{slug}/guests/`          | Add guest RSVP               |
| GET    | `/api/songs/`                              | List songs                   |
| GET    | `/api/songs/?category={slug}`              | Filter songs by category     |
| GET    | `/api/songs/{id}/`                         | Song detail + increment play |
| GET    | `/api/songs/categories/`                   | List song categories         |
| GET    | `/api/blog/`                               | List published blog posts    |
| GET    | `/api/blog/{slug}/`                        | Blog post detail             |

---

## Production Deployment

### Backend (Gunicorn + Nginx)

```bash
# Build frontend
cd frontend && npm run generate

# Copy built files to templates/
cp frontend/dist/index.html templates/index.html

# Collect static files
python manage.py collectstatic --no-input

# Set production environment variables
export SECRET_KEY="your-production-secret"
export DEBUG=False
export ALLOWED_HOSTS="yourdomain.com"
export USE_POSTGRES=True
export DB_NAME=shaqyru
export DB_USER=postgres
export DB_PASSWORD=yourpassword

# Run migrations
python manage.py migrate

# Start with Gunicorn
gunicorn NewToi.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Nginx config snippet

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /media/ {
        alias /path/to/project/media/;
    }

    location /static/ {
        alias /path/to/project/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### PostgreSQL setup

```sql
CREATE DATABASE shaqyru;
CREATE USER postgres WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE shaqyru TO postgres;
```

---

## Django Admin

After creating a superuser, visit `/admin/` to:

- Upload **songs** with audio files
- Create **song categories**
- Add **invitation templates** with gradient colors
- Write and publish **blog posts**
- View all **invitations** created by users

---

## Invitation Categories

| Slug         | Name          |
|--------------|---------------|
| `uzatu`      | Ұзату той     |
| `qyz_uzatu`  | Қыз ұзату     |
| `sunnet`     | Сүндет той    |
| `tusaukesar` | Тұсаукесер    |
| `merey`      | Мерей той     |
| `besik`      | Бесік той     |
| `betashar`   | Беташар       |
| `other`      | Асау тойлар   |
