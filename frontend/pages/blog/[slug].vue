<template>
  <div class="py-12 md:py-16 min-h-screen bg-cream-100">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div v-if="loading" class="animate-pulse">
        <div class="h-8 bg-gray-200 rounded w-1/3 mb-6" />
        <div class="h-64 bg-gray-200 rounded-2xl mb-6" />
        <div class="space-y-3">
          <div class="h-4 bg-gray-100 rounded w-full" />
          <div class="h-4 bg-gray-100 rounded w-full" />
          <div class="h-4 bg-gray-100 rounded w-5/6" />
        </div>
      </div>

      <template v-else-if="error">
        <div class="text-center py-16 text-gray-500">
          <p class="text-sm">{{ error }}</p>
          <NuxtLink to="/blog" class="text-brand-green font-medium mt-4 inline-block">← Барлық жаңалықтар</NuxtLink>
        </div>
      </template>

      <article v-else-if="post" class="bg-white rounded-2xl shadow-sm overflow-hidden">
        <div
          v-if="post.cover_image"
          class="aspect-video overflow-hidden"
        >
          <img
            :src="post.cover_image"
            :alt="post.title"
            class="w-full h-full object-cover"
          />
        </div>
        <div
          v-else
          class="aspect-video bg-gradient-to-br from-indigo-500 to-purple-700 flex items-end p-8"
        >
          <span class="text-white/80 text-sm font-sans uppercase tracking-widest">Жаңалық</span>
        </div>
        <div class="p-6 md:p-10">
          <p class="text-sm text-gray-400 font-sans mb-3">
            {{ formatDate(post.published_at || post.created_at) }}
          </p>
          <h1 class="font-serif text-2xl md:text-3xl font-bold text-gray-900 mb-4 leading-tight">
            {{ post.title }}
          </h1>
          <div
            class="prose prose-gray max-w-none text-gray-600 leading-relaxed"
            v-html="contentHtml"
          />
          <NuxtLink
            to="/blog"
            class="mt-10 inline-flex items-center gap-1 text-brand-green font-sans font-medium hover:text-brand-green-dark"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Барлық жаңалықтар
          </NuxtLink>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const slug = computed(() => route.params.slug)

const { get } = useApi()

const { data: post, error: fetchError, pending: loading } = await useAsyncData(
  `blog-${route.params.slug}`,
  () => get(`/api/blog/${slug.value}/`).catch(() => null),
  { watch: [slug] }
)

const error = computed(() => {
  if (fetchError.value) return 'Жаңалық табылмады.'
  if (!loading.value && !post.value) return 'Жаңалық табылмады.'
  return ''
})

const contentHtml = computed(() => {
  const text = post.value?.content ?? ''
  if (!text) return ''
  return text
    .split('\n')
    .map((p) => p.trim())
    .filter(Boolean)
    .map((p) => `<p class="mb-4">${escapeHtml(p)}</p>`)
    .join('')
})

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

useHead(() => ({
  title: post.value ? `${post.value.title} — Shaqyru.kz` : 'Жаңалық — Shaqyru.kz',
  meta: post.value?.excerpt
    ? [{ name: 'description', content: post.value.excerpt }]
    : [],
}))

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('kk-KZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
