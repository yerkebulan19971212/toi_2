<template>
  <div class="min-h-screen bg-cream-100 py-12">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center mb-10">
        <p class="section-label mb-2">Шақыру жасау</p>
        <h1 class="section-title">Той шақыруыңызды жасаңыз</h1>
      </div>

      <!-- Step indicator -->
      <div class="flex items-center justify-center mb-10">
        <div
          v-for="(step, i) in steps"
          :key="i"
          class="flex items-center"
        >
          <div
            class="w-9 h-9 rounded-full flex items-center justify-center text-sm font-sans font-bold transition-all"
            :class="
              currentStep > i
                ? 'bg-brand-green text-white'
                : currentStep === i
                ? 'bg-brand-green text-white ring-4 ring-brand-green/20'
                : 'bg-white border-2 border-gray-200 text-gray-400'
            "
          >
            <svg
              v-if="currentStep > i"
              class="w-4 h-4"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              />
            </svg>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <div class="flex flex-col items-start ml-2 mr-6">
            <span
              class="text-xs font-sans font-semibold"
              :class="currentStep === i ? 'text-brand-green' : 'text-gray-400'"
            >{{ step }}</span>
          </div>
          <div v-if="i < steps.length - 1" class="w-8 h-px bg-gray-200 mr-6" />
        </div>
      </div>

      <!-- Step 1: Template selection -->
      <div v-if="currentStep === 0" class="animate-slide-up">
        <h2 class="font-serif text-xl font-semibold text-gray-900 mb-5">Үлгі таңдаңыз</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
          <div
            v-for="tpl in templates"
            :key="tpl.id"
            class="rounded-xl overflow-hidden cursor-pointer transition-all ring-2"
            :class="
              form.template === tpl.id
                ? 'ring-brand-green shadow-lg scale-[1.02]'
                : 'ring-transparent hover:ring-brand-green/30 hover:shadow-md'
            "
            @click="form.template = tpl.id"
          >
            <div
              class="h-32 flex items-center justify-center"
              :style="`background: linear-gradient(135deg, ${tpl.gradient_from}, ${tpl.gradient_to})`"
            >
              <span class="font-serif text-xl font-bold text-white drop-shadow-sm">{{ tpl.name }}</span>
            </div>
            <div class="bg-white px-3 py-2 flex justify-between items-center">
              <span class="text-xs font-sans text-gray-600">{{ tpl.name }}</span>
              <span class="text-xs font-bold text-brand-green font-sans">
                {{ tpl.is_free ? 'Тегін' : `${tpl.price} ₸` }}
              </span>
            </div>
          </div>
        </div>
        <div class="flex justify-end">
          <button
            class="btn-primary"
            :disabled="!form.template"
            :class="{ 'opacity-50 cursor-not-allowed': !form.template }"
            @click="currentStep = 1"
          >
            Келесі
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Step 2: Fill in details -->
      <div v-else-if="currentStep === 1" class="animate-slide-up">
        <h2 class="font-serif text-xl font-semibold text-gray-900 mb-5">Мәліметтерді толтырыңыз</h2>
        <div class="bg-white rounded-2xl shadow-sm p-6 space-y-5">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
                Бойжеткен есімі *
              </label>
              <input
                v-model="form.bride_name"
                type="text"
                placeholder="Мысалы: Айгерім"
                class="input-field"
              />
            </div>
            <div>
              <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
                Жігіт есімі *
              </label>
              <input
                v-model="form.groom_name"
                type="text"
                placeholder="Мысалы: Асан"
                class="input-field"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
                Той күні *
              </label>
              <input v-model="form.date" type="date" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
                Уақыты *
              </label>
              <input v-model="form.time" type="time" class="input-field" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
              Мекеме / Зал атауы *
            </label>
            <input
              v-model="form.location"
              type="text"
              placeholder="Мысалы: Рахат сарайы"
              class="input-field"
            />
          </div>

          <div>
            <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
              Мекен-жай
            </label>
            <textarea
              v-model="form.address"
              placeholder="Толық мекен-жай..."
              rows="2"
              class="input-field resize-none"
            />
          </div>

          <div>
            <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
              Карта сілтемесі (Google Maps)
            </label>
            <input
              v-model="form.map_url"
              type="url"
              placeholder="https://maps.google.com/..."
              class="input-field"
            />
          </div>
        </div>

        <div class="flex justify-between mt-6">
          <button class="btn-secondary" @click="currentStep = 0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Артқа
          </button>
          <button
            class="btn-primary"
            :disabled="!isFormValid"
            :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }"
            @click="submit"
          >
            <span v-if="submitting">Жасалуда...</span>
            <span v-else>Шақыру жасау</span>
            <svg v-if="!submitting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Step 3: Share -->
      <div v-else-if="currentStep === 2" class="animate-slide-up">
        <div class="text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-5">
            <svg class="w-8 h-8 text-brand-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 class="font-serif text-2xl font-bold text-gray-900 mb-2">
            Шақыру дайын!
          </h2>
          <p class="text-gray-500 mb-8">Сілтемені бөлісіп, қонақтарыңызды шақырыңыз</p>

          <!-- Link box -->
          <div class="bg-white rounded-2xl shadow-sm p-5 mb-6">
            <p class="text-xs text-gray-400 font-sans mb-2">Шақыру сілтемесі:</p>
            <div class="flex items-center gap-2">
              <input
                :value="inviteUrl"
                readonly
                class="flex-1 bg-cream-100 rounded-lg px-3 py-2.5 text-sm font-sans text-gray-700 border-0 focus:ring-2 focus:ring-brand-green/30 outline-none"
              />
              <button
                class="btn-primary py-2.5 px-4 text-sm"
                @click="copyLink"
              >
                {{ copied ? 'Көшірілді!' : 'Көшіру' }}
              </button>
            </div>
          </div>

          <!-- Share buttons -->
          <div class="flex flex-wrap justify-center gap-3 mb-8">
            <a
              :href="`https://wa.me/?text=${encodeURIComponent(inviteUrl)}`"
              target="_blank"
              class="flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-5 py-2.5 rounded-xl font-sans font-medium text-sm transition-colors shadow-sm"
            >
              WhatsApp
            </a>
            <a
              :href="`https://t.me/share/url?url=${encodeURIComponent(inviteUrl)}`"
              target="_blank"
              class="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-5 py-2.5 rounded-xl font-sans font-medium text-sm transition-colors shadow-sm"
            >
              Telegram
            </a>
          </div>

          <NuxtLink to="/" class="btn-secondary">
            Басты бетке оралу
          </NuxtLink>
        </div>
      </div>

      <!-- Error -->
      <div
        v-if="error"
        class="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm font-sans"
      >
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: 'Шақыру жасау — Shaqyru.kz' })

const route = useRoute()
const { post } = useApi()
const requestURL = useRequestURL()

const currentStep = ref(0)
const submitting = ref(false)
const error = ref(null)
const createdSlug = ref(null)
const copied = ref(false)

const form = reactive({
  template: route.query.template ? Number(route.query.template) : null,
  bride_name: '',
  groom_name: '',
  date: '',
  time: '',
  location: '',
  address: '',
  map_url: '',
})

// Start at step 1 if template pre-selected
if (form.template) currentStep.value = 1

const templates = [
  { id: 1, name: 'PRESTIGE', gradient_from: '#C9A84C', gradient_to: '#8B6914', price: 2500, is_free: false },
  { id: 2, name: 'DARАБОЗА', gradient_from: '#2D5016', gradient_to: '#1A3009', price: 3000, is_free: false },
  { id: 3, name: 'MIRELA', gradient_from: '#7B3F00', gradient_to: '#4A2500', price: 3500, is_free: false },
  { id: 4, name: 'Алтын той', gradient_from: '#F6C15C', gradient_to: '#E8963C', price: 2000, is_free: false },
  { id: 5, name: 'Аспан', gradient_from: '#667EEA', gradient_to: '#764BA2', price: 2000, is_free: false },
  { id: 6, name: 'Арман', gradient_from: '#9333EA', gradient_to: '#EC4899', price: 0, is_free: true },
]

const isFormValid = computed(() =>
  form.bride_name.trim() &&
  form.groom_name.trim() &&
  form.date &&
  form.time &&
  form.location.trim()
)

const submit = async () => {
  if (!isFormValid.value) return
  submitting.value = true
  error.value = null
  try {
    const result = await post('/api/invitations/', { ...form })
    createdSlug.value = result.slug
    currentStep.value = 2
  } catch (e) {
    error.value = 'Қате болды. Қайтадан байқаңыз.'
  } finally {
    submitting.value = false
  }
}

const inviteUrl = computed(() => {
  if (!createdSlug.value) return ''
  return `${requestURL.origin}/invite/${createdSlug.value}`
})

const copyLink = async () => {
  if (process.client && inviteUrl.value) {
    await navigator.clipboard.writeText(inviteUrl.value).catch(() => {})
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
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
