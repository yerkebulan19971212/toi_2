<template>
  <section class="bg-brand-dark py-16 md:py-20 relative overflow-hidden">
    <!-- Decorative gradient -->
    <div
      class="absolute top-0 left-0 w-72 h-72 bg-brand-green/10 rounded-full blur-3xl pointer-events-none"
    />
    <div
      class="absolute bottom-0 right-0 w-72 h-72 bg-brand-gold/10 rounded-full blur-3xl pointer-events-none"
    />

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
      <p class="section-label text-brand-gold/80 mb-4">Қазір бастаңыз</p>
      <h2 class="font-serif text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-5 leading-tight">
        Тойыңыздың шақыруын<br class="hidden md:block" />
        <span class="text-brand-gold">бүтін жасаңыз!</span>
      </h2>
      <p class="text-gray-400 text-lg mb-8 max-w-xl mx-auto">
        Мыңдаған отбасылар Shaqyru.kz арқылы — тойыңыздың ең бір мәнді сәттерін мәңгіге сақтаңыз
      </p>
      <div class="flex flex-wrap justify-center gap-4">
        <NuxtLink to="/builder" class="btn-primary text-base px-8 py-3.5">
          Шақыру жасау
        </NuxtLink>
        <NuxtLink to="/templates" class="btn-secondary text-base px-8 py-3.5 border-gray-600 text-gray-300 hover:border-white hover:text-white hover:bg-transparent">
          Үлгілерді қарау
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
