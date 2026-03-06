<template>
  <nav class="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center space-x-2 shrink-0">
          <div
            class="w-8 h-8 bg-brand-green rounded-lg flex items-center justify-center shadow-sm"
          >
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2.5"
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </div>
          <span class="font-serif font-bold text-lg text-gray-900">shaqyru.kz</span>
        </NuxtLink>

        <!-- Desktop Nav -->
        <div class="hidden md:flex items-center space-x-8">
          <NuxtLink to="/" class="nav-link" active-class="nav-link-active" exact>Басты бет</NuxtLink>
          <NuxtLink to="/templates" class="nav-link" active-class="nav-link-active">Үлгілер</NuxtLink>
          <NuxtLink to="/songs" class="nav-link" active-class="nav-link-active">Той әндері</NuxtLink>
          <NuxtLink to="/blog" class="nav-link" active-class="nav-link-active">Блог</NuxtLink>
        </div>

        <!-- Right side -->
        <div class="hidden md:flex items-center space-x-4">
          <a
            href="tel:+77486409093"
            class="text-sm font-sans text-gray-600 hover:text-brand-green font-medium transition-colors"
          >
            +7 748 640 90 93
          </a>
          <NuxtLink to="/builder" class="btn-primary text-sm py-2 px-4">
            Шақыру жасау
          </NuxtLink>
        </div>

        <!-- Mobile hamburger -->
        <button
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="Menu"
          @click="menuOpen = !menuOpen"
        >
          <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              v-if="!menuOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="menuOpen"
        class="md:hidden border-t border-gray-100 bg-white px-4 py-4 space-y-1"
      >
        <NuxtLink
          to="/"
          class="block px-3 py-2.5 rounded-lg text-gray-700 hover:bg-cream-100 hover:text-brand-green font-medium transition-colors"
          @click="menuOpen = false"
        >Басты бет</NuxtLink>
        <NuxtLink
          to="/templates"
          class="block px-3 py-2.5 rounded-lg text-gray-700 hover:bg-cream-100 hover:text-brand-green font-medium transition-colors"
          @click="menuOpen = false"
        >Үлгілер</NuxtLink>
        <NuxtLink
          to="/songs"
          class="block px-3 py-2.5 rounded-lg text-gray-700 hover:bg-cream-100 hover:text-brand-green font-medium transition-colors"
          @click="menuOpen = false"
        >Той әндері</NuxtLink>
        <NuxtLink
          to="/blog"
          class="block px-3 py-2.5 rounded-lg text-gray-700 hover:bg-cream-100 hover:text-brand-green font-medium transition-colors"
          @click="menuOpen = false"
        >Блог</NuxtLink>
        <div class="pt-2 border-t border-gray-100 space-y-2">
          <NuxtLink to="/builder" class="btn-primary w-full justify-center" @click="menuOpen = false">
            Шақыру жасау
          </NuxtLink>
          <a
            href="tel:+77486409093"
            class="block text-center py-2 text-brand-green font-medium font-sans text-sm"
          >
            +7 748 640 90 93
          </a>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
const menuOpen = ref(false)
const route = useRoute()
watch(() => route.path, () => { menuOpen.value = false })
</script>
