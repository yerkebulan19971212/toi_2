<template>
  <section class="py-16 md:py-24 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <p class="section-label mb-3">Блог</p>
        <h2 class="section-title">Соңғы жаңалықтар</h2>
      </div>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="i in 3"
          :key="i"
          class="rounded-2xl overflow-hidden shadow-md animate-pulse"
        >
          <div class="h-44 bg-gray-200" />
          <div class="p-5 space-y-3">
            <div class="h-3 bg-gray-100 rounded w-1/3" />
            <div class="h-5 bg-gray-200 rounded w-full" />
            <div class="h-4 bg-gray-100 rounded w-2/3" />
          </div>
        </div>
      </div>

      <div v-else-if="error" class="text-center py-12 text-gray-500 text-sm">
        {{ error }}
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <article
          v-for="post in displayPosts"
          :key="post.id"
          class="card overflow-hidden group cursor-pointer"
        >
          <NuxtLink :to="`/blog/${post.slug}`" class="block">
            <div
              class="h-44 overflow-hidden relative"
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
            <h3
              class="font-serif font-semibold text-gray-900 mb-2 group-hover:text-brand-green transition-colors leading-snug"
            >
              <NuxtLink :to="`/blog/${post.slug}`">{{ post.title }}</NuxtLink>
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

const { data: posts, pending: loading, error: fetchError } = await useAsyncData(
  'blog-section-posts',
  () => get('/api/blog/').then((r) => r.results ?? r ?? []).catch(() => [])
)

const error = computed(() => (fetchError.value ? 'Жаңалықтарды жүктеу мүмкін болмады.' : ''))

const displayPosts = computed(() => (posts.value || []).slice(0, 3))

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('kk-KZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
