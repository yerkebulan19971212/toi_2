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
          <div class="hidden sm:flex flex-col items-start ml-2 mr-6">
            <span
              class="text-xs font-sans font-semibold"
              :class="currentStep === i ? 'text-brand-green' : 'text-gray-400'"
            >{{ step }}</span>
          </div>
          <div v-if="i < steps.length - 1" class="w-4 sm:w-8 h-px bg-gray-200 mr-2 sm:mr-6" />
        </div>
      </div>

      <!-- Step 1: Template selection -->
      <div v-if="currentStep === 0" class="animate-slide-up">
        <h2 class="font-serif text-xl font-semibold text-gray-900 mb-5">Үлгі таңдаңыз</h2>
        <div v-if="templatesLoading" class="text-center py-12 text-gray-400 font-sans">Жүктелуде...</div>
        <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
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

      <!-- Step 2: Fill in details (dynamic from form_schema) -->
      <div v-else-if="currentStep === 1" class="animate-slide-up">
        <h2 class="font-serif text-xl font-semibold text-gray-900 mb-5">Мәліметтерді толтырыңыз</h2>
        <div class="bg-white rounded-2xl shadow-sm p-6 space-y-5">
          <template v-for="field in schemaFields" :key="field.name">
            <div>
              <label class="block text-sm font-sans font-medium text-gray-700 mb-1.5">
                {{ field.label }}<span v-if="field.required" class="text-red-400"> *</span>
              </label>

              <!-- Image list upload -->
              <template v-if="field.type === 'image_list'">
                <div
                  class="border-2 border-dashed border-gray-200 rounded-xl p-5 text-center cursor-pointer hover:border-brand-green/50 transition-colors"
                  @click="triggerPhotoInput(field.name)"
                  @dragover.prevent
                  @drop.prevent="onPhotoDrop($event, field.name)"
                >
                  <input
                    :ref="el => photoInputRefs[field.name] = el"
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    multiple
                    class="hidden"
                    @change="onPhotoChange($event, field.name)"
                  />
                  <svg class="w-8 h-8 text-gray-300 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  <p class="text-sm text-gray-400 font-sans">Суреттерді осы жерге сүйреңіз немесе <span class="text-brand-green font-medium">таңдаңыз</span></p>
                  <p class="text-xs text-gray-300 mt-1">JPG, PNG, WEBP · Макс {{ field.max_count || 6 }} сурет · {{ field.max_size_mb || 5 }} МБ</p>
                </div>
                <!-- Previews -->
                <div v-if="photoPreviews[field.name]?.length" class="grid grid-cols-3 gap-2 mt-3">
                  <div
                    v-for="(src, idx) in photoPreviews[field.name]"
                    :key="idx"
                    class="relative aspect-square rounded-lg overflow-hidden group"
                  >
                    <img :src="src" class="w-full h-full object-cover" />
                    <button
                      type="button"
                      class="absolute top-1 right-1 w-5 h-5 bg-black/50 rounded-full text-white text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                      @click.stop="removePhoto(field.name, idx)"
                    >✕</button>
                  </div>
                </div>
              </template>

              <textarea
                v-else-if="field.type === 'textarea'"
                v-model="formData[field.name]"
                :placeholder="field.placeholder || ''"
                rows="2"
                class="input-field resize-none"
              />
              <input
                v-else
                v-model="formData[field.name]"
                :type="field.type"
                :placeholder="field.placeholder || ''"
                class="input-field"
              />
            </div>
          </template>
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
          <div class="flex flex-wrap justify-center gap-3 mb-6">
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

          <!-- QR Code -->
          <div v-if="createdSlug" class="bg-white rounded-2xl shadow-sm p-5 mb-6 inline-block">
            <p class="text-xs text-gray-400 font-sans mb-3 text-center">QR код — телефонмен сканерлеңіз</p>
            <img
              :src="`/api/invitations/${createdSlug}/qr/`"
              alt="QR код"
              class="w-40 h-40 mx-auto"
            />
          </div>

          <div class="flex flex-wrap justify-center gap-3">
            <NuxtLink to="/my-invitations" class="btn-secondary">
              Менің шақыруларым
            </NuxtLink>
            <NuxtLink to="/" class="btn-secondary">
              Басты бетке оралу
            </NuxtLink>
          </div>
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
const { get, post, postForm } = useApi()
const requestURL = useRequestURL()

const currentStep = ref(0)
const submitting = ref(false)
const error = ref(null)
const createdSlug = ref(null)
const copied = ref(false)

const steps = ['Үлгі таңдау', 'Мәліметтер', 'Бөлісу']

const form = reactive({
  template: route.query.template ? Number(route.query.template) : null,
})

// formData holds all dynamic field values
const formData = reactive({})

// Photo uploads: { [fieldName]: File[] }
const photoFiles = reactive({})
const photoPreviews = reactive({})
const photoInputRefs = reactive({})

const triggerPhotoInput = (fieldName) => {
  photoInputRefs[fieldName]?.click()
}

const addPhotos = (fieldName, files, maxCount = 6) => {
  if (!photoFiles[fieldName]) photoFiles[fieldName] = []
  if (!photoPreviews[fieldName]) photoPreviews[fieldName] = []
  for (const file of files) {
    if (photoFiles[fieldName].length >= maxCount) break
    photoFiles[fieldName].push(file)
    photoPreviews[fieldName].push(URL.createObjectURL(file))
  }
}

const onPhotoChange = (event, fieldName) => {
  const field = schemaFields.value.find(f => f.name === fieldName)
  addPhotos(fieldName, Array.from(event.target.files), field?.max_count || 6)
  event.target.value = ''
}

const onPhotoDrop = (event, fieldName) => {
  const field = schemaFields.value.find(f => f.name === fieldName)
  const files = Array.from(event.dataTransfer.files).filter(f => f.type.startsWith('image/'))
  addPhotos(fieldName, files, field?.max_count || 6)
}

const removePhoto = (fieldName, idx) => {
  URL.revokeObjectURL(photoPreviews[fieldName][idx])
  photoFiles[fieldName].splice(idx, 1)
  photoPreviews[fieldName].splice(idx, 1)
}

// Start at step 1 if template pre-selected
if (form.template) currentStep.value = 1

// Load templates from API
const templatesLoading = ref(true)
const templates = ref([])
const { data: templatesData } = await useAsyncData('templates', () => get('/api/invitations/templates/'))
const raw = templatesData.value
templates.value = Array.isArray(raw) ? raw : (raw?.results ?? [])
templatesLoading.value = false

const selectedTemplate = computed(() => templates.value.find(t => t.id === form.template) || null)

const schemaFields = computed(() => selectedTemplate.value?.form_schema?.fields || [])

const CORE_FIELDS = new Set(['bride_name', 'groom_name', 'date', 'time', 'location', 'address', 'map_url', 'description', 'event_title'])

const isFormValid = computed(() =>
  schemaFields.value
    .filter(f => f.required)
    .every(f => String(formData[f.name] || '').trim())
)

const submit = async () => {
  if (!isFormValid.value) return
  submitting.value = true
  error.value = null
  try {
    const extra_data = {}
    const fd = new FormData()
    fd.append('template', form.template)

    for (const field of schemaFields.value) {
      if (field.type === 'image_list') continue
      const val = formData[field.name]
      if (val == null || val === '') continue
      if (CORE_FIELDS.has(field.name)) {
        fd.append(field.name, val)
      } else {
        extra_data[field.name] = val
      }
    }
    fd.append('extra_data', JSON.stringify(extra_data))

    // Append all photo files
    for (const field of schemaFields.value) {
      if (field.type !== 'image_list') continue
      for (const file of (photoFiles[field.name] || [])) {
        fd.append('photos', file)
      }
    }

    const result = await postForm('/api/invitations/', fd)
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
  return `${requestURL.origin}/i/${createdSlug.value}/`
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
