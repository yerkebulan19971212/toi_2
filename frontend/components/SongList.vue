<template>
  <div>
    <!-- Song rows -->
    <div
      v-for="(song, index) in songs"
      :key="song.id"
      class="flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-gray-50 group cursor-pointer transition-colors"
      :class="{ 'bg-brand-green/5': isCurrentSong(song) }"
      @click="playSong(song)"
    >
      <!-- Index / Play indicator -->
      <div class="w-8 flex-shrink-0 flex items-center justify-center">
        <span
          v-if="!isCurrentSong(song)"
          class="text-sm text-gray-400 group-hover:hidden font-sans"
        >{{ index + 1 }}</span>
        <button
          class="hidden group-hover:flex w-7 h-7 bg-brand-green rounded-full items-center justify-center shadow-sm"
          :class="{ '!flex': isCurrentSong(song) }"
          aria-label="Ойнату"
        >
          <!-- Playing animation bars -->
          <svg
            v-if="isCurrentSong(song) && playerStore.isPlaying"
            class="w-3 h-3 text-white"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <rect x="3" y="8" width="4" height="8" rx="1" />
            <rect x="10" y="4" width="4" height="16" rx="1" />
            <rect x="17" y="10" width="4" height="6" rx="1" />
          </svg>
          <svg v-else class="w-3 h-3 text-white ml-0.5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </button>
      </div>

      <!-- Song cover dot -->
      <div
        class="w-10 h-10 rounded-lg flex-shrink-0 flex items-center justify-center"
        :style="songGradient(song)"
      >
        <svg class="w-4 h-4 text-white/70" fill="currentColor" viewBox="0 0 24 24">
          <path
            d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"
          />
        </svg>
      </div>

      <!-- Title + artist -->
      <div class="flex-1 min-w-0">
        <p
          class="text-sm font-sans font-medium truncate"
          :class="isCurrentSong(song) ? 'text-brand-green' : 'text-gray-900'"
        >{{ song.title }}</p>
        <p class="text-xs text-gray-400 truncate">{{ song.artist || '—' }}</p>
      </div>

      <!-- Category -->
      <span
        v-if="song.category_detail?.name"
        class="hidden sm:block text-xs text-gray-400 font-sans bg-gray-100 px-2 py-0.5 rounded-full"
      >{{ song.category_detail.name }}</span>

      <!-- Duration -->
      <span class="text-xs text-gray-400 font-sans flex-shrink-0 w-10 text-right">
        {{ song.duration_display || formatDuration(song.duration) }}
      </span>
    </div>

    <!-- Empty state -->
    <div v-if="songs.length === 0" class="text-center py-12 text-gray-400">
      <svg
        class="w-12 h-12 mx-auto mb-3 text-gray-200"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="1.5"
          d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
        />
      </svg>
      <p class="text-sm">Әндер табылмады</p>
    </div>
  </div>
</template>

<script setup>
import { usePlayerStore } from '~/stores/player'

const props = defineProps({
  songs: {
    type: Array,
    default: () => [],
  },
})

const playerStore = usePlayerStore()

const isCurrentSong = (song) => playerStore.currentSong?.id === song.id

const playSong = (song) => {
  playerStore.playSong(song, props.songs)
}

const gradients = [
  'background: linear-gradient(135deg, #F6C15C, #E8963C)',
  'background: linear-gradient(135deg, #667EEA, #764BA2)',
  'background: linear-gradient(135deg, #40B49A, #0D7B6A)',
  'background: linear-gradient(135deg, #F97316, #EF4444)',
  'background: linear-gradient(135deg, #9333EA, #EC4899)',
  'background: linear-gradient(135deg, #C9A84C, #8B6914)',
]

const songGradient = (song) => gradients[(song.id ?? 0) % gradients.length]

const formatDuration = (secs) => {
  if (!secs) return '--:--'
  const m = Math.floor(secs / 60)
  const s = secs % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}
</script>
