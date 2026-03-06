<script setup>
import axios from 'axios'
import { computed, onMounted, reactive, ref, watch } from 'vue'

const props = defineProps({
  slug: {
    type: String,
    required: true,
  },
})

const loading = ref(false)
const error = ref('')

const event = reactive({
  coupleNames: '',
  date: '',
  time: '',
  location: '',
})

const guests = ref([])

const apiBase = computed(() => `${window.location.origin}/api/invitations`)

const totals = computed(() => {
  const total = guests.value.length
  const yes = guests.value.filter(g => g.status === 'yes').length
  const no = guests.value.filter(g => g.status === 'no').length
  const maybe = guests.value.filter(g => g.status === 'maybe').length
  return { total, yes, no, maybe }
})

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await axios.get(`${apiBase.value}/${props.slug}/`)
    event.coupleNames = data.couple_names
    event.date = data.date
    event.time = data.time
    event.location = data.location
    guests.value = data.guests || []
  } catch (e) {
    console.error(e)
    error.value = 'Мәліметтерді жүктеу кезінде қате шықты.'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

watch(
  () => props.slug,
  () => loadData()
)
</script>

<template>
  <div class="dashboard">
    <section class="top">
      <div class="top-inner">
        <div class="event-main">
          <div class="event-avatar">T</div>
          <div>
            <p class="event-label">Той ақпараты</p>
            <h1 class="event-title">{{ event.coupleNames || 'Той сайтын басқару' }}</h1>
            <p class="event-subtitle">
              {{ event.date }} · {{ event.time }} · {{ event.location }}
            </p>
          </div>
        </div>

        <div class="event-stats">
          <div class="stat">
            <p class="stat-label">Барлығы</p>
            <p class="stat-value">{{ totals.total }}</p>
          </div>
          <div class="stat">
            <p class="stat-label">Қатысады</p>
            <p class="stat-value stat-yes">{{ totals.yes }}</p>
          </div>
          <div class="stat">
            <p class="stat-label">Қатыса алмайды</p>
            <p class="stat-value stat-no">{{ totals.no }}</p>
          </div>
          <div class="stat">
            <p class="stat-label">Әлі ойлануда</p>
            <p class="stat-value stat-maybe">{{ totals.maybe }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="content">
      <div class="content-inner">
        <h2 class="table-title">Қонақтар тізімі</h2>
        <p v-if="error" class="error-text">
          {{ error }}
        </p>
        <div v-else-if="loading" class="loading">Жүктелуде...</div>
        <div v-else class="guest-table">
          <div class="guest-row guest-row-head">
            <div>Қонақ</div>
            <div>Телефон</div>
            <div>Статус</div>
            <div>Үстел</div>
          </div>
          <div
            v-for="g in guests"
            :key="g.id"
            class="guest-row"
          >
            <div class="guest-main">
              <span class="guest-name">{{ g.name }}</span>
            </div>
            <div class="guest-phone">{{ g.phone || '—' }}</div>
            <div class="guest-status">
              <span class="status-pill" :data-status="g.status">
                <span v-if="g.status === 'yes'">Қатысады</span>
                <span v-else-if="g.status === 'no'">Қатыса алмайды</span>
                <span v-else>Әлі ойлануда</span>
              </span>
            </div>
            <div class="guest-table-num">
              {{ g.table_number || '—' }}
            </div>
          </div>
          <p v-if="!guests.length" class="empty-text">
            Қонақтар әлі қосылмаған. Сілтемені қонақтарға жіберген соң осы жерде олардың
            жауаптары шығады.
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: calc(100vh - 80px);
  display: flex;
  flex-direction: column;
}

.top {
  background: linear-gradient(180deg, #fef3e8 0%, #f5f5f4 100%);
  padding: 20px 16px 18px;
}

@media (min-width: 1024px) {
  .top {
    padding: 24px 40px 20px;
  }
}

.top-inner {
  max-width: 1120px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (min-width: 768px) {
  .top-inner {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.event-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.event-avatar {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  background: #facc15;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #854d0e;
}

.event-label {
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9ca3af;
}

.event-title {
  font-size: 18px;
  font-weight: 700;
}

.event-subtitle {
  font-size: 13px;
  color: #6b7280;
}

.event-stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

@media (min-width: 640px) {
  .event-stats {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.stat {
  padding: 8px 10px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(229, 231, 235, 0.9);
}

.stat-label {
  font-size: 11px;
  color: #6b7280;
}

.stat-value {
  margin-top: 2px;
  font-size: 16px;
  font-weight: 700;
}

.stat-yes {
  color: #16a34a;
}

.stat-no {
  color: #b91c1c;
}

.stat-maybe {
  color: #f59e0b;
}

.content {
  flex: 1;
  background: #020617;
  padding: 22px 16px 28px;
}

@media (min-width: 1024px) {
  .content {
    padding: 26px 40px 36px;
  }
}

.content-inner {
  max-width: 1120px;
  margin: 0 auto;
  background: #020617;
  border-radius: 20px;
  padding: 16px 14px 18px;
  box-shadow:
    0 20px 50px rgba(15, 23, 42, 0.9),
    0 0 0 1px rgba(30, 64, 175, 0.2);
}

@media (min-width: 768px) {
  .content-inner {
    padding: 18px 18px 20px;
  }
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: #e5e7eb;
  margin-bottom: 10px;
}

.error-text {
  font-size: 13px;
  color: #fecaca;
}

.loading {
  font-size: 13px;
  color: #e5e7eb;
}

.guest-table {
  margin-top: 8px;
}

.guest-row {
  display: grid;
  grid-template-columns: 2fr 1.3fr 1.4fr 0.7fr;
  gap: 8px;
  padding: 8px 8px;
  border-radius: 10px;
  font-size: 13px;
  color: #e5e7eb;
}

.guest-row:nth-child(odd):not(.guest-row-head) {
  background: rgba(15, 23, 42, 0.6);
}

.guest-row:nth-child(even):not(.guest-row-head) {
  background: rgba(15, 23, 42, 0.85);
}

.guest-row-head {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  border-bottom: 1px solid rgba(55, 65, 81, 0.9);
  border-radius: 0;
}

.guest-main {
  display: flex;
  flex-direction: column;
}

.guest-name {
  font-weight: 500;
}

.guest-phone {
  color: #9ca3af;
}

.guest-status {
  display: flex;
  align-items: center;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 96px;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 11px;
}

.status-pill[data-status='yes'] {
  background: rgba(22, 163, 74, 0.16);
  color: #4ade80;
}

.status-pill[data-status='no'] {
  background: rgba(248, 113, 113, 0.18);
  color: #fecaca;
}

.status-pill[data-status='maybe'] {
  background: rgba(234, 179, 8, 0.18);
  color: #facc15;
}

.guest-table-num {
  text-align: right;
}

.empty-text {
  margin-top: 10px;
  font-size: 12px;
  color: #9ca3af;
}

@media (max-width: 640px) {
  .guest-row {
    grid-template-columns: 2fr 1.4fr;
    grid-template-rows: auto auto;
  }
  .guest-phone {
    grid-column: 1 / 3;
  }
  .guest-status {
    justify-content: flex-start;
  }
  .guest-table-num {
    text-align: left;
  }
}
</style>

