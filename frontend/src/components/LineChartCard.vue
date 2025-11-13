<template>
  <div class="line-chart-card">
    <h3 class="card-title">{{ title }}</h3>
    <div v-if="chartData" class="chart-container">
      <LineChart :chartData="chartData" />
    </div>
    <div v-else class="no-data-message">
      <p>Nenhum dado disponível para o gráfico.</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import LineChart from './LineChart.vue';

defineProps({
  title: {
    type: String,
    required: true
  },
  chartData: {
    type: Object,
    default: () => null
  }
});
</script>

<style scoped>
.line-chart-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 30px;
}

.line-chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 10px;
  text-align: center;
}

.chart-container {
  position: relative;
  height: 300px; /* Altura fixa para corresponder ao gráfico de pizza */
  width: 100%;
}

.no-data-message {
  color: #6c757d;
  margin-top: 20px;
  text-align: center;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
