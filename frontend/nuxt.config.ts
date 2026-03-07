export default defineNuxtConfig({
  ssr: true,

  devtools: { enabled: false },

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
  ],

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
    },
  },

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'Shaqyru.kz — Тойыңызға арнайы шақыру',
      meta: [
        {
          name: 'description',
          content:
            'Тойыңызға арнайы шақыру 5 минутта дайын. Той шақырулары, той әндері.',
        },
        { property: 'og:title', content: 'Shaqyru.kz — Тойыңызға арнайы шақыру' },
        {
          property: 'og:description',
          content: 'Тойыңызға арнайы шақыру 5 минутта дайын',
        },
        { property: 'og:type', content: 'website' },
        { name: 'theme-color', content: '#2D6A4F' },
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        {
          rel: 'preconnect',
          href: 'https://fonts.gstatic.com',
          crossorigin: '',
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap',
        },
      ],
    },
  },

  compatibilityDate: '2025-01-01',
})
