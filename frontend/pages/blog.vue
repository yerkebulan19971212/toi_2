<template>
  <div class="py-12 md:py-16 min-h-screen bg-cream-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-10">
        <p class="section-label mb-2">Блог</p>
        <h1 class="section-title mb-2">Барлық жаңалықтар</h1>
        <p class="text-gray-500 text-sm max-w-lg">
          Той мәдениеті, кеңестер және Shaqyru.kz жаңалықтары
        </p>
      </div>

      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="i in 6"
          :key="i"
          class="rounded-2xl overflow-hidden shadow-md animate-pulse bg-white"
        >
          <div class="h-48 bg-gray-200" />
          <div class="p-5 space-y-3">
            <div class="h-3 bg-gray-100 rounded w-1/3" />
            <div class="h-5 bg-gray-200 rounded w-full" />
            <div class="h-4 bg-gray-100 rounded w-2/3" />
          </div>
        </div>
      </div>

      <div v-else-if="error" class="text-center py-16 text-gray-500">
        <p class="text-sm">{{ error }}</p>
      </div>

      <div v-else-if="posts.length === 0" class="text-center py-16 text-gray-500">
        <p class="text-sm">Жаңалықтар әлі жоқ</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <article
          v-for="post in posts"
          :key="post.id"
          class="card overflow-hidden group bg-white"
        >
          <NuxtLink :to="`/blog/${post.slug}`" class="block">
            <div
              class="h-48 overflow-hidden relative"
              :style="!post.cover_image ? 'background: linear-gradient(135deg, #667EEA, #764BA2)' : ''"
            >
              <img
                v-if="post.cover_image"
                :src="post.cover_image"
                :alt="post.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                loading="lazy"
              />
              <div
                v-else
                class="absolute inset-0 flex items-end p-5"
              >
                <span class="text-white/80 text-xs font-sans uppercase tracking-widest">Жаңалық</span>
              </div>
            </div>
          </NuxtLink>
          <div class="p-5">
            <p class="text-xs text-gray-400 font-sans mb-2">
              {{ formatDate(post.published_at || post.created_at) }}
            </p>
            <h2
              class="font-serif font-semibold text-gray-900 mb-2 group-hover:text-brand-green transition-colors leading-snug"
            >
              <NuxtLink :to="`/blog/${post.slug}`">{{ post.title }}</NuxtLink>
            </h2>
            <p class="text-sm text-gray-500 leading-relaxed line-clamp-2 mb-4">
              {{ post.excerpt }}
            </p>
            <NuxtLink
              :to="`/blog/${post.slug}`"
              class="text-brand-green text-sm font-sans font-medium hover:text-brand-green-dark inline-flex items-center gap-1"
            >
              Толығырақ
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: 'Барлық жаңалықтар — Shaqyru.kz' })

const { get } = useApi()
const posts = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    const data = await get('/api/blog/')
    posts.value = data.results ?? data ?? []
  } catch (e) {
    console.error('fetch blog list:', e)
    error.value = 'Жаңалықтарды жүктеу мүмкін болмады.'
    posts.value = []
  } finally {
    loading.value = false
  }
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('kk-KZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
