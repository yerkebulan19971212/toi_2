<template>
  <section class="py-16 md:py-24 bg-cream-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-14">
        <p class="section-label mb-3">Жұмыс принципі</p>
        <h2 class="section-title">3 қадамда шақыру дайын</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
        <!-- Connector line (desktop only) -->
        <div
          class="hidden md:block absolute top-10 left-1/4 right-1/4 h-px bg-gradient-to-r from-brand-gold/30 via-brand-gold/60 to-brand-gold/30"
        />

        <div
          v-for="(step, i) in steps"
          :key="i"
          class="flex flex-col items-center text-center relative"
        >
          <!-- Step number bubble -->
          <div
            class="w-20 h-20 rounded-full flex items-center justify-center mb-5 shadow-lg relative z-10"
            :class="step.bubbleClass"
          >
            <span class="text-3xl" role="img" :aria-label="step.title">{{ step.icon }}</span>
          </div>
          <div
            class="absolute top-0 left-1/2 -translate-x-1/2 w-6 h-6 rounded-full border-2 border-brand-gold bg-white text-brand-gold text-xs font-bold flex items-center justify-center -mt-2 z-20 shadow-sm"
          >
            {{ i + 1 }}
          </div>
          <h3 class="font-serif text-xl font-semibold text-gray-900 mb-2">{{ step.title }}</h3>
          <p class="text-sm text-gray-500 leading-relaxed max-w-xs">{{ step.desc }}</p>
        </div>
      </div>

      <div class="text-center mt-12">
        <NuxtLink to="/builder" class="btn-primary text-base px-8 py-3.5">
          Қазір бастау
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup>
const steps = [
  {
    icon: '🎨',
    title: 'Таңдау',
    desc: 'Тойыңызға сәйкес үлгіні 500+ шаблон ішінен таңдаңыз.',
    bubbleClass: 'bg-amber-50',
  },
  {
    icon: '✏️',
    title: 'Мәлімет енгізу',
    desc: 'Есімдер, күн, уақыт және орынды толтырыңыз. 2 минут жетеді.',
    bubbleClass: 'bg-green-50',
  },
  {
    icon: '🔗',
    title: 'Бөлісу',
    desc: 'Сілтемені WhatsApp, Instagram немесе SMS арқылы жіберіңіз.',
    bubbleClass: 'bg-blue-50',
  },
]
</script>
