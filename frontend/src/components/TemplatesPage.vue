<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const templates = [
  { name: 'Premium Gold', type: 'Үйлену тойы', color: 'gold' },
  { name: 'Classic Green', type: 'Құдалық', color: 'green' },
  { name: 'Velvet Night', type: 'Кешкі той', color: 'purple' },
  { name: 'Soft Peach', type: 'Туған күн', color: 'peach' },
  { name: 'Minimal White', type: 'Корпоратив', color: 'blue' },
  { name: 'Traditional', type: 'Сүндет той', color: 'amber' },
  { name: 'Summer Breeze', type: 'Outdoor', color: 'emerald' },
  { name: 'City Lights', type: 'Modern', color: 'indigo' },
]

function openSample() {
  router.push({ name: 'invitation', params: { slug: 'ayan-aruzhan' } })
}
</script>

<template>
  <div class="templates">
    <section class="header">
      <div class="header-inner">
        <div>
          <p class="eyebrow">Shaqyru.kz</p>
          <h1 class="title">Сайт шақыру үлгілері</h1>
          <p class="subtitle">
            Әр үлгі мобильді құрылғыларға бейімделген және сіздің тойыңызға арнайы бапталады.
          </p>
        </div>
        <button type="button" class="btn" @click="openSample">Дайын үлгіні ашу</button>
      </div>
    </section>

    <section class="grid-wrap">
      <div class="grid">
        <article
          v-for="tpl in templates"
          :key="tpl.name"
          class="tpl-card"
          :data-color="tpl.color"
        >
          <div class="tpl-gradient" />
          <div class="tpl-content">
            <p class="tpl-type">{{ tpl.type }}</p>
            <h2 class="tpl-name">{{ tpl.name }}</h2>
            <p class="tpl-footer">Мобильді · QR арқылы ашылады</p>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.templates {
  padding: 24px 16px 40px;
}

@media (min-width: 1024px) {
  .templates {
    padding: 32px 40px 56px;
  }
}

.header-inner {
  max-width: 1120px;
  margin: 0 auto 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (min-width: 768px) {
  .header-inner {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-end;
  }
}

.eyebrow {
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9ca3af;
}

.title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: #111827;
}

.subtitle {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.btn {
  align-self: flex-start;
  margin-top: 4px;
  border-radius: 999px;
  padding: 8px 16px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  background: linear-gradient(135deg, #f97316, #e11d48);
  color: #fff;
  cursor: pointer;
}

.grid-wrap {
  max-width: 1120px;
  margin: 0 auto;
}

.grid {
  display: grid;
  gap: 16px;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.tpl-card {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  min-height: 130px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.16);
}

.tpl-gradient {
  position: absolute;
  inset: 0;
  opacity: 0.98;
}

.tpl-card[data-color='gold'] .tpl-gradient {
  background: linear-gradient(135deg, #facc15, #f97316, #b45309);
}

.tpl-card[data-color='green'] .tpl-gradient {
  background: linear-gradient(135deg, #22c55e, #16a34a, #15803d);
}

.tpl-card[data-color='purple'] .tpl-gradient {
  background: linear-gradient(135deg, #a855f7, #7e22ce, #312e81);
}

.tpl-card[data-color='peach'] .tpl-gradient {
  background: linear-gradient(135deg, #fb923c, #f97316, #e11d48);
}

.tpl-card[data-color='blue'] .tpl-gradient {
  background: linear-gradient(135deg, #38bdf8, #0ea5e9, #1d4ed8);
}

.tpl-card[data-color='amber'] .tpl-gradient {
  background: linear-gradient(135deg, #fbbf24, #f97316, #92400e);
}

.tpl-card[data-color='emerald'] .tpl-gradient {
  background: linear-gradient(135deg, #34d399, #059669, #065f46);
}

.tpl-card[data-color='indigo'] .tpl-gradient {
  background: linear-gradient(135deg, #4f46e5, #1d4ed8, #0f172a);
}

.tpl-content {
  position: relative;
  padding: 14px 14px 16px;
  color: #f9fafb;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.tpl-type {
  font-size: 12px;
  opacity: 0.9;
}

.tpl-name {
  margin-top: 6px;
  font-size: 17px;
  font-weight: 700;
}

.tpl-footer {
  margin-top: 8px;
  font-size: 11px;
  opacity: 0.92;
}
</style>

