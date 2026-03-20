<template>
  <div class="min-h-screen bg-cream-100 flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <NuxtLink to="/" class="inline-flex items-center space-x-2 mb-6">
          <div class="w-8 h-8 bg-brand-green rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <span class="font-serif font-bold text-lg text-gray-900">shaqyru.kz</span>
        </NuxtLink>
        <h1 class="font-serif text-2xl font-bold text-gray-900">Тіркелу</h1>
        <p class="text-gray-500 font-sans text-sm mt-1">Жаңа аккаунт жасаңыз</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm p-8">
        <form @submit.prevent="submit" class="space-y-4">
          <div>
            <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">Логин</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="Логин"
              class="input-field"
              autocomplete="username"
            />
          </div>
          <div>
            <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">Email (міндетті емес)</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="email@example.com"
              class="input-field"
              autocomplete="email"
            />
          </div>
          <div>
            <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">Құпия сөз</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="Кем дегенде 6 таңба"
              class="input-field"
              autocomplete="new-password"
            />
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm font-sans">
            {{ error }}
          </div>

          <button type="submit" class="btn-primary w-full justify-center" :disabled="loading">
            <span v-if="loading">Жүктелуде...</span>
            <span v-else>Тіркелу</span>
          </button>
        </form>

        <p class="text-center text-sm font-sans text-gray-500 mt-6">
          Аккаунтыңыз бар ма?
          <NuxtLink to="/login" class="text-brand-green font-medium hover:underline">Кіру</NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'blank' })
useHead({ title: 'Тіркелу — Shaqyru.kz' })

const authStore = useAuthStore()
const router = useRouter()

if (authStore.isLoggedIn) {
  await navigateTo('/my-invitations')
}

const form = reactive({ username: '', email: '', password: '' })
const loading = ref(false)
const error = ref(null)

const submit = async () => {
  if (!form.username || !form.password) return
  loading.value = true
  error.value = null
  try {
    await authStore.register(form.username, form.email, form.password)
    await navigateTo('/my-invitations')
  } catch (e) {
    const detail = e?.response?.data
    if (detail?.username) {
      error.value = 'Бұл логин бос емес'
    } else {
      error.value = 'Тіркелу мүмкін болмады. Қайтадан байқаңыз.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input-field {
  @apply w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm font-sans text-gray-800
         focus:outline-none focus:ring-2 focus:ring-brand-green/30 focus:border-brand-green
         transition-colors bg-white;
}
</style>
