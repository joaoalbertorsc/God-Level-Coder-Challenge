<template>
  <div class="product-margin-analysis">
    <div class="filter-card">
      <h1 class="page-title">Margem de Produtos</h1>
      <p class="page-description">Analise a margem de lucro dos seus produtos com base nos custos definidos.</p>
      <div class="filter-bar">
        <CustomDatepicker id="start-date" label="Data de Início" v-model="filters.startDate" />
        <CustomDatepicker id="end-date" label="Data de Fim" v-model="filters.endDate" />
        <button @click="loadMarginData" :disabled="loading" class="load-button">
          {{ loading ? 'Carregando...' : 'Analisar Margens' }}
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
      <DataTable :columns="tableColumns" :data="formattedResults" />
    </div>
    <div v-else class="no-data-message">
      <p>Nenhuma análise de margem disponível. Verifique se os custos dos produtos foram definidos na tela de Gestão de Custos e se há vendas no período selecionado.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getProductsByMargin } from '../services/api';
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
  { key: 'product_name', label: 'Nome do Produto' },
  { key: 'total_revenue', label: 'Receita Total', isCurrency: true },
  { key: 'total_cost', label: 'Custo Total', isCurrency: true },
  { key: 'total_margin_value', label: 'Margem (R$)', isCurrency: true },
  { key: 'total_margin_percent', label: 'Margem (%)' },
];

const formattedResults = computed(() => {
  return results.value?.map(p => ({ 
    ...p, 
    total_margin_percent: `${p.total_margin_percent.toFixed(2)}%`
  })) || [];
});

const loadMarginData = async () => {
  loading.value = true;
  error.value = null;
  results.value = null;
  try {
    const response = await getProductsByMargin(filters.value.startDate, filters.value.endDate);
    if (response.data && response.data.products && response.data.products.length > 0) {
      results.value = response.data.products;
    } else {
      results.value = [];
    }
  } catch (err) {
    console.error("Failed to load product margin analysis:", err);
    error.value = "Falha ao carregar a análise de margem. Por favor, tente novamente.";
  }
  loading.value = false;
};

onMounted(loadMarginData);
</script>

<style scoped>
.product-margin-analysis {
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
