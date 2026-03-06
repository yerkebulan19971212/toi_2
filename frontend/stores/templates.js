import { defineStore } from 'pinia'

export const useTemplatesStore = defineStore('templates', {
  state: () => ({
    templates: [],
    featured: [],
    activeCategory: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchTemplates(category = null) {
      const { get } = useApi()
      this.loading = true
      this.error = null
      try {
        const params = category ? { category } : {}
        const data = await get('/api/invitations/templates/', params)
        this.templates = data.results ?? data
        this.activeCategory = category
      } catch (e) {
        this.error = 'Жүктеу қатесі'
        console.error('fetchTemplates:', e)
      } finally {
        this.loading = false
      }
    },

    async fetchFeatured() {
      const { get } = useApi()
      try {
        const data = await get('/api/invitations/templates/', { is_featured: true })
        this.featured = (data.results ?? data).filter((t) => t.is_featured)
      } catch (e) {
        console.error('fetchFeatured:', e)
      }
    },
  },
})
