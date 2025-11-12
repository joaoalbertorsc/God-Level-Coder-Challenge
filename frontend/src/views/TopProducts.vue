<template>
  <div class="top-products">
    <div class="filter-card">
      <h1 class="page-title">Análise de Produtos</h1>
      <p class="page-description">Filtre para encontrar os produtos mais vendidos por receita em diferentes cenários.</p>
      <div class="filter-bar">
        <CustomDatepicker id="start-date" label="Data de Início" v-model="filters.start_date" />
        <CustomDatepicker id="end-date" label="Data de Fim" v-model="filters.end_date" />
        <SelectInput id="channel" label="Canal de Venda" v-model="filters.channel_id" :options="filterOptions.channels" />
        <SelectInput id="store" label="Loja" v-model="filters.store_id" :options="filterOptions.stores" />
        <SelectInput id="day-of-week" label="Dia da Semana" v-model="filters.day_of_week" :options="dayOfWeekOptions" />
        <NumberInput id="start-hour" label="Hora Início" v-model="filters.start_hour" :min="0" :max="23" />
        <NumberInput id="end-hour" label="Hora Fim" v-model="filters.end_hour" :min="0" :max="23" />
        <NumberInput id="limit" label="Limite" v-model="filters.limit" :min="1" :max="100" />
      </div>
      <button @click="loadTopProducts" :disabled="loading" class="load-button">
        {{ loading ? 'Carregando...' : 'Analisar Produtos' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="loading" class="loading-message">
      <p>Carregando dados...</p>
    </div>

    <div v-else-if="results && formattedResults.length > 0">
      <DataTable :columns="tableColumns" :data="formattedResults" />
    </div>
    <div v-else class="no-data-message">
      <p>Nenhum produto encontrado com os critérios selecionados. Ajuste os filtros e tente novamente.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getTopProducts, getFilterOptions } from '../services/api';
import CustomDatepicker from '../components/CustomDatepicker.vue';
import SelectInput from '../components/SelectInput.vue';
import NumberInput from '../components/NumberInput.vue';
import DataTable from '../components/DataTable.vue';

const loading = ref(false);
const error = ref(null);
const results = ref(null);

const filterOptions = ref({ channels: [], stores: [] });
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
  limit: 10,
  channel_id: '',
  store_id: '',
  day_of_week: '',
  start_hour: '',
  end_hour: ''
});

const tableColumns = [
  { key: 'rank', label: '#' },
  { key: 'product_name', label: 'Nome do Produto' },
  { key: 'total_revenue', label: 'Faturamento Total', isCurrency: true },
  { key: 'total_sales_count', label: 'Total de Vendas' },
];

const formattedResults = computed(() => {
  return results.value?.top_products.map((p, index) => ({ ...p, rank: index + 1 })) || [];
});

const loadInitialData = async () => {
  try {
    const [optionsResponse] = await Promise.all([
      getFilterOptions(),
    ]);
    filterOptions.value = optionsResponse.data;
    await loadTopProducts(); // Load initial results with default filters
  } catch (err) {
    console.error("Failed to load initial data:", err);
    error.value = "Falha ao carregar opções de filtro.";
  }
};

const loadTopProducts = async () => {
  loading.value = true;
  error.value = null;
  results.value = null; // Clear previous results
  try {
    const response = await getTopProducts(filters.value);
    if (response.data && response.data.top_products && response.data.top_products.length > 0) {
      results.value = response.data;
    } else {
      results.value = null; // Explicitly set to null if no meaningful data
    }
  } catch (err) {
    console.error("Failed to load top products:", err);
    error.value = "Falha ao carregar os dados dos produtos. Por favor, tente novamente.";
  }
  loading.value = false;
};

onMounted(loadInitialData);

</script>

<style scoped>
.top-products {
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
