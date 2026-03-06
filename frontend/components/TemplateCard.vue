<template>
  <div class="card overflow-hidden group">
    <!-- Gradient preview -->
    <NuxtLink :to="`/builder?template=${template.id}`" class="block">
      <div
        class="h-48 relative overflow-hidden"
        :style="`background: linear-gradient(135deg, ${template.gradient_from}, ${template.gradient_to})`"
      >
        <!-- Template name overlay -->
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <p class="text-white/40 text-xs font-sans uppercase tracking-widest mb-2">Шақыру</p>
          <h3 class="font-serif text-2xl font-bold text-white drop-shadow-sm">
            {{ template.name }}
          </h3>
        </div>

        <!-- Badge -->
        <div class="absolute top-3 right-3">
          <span
            v-if="template.is_free"
            class="bg-brand-green text-white text-xs font-sans font-semibold px-2.5 py-1 rounded-full shadow"
          >Тегін</span>
          <span
            v-else
            class="bg-white/20 backdrop-blur-sm text-white text-xs font-sans font-semibold px-2.5 py-1 rounded-full"
          >Ақылы</span>
        </div>

        <!-- Hover overlay -->
        <div
          class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center"
        >
          <span
            class="bg-white text-gray-900 font-sans font-semibold text-sm px-5 py-2.5 rounded-xl shadow-lg"
          >Қарау</span>
        </div>
      </div>
    </NuxtLink>

    <!-- Card body -->
    <div class="p-5">
      <p class="text-xs text-gray-400 font-sans mb-1">
        {{ categoryLabel }}
      </p>
      <div class="flex items-center justify-between mb-4">
        <span class="font-sans font-semibold text-gray-800">{{ template.name }}</span>
        <span class="font-serif font-bold text-brand-green text-lg">
          {{ template.is_free ? 'Тегін' : priceLabel }}
        </span>
      </div>
      <NuxtLink
        :to="`/builder?template=${template.id}`"
        class="btn-primary w-full justify-center text-sm py-2.5"
      >
        Таңдау
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  template: {
    type: Object,
    required: true,
  },
})

const categoryLabels = {
  uzatu: 'Ұзату той шаблоны',
  qyz_uzatu: 'Қыз ұзату шаблоны',
  sunnet: 'Сүндет той шаблоны',
  tusaukesar: 'Тұсаукесер шаблоны',
  merey: 'Мерей той шаблоны',
  besik: 'Бесік той шаблоны',
  betashar: 'Беташар шаблоны',
  other: 'Той шаблоны',
}

const categoryLabel = computed(
  () =>
    props.template.category_label ||
    categoryLabels[props.template.category] ||
    'Той шаблоны'
)

const priceLabel = computed(() => {
  const p = props.template.price
  if (!p || p === '0' || p === 0) return 'Тегін'
  return typeof p === 'number' ? `${p.toLocaleString()} ₸` : `${p} ₸`
})
</script>
