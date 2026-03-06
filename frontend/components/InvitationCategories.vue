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

      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div
          v-for="i in 4"
          :key="i"
          class="card p-5 flex flex-col items-center animate-pulse"
        >
          <div class="w-14 h-14 rounded-2xl bg-gray-200 mb-3" />
          <div class="h-4 bg-gray-200 rounded w-20 mb-2" />
          <div class="h-3 bg-gray-100 rounded w-14" />
        </div>
      </div>

      <div v-else-if="error" class="text-center py-8 text-gray-500 text-sm">
        {{ error }}
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-4 gap-4">
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
          <span v-if="cat.sub" class="text-xs text-gray-400 mt-1">{{ cat.sub }}</span>
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup>
const categories = ref([])
const loading = ref(true)
const error = ref('')

async function loadCategories() {
  loading.value = true
  error.value = ''
  try {
    const { get } = useApi()
    const data = await get('/api/invitations/categories/')
    const raw = Array.isArray(data) ? data : (data.results ?? [])

    categories.value = raw.map((cat) => ({
      slug: cat.code,
      name: cat.name_kz || cat.name_ru || cat.name_en || cat.code,
      sub: cat.subtitle || '',
      icon: cat.icon || '🎉',
      bgClass: cat.bg_class || 'bg-emerald-50 group-hover:bg-emerald-100',
    }))
  } catch (e) {
    console.error('Failed to load invitation categories', e)
    error.value = 'Санаттарды жүктеу мүмкін болмады. Кейінірек қайталап көріңіз.'
    categories.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadCategories)
</script>
