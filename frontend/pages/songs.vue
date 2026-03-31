<template>
  <div class="py-12 md:py-16 min-h-screen bg-cream-100" :class="playerStore.currentSong ? 'pb-28 md:pb-0' : ''">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <p class="section-label mb-2">Музыка</p>
        <h1 class="section-title mb-2">Той әндері</h1>
        <p class="text-gray-500 text-sm">
          Тойыңызда үнемі үйлесімді дыбыс болу үшін сайтымызда ең үздік той музыкасы
        </p>
      </div>

      <!-- Player (sticky top on mobile when playing) -->
      <div
        class="mb-8 transition-all duration-300"
        :class="playerStore.currentSong ? 'opacity-100' : 'opacity-70'"
      >
        <SongPlayer />
      </div>

      <!-- Category tabs -->
      <div class="flex flex-wrap gap-2 mb-6">
        <button
          class="px-4 py-2 rounded-full text-sm font-sans font-medium transition-all"
          :class="
            activeCategory === null
              ? 'bg-gray-900 text-white shadow-sm'
              : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
          "
          @click="setCategory(null)"
        >
          Барлық әндер
        </button>
        <template v-if="songsStore.categoriesLoading">
          <div
            v-for="i in 5"
            :key="i"
            class="h-9 w-24 bg-gray-200 rounded-full animate-pulse"
          />
        </template>
        <template v-else>
          <button
            v-for="cat in songsStore.categories"
            :key="cat.slug"
            class="px-4 py-2 rounded-full text-sm font-sans font-medium transition-all"
            :class="
              activeCategory === cat.slug
                ? 'bg-gray-900 text-white shadow-sm'
                : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
            "
            @click="setCategory(cat.slug)"
          >
            {{ cat.name }}
          </button>
        </template>
      </div>

      <!-- Song list -->
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
        <!-- List header -->
        <div class="flex items-center gap-4 px-4 py-3 border-b border-gray-100 text-xs text-gray-400 font-sans uppercase tracking-wider">
          <div class="w-8" />
          <div class="w-10" />
          <div class="flex-1">Ән</div>
          <div class="hidden sm:block w-32">Категория</div>
          <div class="w-10 text-right">Уақыт</div>
        </div>

        <!-- Loading skeleton -->
        <div v-if="songsStore.loading" class="divide-y divide-gray-50">
          <div
            v-for="i in 8"
            :key="i"
            class="flex items-center gap-4 px-4 py-3 animate-pulse"
          >
            <div class="w-8 h-4 bg-gray-100 rounded" />
            <div class="w-10 h-10 bg-gray-100 rounded-lg" />
            <div class="flex-1 space-y-1.5">
              <div class="h-3 bg-gray-100 rounded w-2/5" />
              <div class="h-2.5 bg-gray-50 rounded w-1/4" />
            </div>
            <div class="w-10 h-3 bg-gray-100 rounded" />
          </div>
        </div>

        <template v-else-if="songsStore.error">
          <div class="text-center py-12 text-gray-500">
            <p class="text-sm">{{ songsStore.error }}</p>
          </div>
        </template>

        <SongList v-else :songs="displaySongs" />
      </div>
    </div>

    <!-- Mobile sticky player -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="translate-y-full opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="translate-y-full opacity-0"
      >
        <div
          v-if="playerStore.currentSong"
          class="fixed bottom-0 left-0 right-0 md:hidden z-40 px-4 pb-4"
        >
          <SongPlayer />
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { useSongsStore } from '~/stores/songs'
import { usePlayerStore } from '~/stores/player'

useHead({ title: 'Той әндері — Shaqyru.kz' })

const route = useRoute()
const router = useRouter()
const songsStore = useSongsStore()
const playerStore = usePlayerStore()

// Category from URL (slug), e.g. ?category=traditional
const activeCategory = ref(route.query.category || null)

// Only data from API; no fallback list
const displaySongs = computed(() => songsStore.songs)

function setCategory(slug) {
  activeCategory.value = slug
  router.replace({ query: slug ? { category: slug } : {} })
  songsStore.fetchSongs(slug)
}

onMounted(async () => {
  await songsStore.fetchCategories()
  // Init from URL if present
  if (activeCategory.value) {
    songsStore.fetchSongs(activeCategory.value)
  } else {
    await songsStore.fetchSongs()
  }
})

watch(() => route.query.category, (newSlug) => {
  activeCategory.value = newSlug || null
  if (route.name === 'songs') {
    songsStore.fetchSongs(activeCategory.value)
  }
})
</script>
