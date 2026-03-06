<template>
  <section class="py-16 md:py-24 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <p class="section-label mb-3">Той түрі</p>
        <h2 class="section-title">Той түрін таңдаңыз</h2>
        <p class="mt-3 text-gray-500 max-w-lg mx-auto text-sm">
          Той шақыруының санатын таңдап, тиісті үлгілерді қараңыз
        </p>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <NuxtLink
          v-for="cat in categories"
          :key="cat.slug"
          :to="`/templates?category=${cat.slug}`"
          class="group card p-5 flex flex-col items-center text-center cursor-pointer"
        >
          <div
            class="w-14 h-14 rounded-2xl flex items-center justify-center mb-3 transition-colors duration-200"
            :class="cat.bgClass"
          >
            <span class="text-2xl" role="img" :aria-label="cat.name">{{ cat.icon }}</span>
          </div>
          <span
            class="text-sm font-sans font-medium text-gray-800 group-hover:text-brand-green transition-colors leading-snug"
          >{{ cat.name }}</span>
          <span class="text-xs text-gray-400 mt-1">{{ cat.sub }}</span>
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup>
const categories = [
  {
    slug: 'uzatu',
    name: 'Ұзату той',
    sub: 'Үйлену',
    icon: '💍',
    bgClass: 'bg-amber-50 group-hover:bg-amber-100',
  },
  {
    slug: 'qyz_uzatu',
    name: 'Қыз ұзату',
    sub: 'Қыз шығару',
    icon: '👰',
    bgClass: 'bg-pink-50 group-hover:bg-pink-100',
  },
  {
    slug: 'sunnet',
    name: 'Сүндет той',
    sub: 'Сүндет',
    icon: '🌙',
    bgClass: 'bg-blue-50 group-hover:bg-blue-100',
  },
  {
    slug: 'tusaukesar',
    name: 'Тұсаукесер',
    sub: 'Алғашқы қадам',
    icon: '👶',
    bgClass: 'bg-green-50 group-hover:bg-green-100',
  },
  {
    slug: 'merey',
    name: 'Мерей той',
    sub: 'Мерейтой',
    icon: '🎊',
    bgClass: 'bg-purple-50 group-hover:bg-purple-100',
  },
  {
    slug: 'besik',
    name: 'Бесік той',
    sub: 'Нәресте',
    icon: '🛏️',
    bgClass: 'bg-yellow-50 group-hover:bg-yellow-100',
  },
  {
    slug: 'betashar',
    name: 'Беташар',
    sub: 'Дәстүр',
    icon: '💃',
    bgClass: 'bg-rose-50 group-hover:bg-rose-100',
  },
  {
    slug: 'other',
    name: 'Асау тойлар',
    sub: 'Басқалары',
    icon: '🎉',
    bgClass: 'bg-orange-50 group-hover:bg-orange-100',
  },
]
</script>
