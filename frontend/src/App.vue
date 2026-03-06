<template>
  <div class="app-root">
    <header class="app-header">
      <div class="header-inner">
        <router-link to="/" class="logo">
          Shaqyru<span>.kz</span>
        </router-link>
        <nav class="nav">
          <router-link to="/" class="nav-link">Басты бет</router-link>
          <router-link to="/templates" class="nav-link">Үлгілер</router-link>
          <router-link :to="{ name: 'event-dashboard', params: { slug: 'ayan-aruzhan' } }" class="nav-link">
            Той ақпараты
          </router-link>
        </nav>
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-root {
  min-height: 100vh;
  background: radial-gradient(circle at top left, #fdf4ff 0, #fff 40%, #f3f4ff 100%);
  color: #111827;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter',
    sans-serif;
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(18px);
  background: rgba(255, 255, 255, 0.86);
  border-bottom: 1px solid rgba(229, 231, 235, 0.9);
}

.header-inner {
  max-width: 1120px;
  margin: 0 auto;
  padding: 10px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (min-width: 1024px) {
  .header-inner {
    padding: 10px 40px;
  }
}

.logo {
  font-weight: 800;
  font-size: 18px;
  letter-spacing: -0.05em;
  color: #111827;
  text-decoration: none;
}

.logo span {
  color: #f97316;
}

.nav {
  display: flex;
  gap: 14px;
  font-size: 14px;
}

.nav-link {
  color: #4b5563;
  text-decoration: none;
}

.nav-link.router-link-active {
  color: #111827;
  font-weight: 600;
}

.app-main {
  padding-top: 4px;
}

@media (max-width: 480px) {
  .header-inner {
    padding-inline: 16px;
  }
}
</style>
