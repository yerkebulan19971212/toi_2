import { defineStore } from 'pinia'

export const useSongsStore = defineStore('songs', {
  state: () => ({
    songs: [],
    categories: [],
    activeCategory: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchCategories() {
      const { get } = useApi()
      try {
        const data = await get('/api/songs/categories/')
        this.categories = data.results ?? data
      } catch (e) {
        console.error('fetchCategories:', e)
      }
    },

    async fetchSongs(category = null) {
      const { get } = useApi()
      this.loading = true
      this.error = null
      try {
        const params = category ? { category } : {}
        const data = await get('/api/songs/', params)
        this.songs = data.results ?? data
        this.activeCategory = category
      } catch (e) {
        this.error = 'Жүктеу қатесі'
        console.error('fetchSongs:', e)
      } finally {
        this.loading = false
      }
    },
  },
})
