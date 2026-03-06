<template>
  <div class="py-12 md:py-16 bg-cream-100 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-10">
        <p class="section-label mb-2">Үлгілер</p>
        <h1 class="section-title mb-3">Сайт үлгілері</h1>
        <p class="text-gray-500 text-sm max-w-lg">
          Тойыңызға сәйкес үлгіні таңдаңыз — тегін және ақылы нұсқалар бар.
        </p>
      </div>

      <!-- Category filters -->
      <div class="flex flex-wrap gap-2 mb-8">
        <button
          class="px-4 py-2 rounded-full text-sm font-sans font-medium transition-all duration-150"
          :class="
            activeCategory === null
              ? 'bg-brand-green text-white shadow-sm'
              : 'bg-white text-gray-600 hover:bg-cream-200 border border-gray-200'
          "
          @click="setCategory(null)"
        >
          Барлығы
        </button>
        <button
          v-for="cat in categories"
          :key="cat.slug"
          class="px-4 py-2 rounded-full text-sm font-sans font-medium transition-all duration-150"
          :class="
            activeCategory === cat.slug
              ? 'bg-brand-green text-white shadow-sm'
              : 'bg-white text-gray-600 hover:bg-cream-200 border border-gray-200'
          "
          @click="setCategory(cat.slug)"
        >
          {{ cat.name }}
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        <div
          v-for="i in 8"
          :key="i"
          class="rounded-2xl overflow-hidden shadow-md animate-pulse"
        >
          <div class="h-44 bg-gray-200" />
          <div class="p-4 bg-white space-y-2">
            <div class="h-4 bg-gray-200 rounded w-2/3" />
            <div class="h-3 bg-gray-100 rounded w-1/2" />
            <div class="h-9 bg-gray-100 rounded-xl" />
          </div>
        </div>
      </div>

      <!-- Grid -->
      <div
        v-else-if="displayTemplates.length"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5"
      >
        <TemplateCard
          v-for="tpl in displayTemplates"
          :key="tpl.id"
          :template="tpl"
        />
      </div>

      <!-- Empty -->
      <div v-else class="text-center py-20 text-gray-400">
        <p class="text-lg font-sans">Үлгілер табылмады</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTemplatesStore } from '~/stores/templates'

useHead({ title: 'Үлгілер — Shaqyru.kz' })

const route = useRoute()
const store = useTemplatesStore()

const activeCategory = ref(route.query.category || null)

const categories = [
  { slug: 'uzatu', name: 'Ұзату той' },
  { slug: 'qyz_uzatu', name: 'Қыз ұзату' },
  { slug: 'sunnet', name: 'Сүндет той' },
  { slug: 'tusaukesar', name: 'Тұсаукесер' },
  { slug: 'merey', name: 'Мерей той' },
  { slug: 'besik', name: 'Бесік той' },
  { slug: 'betashar', name: 'Беташар' },
  { slug: 'other', name: 'Басқалары' },
]

const loading = computed(() => store.loading)

const fallbackTemplates = [
  { id: 1, name: 'PRESTIGE', category: 'uzatu', gradient_from: '#C9A84C', gradient_to: '#8B6914', price: 2500, is_free: false, is_featured: true },
  { id: 2, name: 'DARАБОЗА', category: 'sunnet', gradient_from: '#2D5016', gradient_to: '#1A3009', price: 3000, is_free: false, is_featured: true },
  { id: 3, name: 'MIRELA', category: 'qyz_uzatu', gradient_from: '#7B3F00', gradient_to: '#4A2500', price: 3500, is_free: false, is_featured: true },
  { id: 4, name: 'Алтын той', category: 'merey', gradient_from: '#F6C15C', gradient_to: '#E8963C', price: 2000, is_free: false, is_featured: false },
  { id: 5, name: 'Жасыл бақ', category: 'besik', gradient_from: '#40B49A', gradient_to: '#0D7B6A', price: 1500, is_free: false, is_featured: false },
  { id: 6, name: 'Аспан', category: 'betashar', gradient_from: '#667EEA', gradient_to: '#764BA2', price: 2000, is_free: false, is_featured: false },
  { id: 7, name: 'Бесік', category: 'tusaukesar', gradient_from: '#F97316', gradient_to: '#EF4444', price: 0, is_free: true, is_featured: false },
  { id: 8, name: 'Арман', category: 'other', gradient_from: '#9333EA', gradient_to: '#EC4899', price: 0, is_free: true, is_featured: false },
  { id: 9, name: 'Нұрлы', category: 'uzatu', gradient_from: '#C4A35A', gradient_to: '#8B6914', price: 2000, is_free: false, is_featured: false },
  { id: 10, name: 'Тартылыс', category: 'qyz_uzatu', gradient_from: '#4A1942', gradient_to: '#C80064', price: 2500, is_free: false, is_featured: false },
  { id: 11, name: 'Шуақ', category: 'uzatu', gradient_from: '#1A6B3C', gradient_to: '#0A3D22', price: 1500, is_free: false, is_featured: false },
  { id: 12, name: 'Дариға', category: 'merey', gradient_from: '#2C3E6B', gradient_to: '#1A2440', price: 3000, is_free: false, is_featured: false },
]

const displayTemplates = computed(() => {
  const base = store.templates.length > 0 ? store.templates : fallbackTemplates
  if (!activeCategory.value) return base
  return base.filter((t) => t.category === activeCategory.value)
})

const setCategory = (cat) => {
  activeCategory.value = cat
  store.fetchTemplates(cat)
}

onMounted(() => {
  store.fetchTemplates(activeCategory.value)
})
</script>
