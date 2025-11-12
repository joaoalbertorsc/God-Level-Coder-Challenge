<template>
  <div class="customer-retention">
    <div class="filter-card">
      <h1 class="page-title">Retenção de Clientes</h1>
      <p class="page-description">Identifique clientes fiéis com risco de churn com base no número de compras e inatividade.</p>
      <div class="filter-bar">
        <NumberInput id="min-purchases" label="Compras Mínimas" v-model="filters.minPurchases" :min="1" />
        <NumberInput id="inactive-days" label="Dias de Inatividade" v-model="filters.inactiveDays" :min="1" />
        <button @click="loadCustomers" :disabled="loading" class="load-button">
          {{ loading ? 'Carregando...' : 'Analisar Clientes' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="loading" class="loading-message">
      <p>Carregando dados...</p>
    </div>

    <div v-else-if="customers && customers.length > 0" class="results-container">
      <p class="results-summary">
        Clientes com risco de churn ({{ customers.length }} encontrados) que fizeram pelo menos 
        <strong>{{ filters.minPurchases }} compras</strong> e estão inativos há mais de 
        <strong>{{ filters.inactiveDays }} dias</strong>:
      </p>
      <DataTable :columns="tableColumns" :data="customers" />
    </div>
    <div v-else class="no-data-message">
      <p>Nenhum cliente encontrado com os critérios selecionados. Ajuste os filtros e tente novamente.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getCustomerChurnRisk } from '../services/api';
import NumberInput from '../components/NumberInput.vue';
import DataTable from '../components/DataTable.vue';

const loading = ref(false);
const error = ref(null);
const customers = ref(null);

const filters = ref({
  minPurchases: 3,
  inactiveDays: 30,
});

const tableColumns = [
  { key: 'customer_name', label: 'Nome do Cliente' },
  { key: 'total_purchases', label: 'Total de Compras' },
  { key: 'last_purchase_date', label: 'Última Compra' },
];

const loadCustomers = async () => {
  loading.value = true;
  error.value = null;
  customers.value = null; // Clear previous results
  try {
    const response = await getCustomerChurnRisk(filters.value.minPurchases, filters.value.inactiveDays);
    if (response.data && response.data.churn_risk_customers && response.data.churn_risk_customers.length > 0) {
      customers.value = response.data.churn_risk_customers;
    } else {
      customers.value = []; // Explicitly set to empty if no meaningful data
    }
  } catch (err) {
    console.error("Failed to load customer churn risk:", err);
    error.value = "Falha ao carregar os dados de retenção de clientes. Por favor, tente novamente.";
  }
  loading.value = false;
};

onMounted(loadCustomers);
</script>

<style scoped>
.customer-retention {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
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
  padding: 12px 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.load-button:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.load-button:hover:not(:disabled) {
  background-color: #368a67;
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

.results-container {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.results-summary {
  font-size: 1.1rem;
  color: #343a40;
  margin-bottom: 20px;
  text-align: center;
}
</style>
