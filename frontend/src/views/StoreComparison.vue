<template>
  <div class="store-comparison">
    <div class="filter-card">
      <h1 class="page-title">Comparação de Lojas</h1>
      <p class="page-description">Compare a performance de faturamento e vendas entre as suas lojas.</p>
      <div class="filter-bar">
        <CustomDatepicker id="start-date" label="Data de Início" v-model="filters.startDate" />
        <CustomDatepicker id="end-date" label="Data de Fim" v-model="filters.endDate" />
        <button @click="loadComparisonData" :disabled="loading" class="load-button">
          {{ loading ? 'Carregando...' : 'Analisar' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <DataTable v-if="results" :columns="tableColumns" :data="results" />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getStoreComparison } from '../services/api';
import CustomDatepicker from '../components/CustomDatepicker.vue';
import DataTable from '../components/DataTable.vue';

const loading = ref(false);
const error = ref(null);
const results = ref(null);

const filters = ref({
  startDate: new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split('T')[0],
  endDate: new Date().toISOString().split('T')[0],
});

const tableColumns = [
  { key: 'dimension_name', label: 'Nome da Loja' },
  { key: 'total_revenue', label: 'Faturamento Total', isCurrency: true },
  { key: 'total_sales_count', label: 'Total de Pedidos' },
  { key: 'average_ticket_value', label: 'Ticket Médio', isCurrency: true },
];

const loadComparisonData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await getStoreComparison(filters.value.startDate, filters.value.endDate);
    results.value = response.data.breakdown;
  } catch (err) {
    console.error("Failed to load store comparison:", err);
    error.value = "Falha ao carregar os dados de comparação.";
  }
  loading.value = false;
};

onMounted(loadComparisonData);

</script>

<style scoped>
.store-comparison {
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
  font-size: 1.8rem;
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

.error-message {
  color: #dc3545;
  margin: 20px;
  text-align: center;
}
</style>
