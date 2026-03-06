<template>
  <section class="py-16 md:py-24 bg-cream-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <p class="section-label mb-3">Танымал үлгілер</p>
        <h2 class="section-title">Ең көп таңдалған шақырулар</h2>
        <p class="mt-3 text-gray-500 max-w-md mx-auto text-sm">
          Сайт қолданушылары ең жиі таңдайтын — тегін және ақылы нұсқалар
        </p>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="i in 3"
          :key="i"
          class="rounded-2xl overflow-hidden shadow-md animate-pulse"
        >
          <div class="h-48 bg-gray-200" />
          <div class="p-5 bg-white space-y-3">
            <div class="h-4 bg-gray-200 rounded w-2/3" />
            <div class="h-3 bg-gray-100 rounded w-1/2" />
            <div class="h-9 bg-gray-100 rounded-xl" />
          </div>
        </div>
      </div>

      <!-- Static fallback / API data -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <TemplateCard
          v-for="tpl in displayTemplates"
          :key="tpl.id"
          :template="tpl"
        />
      </div>

      <div class="text-center mt-10">
        <NuxtLink to="/templates" class="btn-secondary text-base px-8 py-3.5">
          Барлығын қарау
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useTemplatesStore } from '~/stores/templates'

const store = useTemplatesStore()
const loading = computed(() => store.loading)

onMounted(() => store.fetchFeatured())

// Show API data or static fallbacks while loading
const fallbackTemplates = [
  {
    id: 1,
    name: 'PRESTIGE',
    gradient_from: '#C9A84C',
    gradient_to: '#8B6914',
    price: '2 500',
    is_free: false,
    category: 'uzatu',
    category_label: 'Ұзату той шаблоны PRESTIGE',
  },
  {
    id: 2,
    name: 'DARАБОЗА',
    gradient_from: '#2D5016',
    gradient_to: '#1A3009',
    price: '3 000',
    is_free: false,
    category: 'sunnet',
    category_label: 'Сүндет той шаблоны DARАБОЗА',
  },
  {
    id: 3,
    name: 'MIRELA',
    gradient_from: '#7B3F00',
    gradient_to: '#4A2500',
    price: '3 500',
    is_free: false,
    category: 'qyz_uzatu',
    category_label: 'Мерей той шаблоны MIRELA',
  },
]

const displayTemplates = computed(() =>
  store.featured.length > 0 ? store.featured : fallbackTemplates
)
</script>
