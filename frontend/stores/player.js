import { defineStore } from 'pinia'

export const usePlayerStore = defineStore('player', {
  state: () => ({
    queue: [],
    currentIndex: -1,
    isPlaying: false,
  }),

  getters: {
    currentSong: (state) =>
      state.currentIndex >= 0 ? state.queue[state.currentIndex] : null,
    hasPrev: (state) => state.currentIndex > 0,
    hasNext: (state) => state.currentIndex < state.queue.length - 1,
  },

  actions: {
    setQueue(songs, startIndex = 0) {
      this.queue = songs
      this.currentIndex = startIndex
      this.isPlaying = true
    },

    playSong(song, allSongs = null) {
      if (allSongs) {
        this.queue = allSongs
        this.currentIndex = allSongs.findIndex((s) => s.id === song.id)
      } else if (this.queue.length === 0) {
        this.queue = [song]
        this.currentIndex = 0
      } else {
        const idx = this.queue.findIndex((s) => s.id === song.id)
        if (idx >= 0) {
          this.currentIndex = idx
        } else {
          this.queue.push(song)
          this.currentIndex = this.queue.length - 1
        }
      }
      this.isPlaying = true
    },

    togglePlay() {
      this.isPlaying = !this.isPlaying
    },

    nextSong() {
      if (this.hasNext) {
        this.currentIndex++
        this.isPlaying = true
      }
    },

    prevSong() {
      if (this.hasPrev) {
        this.currentIndex--
        this.isPlaying = true
      }
    },

    stop() {
      this.isPlaying = false
    },
  },
})
