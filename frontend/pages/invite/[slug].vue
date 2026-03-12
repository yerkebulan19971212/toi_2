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
const route = useRoute()
const config = useRuntimeConfig()
const { get, post } = useApi()

const { data: invitation, pending } = await useAsyncData(
  `invite-${route.params.slug}`,
  () => get(`/api/invitations/${route.params.slug}/`).catch(() => null),
  { watch: [() => route.params.slug] }
)

const rsvpSent = ref(false)
const frameRef = ref(null)
const frameHeight = ref('100vh')

// Inject RSVP form + auto-resize script into rendered_html
const renderedDoc = computed(() => {
  const html = invitation.value?.rendered_html
  if (!html) return ''
  const slug = route.params.slug
  const apiBase = config.public.apiBase || ''

  const rsvpScript = `
<style>
#rsvp-box{max-width:480px;margin:2rem auto;padding:1.5rem;font-family:sans-serif}
#rsvp-box h3{text-align:center;margin-bottom:1rem;font-size:1.1rem}
#rsvp-box input{width:100%;padding:.6rem .8rem;margin-bottom:.6rem;border:1px solid #ccc;border-radius:8px;font-size:.95rem;box-sizing:border-box}
.rsvp-btns{display:flex;flex-direction:column;gap:.5rem}
.rsvp-btn{padding:.8rem;border:none;border-radius:10px;font-size:.95rem;cursor:pointer;font-weight:600}
.btn-yes{background:#22c55e;color:#fff}
.btn-pair{background:#3b82f6;color:#fff}
.btn-no{background:#e5e7eb;color:#374151}
#rsvp-msg{margin-top:.8rem;text-align:center;font-size:.9rem;padding:.5rem;border-radius:8px;display:none}
.msg-ok{background:#dcfce7;color:#166534}
.msg-err{background:#fee2e2;color:#991b1b}
</style>
<div id="rsvp-box">
  <h3>Қатысуыңызды растаңыз</h3>
  <input id="rsvp-name" placeholder="Аты-жөні" />
  <input id="rsvp-phone" placeholder="Телефон (міндетті емес)" />
  <div class="rsvp-btns">
    <button class="rsvp-btn btn-yes" onclick="submitRsvp('solo')">Иә, жалғыз өзім барамын</button>
    <button class="rsvp-btn btn-pair" onclick="submitRsvp('with_partner')">Жұбайыммен бірге</button>
    <button class="rsvp-btn btn-no" onclick="submitRsvp('declined')">Келе алмаймын</button>
  </div>
  <div id="rsvp-msg"></div>
</div>
<script>
function submitRsvp(choice){
  var name=document.getElementById('rsvp-name').value.trim();
  if(!name){alert('Аты-жөні міндетті');return;}
  var phone=document.getElementById('rsvp-phone').value.trim();
  document.querySelectorAll('.rsvp-btn').forEach(function(b){b.disabled=true;});
  fetch('${apiBase}/api/invitations/${slug}/rsvp/',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({guest_name:name,phone:phone,response:choice})
  }).then(function(r){
    var msg=document.getElementById('rsvp-msg');
    msg.style.display='block';
    if(r.ok||r.status===409){
      msg.className='msg-ok';
      msg.textContent=r.status===409?'Сіз бұрын жауап бергенсіз.':'Жауабыңыз қабылданды! Рахмет!';
      document.getElementById('rsvp-box').querySelector('h3').style.display='none';
      document.getElementById('rsvp-name').style.display='none';
      document.getElementById('rsvp-phone').style.display='none';
      document.querySelector('.rsvp-btns').style.display='none';
    }else{
      msg.className='msg-err';
      msg.textContent='Қате кетті.';
      document.querySelectorAll('.rsvp-btn').forEach(function(b){b.disabled=false;});
    }
  }).catch(function(){
    var msg=document.getElementById('rsvp-msg');
    msg.style.display='block';msg.className='msg-err';
    msg.textContent='Желі қатесі.';
    document.querySelectorAll('.rsvp-btn').forEach(function(b){b.disabled=false;});
  });
}
// Auto-resize iframe
window.addEventListener('load',function(){
  parent.postMessage({iframeHeight:document.body.scrollHeight},'*');
});
new ResizeObserver(function(){
  parent.postMessage({iframeHeight:document.body.scrollHeight},'*');
}).observe(document.body);
<\/script>`

  if (html.includes('</body>')) {
    return html.replace('</body>', rsvpScript + '</body>')
  }
  return html + rsvpScript
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

useHead(() => ({
  title: invitation.value
    ? `${invitation.value.bride_name} & ${invitation.value.groom_name} — Той шақыруы`
    : 'Шақыру — Shaqyru.kz',
}))
</script>
