<template>
  <div class="sidebar-container" :class="{ 'is-open': isOpen }">
    <!-- Backdrop -->
    <div class="sidebar-backdrop" @click="$emit('close')"></div>

    <!-- Menu -->
    <div class="sidebar-menu">
      <h2 class="sidebar-header">Nola Analytics</h2>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-button" @click="$emit('close')">
          <i class="icon">📊</i> Visão Geral
        </router-link>
        <router-link to="/top-products" class="nav-button" @click="$emit('close')">
          <i class="icon">🏆</i> Análise de Produtos
        </router-link>
        <router-link to="/sales-breakdown" class="nav-button" @click="$emit('close')">
          <i class="icon">📈</i> Análise de Vendas
        </router-link>
        <router-link to="/ticket-trend" class="nav-button" @click="$emit('close')">
          <i class="icon">📉</i> Tendência do Ticket
        </router-link>
        <router-link to="/operational-time" class="nav-button" @click="$emit('close')">
          <i class="icon">⏱️</i> Tempo Operacional
        </router-link>
        <router-link to="/customer-retention" class="nav-button" @click="$emit('close')">
          <i class="icon">👥</i> Retenção de Clientes
        </router-link>
      </nav>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});
defineEmits(['close']);
</script>

<style scoped>
.sidebar-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 999;
  pointer-events: none; /* Allow clicks to pass through when closed */
}

.sidebar-container.is-open {
  pointer-events: auto; /* Capture clicks when open */
}

.sidebar-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.sidebar-container.is-open .sidebar-backdrop {
  opacity: 1;
}

.sidebar-menu {
  position: absolute;
  top: 0;
  left: 0;
  width: 280px;
  height: 100%;
  background-color: #ffffff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.sidebar-container.is-open .sidebar-menu {
  transform: translateX(0);
}

.sidebar-header {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 15px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  color: #495057;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-button:hover {
  background-color: #f0f2f5;
}

.nav-button.router-link-exact-active {
  background-color: #42b983;
  color: white;
}

.icon {
  font-style: normal;
}
</style>
