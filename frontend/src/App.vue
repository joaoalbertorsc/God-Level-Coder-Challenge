<template>
  <div id="app-container">
    <SidebarMenu :isOpen="isSidebarOpen" @close="isSidebarOpen = false" />

    <header class="app-header">
      <button class="menu-toggle" @click="isSidebarOpen = true">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>
      <div class="header-content">
        <h1>Nola Analytic Platform</h1>
        <p class="subtitle">Seu centro de comando para insights de restaurantes.</p>
      </div>
    </header>

    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SidebarMenu from './components/SidebarMenu.vue';

const isSidebarOpen = ref(false);
</script>

<style>
/* Global Styles */
body {
  margin: 0;
  background-color: #f0f2f5;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header Styles */
.app-header {
  display: flex;
  align-items: center;
  background-color: white;
  padding: 15px 30px;
  border-bottom: 1px solid #dee2e6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.menu-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  margin-right: 20px;
}

.menu-toggle svg {
  color: #2c3e50;
}

.header-content {
  text-align: center;
  flex-grow: 1;
}

.app-header h1 {
  margin: 0;
  font-size: 1.8rem;
}

.app-header .subtitle {
  margin: 5px 0 0;
  color: #6c757d;
}

/* Main Content Area */
.app-main {
  flex-grow: 1;
  padding: 20px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .app-header {
    padding: 15px;
  }
  .menu-toggle {
    margin-right: 10px;
  }
  .app-header h1 {
    font-size: 1.4rem;
  }
  .app-header .subtitle {
    font-size: 0.8rem;
  }
  .app-main {
    padding: 10px;
  }
}
</style>
