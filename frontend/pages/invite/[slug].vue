<template>
  <div class="min-h-screen flex flex-col">
    <!-- Loading -->
    <div v-if="pending" class="flex-1 flex items-center justify-center bg-cream-100">
      <div class="text-center">
        <div class="w-12 h-12 border-4 border-brand-green/30 border-t-brand-green rounded-full animate-spin mx-auto mb-4" />
        <p class="text-gray-500 font-sans text-sm">Жүктелуде...</p>
      </div>
    </div>

    <!-- Not found -->
    <div v-else-if="!invitation" class="flex-1 flex items-center justify-center bg-cream-100">
      <div class="text-center px-4">
        <div class="text-6xl mb-4">💌</div>
        <h1 class="font-serif text-2xl font-bold text-gray-900 mb-2">Шақыру табылмады</h1>
        <p class="text-gray-500 mb-6 font-sans text-sm">Сілтеме дұрыс емес немесе мерзімі өтіп кетті</p>
        <NuxtLink to="/" class="btn-primary">Басты бетке</NuxtLink>
      </div>
    </div>

    <!-- Invitation display -->
    <div
      v-else
      class="flex-1 relative min-h-screen"
      :style="bgStyle"
    >
      <!-- Decorative elements -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-0 left-0 w-64 h-64 bg-white/5 rounded-full -translate-x-1/2 -translate-y-1/2" />
        <div class="absolute bottom-0 right-0 w-96 h-96 bg-black/5 rounded-full translate-x-1/3 translate-y-1/3" />
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-16 text-white">
        <!-- Top ornament -->
        <div class="text-white/40 text-5xl mb-6 select-none">✦</div>

        <!-- Category label -->
        <p class="text-white/60 text-xs font-sans uppercase tracking-widest mb-4">
          Той шақыруы
        </p>

        <!-- Names -->
        <h1 class="font-serif text-4xl md:text-5xl lg:text-6xl font-bold text-center mb-2 drop-shadow-sm">
          {{ invitation.bride_name }}
        </h1>
        <div class="flex items-center gap-4 mb-2">
          <div class="w-16 h-px bg-white/40" />
          <span class="text-white/60 text-sm font-sans">&amp;</span>
          <div class="w-16 h-px bg-white/40" />
        </div>
        <h1 class="font-serif text-4xl md:text-5xl lg:text-6xl font-bold text-center mb-8 drop-shadow-sm">
          {{ invitation.groom_name }}
        </h1>

        <!-- Date & time -->
        <div class="bg-white/10 backdrop-blur-sm rounded-2xl px-8 py-5 mb-6 text-center">
          <p class="text-white/60 text-xs font-sans uppercase tracking-wider mb-2">Той күні</p>
          <p class="font-serif text-2xl font-semibold">{{ formattedDate }}</p>
          <p class="text-white/70 font-sans mt-1">{{ formattedTime }}</p>
        </div>

        <!-- Location -->
        <div class="bg-white/10 backdrop-blur-sm rounded-2xl px-8 py-5 mb-6 text-center max-w-sm w-full">
          <p class="text-white/60 text-xs font-sans uppercase tracking-wider mb-2">Орны</p>
          <p class="font-serif text-xl font-semibold">{{ invitation.location }}</p>
          <p v-if="invitation.address" class="text-white/70 font-sans text-sm mt-1">
            {{ invitation.address }}
          </p>
          <a
            v-if="invitation.map_url"
            :href="invitation.map_url"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-1.5 text-white/80 hover:text-white text-xs font-sans mt-3 underline underline-offset-2 transition-colors"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            Картадан қарау
          </a>
        </div>

        <!-- RSVP -->
        <div v-if="!rsvpSent" class="text-center">
          <p class="text-white/70 text-sm font-sans mb-4">Қатысатыныңызды растаңыз</p>
          <div class="flex flex-wrap justify-center gap-3">
            <button
              class="bg-white text-gray-900 font-sans font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-white/90 transition-all active:scale-95"
              @click="rsvp('yes')"
            >
              Қатысамын
            </button>
            <button
              class="bg-white/20 hover:bg-white/30 text-white font-sans font-semibold px-6 py-3 rounded-xl transition-all active:scale-95"
              @click="rsvp('maybe')"
            >
              Ойланайын
            </button>
          </div>
        </div>

        <div
          v-else
          class="bg-white/20 rounded-xl px-6 py-4 text-center"
        >
          <p class="text-white font-sans font-semibold">Жауабыңыз қабылданды!</p>
          <p class="text-white/70 text-sm font-sans mt-1">Рахмет!</p>
        </div>

        <!-- Bottom ornament -->
        <div class="text-white/20 text-3xl mt-12 select-none">❧</div>

        <!-- Branding -->
        <p class="text-white/30 text-xs font-sans mt-8">
          shaqyru.kz арқылы жасалған
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const { get, post } = useApi()

const { data: invitation, pending } = await useAsyncData(
  `invite-${route.params.slug}`,
  () => get(`/api/invitations/${route.params.slug}/`).catch(() => null),
  { watch: [() => route.params.slug] }
)

const rsvpSent = ref(false)

const bgStyle = computed(() => {
  const tpl = invitation.value?.template_detail
  if (tpl) {
    return `background: linear-gradient(135deg, ${tpl.gradient_from}, ${tpl.gradient_to})`
  }
  return 'background: linear-gradient(135deg, #C9A84C, #8B6914)'
})

const formattedDate = computed(() => {
  if (!invitation.value?.date) return ''
  return new Date(invitation.value.date).toLocaleDateString('kk-KZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
})

const formattedTime = computed(() => {
  if (!invitation.value?.time) return ''
  return invitation.value.time.slice(0, 5)
})

const rsvp = async (status) => {
  try {
    await post(`/api/invitations/${route.params.slug}/guests/`, {
      name: 'Қонақ',
      status,
    })
  } catch {}
  rsvpSent.value = true
}

// SEO
useHead(() => ({
  title: invitation.value
    ? `${invitation.value.bride_name} & ${invitation.value.groom_name} — Той шақыруы`
    : 'Шақыру — Shaqyru.kz',
  meta: [
    {
      property: 'og:title',
      content: invitation.value
        ? `${invitation.value.bride_name} & ${invitation.value.groom_name} — Той шақыруы`
        : 'Шақыру',
    },
    {
      property: 'og:description',
      content: invitation.value
        ? `${invitation.value.formattedDate} — ${invitation.value.location}`
        : '',
    },
  ],
}))
</script>
