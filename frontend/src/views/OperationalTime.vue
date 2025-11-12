<template>
  <div class="operational-time">
    <div class="filter-card">
      <h1 class="page-title">Tempo Operacional</h1>
      <p class="page-description">Analise o tempo médio de entrega por loja, bairro ou cidade, com filtros de dia e horário.</p>
      <div class="filter-bar">
        <CustomDatepicker id="start-date" label="Data de Início" v-model="filters.start_date" />
        <CustomDatepicker id="end-date" label="Data de Fim" v-model="filters.end_date" />
        <SelectInput id="dimension" label="Analisar por" v-model="filters.dimension" :options="dimensionOptions" defaultOptionText="Selecione a dimensão" />
        <SelectInput id="day-of-week" label="Dia da Semana" v-model="filters.day_of_week" :options="dayOfWeekOptions" />
        <NumberInput id="start-hour" label="Hora Início" v-model="filters.start_hour" :min="0" :max="23" />
        <NumberInput id="end-hour" label="Hora Fim" v-model="filters.end_hour" :min="0" :max="23" />
        <button @click="loadPerformanceData" :disabled="loading" class="load-button">
          {{ loading ? 'Carregando...' : 'Analisar' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="loading" class="loading-message">
      <p>Carregando dados...</p>
    </div>

    <div v-else-if="!loading && performanceData.length === 0" class="no-data-message">
      <p>Nenhum dado disponível para os critérios selecionados. Ajuste os filtros e tente novamente.</p>
    </div>

    <div v-else>
      <div v-if="topPerformer && bottomPerformer" class="summary-stats">
        <div class="summary-card-wrapper">
          <StatCard 
            :title="`Melhor Performance (${translatedDimension})`" 
            :value="topPerformer.dimension_name" 
            :subValue="`${(topPerformer.average_delivery_seconds / 60).toFixed(1)} min`"
          />
        </div>
        <div class="summary-card-wrapper">
          <StatCard 
            :title="`Pior Performance (${translatedDimension})`" 
            :value="bottomPerformer.dimension_name" 
            :subValue="`${(bottomPerformer.average_delivery_seconds / 60).toFixed(1)} min`"
          />
        </div>
      </div>

      <div v-if="performanceData.length > 0" class="rankings-container">
        <div class="ranking-table">
          <h3>Top 10 Melhores Performances</h3>
          <DataTable :columns="rankingColumns" :data="bestPerformers" />
        </div>
        <div class="ranking-table">
          <h3>Top 10 Piores Performances</h3>
          <DataTable :columns="rankingColumns" :data="worstPerformers" />
        </div>
      </div>

      <div v-if="chartData" class="chart-container">
        <BarChart :chartData="chartData" :chartOptions="chartOptions" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getDeliveryPerformance } from '../services/api';
import CustomDatepicker from '../components/CustomDatepicker.vue';
import SelectInput from '../components/SelectInput.vue';
import NumberInput from '../components/NumberInput.vue';
import BarChart from '../components/BarChart.vue';
import StatCard from '../components/StatCard.vue';
import DataTable from '../components/DataTable.vue';

const loading = ref(false);
const error = ref(null);
const performanceData = ref([]);

const dimensionOptions = ref([
  { id: 'store', name: 'Loja' },
  { id: 'neighborhood', name: 'Bairro' },
  { id: 'city', name: 'Cidade' }
]);

const dayOfWeekOptions = ref([
  { id: 1, name: 'Segunda-feira' },
  { id: 2, name: 'Terça-feira' },
  { id: 3, name: 'Quarta-feira' },
  { id: 4, name: 'Quinta-feira' },
  { id: 5, name: 'Sexta-feira' },
  { id: 6, name: 'Sábado' },
  { id: 7, name: 'Domingo' },
]);

const filters = ref({
  start_date: new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split('T')[0],
  end_date: new Date().toISOString().split('T')[0],
  dimension: 'store',
  day_of_week: '',
  start_hour: '',
  end_hour: ''
});

const translatedDimension = computed(() => {
  const found = dimensionOptions.value.find(opt => opt.id === filters.value.dimension);
  return found ? found.name : '';
});

const topPerformer = computed(() => {
  if (!performanceData.value || performanceData.value.length === 0) return null;
  return performanceData.value[performanceData.value.length - 1];
});

const bottomPerformer = computed(() => {
  if (!performanceData.value || performanceData.value.length === 0) return null;
  return performanceData.value[0];
});

const rankingColumns = computed(() => [
  { key: 'rank', label: '#' },
  { key: 'dimension_name', label: translatedDimension.value },
  { key: 'average_delivery_seconds', label: 'Tempo Médio (min)' },
]);

const processRankingData = (data) => {
  return data.map((p, index) => ({ 
    ...p, 
    rank: index + 1,
    average_delivery_seconds: (p.average_delivery_seconds / 60).toFixed(1)
  }));
};

const worstPerformers = computed(() => processRankingData(performanceData.value.slice(0, 10)));
const bestPerformers = computed(() => processRankingData(performanceData.value.slice(-10).reverse()));

const chartData = computed(() => {
  if (!performanceData.value || performanceData.value.length === 0) return null;
  return {
    labels: performanceData.value.map(d => d.dimension_name),
    datasets: [
      {
        label: 'Tempo Médio de Entrega (minutos)',
        backgroundColor: '#42b983',
        borderColor: '#42b983',
        data: performanceData.value.map(d => (d.average_delivery_seconds / 60).toFixed(2)),
      }
    ]
  };
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Minutos'
      }
    }
  }
});

const loadPerformanceData = async () => {
  loading.value = true;
  error.value = null;
  performanceData.value = []; // Clear previous data
  try {
    const response = await getDeliveryPerformance(filters.value);
    if (response.data && response.data.performance_breakdown && response.data.performance_breakdown.length > 0) {
      performanceData.value = response.data.performance_breakdown;
    } else {
      performanceData.value = []; // Explicitly set to empty if no meaningful data
    }
  } catch (err) {
    console.error("Failed to load delivery performance:", err);
    error.value = "Falha ao carregar os dados de performance. Por favor, tente novamente.";
  }
  loading.value = false;
};

onMounted(loadPerformanceData);

</script>

<style scoped>
.operational-time {
  width: 100%;
  max-width: 1400px;
}

.filter-card, .chart-container {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.filter-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-size: 1.5rem; /* Standardized to 1.5rem */
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

.page-description, .error-message, .summary-stats {
  text-align: center;
  margin-bottom: 20px;
}

.summary-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.summary-card-wrapper {
  flex: 1 1 400px;
  min-width: 300px;
}

.filter-bar {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.load-button {
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.error-message, .loading-message, .no-data-message {
  color: #dc3545;
  margin: 20px;
  text-align: center;
}

.loading-message {
  color: #42b983;
}

.no-data-message {
  color: #6c757d;
}

.chart-container {
  height: 500px;
}

.rankings-container {
  display: flex;
  flex-direction: row;
  gap: 30px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 30px;
}

.ranking-table h3 {
  text-align: center;
  margin-bottom: 15px;
}
</style>
