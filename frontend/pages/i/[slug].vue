<template>
  <div class="min-h-screen flex flex-col">
    <!-- Loading -->
    <div v-if="pending" class="flex-1 flex items-center justify-center bg-gray-50">
      <div class="text-center">
        <div class="w-12 h-12 border-4 border-amber-400/30 border-t-amber-500 rounded-full animate-spin mx-auto mb-4" />
        <p class="text-gray-500 font-sans text-sm">Жүктелуде...</p>
      </div>
    </div>

    <!-- Not found -->
    <div v-else-if="!invitation" class="flex-1 flex items-center justify-center bg-gray-50">
      <div class="text-center px-4">
        <div class="text-6xl mb-4">💌</div>
        <h1 class="font-serif text-2xl font-bold text-gray-900 mb-2">Шақыру табылмады</h1>
        <p class="text-gray-500 mb-6 font-sans text-sm">Сілтеме дұрыс емес немесе мерзімі өтіп кетті</p>
        <NuxtLink to="/" class="btn-primary">Басты бетке</NuxtLink>
      </div>
    </div>

    <!-- Rendered HTML template (when available) -->
    <template v-else-if="invitation.rendered_html">
      <iframe
        ref="frameRef"
        :srcdoc="renderedDoc"
        class="w-full border-0 flex-1"
        :style="{ height: frameHeight }"
        sandbox="allow-scripts allow-same-origin allow-forms allow-top-navigation"
        @load="onFrameLoad"
      />
    </template>

    <!-- Fallback: no rendered HTML — use generic design -->
    <div
      v-else
      class="flex-1 relative min-h-screen"
      :style="bgStyle"
    >
      <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-16 text-white">
        <div class="text-white/40 text-5xl mb-6 select-none">✦</div>
        <p class="text-white/60 text-xs font-sans uppercase tracking-widest mb-4">Той шақыруы</p>
        <h1 class="font-serif text-4xl md:text-6xl font-bold text-center mb-2">{{ invitation.bride_name }}</h1>
        <div class="flex items-center gap-4 mb-2">
          <div class="w-16 h-px bg-white/40" />
          <span class="text-white/60 text-sm">&amp;</span>
          <div class="w-16 h-px bg-white/40" />
        </div>
        <h1 class="font-serif text-4xl md:text-6xl font-bold text-center mb-8">{{ invitation.groom_name }}</h1>
        <div class="bg-white/10 backdrop-blur-sm rounded-2xl px-8 py-5 mb-4 text-center">
          <p class="text-white/60 text-xs uppercase tracking-wider mb-1">Той күні</p>
          <p class="font-serif text-2xl font-semibold">{{ formattedDate }}</p>
          <p class="text-white/70 text-sm mt-1">{{ formattedTime }}</p>
        </div>
        <div v-if="invitation.location" class="bg-white/10 backdrop-blur-sm rounded-2xl px-8 py-5 mb-6 text-center max-w-sm w-full">
          <p class="text-white/60 text-xs uppercase tracking-wider mb-1">Орны</p>
          <p class="font-serif text-xl font-semibold">{{ invitation.location }}</p>
          <p v-if="invitation.address" class="text-white/70 text-sm mt-1">{{ invitation.address }}</p>
        </div>
        <div v-if="!rsvpSent" class="text-center">
          <p class="text-white/70 text-sm mb-4">Қатысатыныңызды растаңыз</p>
          <div class="flex flex-wrap justify-center gap-3">
            <button class="bg-white text-gray-900 font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-white/90 transition-all" @click="rsvp('yes')">Қатысамын</button>
            <button class="bg-white/20 hover:bg-white/30 text-white font-semibold px-6 py-3 rounded-xl transition-all" @click="rsvp('maybe')">Ойланайын</button>
          </div>
        </div>
        <div v-else class="bg-white/20 rounded-xl px-6 py-4 text-center">
          <p class="text-white font-semibold">Жауабыңыз қабылданды!</p>
          <p class="text-white/70 text-sm mt-1">Рахмет!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'blank' })

const route = useRoute()
const { get, post } = useApi()

const { data: invitation, pending } = await useAsyncData(
  `invite-${route.params.slug}`,
  () => get(`/api/invitations/${route.params.slug}/`).catch(() => null),
  { watch: [() => route.params.slug] }
)

const rsvpSent = ref(false)
const frameRef = ref(null)
const frameHeight = ref('100vh')

// Inject auto-resize script into rendered_html
const renderedDoc = computed(() => {
  const html = invitation.value?.rendered_html
  if (!html) return ''

  const resizeScript = `<script>
window.addEventListener('load',function(){
  parent.postMessage({iframeHeight:document.body.scrollHeight},'*');
});
new ResizeObserver(function(){
  parent.postMessage({iframeHeight:document.body.scrollHeight},'*');
}).observe(document.body);
<\/script>`

  if (html.includes('</body>')) {
    return html.replace('</body>', resizeScript + '</body>')
  }
  return html + resizeScript
})

function onFrameLoad() {
  // fallback height
  frameHeight.value = '100vh'
}

// Listen for height messages from iframe
if (import.meta.client) {
  window.addEventListener('message', (e) => {
    if (e.data?.iframeHeight) {
      frameHeight.value = e.data.iframeHeight + 'px'
    }
  })
}

const bgStyle = computed(() => {
  const tpl = invitation.value?.template_detail
  if (tpl) return `background: linear-gradient(135deg, ${tpl.gradient_from}, ${tpl.gradient_to})`
  return 'background: linear-gradient(135deg, #C9A84C, #8B6914)'
})

const formattedDate = computed(() => {
  if (!invitation.value?.date) return ''
  return new Date(invitation.value.date).toLocaleDateString('ru-RU', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
})

const formattedTime = computed(() => {
  if (!invitation.value?.time) return ''
  return invitation.value.time.slice(0, 5)
})

const rsvp = async (status) => {
  try {
    await post(`/api/invitations/${route.params.slug}/guests/`, { name: 'Қонақ', status })
  } catch {}
  rsvpSent.value = true
}

const invitationTitle = computed(() => {
  const inv = invitation.value
  if (!inv) return 'Шақыру — Shaqyru.kz'
  const name = inv.event_title || (inv.bride_name && inv.groom_name
    ? `${inv.bride_name} & ${inv.groom_name}`
    : inv.bride_name || inv.groom_name || 'Той шақыруы')
  return `${name} — Той шақыруы`
})

useHead(() => ({ title: invitationTitle.value }))
</script>
