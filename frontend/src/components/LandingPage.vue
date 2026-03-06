<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const inviteTypes = [
  { title: 'Үйлену тойы', description: 'Классикалық және заманауи шақырулар', icon: '💍' },
  { title: 'Сүндет той', description: 'Балаларға арналған қуанышты стиль', icon: '🧒' },
  { title: 'Туған күн', description: 'Жанды және көңілді дизайндар', icon: '🎂' },
  { title: 'Корпоратив', description: 'Іскерлік стильдегі шақырулар', icon: '🏢' },
  { title: 'Құдалық', description: 'Дәстүрлі элементтері бар шақырулар', icon: '🧿' },
  { title: 'Басқа', description: 'Өзіңізге арнайы формат', icon: '✨' },
]

const popularInvites = [
  {
    title: 'Premium Gold',
    subtitle: 'Заманауи, минимал стиль',
    badge: 'Ең танымал',
    tone: 'gold',
  },
  {
    title: 'Classic Green',
    subtitle: 'Дәстүрлі тойларға',
    badge: 'Ұсынылады',
    tone: 'green',
  },
  {
    title: 'Night Velvet',
    subtitle: 'Вечерние тойларға',
    badge: 'Жаңа',
    tone: 'brown',
  },
]

const steps = [
  {
    title: 'Той түрін таңдаңыз',
    description: 'Сізге қажет той түрін және шақыру үлгісін таңдаңыз.',
  },
  {
    title: 'Ақпаратты енгізіңіз',
    description: 'Қонақтар, мекенжай, уақыт және басқа деректерді толтырыңыз.',
  },
  {
    title: 'Сілтемені бөлісіңіз',
    description: 'Дайын шақыру сілтемесін WhatsApp немесе әлеуметтік желілерде жіберіңіз.',
  },
]

const currentYear = computed(() => new Date().getFullYear())

function goToTemplates() {
  router.push({ name: 'templates' })
}

function goToSample() {
  router.push({ name: 'invitation', params: { slug: 'ayan-aruzhan' } })
}
</script>

<template>
  <div class="landing">
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <p class="hero-pill">Shaqyru.kz · Онлайн шақыру</p>
          <h1 class="hero-title">
            Тойыңызға арналған шақыру
            <span class="hero-gradient">5 минутта дайын</span>
          </h1>
          <p class="hero-subtitle">
            Қағаз шақырусыз, кез келген құрылғыдан ашылатын заманауи сайт-шақыру жасаңыз.
          </p>

          <div class="hero-actions">
            <button type="button" class="btn btn-primary" @click="goToTemplates">
              Шақыру үлгілерін көру
            </button>
            <button type="button" class="btn btn-secondary" @click="goToSample">
              Дайын сайт мысалын ашу
            </button>
          </div>

          <div class="hero-metrics">
            <div class="metric">
              <span class="metric-value">3k+</span>
              <span class="metric-label">дайын шақыру</span>
            </div>
            <div class="metric">
              <span class="metric-value">5 мин</span>
              <span class="metric-label">орташа жасау уақыты</span>
            </div>
            <div class="metric">
              <span class="metric-value">24/7</span>
              <span class="metric-label">қолжетімді</span>
            </div>
          </div>
        </div>

        <div class="hero-phone">
          <div class="phone-frame">
            <div class="phone-screen">
              <p class="phone-badge">Live preview</p>
              <p class="phone-title">Shaqyru.kz</p>
              <p class="phone-text">Қонаққа арналған дайын сайт көрінісі.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <h2 class="section-title">Той түрін таңдаңыз</h2>
        <p class="section-subtitle">
          Әр той түріне бөлек стиль, түс және сценарий ұсынылады.
        </p>
      </div>
      <div class="grid invite-types">
        <article v-for="t in inviteTypes" :key="t.title" class="card-type">
          <div class="card-icon">{{ t.icon }}</div>
          <h3 class="card-title">{{ t.title }}</h3>
          <p class="card-text">{{ t.description }}</p>
        </article>
      </div>
    </section>

    <section class="section section-alt">
      <div class="section-header">
        <h2 class="section-title">3 қадаммен шақыру</h2>
        <p class="section-subtitle">Той сайтын жасау процесі өте қарапайым.</p>
      </div>
      <div class="grid steps">
        <article v-for="(s, idx) in steps" :key="s.title" class="card-step">
          <span class="step-index">{{ idx + 1 }}</span>
          <h3 class="card-title">{{ s.title }}</h3>
          <p class="card-text">{{ s.description }}</p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <h2 class="section-title">Ең көп таңдалатын шақырулар</h2>
        <p class="section-subtitle">
          Пайдаланушылар жиі таңдайтын танымал сайт-шақырулар.
        </p>
      </div>
      <div class="popular-grid">
        <article
          v-for="p in popularInvites"
          :key="p.title"
          class="popular-card"
          :data-tone="p.tone"
        >
          <span class="popular-badge">{{ p.badge }}</span>
          <h3 class="popular-title">{{ p.title }}</h3>
          <p class="popular-subtitle">{{ p.subtitle }}</p>
          <button type="button" class="popular-link" @click="goToTemplates">
            Үлгіні көру
          </button>
        </article>
      </div>
    </section>

    <section class="section section-cta">
      <div class="cta-card">
        <div>
          <h2 class="cta-title">Тойыңызға шақыруды бүгін бастаңыз</h2>
          <p class="cta-text">
            Бірнеше минут ішінде сайтты дайындап, қонақтарыңызға әдемі сілтеме жіберіңіз.
          </p>
        </div>
        <button type="button" class="btn btn-light" @click="goToSample">
          Дайын мысалды ашу
        </button>
      </div>
    </section>

    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-main">
          <p class="footer-logo">Shaqyru.kz</p>
          <p class="footer-text">Той шақыруға арналған заманауи онлайн-платформа.</p>
        </div>
        <div class="footer-links">
          <a href="#" class="footer-link">Құпиялылық</a>
          <a href="#" class="footer-link">Қолдау</a>
        </div>
        <p class="footer-copy">© {{ currentYear }} Shaqyru.kz. Барлық құқықтар қорғалған.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.hero {
  background: linear-gradient(180deg, #fef3e8 0%, #fff7ed 40%, #ffffff 100%);
  padding: 24px 16px 40px;
}

@media (min-width: 1024px) {
  .hero {
    padding: 32px 40px 56px;
  }
}

.hero-inner {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
  gap: 32px;
  align-items: center;
}

@media (max-width: 768px) {
  .hero-inner {
    grid-template-columns: minmax(0, 1fr);
  }
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.hero-pill {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 600;
  border-radius: 999px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: rgba(251, 191, 36, 0.08);
  color: #92400e;
}

.hero-title {
  font-size: 28px;
  line-height: 1.15;
  letter-spacing: -0.04em;
  color: #111827;
}

.hero-gradient {
  display: block;
  background: linear-gradient(135deg, #f97316, #e11d48);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
}

.hero-subtitle {
  font-size: 14px;
  color: #4b5563;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hero-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 6px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metric-value {
  font-weight: 700;
  font-size: 18px;
}

.metric-label {
  font-size: 12px;
  color: #6b7280;
}

.hero-phone {
  display: flex;
  justify-content: center;
}

.phone-frame {
  width: 220px;
  height: 420px;
  border-radius: 32px;
  padding: 12px;
  background: linear-gradient(145deg, #f97316, #facc15);
  box-shadow:
    0 24px 60px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.5);
}

.phone-screen {
  width: 100%;
  height: 100%;
  border-radius: 26px;
  background: radial-gradient(circle at top, #f9fafb 0%, #e5e7eb 60%, #d1d5db 100%);
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 6px;
}

.phone-badge {
  align-self: flex-start;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.9);
  color: #e5e7eb;
}

.phone-title {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.phone-text {
  font-size: 12px;
  color: #4b5563;
}

.section {
  padding: 0 16px;
}

.section-alt {
  background: #f9fafb;
  padding-top: 28px;
  padding-bottom: 28px;
}

@media (min-width: 1024px) {
  .section,
  .section-alt {
    padding: 0 40px;
  }
}

.section-header {
  max-width: 1120px;
  margin: 0 auto 16px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.section-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.grid {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  gap: 12px;
}

.invite-types {
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
}

.card-type {
  background: #ffffff;
  border-radius: 18px;
  padding: 14px 14px 16px;
  border: 1px solid rgba(229, 231, 235, 0.9);
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.04);
}

.card-icon {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(249, 250, 251, 0.9);
  margin-bottom: 8px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.card-text {
  font-size: 13px;
  color: #6b7280;
}

.steps {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.card-step {
  background: #ffffff;
  border-radius: 18px;
  padding: 16px 16px 18px;
  border: 1px dashed rgba(209, 213, 219, 0.9);
}

.step-index {
  display: inline-flex;
  width: 26px;
  height: 26px;
  border-radius: 999px;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  background: rgba(249, 115, 22, 0.1);
  color: #ea580c;
  margin-bottom: 8px;
}

.popular-grid {
  max-width: 1120px;
  margin: 8px auto 0;
  display: grid;
  gap: 16px;
}

@media (min-width: 768px) {
  .popular-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.popular-card {
  border-radius: 18px;
  padding: 18px 16px 16px;
  color: #f9fafb;
  position: relative;
  overflow: hidden;
}

.popular-card::before {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.94;
}

.popular-card[data-tone='gold']::before {
  background: linear-gradient(135deg, #facc15, #f97316, #b45309);
}

.popular-card[data-tone='green']::before {
  background: linear-gradient(135deg, #22c55e, #15803d, #052e16);
}

.popular-card[data-tone='brown']::before {
  background: linear-gradient(135deg, #7c2d12, #4b1d0a, #111827);
}

.popular-card > * {
  position: relative;
}

.popular-badge {
  display: inline-flex;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(15, 23, 42, 0.85);
}

.popular-title {
  margin-top: 10px;
  font-size: 18px;
  font-weight: 700;
}

.popular-subtitle {
  font-size: 13px;
  margin-top: 4px;
  opacity: 0.9;
}

.popular-link {
  margin-top: 12px;
  background: rgba(15, 23, 42, 0.1);
  border-radius: 999px;
  border: 1px solid rgba(249, 250, 251, 0.4);
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 500;
  color: inherit;
  cursor: pointer;
}

.section-cta {
  padding-bottom: 32px;
}

.cta-card {
  max-width: 1120px;
  margin: 0 auto;
  background: linear-gradient(135deg, #f97316, #facc15);
  border-radius: 24px;
  padding: 18px 18px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  color: #111827;
}

@media (min-width: 768px) {
  .cta-card {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.cta-title {
  font-size: 18px;
  font-weight: 700;
}

.cta-text {
  font-size: 14px;
}

.btn {
  border-radius: 999px;
  padding: 9px 18px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #f97316, #e11d48);
  color: #fff;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.6);
  color: #111827;
  border: 1px solid rgba(209, 213, 219, 0.8);
}

.btn-light {
  background: #111827;
  color: #f9fafb;
}

.site-footer {
  background: #020617;
  color: #9ca3af;
  padding: 24px 16px 28px;
  margin-top: 8px;
}

.footer-inner {
  max-width: 1120px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-logo {
  font-weight: 700;
  color: #e5e7eb;
}

.footer-text {
  font-size: 13px;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 13px;
}

.footer-link {
  color: inherit;
  text-decoration: none;
}

.footer-link:hover {
  color: #e5e7eb;
}

.footer-copy {
  font-size: 12px;
  color: #6b7280;
}

@media (max-width: 480px) {
  .cta-card {
    border-radius: 20px;
  }

  .hero {
    padding-bottom: 32px;
  }
}
</style>

