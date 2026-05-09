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
        <template v-if="categoriesLoading">
          <div
            v-for="i in 6"
            :key="i"
            class="h-9 w-24 bg-gray-200 rounded-full animate-pulse"
          />
        </template>
        <template v-else>
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
        </template>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-5">
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
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-5"
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
const router = useRouter()
const store = useTemplatesStore()

// Category from URL (code), e.g. ?category=uzatu
const activeCategory = ref(route.query.category || null)

// Categories loaded from API (dynamic)
const categories = ref([])
const categoriesLoading = ref(true)

async function loadCategories() {
  categoriesLoading.value = true
  try {
    const { get } = useApi()
    const data = await get('/api/invitations/categories/')
    const raw = Array.isArray(data) ? data : (data.results ?? [])
    categories.value = raw.map((cat) => ({
      slug: cat.code,
      name: cat.name_kz || cat.name_ru || cat.name_en || cat.code,
    }))
  } catch (e) {
    console.error('loadCategories:', e)
    categories.value = []
  } finally {
    categoriesLoading.value = false
  }
}

const loading = computed(() => store.loading)

const displayTemplates = computed(() => store.templates)

function setCategory(code) {
  activeCategory.value = code
  router.replace({ query: code ? { category: code } : {} })
  store.fetchTemplates(code)
}

// Init from URL and load categories
onMounted(() => {
  loadCategories()
  store.fetchTemplates(activeCategory.value)
})

watch(() => route.query.category, (newCode) => {
  activeCategory.value = newCode || null
  if (route.name === 'templates') {
    store.fetchTemplates(activeCategory.value)
  }
})
</script>
