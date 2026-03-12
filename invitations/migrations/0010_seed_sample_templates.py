from django.db import migrations

CLASSIC_HTML = """<!DOCTYPE html>
<html lang="kk">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Georgia', serif; background: #fdf6ec; color: #3a2a1a; }
  .page { max-width: 480px; margin: 0 auto; text-align: center; padding: 48px 24px; }
  .ornament { color: #c9a84c; font-size: 2rem; margin-bottom: 8px; }
  .names { font-size: 2.4rem; font-weight: bold; color: #8b4513; margin: 16px 0; line-height: 1.2; }
  .divider { width: 80px; height: 2px; background: linear-gradient(90deg, transparent, #c9a84c, transparent); margin: 20px auto; }
  .detail-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #a08060; margin-top: 20px; }
  .detail-value { font-size: 1.1rem; color: #3a2a1a; margin-top: 4px; }
  .map-btn { display: inline-block; margin-top: 28px; background: #c9a84c; color: white; padding: 12px 32px; border-radius: 32px; text-decoration: none; font-size: 0.9rem; letter-spacing: 1px; }
  .footer { margin-top: 40px; font-size: 0.8rem; color: #c9a84c; letter-spacing: 3px; }
</style>
</head>
<body>
<div class="page">
  <div class="ornament">✦ ✦ ✦</div>
  <div class="names">{{ bride_name }}<br>&amp;<br>{{ groom_name }}</div>
  <div class="ornament" style="font-size:1.2rem">— ❤ —</div>
  <div class="divider"></div>
  <p class="detail-label">Той күні</p>
  <p class="detail-value">{{ event_date }}</p>
  <p class="detail-label">Уақыты</p>
  <p class="detail-value">{{ event_time }}</p>
  {% if event_location %}
  <p class="detail-label">Мекеме</p>
  <p class="detail-value">{{ event_location }}</p>
  {% endif %}
  {% if address %}
  <p class="detail-label">Мекен-жай</p>
  <p class="detail-value">{{ address }}</p>
  {% endif %}
  {% if map_link %}
  <a href="{{ map_link }}" class="map-btn">Картада қарау</a>
  {% endif %}
  <div class="footer">✦ ШАҚЫРУ ✦</div>
</div>
</body>
</html>"""

MODERN_HTML = """<!DOCTYPE html>
<html lang="kk">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, 'Helvetica Neue', sans-serif; background: #f9f9f7; color: #111; }
  .page { max-width: 480px; margin: 0 auto; padding: 56px 24px; }
  .tag { font-size: 0.7rem; letter-spacing: 4px; text-transform: uppercase; color: #888; }
  .names { font-size: 3rem; font-weight: 700; line-height: 1.1; margin: 12px 0 24px; }
  .names span { color: #888; font-weight: 300; font-size: 1.8rem; display: block; }
  .line { width: 40px; height: 3px; background: #111; margin-bottom: 32px; }
  .row { display: flex; gap: 8px; margin-bottom: 16px; }
  .pill { background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 12px 16px; flex: 1; }
  .pill-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2px; color: #aaa; margin-bottom: 4px; }
  .pill-value { font-size: 0.95rem; font-weight: 600; }
  .venue { background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
  .map-btn { display: block; background: #111; color: #fff; text-align: center; padding: 16px; border-radius: 12px; text-decoration: none; font-size: 0.85rem; letter-spacing: 1px; margin-top: 24px; }
</style>
</head>
<body>
<div class="page">
  <p class="tag">Үйлену шақыруы</p>
  <h1 class="names">{{ bride_name }}<span>&amp; {{ groom_name }}</span></h1>
  <div class="line"></div>
  <div class="row">
    <div class="pill">
      <div class="pill-label">Күні</div>
      <div class="pill-value">{{ event_date }}</div>
    </div>
    <div class="pill">
      <div class="pill-label">Уақыты</div>
      <div class="pill-value">{{ event_time }}</div>
    </div>
  </div>
  {% if event_location %}
  <div class="venue">
    <div class="pill-label">Мекеме</div>
    <div class="pill-value" style="margin-top:4px">{{ event_location }}</div>
    {% if address %}<div style="font-size:0.85rem;color:#888;margin-top:4px">{{ address }}</div>{% endif %}
  </div>
  {% endif %}
  {% if map_link %}
  <a href="{{ map_link }}" class="map-btn">→ Картада ашу</a>
  {% endif %}
</div>
</body>
</html>"""

FORM_SCHEMA = {
    "fields": [
        {"name": "bride_name", "label": "Бойжеткен есімі", "type": "text", "required": True, "placeholder": "Мысалы: Айгерім"},
        {"name": "groom_name", "label": "Жігіт есімі", "type": "text", "required": True, "placeholder": "Мысалы: Асан"},
        {"name": "date", "label": "Той күні", "type": "date", "required": True},
        {"name": "time", "label": "Уақыты", "type": "time", "required": True},
        {"name": "location", "label": "Мекеме / Зал атауы", "type": "text", "required": True, "placeholder": "Мысалы: Рахат сарайы"},
        {"name": "address", "label": "Мекен-жай", "type": "textarea", "placeholder": "Толық мекен-жай..."},
        {"name": "map_url", "label": "Карта сілтемесі (Google Maps)", "type": "url", "placeholder": "https://maps.google.com/..."},
    ]
}


def seed_templates(apps, schema_editor):
    InvitationTemplate = apps.get_model("invitations", "InvitationTemplate")
    InvitationTemplate.objects.get_or_create(
        slug="classic-wedding",
        defaults={
            "name": "Классикалық",
            "html_template": CLASSIC_HTML,
            "form_schema": FORM_SCHEMA,
            "gradient_from": "#C9A84C",
            "gradient_to": "#8B6914",
            "is_free": True,
            "is_active": True,
        },
    )
    InvitationTemplate.objects.get_or_create(
        slug="modern-minimal",
        defaults={
            "name": "Заманауи",
            "html_template": MODERN_HTML,
            "form_schema": FORM_SCHEMA,
            "gradient_from": "#111111",
            "gradient_to": "#444444",
            "is_free": True,
            "is_active": True,
        },
    )


def unseed_templates(apps, schema_editor):
    InvitationTemplate = apps.get_model("invitations", "InvitationTemplate")
    InvitationTemplate.objects.filter(slug__in=["classic-wedding", "modern-minimal"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("invitations", "0009_invitationtemplate_form_schema"),
    ]

    operations = [
        migrations.RunPython(seed_templates, reverse_code=unseed_templates),
    ]
