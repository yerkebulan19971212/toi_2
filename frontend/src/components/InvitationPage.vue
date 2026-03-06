<script setup>
const event = {
  title: 'Shaqyru.kz',
  subtitle: 'Онлайн шақыру',
  coupleNames: 'Аян & Аружан',
  date: '24 Тамыз 2026',
  time: '19:00',
  location: 'Almaty, Dostyk Plaza Event Hall',
  description:
    'Сізді біздің ең қуанышты күнімізге ортақтасуға шақырамыз. Төменде өзіңізге қолайлы статусты таңдап, қатысуыңызды растаңыз.',
}

const stats = [
  { label: 'Қонақтар', value: '120+' },
  { label: 'Үстелдер', value: '12' },
  { label: 'Қатысушылар', value: '85%' },
]
</script>

<template>
  <main class="page">
    <section class="hero">
      <div class="hero-card">
        <header class="hero-header">
          <p class="hero-pill">Shaqyru.kz · Wedding invite</p>
          <h1 class="hero-title">
            {{ event.coupleNames }}
          </h1>
          <p class="hero-subtitle">
            {{ event.subtitle }}
          </p>
        </header>

        <div class="hero-body">
          <div class="hero-info">
            <div class="info-row">
              <span class="info-label">Күні</span>
              <span class="info-value">{{ event.date }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Уақыты</span>
              <span class="info-value">{{ event.time }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Мекенжай</span>
              <span class="info-value">{{ event.location }}</span>
            </div>
          </div>

          <p class="hero-description">
            {{ event.description }}
          </p>

          <div class="hero-actions">
            <button type="button" class="btn btn-primary">Қатысамын</button>
            <button type="button" class="btn btn-secondary">Қатыса алмаймын</button>
          </div>
        </div>

        <footer class="hero-footer">
          <div
            v-for="item in stats"
            :key="item.label"
            class="stat"
          >
            <p class="stat-value">{{ item.value }}</p>
            <p class="stat-label">{{ item.label }}</p>
          </div>
        </footer>
      </div>
    </section>

    <section class="details">
      <div class="details-card">
        <h2 class="details-title">Қонақ деректерін толтыру</h2>
        <p class="details-text">
          Бұл жерде кейін Django арқылы қонақтар тізімі, үстел нөмірлері, RSVP статустар және
          басқа да деректер байланысады. Қазір бұл статикалық макет, бірақ дизайн мобильді
          құрылғыларға толық бейімделген.
        </p>

        <form class="guest-form">
          <div class="form-grid">
            <label class="field">
              <span class="field-label">Аты-жөні</span>
              <input class="field-input" type="text" placeholder="Қонақтың аты" />
            </label>

            <label class="field">
              <span class="field-label">Телефон</span>
              <input class="field-input" type="tel" placeholder="+7 (___) ___‑__‑__" />
            </label>

            <label class="field">
              <span class="field-label">Статус</span>
              <select class="field-input">
                <option>Қатысады</option>
                <option>Қатыса алмайды</option>
                <option>Әлі ойлануда</option>
              </select>
            </label>

            <label class="field">
              <span class="field-label">Үстел</span>
              <input class="field-input" type="number" min="1" placeholder="№" />
            </label>
          </div>

          <label class="field field-full">
            <span class="field-label">Қосымша ақпарат</span>
            <textarea
              class="field-input field-textarea"
              rows="3"
              placeholder="Мысалы: вегетариандық мәзір, балалар саны және т.б."
            />
          </label>

          <div class="form-footer">
            <button type="button" class="btn btn-primary">Қонақты қосу (болашақта API)</button>
            <p class="form-hint">
              Деректер кейін Django API арқылы сақталады, ал шақыру бетінде Vue оларды көрсетеді.
            </p>
          </div>
        </form>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page {
  max-width: 1120px;
  margin: 0 auto;
  padding: 24px 16px 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (min-width: 1024px) {
  .page {
    padding: 40px 24px 56px;
    gap: 32px;
  }
}

.hero {
  display: flex;
  justify-content: center;
}

.hero-card {
  width: 100%;
  max-width: 960px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 28px;
  padding: 20px 18px 18px;
  box-shadow:
    0 24px 60px rgba(15, 23, 42, 0.14),
    0 0 0 1px rgba(148, 163, 184, 0.3);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (min-width: 640px) {
  .hero-card {
    padding: 24px 24px 20px;
    gap: 18px;
  }
}

.hero-header {
  text-align: left;
}

.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  background: radial-gradient(circle at top left, #f9e8ff 0, #fdf2ff 45%, #eff6ff 100%);
  color: #6b21a8;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.hero-title {
  margin-top: 10px;
  font-size: 28px;
  line-height: 1.15;
  letter-spacing: -0.04em;
  font-weight: 800;
}

@media (min-width: 640px) {
  .hero-title {
    font-size: 36px;
  }
}

.hero-subtitle {
  margin-top: 4px;
  font-size: 14px;
  color: #6b7280;
}

.hero-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

@media (min-width: 768px) {
  .hero-body {
    flex-direction: row;
    align-items: flex-start;
    gap: 24px;
  }
}

.hero-info {
  flex: 0 0 220px;
  padding: 12px 14px;
  border-radius: 18px;
  background: linear-gradient(145deg, #f9fafb, #eff6ff);
  border: 1px solid rgba(209, 213, 219, 0.8);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 13px;
}

.info-label {
  color: #6b7280;
}

.info-value {
  font-weight: 600;
  color: #111827;
}

.hero-description {
  flex: 1;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.btn {
  border-radius: 999px;
  padding: 9px 18px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition:
    transform 120ms ease,
    box-shadow 120ms ease,
    background-color 120ms ease,
    color 120ms ease;
}

.btn-primary {
  background: linear-gradient(135deg, #7c3aed, #ec4899);
  color: #fff;
  box-shadow:
    0 14px 30px rgba(129, 140, 248, 0.45),
    0 0 0 1px rgba(255, 255, 255, 0.4);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow:
    0 18px 40px rgba(129, 140, 248, 0.6),
    0 0 0 1px rgba(255, 255, 255, 0.6);
}

.btn-secondary {
  background: rgba(15, 23, 42, 0.02);
  color: #111827;
  border: 1px solid rgba(148, 163, 184, 0.8);
}

.btn-secondary:hover {
  background: rgba(15, 23, 42, 0.04);
}

.hero-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding-top: 10px;
  border-top: 1px dashed rgba(209, 213, 219, 0.7);
}

.stat {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(249, 250, 251, 0.8);
  border: 1px solid rgba(229, 231, 235, 0.9);
  display: inline-flex;
  align-items: baseline;
  gap: 6px;
}

.stat-value {
  font-weight: 700;
  font-size: 14px;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

.details {
  display: flex;
  justify-content: center;
}

.details-card {
  width: 100%;
  max-width: 960px;
  background: rgba(15, 23, 42, 0.9);
  color: #e5e7eb;
  border-radius: 24px;
  padding: 18px 16px 20px;
  box-shadow:
    0 20px 50px rgba(15, 23, 42, 0.6),
    0 0 0 1px rgba(31, 41, 55, 0.9);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (min-width: 640px) {
  .details-card {
    padding: 22px 20px 22px;
  }
}

.details-title {
  font-size: 18px;
  font-weight: 700;
}

.details-text {
  font-size: 13px;
  color: #9ca3af;
  line-height: 1.7;
}

.guest-form {
  margin-top: 2px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 10px;
}

@media (min-width: 640px) {
  .form-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-full {
  width: 100%;
}

.field-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #9ca3af;
}

.field-input {
  border-radius: 999px;
  border: 1px solid rgba(55, 65, 81, 0.9);
  background: rgba(17, 24, 39, 0.9);
  color: #e5e7eb;
  padding: 8px 12px;
  font-size: 14px;
  outline: none;
  transition:
    border-color 120ms ease,
    box-shadow 120ms ease,
    background-color 120ms ease;
}

.field-input::placeholder {
  color: #4b5563;
}

.field-input:focus {
  border-color: #a855f7;
  box-shadow: 0 0 0 1px rgba(168, 85, 247, 0.9);
  background: rgba(17, 24, 39, 0.98);
}

.field-textarea {
  border-radius: 18px;
  resize: vertical;
  min-height: 88px;
}

.form-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 6px;
}

.form-hint {
  font-size: 12px;
  color: #9ca3af;
}

@media (max-width: 480px) {
  .hero-card {
    padding: 18px 14px 16px;
    border-radius: 22px;
  }

  .hero-title {
    font-size: 24px;
  }

  .hero-body {
    gap: 10px;
  }

  .hero-info {
    padding: 10px 12px;
  }

  .details-card {
    padding: 16px 12px 18px;
    border-radius: 20px;
  }

  .btn {
    width: 100%;
    justify-content: center;
    text-align: center;
  }
}
</style>
