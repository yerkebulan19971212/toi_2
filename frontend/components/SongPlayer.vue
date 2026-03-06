<template>
  <div class="bg-gray-900 rounded-2xl p-6 text-white shadow-2xl">
    <!-- Main row -->
    <div class="flex items-center gap-5">
      <!-- Album art / icon -->
      <div
        class="w-16 h-16 rounded-xl flex-shrink-0 overflow-hidden flex items-center justify-center shadow-lg"
        :style="coverGradient"
      >
        <svg
          v-if="!currentSong?.cover_image"
          class="w-7 h-7 text-white/70"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"
          />
        </svg>
        <img
          v-else
          :src="currentSong.cover_image"
          alt=""
          class="w-full h-full object-cover"
        />
      </div>

      <!-- Song info -->
      <div class="flex-1 min-w-0">
        <h3 class="font-serif text-lg font-semibold truncate">
          {{ currentSong?.title || 'Ән таңдаңыз' }}
        </h3>
        <p class="text-gray-400 text-sm truncate">
          {{ currentSong?.artist || '—' }}
        </p>
      </div>

      <!-- Controls -->
      <div class="flex items-center gap-2 flex-shrink-0">
        <button
          class="w-9 h-9 flex items-center justify-center hover:bg-white/10 rounded-full transition-colors"
          :disabled="!player.hasPrev"
          :class="player.hasPrev ? 'text-white' : 'text-gray-600'"
          aria-label="Алдыңғы"
          @click="player.prevSong()"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 6h2v12H6zm3.5 6 8.5 6V6z" />
          </svg>
        </button>

        <button
          class="w-12 h-12 rounded-full flex items-center justify-center shadow-lg transition-all active:scale-95"
          :class="currentSong ? 'bg-amber-500 hover:bg-amber-400' : 'bg-gray-700 cursor-not-allowed'"
          :disabled="!currentSong"
          aria-label="Ойнату / Тоқтату"
          @click="togglePlay"
        >
          <!-- Play -->
          <svg v-if="!isPlaying" class="w-6 h-6 text-white ml-0.5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
          <!-- Pause -->
          <svg v-else class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
          </svg>
        </button>

        <button
          class="w-9 h-9 flex items-center justify-center hover:bg-white/10 rounded-full transition-colors"
          :disabled="!player.hasNext"
          :class="player.hasNext ? 'text-white' : 'text-gray-600'"
          aria-label="Келесі"
          @click="player.nextSong()"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Progress bar -->
    <div class="mt-5">
      <input
        type="range"
        :value="progress"
        min="0"
        max="100"
        step="0.1"
        class="w-full h-1 accent-amber-500"
        @input="onSeek"
      />
      <div class="flex justify-between text-xs text-gray-500 mt-1.5 font-sans">
        <span>{{ formatTime(currentTime) }}</span>
        <span>{{ formatTime(audioDuration) }}</span>
      </div>
    </div>

    <!-- Hidden audio element -->
    <audio
      ref="audioEl"
      :src="currentSong?.audio || ''"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoaded"
      @ended="player.nextSong()"
      @error="onError"
    />
  </div>
</template>

<script setup>
import { usePlayerStore } from '~/stores/player'

const player = usePlayerStore()
const audioEl = ref(null)
const currentTime = ref(0)
const audioDuration = ref(0)
const progress = ref(0)

const currentSong = computed(() => player.currentSong)
const isPlaying = computed(() => player.isPlaying)

const coverGradients = [
  'background: linear-gradient(135deg, #F6C15C, #E8963C)',
  'background: linear-gradient(135deg, #667EEA, #764BA2)',
  'background: linear-gradient(135deg, #40B49A, #0D7B6A)',
  'background: linear-gradient(135deg, #F97316, #EF4444)',
]
const coverGradient = computed(() => {
  if (!currentSong.value) return coverGradients[0]
  return coverGradients[(currentSong.value.id ?? 0) % coverGradients.length]
})

const togglePlay = () => {
  if (!currentSong.value) return
  player.togglePlay()
}

const onTimeUpdate = () => {
  if (!audioEl.value) return
  currentTime.value = audioEl.value.currentTime
  if (audioDuration.value > 0) {
    progress.value = (audioEl.value.currentTime / audioDuration.value) * 100
  }
}

const onLoaded = () => {
  if (audioEl.value) audioDuration.value = audioEl.value.duration || 0
}

const onSeek = (e) => {
  if (!audioEl.value || !audioDuration.value) return
  const newTime = (Number(e.target.value) / 100) * audioDuration.value
  audioEl.value.currentTime = newTime
}

const onError = () => {
  // Silently handle missing audio files in dev
}

const formatTime = (s) => {
  if (!s || isNaN(s)) return '0:00'
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${sec.toString().padStart(2, '0')}`
}

watch(
  () => player.currentSong,
  async (song) => {
    if (!song || !audioEl.value) return
    audioEl.value.src = song.audio || ''
    currentTime.value = 0
    audioDuration.value = song.duration || 0
    progress.value = 0
    if (player.isPlaying) {
      await nextTick()
      audioEl.value.play().catch(() => {})
    }
  }
)

watch(
  () => player.isPlaying,
  (playing) => {
    if (!audioEl.value) return
    if (playing) audioEl.value.play().catch(() => {})
    else audioEl.value.pause()
  }
)
</script>
