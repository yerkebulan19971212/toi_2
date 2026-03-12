<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const props = defineProps({
  groomName: { type: String, default: 'Анатолий' },
  brideName: { type: String, default: 'Ксения' },
  weddingDate: { type: String, default: '2025-10-03' },
  weddingTime: { type: String, default: '16:00' },
  endTime: { type: String, default: '22:30' },
  location: { type: String, default: 'Банкетный зал «Легенда»' },
  telegramLink: { type: String, default: '#' },
  organizerName: { type: String, default: 'Ольги' },
  organizerTg: { type: String, default: '#' },
  organizerInst: { type: String, default: '#' },
})

const envelopeOpen = ref(false)
const countdown = ref({ days: 0, hours: 0, minutes: 0, seconds: 0 })
let timer = null

function calcCountdown() {
  const target = new Date(props.weddingDate + 'T' + props.weddingTime)
  const now = new Date()
  let diff = Math.max(0, target - now)
  countdown.value.days = Math.floor(diff / 86400000)
  diff %= 86400000
  countdown.value.hours = Math.floor(diff / 3600000)
  diff %= 3600000
  countdown.value.minutes = Math.floor(diff / 60000)
  diff %= 60000
  countdown.value.seconds = Math.floor(diff / 1000)
}

const dateParts = computed(() => {
  const d = new Date(props.weddingDate)
  return {
    day: String(d.getDate()).padStart(2, '0'),
    month: String(d.getMonth() + 1).padStart(2, '0'),
    year: String(d.getFullYear()).slice(2),
  }
})

const calendarDays = computed(() => {
  const d = new Date(props.weddingDate)
  const year = d.getFullYear()
  const month = d.getMonth()
  const weddingDay = d.getDate()
  const firstDay = new Date(year, month, 1).getDay()
  const offset = firstDay === 0 ? 6 : firstDay - 1
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const daysInPrev = new Date(year, month, 0).getDate()
  const cells = []
  for (let i = offset - 1; i >= 0; i--) {
    cells.push({ day: daysInPrev - i, current: false, isWedding: false })
  }
  for (let i = 1; i <= daysInMonth; i++) {
    cells.push({ day: i, current: true, isWedding: i === weddingDay })
  }
  return cells
})

const monthNameRu = computed(() => {
  const d = new Date(props.weddingDate)
  return d.toLocaleString('ru-RU', { month: 'long', year: 'numeric' })
})

onMounted(() => {
  calcCountdown()
  timer = setInterval(calcCountdown, 1000)
})
onUnmounted(() => clearInterval(timer))
</script>

<template>
  <div class="invite-wrap">

    <!-- SECTION 1: ENVELOPE COVER -->
    <section class="w-section envelope-section">
      <div class="envelope-bg">
        <div class="env-flap"></div>
        <div class="env-body">
          <p class="inv-label">ВЫ</p>
          <p class="inv-label">ПРИГЛАШЕНЫ</p>
          <p class="inv-script">на свадьбу</p>
          <button class="wax-seal" @click="envelopeOpen = !envelopeOpen">
            <span class="seal-text">{{ envelopeOpen ? 'ОТКРЫТО' : 'НАЖМИТЕ' }}</span>
          </button>
          <p class="env-text">
            Вы не просто так получили это приглашение!<br>
            В особенный для нас день мы очень хотим,<br>
            чтобы вы были рядом!
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 2: NAMES & DATE -->
    <section class="w-section names-section">
      <div class="names-frame">
        <div class="monogram">м</div>
        <h1 class="groom-name">{{ groomName }}</h1>
        <div class="ampersand">&amp;</div>
        <h1 class="bride-name">{{ brideName }}</h1>
        <p class="announce">Спешим сообщить радостную<br>новость — мы женимся!</p>
        <div class="date-display">
          <span class="date-part">{{ dateParts.day }}</span>
          <span class="date-dot">·</span>
          <span class="date-part">{{ dateParts.month }}</span>
          <span class="date-dot">·</span>
          <span class="date-part">{{ dateParts.year }}</span>
        </div>
      </div>
    </section>

    <!-- SECTION 3: DEAR GUESTS -->
    <section class="w-section guests-section">
      <h2 class="script-heading">Дорогие гости!</h2>
      <p class="body-text">
        Мы приглашаем вас разделить с нами радостный день,<br>
        в который мы станем семьёй!
      </p>
      <p class="body-text" style="margin-top:12px;">
        В этот волшебный день мы скажем друг другу «Да»<br>
        и соединим наши сердца и судьбы в окружении<br>
        самых близких и родных людей.
      </p>

      <div class="calendar-wrap">
        <p class="calendar-month">{{ monthNameRu }}</p>
        <div class="calendar-grid">
          <div v-for="h in ['ПН','ВТ','СР','ЧТ','ПТ','СБ','ВС']" :key="h" class="cal-head">{{ h }}</div>
          <div
            v-for="(cell, i) in calendarDays"
            :key="i"
            class="cal-cell"
            :class="{ 'cal-other': !cell.current, 'cal-wedding': cell.isWedding }"
          >
            <span v-if="cell.isWedding">❤</span>
            <span v-else>{{ cell.day }}</span>
          </div>
        </div>
      </div>

      <p class="script-subheading">Наш октябрь</p>

      <div class="location-icon">
        <svg viewBox="0 0 60 80" width="52" height="70" fill="none" stroke="#2d5a3d" stroke-width="2">
          <rect x="5" y="20" width="50" height="55" rx="4"/>
          <rect x="20" y="45" width="20" height="30"/>
          <path d="M5 20 L30 4 L55 20"/>
          <rect x="14" y="28" width="10" height="12" rx="1"/>
          <rect x="36" y="28" width="10" height="12" rx="1"/>
        </svg>
      </div>
    </section>

    <!-- SECTION 4: END TIME -->
    <section class="w-section time-section">
      <svg viewBox="0 0 60 80" width="44" height="60" fill="none" stroke="#2d5a3d" stroke-width="1.5">
        <line x1="20" y1="70" x2="20" y2="30"/>
        <line x1="40" y1="70" x2="40" y2="20"/>
        <path d="M18 28 Q20 22 22 28" fill="#c9a84c" stroke="#c9a84c"/>
        <path d="M38 18 Q40 12 42 18" fill="#c9a84c" stroke="#c9a84c"/>
        <line x1="5" y1="70" x2="55" y2="70"/>
      </svg>
      <p class="script-heading" style="margin-bottom:4px;">Завершение</p>
      <p class="time-display">{{ endTime }}</p>
    </section>

    <!-- SECTION 5: QUOTE -->
    <section class="w-section quote-section">
      <div class="quote-box">
        <p class="quote-text">
          Жизнь — прекрасное путешествие.<br>
          Глупо тратить бесценное время на то,<br>
          что не про любовь.
        </p>
      </div>
    </section>

    <!-- SECTION 6: KEY ILLUSTRATION -->
    <section class="w-section illustration-section">
      <svg viewBox="0 0 80 80" width="80" height="80" fill="none" stroke="#c9627e" stroke-width="1.5">
        <circle cx="25" cy="30" r="16"/>
        <circle cx="25" cy="30" r="9"/>
        <line x1="38" y1="38" x2="68" y2="68"/>
        <line x1="55" y1="55" x2="55" y2="68"/>
        <line x1="62" y1="62" x2="68" y2="55"/>
      </svg>
    </section>

    <!-- SECTION 7: WISHES -->
    <section class="w-section wishes-section">
      <h2 class="script-heading">Пожелания</h2>

      <div class="wish-item">
        <span class="wish-num">1</span>
        <p class="body-text" style="text-align:left;">
          Мы будем признательны, если Вы поможете осуществить наши мечты,
          подарив Ваши пожелания в конверте.
        </p>
      </div>

      <div class="wish-item">
        <span class="wish-num">2</span>
        <p class="body-text" style="text-align:left;">
          Наш праздник имеет формат 18+, поэтому просим заранее предусмотреть,
          с кем останутся ваши детки, пока вы будете отдыхать на празднике.
        </p>
      </div>

      <div class="wish-item" style="flex-direction:column; align-items:flex-start;">
        <div style="display:flex; gap:16px; align-items:flex-start;">
          <span class="wish-num">3</span>
          <p class="body-text" style="text-align:left;">
            Мы создали телеграм-чат нашего праздника, где можно будет узнать
            дополнительную информацию, а также поделиться фотографиями и видео
            в день свадьбы и после.
          </p>
        </div>
        <a :href="telegramLink" class="btn-join">вступить</a>
      </div>
    </section>

    <!-- SECTION 8: ORGANIZER -->
    <section class="w-section organizer-section">
      <p class="body-text">
        Мы будем очень волноваться на свадьбе, поэтому все вопросы
        доверили в руки нашего свадебного организатора {{ organizerName }}
      </p>
      <div class="social-row">
        <a :href="organizerTg" class="social-btn tg-btn" title="Telegram">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
            <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-1.97 9.289c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.932z"/>
          </svg>
        </a>
        <a :href="organizerInst" class="social-btn inst-btn" title="Instagram">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
          </svg>
        </a>
      </div>
      <div class="envelope-small">
        <svg viewBox="0 0 120 80" width="120" height="80" fill="none">
          <rect x="2" y="2" width="116" height="76" rx="6" fill="#2d5a3d"/>
          <path d="M2 2 L60 46 L118 2" stroke="#3d7a53" stroke-width="1.5" fill="none"/>
          <path d="M2 78 L44 44" stroke="#3d7a53" stroke-width="1"/>
          <path d="M118 78 L76 44" stroke="#3d7a53" stroke-width="1"/>
        </svg>
      </div>
    </section>

    <!-- SECTION 9: COUNTDOWN -->
    <section class="w-section countdown-section">
      <h2 class="script-heading">Мы скажем<br>«Да» через...</h2>
      <div class="countdown-grid">
        <div class="countdown-unit">
          <span class="countdown-num">{{ String(countdown.days).padStart(2,'0') }}</span>
          <span class="countdown-label">дней</span>
        </div>
        <span class="countdown-sep">:</span>
        <div class="countdown-unit">
          <span class="countdown-num">{{ String(countdown.hours).padStart(2,'0') }}</span>
          <span class="countdown-label">часов</span>
        </div>
        <span class="countdown-sep">:</span>
        <div class="countdown-unit">
          <span class="countdown-num">{{ String(countdown.minutes).padStart(2,'0') }}</span>
          <span class="countdown-label">минут</span>
        </div>
        <span class="countdown-sep">:</span>
        <div class="countdown-unit">
          <span class="countdown-num">{{ String(countdown.seconds).padStart(2,'0') }}</span>
          <span class="countdown-label">секунд</span>
        </div>
      </div>
      <svg viewBox="0 0 100 60" width="100" height="60" fill="none" stroke="#c9627e" stroke-width="2">
        <circle cx="35" cy="30" r="22"/>
        <circle cx="65" cy="30" r="22"/>
        <path d="M65 10 L68 5 L72 8 L70 12" stroke="#c9a84c" stroke-width="1.5"/>
      </svg>
    </section>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Great+Vibes&family=Montserrat:wght@400;600;700&display=swap');

.invite-wrap {
  max-width: 420px;
  margin: 0 auto;
  background: #f9f5f0;
  font-family: 'Montserrat', sans-serif;
  color: #1a1a1a;
}

.w-section {
  padding: 32px 24px;
  border-bottom: 1px solid rgba(45,90,61,0.1);
}

.script-heading {
  font-family: 'Great Vibes', cursive;
  font-size: 36px;
  color: #2d5a3d;
  text-align: center;
  margin-bottom: 16px;
  line-height: 1.2;
}

.script-subheading {
  font-family: 'Great Vibes', cursive;
  font-size: 28px;
  color: #2d5a3d;
  text-align: center;
  margin-top: 12px;
}

.body-text {
  font-size: 13px;
  line-height: 1.7;
  color: #3a3a3a;
  text-align: center;
}

/* ENVELOPE */
.envelope-section {
  padding: 0;
  border: none;
  overflow: hidden;
}

.envelope-bg {
  background: #2d5a3d;
  padding: 40px 28px 36px;
  position: relative;
}

.env-flap {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 100px;
  background: #245230;
  clip-path: polygon(0 0, 50% 80%, 100% 0);
}

.env-body {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding-top: 48px;
}

.inv-label {
  font-weight: 700;
  font-size: 20px;
  letter-spacing: 0.15em;
  color: #fff;
  text-transform: uppercase;
}

.inv-script {
  font-family: 'Great Vibes', cursive;
  font-size: 32px;
  color: #c9e8d4;
  margin-bottom: 24px;
}

.wax-seal {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #d4a44c, #a07830);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(0,0,0,0.4), inset 0 2px 4px rgba(255,255,255,0.2);
  transition: transform 0.2s;
  margin: 8px 0 24px;
}
.wax-seal:hover { transform: scale(1.05); }

.seal-text {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #3a2000;
  text-transform: uppercase;
  text-align: center;
}

.env-text {
  font-size: 12px;
  color: rgba(255,255,255,0.8);
  text-align: center;
  line-height: 1.8;
}

/* NAMES */
.names-section {
  background: #2d5a3d;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: none;
}

.names-frame {
  border: 2px solid rgba(201,168,76,0.5);
  border-radius: 60% 60% 50% 50% / 40% 40% 60% 60%;
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  width: 100%;
  max-width: 280px;
}

.monogram {
  font-family: 'Great Vibes', cursive;
  font-size: 28px;
  color: rgba(201,168,76,0.8);
  margin-bottom: 8px;
}

.groom-name, .bride-name {
  font-family: 'Great Vibes', cursive;
  font-size: 46px;
  color: #fff;
  line-height: 1.1;
  margin: 0;
}

.ampersand {
  font-family: 'Great Vibes', cursive;
  font-size: 28px;
  color: rgba(201,168,76,0.8);
}

.announce {
  font-size: 11px;
  color: rgba(255,255,255,0.75);
  text-align: center;
  margin-top: 12px;
  line-height: 1.6;
}

.date-display {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.date-part {
  font-family: 'Cormorant Garamond', serif;
  font-size: 40px;
  font-weight: 600;
  color: #fff;
}

.date-dot {
  font-size: 28px;
  color: rgba(201,168,76,0.8);
  line-height: 1;
}

/* GUESTS */
.guests-section { background: #fff; }

.calendar-wrap {
  margin: 20px auto 0;
  max-width: 300px;
  width: 100%;
}

.calendar-month {
  text-align: center;
  font-size: 11px;
  text-transform: capitalize;
  letter-spacing: 0.1em;
  color: #6b7280;
  margin-bottom: 8px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.cal-head {
  font-size: 10px;
  font-weight: 700;
  text-align: center;
  color: #2d5a3d;
  padding: 4px 0;
}

.cal-cell {
  font-size: 12px;
  text-align: center;
  padding: 5px 2px;
  border-radius: 4px;
  color: #374151;
}

.cal-other { color: #d1d5db; }

.cal-wedding {
  background: #c9627e;
  color: #fff;
  border-radius: 50%;
  font-size: 14px;
}

.location-icon {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  opacity: 0.7;
}

/* TIME */
.time-section {
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.time-display {
  font-family: 'Cormorant Garamond', serif;
  font-size: 42px;
  font-weight: 600;
  color: #2d5a3d;
}

/* QUOTE */
.quote-section {
  background: #2d5a3d;
  padding: 24px;
}

.quote-box {
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 8px;
  padding: 18px 20px;
}

.quote-text {
  font-size: 13px;
  color: rgba(255,255,255,0.9);
  text-align: center;
  line-height: 1.7;
  font-style: italic;
}

/* ILLUSTRATION */
.illustration-section {
  background: #fff;
  display: flex;
  justify-content: center;
  padding: 24px;
}

/* WISHES */
.wishes-section { background: #fff; }

.wish-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-top: 20px;
}

.wish-num {
  font-family: 'Great Vibes', cursive;
  font-size: 52px;
  color: #2d5a3d;
  line-height: 1;
  flex-shrink: 0;
  min-width: 36px;
}

.btn-join {
  display: inline-block;
  margin-top: 12px;
  margin-left: 52px;
  padding: 8px 28px;
  border: 1px solid #2d5a3d;
  border-radius: 4px;
  font-size: 12px;
  letter-spacing: 0.08em;
  color: #2d5a3d;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}
.btn-join:hover { background: #2d5a3d; color: #fff; }

/* ORGANIZER */
.organizer-section {
  background: #f9f5f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.social-row { display: flex; gap: 12px; }

.social-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: transform 0.2s;
}
.social-btn:hover { transform: scale(1.1); }

.tg-btn { background: #2d5a3d; color: #fff; }
.inst-btn {
  background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
  color: #fff;
}

.envelope-small {
  filter: drop-shadow(0 4px 12px rgba(45,90,61,0.3));
}

/* COUNTDOWN */
.countdown-section {
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.countdown-grid {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin: 8px 0 16px;
}

.countdown-unit {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.countdown-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 48px;
  font-weight: 600;
  color: #2d5a3d;
  line-height: 1;
}

.countdown-sep {
  font-size: 40px;
  color: #2d5a3d;
  line-height: 1.1;
  padding-top: 4px;
}

.countdown-label {
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #9ca3af;
  margin-top: 2px;
}
</style>
