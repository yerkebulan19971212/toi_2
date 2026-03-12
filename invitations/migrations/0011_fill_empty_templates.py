from django.db import migrations

# ── Алтын той (Gold gradient — matches the screenshot) ──────────────────────
ALTYN_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Georgia',serif;min-height:100vh;background:linear-gradient(160deg,#c9a84c 0%,#a07020 40%,#7a5010 100%);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:2.5rem 1rem 3rem}
.star{font-size:1.8rem;color:rgba(255,255,255,.7);margin-bottom:.4rem}
.label{font-size:.65rem;letter-spacing:.25em;text-transform:uppercase;color:rgba(255,255,255,.65);margin-bottom:.8rem}
.bride{font-size:clamp(2.4rem,10vw,4rem);font-weight:bold;line-height:1.05;text-align:center}
.sep{display:flex;align-items:center;gap:.7rem;width:60%;max-width:200px;margin:.5rem auto}
.sep-line{flex:1;height:1px;background:rgba(255,255,255,.4)}
.sep-amp{font-size:.9rem;color:rgba(255,255,255,.6)}
.groom{font-size:clamp(2.4rem,10vw,4rem);font-weight:bold;line-height:1.05;text-align:center;margin-bottom:2rem}
.card{background:rgba(255,255,255,.18);backdrop-filter:blur(8px);border-radius:18px;padding:1.2rem 1.6rem;width:100%;max-width:360px;margin-bottom:1rem;text-align:center}
.card-label{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:.3rem}
.card-main{font-size:1.25rem;font-weight:bold;color:#fff}
.card-sub{font-size:.9rem;color:rgba(255,255,255,.75);margin-top:.15rem}
.map-link{display:inline-flex;align-items:center;gap:.3rem;margin-top:.6rem;font-size:.8rem;color:rgba(255,255,255,.8);text-decoration:underline}
{% if description %}
.desc-card{background:rgba(255,255,255,.12);border-radius:14px;padding:1rem 1.4rem;width:100%;max-width:360px;font-size:.9rem;line-height:1.6;color:rgba(255,255,255,.85);text-align:center;margin-bottom:1rem}
{% endif %}
</style>
</head>
<body>
  <div class="star">✦</div>
  <p class="label">Той шақыруы</p>
  <div class="bride">{{ bride_name }}</div>
  <div class="sep"><div class="sep-line"></div><span class="sep-amp">&amp;</span><div class="sep-line"></div></div>
  <div class="groom">{{ groom_name }}</div>

  <div class="card">
    <div class="card-label">Той күні</div>
    <div class="card-main">{{ event_date }}</div>
    {% if event_time %}<div class="card-sub">{{ event_time }}</div>{% endif %}
  </div>

  {% if event_location %}
  <div class="card">
    <div class="card-label">Орны</div>
    <div class="card-main">{{ event_location }}</div>
    {% if address %}<div class="card-sub">{{ address }}</div>{% endif %}
    {% if map_link %}
    <a class="map-link" href="{{ map_link }}" target="_blank" rel="noopener">
      &#x1F4CD; Картадан қарау
    </a>
    {% endif %}
  </div>
  {% endif %}

  {% if description %}
  <div class="desc-card">{{ description }}</div>
  {% endif %}

  <div id="rsvp-section"></div>
</body>
</html>"""

# ── PRESTIGE (dark luxury) ───────────────────────────────────────────────────
PRESTIGE_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Georgia',serif;background:#0d0d0d;color:#e8d5a3;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:3rem 1rem}
.ornament{font-size:1.2rem;letter-spacing:.5em;color:#c9a84c;margin-bottom:1rem}
.eyebrow{font-size:.6rem;letter-spacing:.35em;text-transform:uppercase;color:#888;margin-bottom:1.5rem}
.names{font-size:clamp(2rem,9vw,3.5rem);font-weight:400;text-align:center;line-height:1.15;color:#f0e0b0;letter-spacing:.08em}
.names .amp{color:#c9a84c;font-style:italic}
.divider{width:60px;height:1px;background:linear-gradient(90deg,transparent,#c9a84c,transparent);margin:1.5rem auto}
.info{display:grid;gap:.8rem;width:100%;max-width:340px;margin:1rem 0}
.info-row{display:flex;justify-content:space-between;border-bottom:1px solid rgba(201,168,76,.15);padding-bottom:.6rem;font-size:.9rem}
.info-label{color:#888;font-size:.7rem;letter-spacing:.15em;text-transform:uppercase;align-self:center}
.info-val{color:#f0e0b0;font-weight:bold;text-align:right}
.map-btn{margin-top:1.5rem;display:inline-block;padding:.7rem 2rem;border:1px solid #c9a84c;color:#c9a84c;text-decoration:none;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;border-radius:2px;transition:.2s}
.map-btn:hover{background:#c9a84c;color:#0d0d0d}
</style>
</head>
<body>
  <div class="ornament">— ✦ —</div>
  <p class="eyebrow">Той шақыруы</p>
  <div class="names">{{ bride_name }}<br><span class="amp">&amp;</span><br>{{ groom_name }}</div>
  <div class="divider"></div>
  <div class="info">
    <div class="info-row"><span class="info-label">Күні</span><span class="info-val">{{ event_date }}</span></div>
    {% if event_time %}<div class="info-row"><span class="info-label">Уақыты</span><span class="info-val">{{ event_time }}</span></div>{% endif %}
    {% if event_location %}<div class="info-row"><span class="info-label">Мекеме</span><span class="info-val">{{ event_location }}</span></div>{% endif %}
    {% if address %}<div class="info-row"><span class="info-label">Мекен-жай</span><span class="info-val">{{ address }}</span></div>{% endif %}
  </div>
  {% if map_link %}<a class="map-btn" href="{{ map_link }}" target="_blank">Картада қарау</a>{% endif %}
  <div id="rsvp-section"></div>
</body>
</html>"""

# ── DARАБОЗА (traditional Kazakh — warm earthy tones) ───────────────────────
DARABOZA_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Georgia',serif;background:#fdf0e0;color:#3a1a00;min-height:100vh}
.header{background:linear-gradient(135deg,#8b3a0f,#c05010);padding:3rem 1.5rem 2rem;text-align:center}
.header-ornament{font-size:1.4rem;color:rgba(255,220,150,.7);letter-spacing:.4em;margin-bottom:.5rem}
.header-label{font-size:.65rem;letter-spacing:.3em;text-transform:uppercase;color:rgba(255,220,150,.8)}
.names{font-size:clamp(2rem,9vw,3.2rem);font-weight:bold;color:#fff;margin:.6rem 0;line-height:1.1;text-align:center}
.amp{color:rgba(255,220,150,.8);font-style:italic;font-size:1.5rem;display:block}
.body{padding:2rem 1rem;max-width:440px;margin:0 auto}
.detail-block{background:#fff;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.8rem;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.detail-label{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:#a05030;margin-bottom:.2rem}
.detail-val{font-size:1.05rem;font-weight:bold;color:#3a1a00}
.detail-sub{font-size:.85rem;color:#666;margin-top:.15rem}
.map-btn{display:block;margin:.8rem auto 0;width:fit-content;padding:.7rem 1.8rem;background:#8b3a0f;color:#fff;text-decoration:none;border-radius:24px;font-size:.85rem}
</style>
</head>
<body>
  <div class="header">
    <div class="header-ornament">❧ ❧ ❧</div>
    <p class="header-label">Той шақыруы</p>
    <div class="names">{{ bride_name }}<span class="amp">&amp;</span>{{ groom_name }}</div>
  </div>
  <div class="body">
    <div class="detail-block">
      <div class="detail-label">Той күні</div>
      <div class="detail-val">{{ event_date }}</div>
      {% if event_time %}<div class="detail-sub">{{ event_time }}</div>{% endif %}
    </div>
    {% if event_location %}
    <div class="detail-block">
      <div class="detail-label">Орны</div>
      <div class="detail-val">{{ event_location }}</div>
      {% if address %}<div class="detail-sub">{{ address }}</div>{% endif %}
      {% if map_link %}<a class="map-btn" href="{{ map_link }}" target="_blank">Картада қарау</a>{% endif %}
    </div>
    {% endif %}
    {% if description %}<div class="detail-block"><div class="detail-label">Хабарлама</div><div class="detail-sub" style="font-size:.95rem">{{ description }}</div></div>{% endif %}
  </div>
  <div id="rsvp-section"></div>
</body>
</html>"""

# ── MIRELA (modern feminine — blush/rose) ───────────────────────────────────
MIRELA_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=Lato:wght@300;400&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Lato',sans-serif;background:#fdf6f9;color:#3a2030;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:3rem 1.2rem 4rem}
.top-line{width:40px;height:2px;background:#d4849a;margin-bottom:1.5rem}
.eyebrow{font-size:.6rem;letter-spacing:.35em;text-transform:uppercase;color:#a06080;margin-bottom:1rem}
.names{font-family:'Playfair Display',serif;font-size:clamp(2.2rem,9vw,3.8rem);line-height:1.1;text-align:center;color:#7a2040;font-style:italic}
.amp{color:#d4849a;display:block;font-size:1.8rem;margin:.3rem 0}
.divider{width:100px;height:1px;background:linear-gradient(90deg,transparent,#d4849a,transparent);margin:1.5rem 0}
.pill{background:#fff;border:1px solid #f0c0d0;border-radius:14px;padding:1rem 1.4rem;width:100%;max-width:340px;margin-bottom:.7rem;text-align:center}
.pill-label{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:#a06080;margin-bottom:.3rem}
.pill-main{font-size:1.05rem;font-weight:600;color:#7a2040}
.pill-sub{font-size:.85rem;color:#a08090;margin-top:.2rem}
.btn-map{margin-top:.6rem;display:inline-block;font-size:.8rem;color:#d4849a;text-decoration:underline}
</style>
</head>
<body>
  <div class="top-line"></div>
  <p class="eyebrow">Үйлену тойы</p>
  <div class="names">{{ bride_name }}<span class="amp">&amp;</span>{{ groom_name }}</div>
  <div class="divider"></div>
  <div class="pill">
    <div class="pill-label">Той күні</div>
    <div class="pill-main">{{ event_date }}</div>
    {% if event_time %}<div class="pill-sub">{{ event_time }}</div>{% endif %}
  </div>
  {% if event_location %}
  <div class="pill">
    <div class="pill-label">Мекен-жай</div>
    <div class="pill-main">{{ event_location }}</div>
    {% if address %}<div class="pill-sub">{{ address }}</div>{% endif %}
    {% if map_link %}<a class="btn-map" href="{{ map_link }}" target="_blank">Картадан қарау</a>{% endif %}
  </div>
  {% endif %}
  <div id="rsvp-section"></div>
</body>
</html>"""

# ── Арман (romantic dreamy — deep blue/indigo) ───────────────────────────────
ARMAN_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Georgia',serif;background:linear-gradient(160deg,#1a1a4e 0%,#0d0d30 100%);color:#e0e8ff;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:3rem 1rem 4rem}
.stars{font-size:1rem;letter-spacing:.6em;color:rgba(200,210,255,.4);margin-bottom:1.2rem}
.label{font-size:.6rem;letter-spacing:.3em;text-transform:uppercase;color:rgba(180,200,255,.5);margin-bottom:1.2rem}
.names{font-size:clamp(2.2rem,9vw,3.6rem);font-weight:400;text-align:center;line-height:1.15;color:#c8d4ff;letter-spacing:.05em}
.amp{color:rgba(180,200,255,.4);font-style:italic;font-size:1.5rem;display:block;margin:.2rem 0}
.sep{width:50px;height:1px;background:rgba(180,200,255,.2);margin:1.5rem auto}
.card{background:rgba(255,255,255,.07);border:1px solid rgba(180,200,255,.15);border-radius:14px;padding:1rem 1.4rem;width:100%;max-width:340px;margin-bottom:.7rem;text-align:center}
.card-label{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(180,200,255,.45);margin-bottom:.3rem}
.card-main{font-size:1.1rem;font-weight:bold;color:#c8d4ff}
.card-sub{font-size:.85rem;color:rgba(200,220,255,.6);margin-top:.2rem}
.map-link{display:inline-block;margin-top:.5rem;font-size:.8rem;color:rgba(180,200,255,.7);text-decoration:underline}
</style>
</head>
<body>
  <div class="stars">★ ★ ★</div>
  <p class="label">Той шақыруы</p>
  <div class="names">{{ bride_name }}<span class="amp">&amp;</span>{{ groom_name }}</div>
  <div class="sep"></div>
  <div class="card">
    <div class="card-label">Той күні</div>
    <div class="card-main">{{ event_date }}</div>
    {% if event_time %}<div class="card-sub">{{ event_time }}</div>{% endif %}
  </div>
  {% if event_location %}
  <div class="card">
    <div class="card-label">Орны</div>
    <div class="card-main">{{ event_location }}</div>
    {% if address %}<div class="card-sub">{{ address }}</div>{% endif %}
    {% if map_link %}<a class="map-link" href="{{ map_link }}" target="_blank">Картадан қарау</a>{% endif %}
  </div>
  {% endif %}
  <div id="rsvp-section"></div>
</body>
</html>"""

# ── Аспан (sky blue — airy) ─────────────────────────────────────────────────
ASPAN_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,sans-serif;background:linear-gradient(180deg,#e8f4ff 0%,#c8e6ff 100%);color:#1a3050;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:3rem 1rem 4rem}
.cloud{font-size:1.6rem;margin-bottom:.5rem;opacity:.6}
.label{font-size:.6rem;letter-spacing:.3em;text-transform:uppercase;color:#5090c0;margin-bottom:1.2rem}
.names{font-size:clamp(2rem,9vw,3.4rem);font-weight:700;text-align:center;line-height:1.1;color:#1a3050}
.amp{color:#5090c0;font-size:1.4rem;display:block;margin:.3rem 0;font-weight:300}
.line{width:50px;height:2px;background:#5090c0;border-radius:2px;margin:1.2rem auto}
.card{background:#fff;border-radius:16px;padding:1rem 1.4rem;width:100%;max-width:340px;margin-bottom:.7rem;box-shadow:0 4px 20px rgba(80,144,192,.12);text-align:center}
.card-label{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:#5090c0;margin-bottom:.3rem}
.card-main{font-size:1.1rem;font-weight:700;color:#1a3050}
.card-sub{font-size:.85rem;color:#6080a0;margin-top:.15rem}
.map-link{margin-top:.5rem;display:inline-block;font-size:.8rem;color:#5090c0;text-decoration:underline}
</style>
</head>
<body>
  <div class="cloud">☁</div>
  <p class="label">Той шақыруы</p>
  <div class="names">{{ bride_name }}<span class="amp">&amp;</span>{{ groom_name }}</div>
  <div class="line"></div>
  <div class="card">
    <div class="card-label">Той күні</div>
    <div class="card-main">{{ event_date }}</div>
    {% if event_time %}<div class="card-sub">{{ event_time }}</div>{% endif %}
  </div>
  {% if event_location %}
  <div class="card">
    <div class="card-label">Орны</div>
    <div class="card-main">{{ event_location }}</div>
    {% if address %}<div class="card-sub">{{ address }}</div>{% endif %}
    {% if map_link %}<a class="map-link" href="{{ map_link }}" target="_blank">Картадан қарау</a>{% endif %}
  </div>
  {% endif %}
  <div id="rsvp-section"></div>
</body>
</html>"""

# ── Бесік (baby cradle — soft mint/green) ───────────────────────────────────
BESIK_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Georgia',serif;background:#f0faf4;color:#1a3a2a;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:3rem 1rem 4rem}
.icon{font-size:2rem;margin-bottom:.5rem}
.label{font-size:.6rem;letter-spacing:.3em;text-transform:uppercase;color:#4a8060;margin-bottom:1.2rem}
.title{font-size:clamp(1.6rem,7vw,2.8rem);font-weight:bold;text-align:center;color:#1a3a2a;line-height:1.2}
.sep{width:60px;height:2px;background:linear-gradient(90deg,transparent,#4a8060,transparent);margin:1rem auto}
.card{background:#fff;border-left:3px solid #4a8060;border-radius:0 12px 12px 0;padding:1rem 1.2rem;width:100%;max-width:340px;margin-bottom:.7rem}
.card-label{font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;color:#4a8060;margin-bottom:.25rem}
.card-main{font-size:1.05rem;font-weight:bold}
.card-sub{font-size:.85rem;color:#567060;margin-top:.15rem}
.map-link{margin-top:.5rem;display:inline-block;font-size:.8rem;color:#4a8060;text-decoration:underline}
</style>
</head>
<body>
  <div class="icon">🌿</div>
  <p class="label">Бесік той шақыруы</p>
  <div class="title">{{ event_title }}</div>
  <div class="sep"></div>
  <div class="card">
    <div class="card-label">Той күні</div>
    <div class="card-main">{{ event_date }}</div>
    {% if event_time %}<div class="card-sub">{{ event_time }}</div>{% endif %}
  </div>
  {% if event_location %}
  <div class="card">
    <div class="card-label">Орны</div>
    <div class="card-main">{{ event_location }}</div>
    {% if address %}<div class="card-sub">{{ address }}</div>{% endif %}
    {% if map_link %}<a class="map-link" href="{{ map_link }}" target="_blank">Картадан қарау</a>{% endif %}
  </div>
  {% endif %}
  {% if description %}<div class="card"><div class="card-label">Хабарлама</div><div class="card-sub" style="font-size:.9rem">{{ description }}</div></div>{% endif %}
  <div id="rsvp-section"></div>
</body>
</html>"""

# ── Жасыл бақ (Green garden — fresh) ────────────────────────────────────────
JASYL_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ event_title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Georgia',serif;background:#f5fbf0;color:#1a3010;min-height:100vh}
.hero{background:linear-gradient(135deg,#2d7a3a,#1a5025);padding:3rem 1.5rem 2.5rem;text-align:center}
.leaf{font-size:1.4rem;opacity:.7;margin-bottom:.5rem}
.hero-label{font-size:.6rem;letter-spacing:.3em;text-transform:uppercase;color:rgba(200,240,180,.7);margin-bottom:.8rem}
.names{font-size:clamp(2rem,9vw,3.4rem);font-weight:bold;color:#fff;line-height:1.1}
.amp{color:rgba(200,240,180,.6);font-style:italic;font-size:1.5rem;display:block;margin:.2rem 0}
.body{padding:1.5rem 1rem 2rem;max-width:440px;margin:0 auto}
.item{background:#fff;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.7rem;border:1px solid #d0ecc0}
.item-label{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:#3a7030;margin-bottom:.25rem}
.item-main{font-size:1.05rem;font-weight:bold;color:#1a3010}
.item-sub{font-size:.85rem;color:#567050;margin-top:.15rem}
.map-btn{margin-top:.5rem;display:inline-block;padding:.45rem 1.2rem;background:#2d7a3a;color:#fff;text-decoration:none;border-radius:20px;font-size:.8rem}
</style>
</head>
<body>
  <div class="hero">
    <div class="leaf">🌿</div>
    <p class="hero-label">Той шақыруы</p>
    <div class="names">{{ bride_name }}<span class="amp">&amp;</span>{{ groom_name }}</div>
  </div>
  <div class="body">
    <div class="item">
      <div class="item-label">Той күні</div>
      <div class="item-main">{{ event_date }}</div>
      {% if event_time %}<div class="item-sub">{{ event_time }}</div>{% endif %}
    </div>
    {% if event_location %}
    <div class="item">
      <div class="item-label">Орны</div>
      <div class="item-main">{{ event_location }}</div>
      {% if address %}<div class="item-sub">{{ address }}</div>{% endif %}
      {% if map_link %}<a class="map-btn" href="{{ map_link }}" target="_blank">Картада қарау</a>{% endif %}
    </div>
    {% endif %}
    {% if description %}<div class="item"><div class="item-label">Хабарлама</div><div class="item-sub" style="font-size:.9rem">{{ description }}</div></div>{% endif %}
  </div>
  <div id="rsvp-section"></div>
</body>
</html>"""

TEMPLATE_MAP = {
    "алтын-той-93aaab":   ALTYN_HTML,
    "prestige-ea88c8":    PRESTIGE_HTML,
    "darабоза-14f0d3":    DARABOZA_HTML,
    "mirela-d3a274":      MIRELA_HTML,
    "арман-ca624d":       ARMAN_HTML,
    "аспан-ca24d9":       ASPAN_HTML,
    "бесік-fc3abc":       BESIK_HTML,
    "жасыл-бақ-2da339":  JASYL_HTML,
}


def fill_templates(apps, schema_editor):
    InvitationTemplate = apps.get_model("invitations", "InvitationTemplate")
    for slug, html in TEMPLATE_MAP.items():
        InvitationTemplate.objects.filter(slug=slug, html_template="").update(html_template=html)


def unfill_templates(apps, schema_editor):
    InvitationTemplate = apps.get_model("invitations", "InvitationTemplate")
    InvitationTemplate.objects.filter(slug__in=list(TEMPLATE_MAP.keys())).update(html_template="")


class Migration(migrations.Migration):

    dependencies = [
        ("invitations", "0010_seed_sample_templates"),
    ]

    operations = [
        migrations.RunPython(fill_templates, reverse_code=unfill_templates),
    ]
