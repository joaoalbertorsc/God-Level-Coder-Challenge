<template>
  <div class="sales-breakdown">
    <div class="filter-card">
      <h1 class="page-title">Análise de Vendas</h1>
      <p class="page-description">Compare a performance de faturamento e vendas entre suas lojas ou canais.</p>
      <div class="filter-bar">
        <CustomDatepicker id="start-date" label="Data de Início" v-model="filters.startDate" />
        <CustomDatepicker id="end-date" label="Data de Fim" v-model="filters.endDate" />
        <SelectInput id="dimension" label="Analisar por" v-model="filters.dimension" :options="dimensionOptions" />
        <button @click="loadBreakdownData" :disabled="loading" class="load-button">
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

    <div v-else-if="results && results.length > 0">
      <DataTable :columns="tableColumns" :data="results" />
    </div>
    <div v-else class="no-data-message">
      <p>Nenhum dado disponível para os critérios selecionados. Ajuste os filtros e tente novamente.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getSalesBreakdown } from '../services/api';
import CustomDatepicker from '../components/CustomDatepicker.vue';
import SelectInput from '../components/SelectInput.vue';
import DataTable from '../components/DataTable.vue';

const loading = ref(false);
const error = ref(null);
const results = ref(null);

const filters = ref({
  startDate: new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split('T')[0],
  endDate: new Date().toISOString().split('T')[0],
  dimension: 'store' // Default to store
});

const dimensionOptions = ref([
  { id: 'store', name: 'Loja' },
  { id: 'channel', name: 'Canal' }
]);

const tableColumns = computed(() => {
  const dimensionLabel = filters.value.dimension === 'store' ? 'Nome da Loja' : 'Nome do Canal';
  return [
    { key: 'dimension_name', label: dimensionLabel },
    { key: 'total_revenue', label: 'Faturamento Total', isCurrency: true },
    { key: 'total_sales_count', label: 'Total de Pedidos' },
    { key: 'average_ticket_value', label: 'Ticket Médio', isCurrency: true },
  ];
});

const loadBreakdownData = async () => {
  loading.value = true;
  error.value = null;
  results.value = null; // Clear previous results
  try {
    const response = await getSalesBreakdown(filters.value.startDate, filters.value.endDate, filters.value.dimension);
    if (response.data && response.data.breakdown && response.data.breakdown.length > 0) {
      results.value = response.data.breakdown;
    } else {
      results.value = null; // Explicitly set to null if no meaningful data
    }
  } catch (err) {
    console.error("Failed to load sales breakdown:", err);
    error.value = "Falha ao carregar os dados de análise de vendas. Por favor, tente novamente.";
  }
  loading.value = false;
};

onMounted(loadBreakdownData);

</script>

<style scoped>
.sales-breakdown {
  width: 100%;
  max-width: 1400px;
}

.filter-card {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
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

.page-description {
  margin-top: 0;
  margin-bottom: 20px;
  color: #6c757d;
  font-size: 1rem;
  text-align: center;
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
</style>
