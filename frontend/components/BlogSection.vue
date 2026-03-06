<template>
  <section class="py-16 md:py-24 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <p class="section-label mb-3">Блог</p>
        <h2 class="section-title">Соңғы жаңалықтар</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <article
          v-for="post in displayPosts"
          :key="post.id"
          class="card overflow-hidden group cursor-pointer"
        >
          <!-- Cover image / gradient placeholder -->
          <div
            class="h-44 overflow-hidden relative"
            :style="post.cover_image ? '' : `background: linear-gradient(135deg, ${post.gradientFrom}, ${post.gradientTo})`"
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

          <div class="p-5">
            <p class="text-xs text-gray-400 font-sans mb-2">
              {{ formatDate(post.published_at || post.created_at) }}
            </p>
            <h3
              class="font-serif font-semibold text-gray-900 mb-2 group-hover:text-brand-green transition-colors leading-snug"
            >
              {{ post.title }}
            </h3>
            <p class="text-sm text-gray-500 leading-relaxed line-clamp-2 mb-4">
              {{ post.excerpt }}
            </p>
            <NuxtLink
              :to="`/blog/${post.slug}`"
              class="text-brand-green text-sm font-sans font-medium hover:text-brand-green-dark flex items-center gap-1 transition-colors"
            >
              Толығырақ
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </NuxtLink>
          </div>
        </article>
      </div>

      <div class="text-center mt-10">
        <NuxtLink to="/blog" class="btn-secondary text-base px-8 py-3.5">
          Барлық жаңалықтар
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup>
const { get } = useApi()
const posts = ref([])

const fallbackPosts = [
  {
    id: 1,
    slug: 'top-wedding-wishes',
    title: 'Үйлену тойына арналған ең үздік тілектер',
    excerpt: 'Тойыңызды ерекше ету үшін ең жылы тілектер жинағы.',
    published_at: new Date().toISOString(),
    gradientFrom: '#F6C15C',
    gradientTo: '#E8963C',
  },
  {
    id: 2,
    slug: 'traditional-wedding-games',
    title: 'Үйлену тойында дәстүрлі ойындарды қалай ұйымдастыруға болады?',
    excerpt: 'Қазақ тойының дәстүрлі ойындары мен оларды ұйымдастыру кеңестері.',
    published_at: new Date().toISOString(),
    gradientFrom: '#F97316',
    gradientTo: '#EF4444',
  },
  {
    id: 3,
    slug: 'how-to-make-invitation',
    title: 'Той шақыруын қалай дайындауға болады?',
    excerpt: 'Shaqyru.kz арқылы 5 минутта кәсіби той шақыруын жасаңыз.',
    published_at: new Date().toISOString(),
    gradientFrom: '#667EEA',
    gradientTo: '#764BA2',
  },
]

onMounted(async () => {
  try {
    const data = await get('/api/blog/')
    posts.value = data.results ?? data
  } catch {
    posts.value = []
  }
})

const displayPosts = computed(() =>
  posts.value.length > 0 ? posts.value.slice(0, 3) : fallbackPosts
)

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('kk-KZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
