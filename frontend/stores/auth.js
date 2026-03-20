import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.user,
  },

  actions: {
    init() {
      if (!import.meta.client) return
      const access = localStorage.getItem('access_token')
      const refresh = localStorage.getItem('refresh_token')
      const user = localStorage.getItem('auth_user')
      if (access && user) {
        this.accessToken = access
        this.refreshToken = refresh
        this.user = JSON.parse(user)
      }
    },

    async login(username, password) {
      const { post } = useApi()
      const data = await post('/api/auth/login/', { username, password })
      this._setTokens(data.access, data.refresh)
      await this.fetchMe()
    },

    async register(username, email, password) {
      const { post } = useApi()
      const data = await post('/api/auth/register/', { username, email, password })
      this._setTokens(data.access, data.refresh)
      this.user = data.user
      if (import.meta.client) {
        localStorage.setItem('auth_user', JSON.stringify(data.user))
      }
    },

    async fetchMe() {
      const { get } = useApi()
      const user = await get('/api/auth/me/')
      this.user = user
      if (import.meta.client) {
        localStorage.setItem('auth_user', JSON.stringify(user))
      }
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      if (import.meta.client) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('auth_user')
      }
    },

    _setTokens(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
      if (import.meta.client) {
        localStorage.setItem('access_token', access)
        if (refresh) localStorage.setItem('refresh_token', refresh)
      }
    },
  },
})
