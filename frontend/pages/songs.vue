<template>
  <div class="py-12 md:py-16 min-h-screen bg-cream-100">
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

const songsStore = useSongsStore()
const playerStore = usePlayerStore()

const activeCategory = ref(null)

const fallbackSongs = [
  { id: 1, title: 'Жар жар', artist: 'Халық әні', duration: 185, duration_display: '3:05', category_detail: { name: 'Дәстүрлі той' } },
  { id: 2, title: 'Беташар', artist: 'Халық әні', duration: 210, duration_display: '3:30', category_detail: { name: 'Беташар' } },
  { id: 3, title: 'Құдаша', artist: 'Халық әні', duration: 195, duration_display: '3:15', category_detail: { name: 'Дәстүрлі той' } },
  { id: 4, title: 'Шашу', artist: 'Халық әні', duration: 160, duration_display: '2:40', category_detail: { name: 'Дәстүрлі той' } },
  { id: 5, title: 'Той бастар', artist: 'Халық әні', duration: 240, duration_display: '4:00', category_detail: { name: 'Дәстүрлі той' } },
  { id: 6, title: 'Келін түсіру', artist: 'Халық әні', duration: 220, duration_display: '3:40', category_detail: { name: 'Дәстүрлі той' } },
  { id: 7, title: 'Думан той', artist: 'Халық әні', duration: 175, duration_display: '2:55', category_detail: { name: 'Заманауи той' } },
  { id: 8, title: 'Қыз ұзату', artist: 'Халық әні', duration: 230, duration_display: '3:50', category_detail: { name: 'Жар жар' } },
  { id: 9, title: 'Сыңсу', artist: 'Халық әні', duration: 200, duration_display: '3:20', category_detail: { name: 'Жар жар' } },
  { id: 10, title: 'Бесік жыры', artist: 'Халық әні', duration: 180, duration_display: '3:00', category_detail: { name: 'Дәстүрлі той' } },
  { id: 11, title: 'Жеңге той', artist: 'Халық әні', duration: 165, duration_display: '2:45', category_detail: { name: 'Заманауи той' } },
  { id: 12, title: 'Той думан', artist: 'Халық әні', duration: 190, duration_display: '3:10', category_detail: { name: 'Заманауи той' } },
]

const displaySongs = computed(() =>
  songsStore.songs.length > 0 ? songsStore.songs : fallbackSongs
)

const setCategory = (cat) => {
  activeCategory.value = cat
  songsStore.fetchSongs(cat)
}

onMounted(async () => {
  await Promise.all([songsStore.fetchCategories(), songsStore.fetchSongs()])
})
</script>
