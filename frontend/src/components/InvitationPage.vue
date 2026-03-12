<script setup>
import axios from 'axios'
import { computed, onMounted, ref, watch } from 'vue'

const props = defineProps({
  slug: {
    type: String,
    default: 'ayan-aruzhan',
  },
})

const loading = ref(true)
const error = ref('')
const renderedHtml = ref('')
const invitation = ref(null)

const apiBase = computed(() => `${window.location.origin}/api/invitations`)
const htmlPageUrl = computed(() => `/i/${props.slug}/`)

async function loadInvitation() {
  loading.value = true
  error.value = ''
  renderedHtml.value = ''
  try {
    const { data } = await axios.get(`${apiBase.value}/${props.slug}/`)
    invitation.value = data
    renderedHtml.value = data.rendered_html || ''
  } catch (e) {
    error.value = 'Шақыру табылмады немесе сервер қателігі.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(loadInvitation)

watch(() => props.slug, loadInvitation)
</script>

<template>
  <div class="inv-wrap">
    <div v-if="loading" class="center-msg">Жүктелуде…</div>

    <div v-else-if="error" class="center-msg error">{{ error }}</div>

    <template v-else>
      <!-- Open full page button -->
      <div class="open-bar">
        <a :href="htmlPageUrl" target="_blank" class="open-btn">
          Толық беттен ашу ↗
        </a>
      </div>

      <!-- Rendered invitation HTML in iframe -->
      <iframe
        v-if="renderedHtml"
        :srcdoc="renderedHtml"
        class="inv-frame"
        title="Шақыру"
        sandbox="allow-scripts allow-same-origin allow-forms"
      />

      <div v-else class="center-msg">
        Бұл шақыру үшін рендерленген HTML жоқ.<br>
        <a :href="htmlPageUrl" class="open-btn" style="margin-top:.8rem;display:inline-block">
          Беттен ашып көру ↗
        </a>
      </div>
    </template>
  </div>
</template>

<style scoped>
.inv-wrap {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.open-bar {
  padding: 8px 16px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  text-align: right;
}

.open-btn {
  display: inline-block;
  padding: 6px 14px;
  background: #111;
  color: #fff;
  border-radius: 8px;
  font-size: 13px;
  text-decoration: none;
  font-weight: 600;
}

.open-btn:hover {
  background: #333;
}

.inv-frame {
  flex: 1;
  width: 100%;
  min-height: calc(100vh - 44px);
  border: 0;
}

.center-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  font-size: 15px;
  color: #6b7280;
  text-align: center;
  padding: 2rem;
}

.center-msg.error {
  color: #b91c1c;
}
</style>

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

.error-text {
  margin-top: 8px;
  font-size: 13px;
  color: #b91c1c;
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

.form-message {
  font-size: 12px;
  color: #a5b4fc;
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
