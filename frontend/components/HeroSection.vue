<template>
  <section class="relative overflow-hidden bg-cream-100 pt-12 pb-20 md:pt-20 md:pb-28">
    <!-- Background decorative blobs -->
    <div
      class="absolute -top-24 -right-24 w-96 h-96 bg-brand-gold/10 rounded-full blur-3xl pointer-events-none"
    />
    <div
      class="absolute -bottom-16 -left-16 w-72 h-72 bg-brand-green/10 rounded-full blur-3xl pointer-events-none"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <!-- Left: Text content -->
        <div class="animate-slide-up">
          <p class="section-label mb-4">Той шақыруы</p>
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
            Тойыңызға<br />
            <span class="text-brand-green">арнайы шақыру</span><br />
            5 минутта дайын
          </h1>
          <p class="text-gray-500 text-lg leading-relaxed mb-8 max-w-lg">
            Жеке шақырулар жасаңыз, той ойыны бөлісіңіз — жылжымалы және кеңейтілген
            шаблондармен тойыңызды ерекше етіңіз.
          </p>

          <div class="flex flex-wrap gap-3 mb-10">
            <NuxtLink to="/builder" class="btn-primary text-base px-7 py-3.5">
              Шақыру жасау
            </NuxtLink>
            <NuxtLink to="/templates" class="btn-secondary text-base px-7 py-3.5">
              Үлгілерді қарау
            </NuxtLink>
          </div>

          <!-- Stats -->
          <div class="flex flex-wrap gap-8">
            <div v-for="stat in stats" :key="stat.label" class="text-center">
              <div class="text-2xl font-bold font-serif text-brand-green">{{ stat.value }}</div>
              <div class="text-xs text-gray-500 mt-0.5 font-sans">{{ stat.label }}</div>
            </div>
          </div>
        </div>

        <!-- Right: Phone mockup -->
        <div class="flex justify-center lg:justify-end animate-fade-in">
          <div class="relative">
            <!-- Decorative ring -->
            <div
              class="absolute inset-0 bg-gradient-to-br from-brand-gold/20 to-brand-green/20 rounded-[3rem] blur-xl scale-110"
            />
            <!-- Phone frame -->
            <div
              class="relative w-[280px] md:w-[300px] bg-gray-900 rounded-[2.5rem] shadow-2xl border-4 border-gray-800 overflow-hidden"
            >
              <!-- Status bar -->
              <div class="bg-gray-900 flex justify-between items-center px-6 py-2">
                <span class="text-white text-xs">9:41</span>
                <div class="w-20 h-5 bg-gray-800 rounded-full mx-auto" />
                <div class="flex gap-1">
                  <div class="w-3 h-2 bg-white/60 rounded-sm" />
                  <div class="w-1 h-2 bg-white/60 rounded-sm" />
                </div>
              </div>
              <!-- Invitation preview card inside phone -->
              <div
                class="bg-gradient-to-br from-amber-300 via-yellow-400 to-amber-600 min-h-[480px] flex flex-col items-center justify-center px-6 py-8 text-center"
              >
                <!-- Decorative ornament -->
                <div class="text-amber-900/40 text-4xl mb-4">✦</div>
                <p class="text-amber-900/70 text-xs font-sans uppercase tracking-widest mb-3">
                  Той шақыруы
                </p>
                <h3 class="font-serif text-2xl font-bold text-amber-900 mb-1">
                  Aiface &amp; Aigerim
                </h3>
                <div class="w-12 h-px bg-amber-900/30 mx-auto my-3" />
                <p class="text-amber-900/80 text-sm font-sans">15 маусым, 2025</p>
                <p class="text-amber-900/70 text-xs font-sans mt-1">18:00</p>
                <div class="mt-5 bg-amber-900/10 rounded-xl px-4 py-2">
                  <p class="text-amber-900/80 text-xs font-sans">Алматы, Рахат сарайы</p>
                </div>
                <div
                  class="mt-6 bg-amber-900 text-amber-100 text-xs font-sans font-medium px-5 py-2.5 rounded-full"
                >
                  Шақыруды қабылдау
                </div>
              </div>
            </div>

            <!-- Floating badge -->
            <div
              class="absolute -top-3 -right-4 bg-white rounded-2xl shadow-lg px-3 py-2 flex items-center gap-2"
            >
              <div class="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
                <svg class="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <span class="text-xs font-sans font-semibold text-gray-700">Жіберілді!</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const stats = [
  { value: '500+', label: 'Шаблондар' },
  { value: '100+', label: 'Той әндері' },
  { value: '5 мин', label: 'Жасалу уақыты' },
]
</script>
