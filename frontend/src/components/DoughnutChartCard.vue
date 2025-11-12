<template>
  <div class="doughnut-chart-card">
    <h3 class="card-title">{{ title }}</h3>
    <p v-if="description" class="card-description">{{ description }}</p>
    <div v-if="chartData" class="chart-container">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
    <div v-else class="no-data-message">
      <p>Nenhum dado disponível para o gráfico.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed !== null) {
            label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed);
          }
          return label;
        }
      }
    }
  }
}));
</script>

<style scoped>
.doughnut-chart-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 30px; /* Add some space below the card */
}

.doughnut-chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 10px;
}

.card-description {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 20px;
}

.chart-container {
  position: relative;
  height: 300px; /* Fixed height for the chart */
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.no-data-message {
  color: #6c757d;
  margin-top: 20px;
}

.no-data-message p {
  font-size: 0.9rem; /* Standardized */
}
</style>
