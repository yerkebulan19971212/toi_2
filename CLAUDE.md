# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Shaqyru.kz** — Kazakh wedding invitation platform. Users pick a template, fill in event details, and get a shareable URL (`/i/<slug>/`) that renders the HTML invitation with an embedded RSVP form.

## Commands

### Backend (Django)

```bash
# Activate virtualenv (project root)
source venv/bin/activate

# Run dev server (PostgreSQL required)
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Seed song categories and sample data
python manage.py seed_data

# Django shell
python manage.py shell
```

### Frontend (Nuxt)

```bash
cd frontend

# Dev server (proxies API to localhost:8000)
npm run dev

# Build for production (output goes to frontend/dist/)
npm run generate

# After build — copy entry point for Django to serve the SPA
cp frontend/dist/index.html templates/index.html
python manage.py collectstatic --no-input
```

### Docker

```bash
# Backend only (no postgres service in compose — relies on local postgres)
docker-compose up --build
# Runs on port 8097
```

## Architecture

### Request Flow

```
Browser
  ├── /* (SPA routes) → Django serves templates/index.html → Nuxt hydrates
  ├── /i/<slug>/      → InvitationHTMLView renders Jinja2 template + injects RSVP form inline
  ├── /api/**         → DRF views
  └── /admin/         → Django Admin
```

### Invitation Rendering Pipeline

The core feature. Lives entirely in `invitations/`:

1. **`InvitationTemplate`** — points to a `.html` file in `invitations/templates_html/` (field: `template_file`, stored without `.html` extension)
2. **`Invitation.get_render_context()`** — builds the Jinja2 variable dict from model fields + `extra_data` JSON
3. **`renderer.py`** — `SandboxedEnvironment` with `autoescape=True` renders the template. Template files use standard Jinja2 syntax (`{{ event_title }}`, `{% for img in images %}`, etc.)
4. **`InvitationHTMLView`** — renders on every GET request (does NOT use `rendered_html` cache for live templates); appends `_RSVP_SNIPPET` before `</body>`
5. **`rendered_html`** field — legacy cache, only used as fallback if `template_file` is missing

Template context variables available in every `.html` template:
`event_title`, `event_date`, `event_time`, `event_location`, `map_link`, `description`, `images` (list of dicts with `url/placement/caption/sort_order`), `image_layout`, `bride_name`, `groom_name`, plus anything in `extra_data` (spread as top-level vars).

### Frontend ↔ Backend

- **`composables/useApi.js`** — thin Axios wrapper. `get(endpoint, params)`, `post(endpoint, data)`, `postForm(endpoint, formData)`. API base set via `NUXT_PUBLIC_API_BASE` env var (default: `http://localhost:8000`).
- **Pinia stores** (`stores/`): `templates.js`, `songs.js`, `player.js`. API returns plain arrays (no pagination wrapper) — do not add `.results` access.
- **`builder.vue`** — multi-step invitation creation form; POSTs to `/api/invitations/`.

### Key Data Relationships

```
InvitationCategory (uzatu, sunnet, besik, etc.)
  └── InvitationTemplate (template_file → templates_html/*.html)
        └── Invitation (slug, extra_data JSON, image_layout)
              ├── InvitationImage (url, placement, sort_order)
              ├── RSVPResponse (unique per phone+invitation)
              ├── GuestComment (is_approved=True by default)
              └── Guest (legacy guest-list management)
```

### Apps

| App | Purpose |
|-----|---------|
| `invitations` | Core: templates, invitations, RSVP, comments, guests |
| `songs` | Wedding songs with audio player (file or URL), play_count tracking |
| `blog` | Simple CMS for blog posts |
| `base` | Abstract models (`TimeStampedModel`, `NameModel` with kz/ru/en fields), shared utilities |

### Settings Notes

- **Database**: Always PostgreSQL (SQLite fallback is commented out). Configure via `.env`: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
- **`ALLOWED_HOSTS = ['*']`** and **`CORS_ORIGIN_ALLOW_ALL = True`** are intentionally left open during development — restrict before production deployment.
- Static files: Django serves the Nuxt build from `frontend/dist/` via WhiteNoise. `STATICFILES_DIRS` points there.
- Language: `kk` (Kazakh), timezone: `Asia/Almaty`.

## Adding a New Invitation Template

1. Create `invitations/templates_html/<name>.html` using Jinja2 syntax
2. In Django Admin → Invitation Templates → set `template_file` to `<name>` (no extension)
3. Set `supported_vars` (JSON list) and `supported_image_layouts` to document what the template expects
4. Use `extra_data` on `Invitation` for any template-specific variables not covered by standard fields

## Invitation Categories (slugs)

`uzatu`, `qyz_uzatu`, `sunnet`, `tusaukesar`, `merey`, `besik`, `betashar`, `other`
