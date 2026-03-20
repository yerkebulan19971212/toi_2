<template>
  <div class="min-h-screen bg-cream-100 py-12">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <p class="section-label mb-1">Жеке кабинет</p>
          <h1 class="section-title">Менің шақыруларым</h1>
        </div>
        <NuxtLink to="/builder" class="btn-primary text-sm">
          + Жаңа шақыру
        </NuxtLink>
      </div>

      <!-- Loading -->
      <div v-if="pending" class="text-center py-16 text-gray-400 font-sans">Жүктелуде...</div>

      <!-- Empty -->
      <div v-else-if="!invitations.length" class="text-center py-16">
        <div class="text-5xl mb-4">💌</div>
        <h2 class="font-serif text-xl font-semibold text-gray-900 mb-2">Шақыру жоқ</h2>
        <p class="text-gray-500 font-sans text-sm mb-6">Алғашқы шақыруыңызды жасаңыз</p>
        <NuxtLink to="/builder" class="btn-primary">Шақыру жасау</NuxtLink>
      </div>

      <!-- List -->
      <div v-else class="grid gap-4 sm:grid-cols-2">
        <div
          v-for="inv in invitations"
          :key="inv.id"
          class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
        >
          <!-- Gradient header -->
          <div
            class="h-20 flex items-center justify-center"
            :style="inv.template_detail
              ? `background: linear-gradient(135deg, ${inv.template_detail.gradient_from}, ${inv.template_detail.gradient_to})`
              : 'background: linear-gradient(135deg, #C9A84C, #8B6914)'"
          >
            <span class="font-serif text-lg font-bold text-white drop-shadow-sm px-4 text-center">
              {{ inv.event_title || `${inv.bride_name} & ${inv.groom_name}` || 'Той шақыруы' }}
            </span>
          </div>

          <div class="p-4">
            <div class="flex items-center gap-2 mb-3">
              <span
                class="text-xs font-sans px-2 py-0.5 rounded-full"
                :class="inv.is_published ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'"
              >
                {{ inv.is_published ? 'Жарияланған' : 'Жарияланбаған' }}
              </span>
              <span class="text-xs font-sans text-gray-400">{{ formatDate(inv.date) }}</span>
            </div>

            <div v-if="inv.location" class="text-sm font-sans text-gray-600 mb-3 truncate">
              {{ inv.location }}
            </div>

            <!-- Quick stats row -->
            <div class="flex items-center gap-3 mb-3 text-xs font-sans text-gray-500">
              <span title="Қаралым саны">👁 {{ inv.view_count ?? 0 }}</span>
              <button
                class="hover:text-brand-green transition-colors underline-offset-2 hover:underline"
                @click="toggleStats(inv.slug)"
              >
                {{ statsOpen === inv.slug ? 'Жабу' : 'Статистика' }}
              </button>
            </div>

            <!-- Analytics panel -->
            <div v-if="statsOpen === inv.slug" class="mb-3 bg-cream-100 rounded-xl p-3">
              <div v-if="stats[inv.slug]" class="space-y-1.5">
                <div class="flex justify-between text-xs font-sans">
                  <span class="text-gray-500">Қаралым</span>
                  <span class="font-medium text-gray-800">{{ stats[inv.slug].view_count }}</span>
                </div>
                <div class="flex justify-between text-xs font-sans">
                  <span class="text-gray-500">Жалғыз барамын</span>
                  <span class="font-medium text-green-700">{{ stats[inv.slug].rsvp.solo }}</span>
                </div>
                <div class="flex justify-between text-xs font-sans">
                  <span class="text-gray-500">Жұбайыммен</span>
                  <span class="font-medium text-blue-600">{{ stats[inv.slug].rsvp.with_partner }}</span>
                </div>
                <div class="flex justify-between text-xs font-sans">
                  <span class="text-gray-500">Келе алмайды</span>
                  <span class="font-medium text-gray-500">{{ stats[inv.slug].rsvp.declined }}</span>
                </div>
                <div class="flex justify-between text-xs font-sans border-t border-gray-200 pt-1.5 mt-1.5">
                  <span class="text-gray-700 font-medium">Барлығы қонақ</span>
                  <span class="font-bold text-brand-green">{{ stats[inv.slug].rsvp.total_guests }}</span>
                </div>
                <div class="flex justify-between text-xs font-sans">
                  <span class="text-gray-500">Пікірлер</span>
                  <span class="font-medium text-gray-800">{{ stats[inv.slug].comments_count }}</span>
                </div>
              </div>
              <div v-else class="text-xs text-gray-400 text-center py-2">Жүктелуде...</div>
            </div>

            <div class="flex gap-2 mb-2">
              <a
                :href="`/i/${inv.slug}/`"
                target="_blank"
                class="flex-1 text-center text-xs font-sans font-medium py-2 rounded-lg border border-gray-200 hover:border-brand-green hover:text-brand-green transition-colors"
              >
                Ашу
              </a>
              <button
                class="flex-1 text-center text-xs font-sans font-medium py-2 rounded-lg bg-cream-100 hover:bg-gray-200 transition-colors"
                @click="copyLink(inv.slug)"
              >
                {{ copied === inv.slug ? 'Көшірілді!' : 'Сілтеме' }}
              </button>
              <button
                class="text-xs font-sans font-medium py-2 px-3 rounded-lg bg-cream-100 hover:bg-gray-200 transition-colors"
                @click="toggleQr(inv.slug)"
              >
                QR
              </button>
            </div>

            <!-- QR popup -->
            <div v-if="qrOpen === inv.slug" class="text-center pt-2 border-t border-gray-100">
              <img
                :src="`/api/invitations/${inv.slug}/qr/`"
                alt="QR"
                class="w-32 h-32 mx-auto"
              />
              <p class="text-xs text-gray-400 font-sans mt-1">Сканерлеп ашыңыз</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: 'Менің шақыруларым — Shaqyru.kz' })

const authStore = useAuthStore()
const router = useRouter()
const { get } = useApi()

if (!authStore.isLoggedIn) {
  await navigateTo('/login?redirect=/my-invitations')
}

const { data, pending } = await useAsyncData(
  'my-invitations',
  () => get('/api/invitations/my/').catch(() => [])
)

const invitations = computed(() => {
  const raw = data.value
  return Array.isArray(raw) ? raw : (raw?.results ?? [])
})

const copied = ref(null)
const qrOpen = ref(null)
const statsOpen = ref(null)
const stats = reactive({})

const toggleQr = (slug) => {
  qrOpen.value = qrOpen.value === slug ? null : slug
}

const toggleStats = async (slug) => {
  if (statsOpen.value === slug) {
    statsOpen.value = null
    return
  }
  statsOpen.value = slug
  if (!stats[slug]) {
    try {
      stats[slug] = await get(`/api/invitations/${slug}/analytics/`)
    } catch {
      stats[slug] = null
    }
  }
}

const copyLink = async (slug) => {
  const url = `${window.location.origin}/i/${slug}/`
  await navigator.clipboard.writeText(url).catch(() => {})
  copied.value = slug
  setTimeout(() => { copied.value = null }, 2000)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
