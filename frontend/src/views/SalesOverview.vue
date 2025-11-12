<template>
  <div class="sales-overview">
    <div v-if="currentMonthRevenueData && previousMonthRevenueData && threeMonthAverageRevenueData" class="monthly-summary-card">
      <h2 class="summary-title">Análise Mensal Comparativa</h2>
      <p class="page-description">Visão geral do desempenho de vendas do mês atual em comparação com períodos anteriores.</p>
      <div class="stats-container top-summary-stats-container">
        <StatCard title="Faturamento Mês Atual (R$)" :value="currentMonthRevenueData.total_revenue" :isCurrency="true" />
        <StatCard 
          title="Faturamento do Último Mês (R$)" 
          :value="previousMonthRevenueData.total_revenue" 
          :isCurrency="true"
          :trendPercentage="previousMonthVsThreeMonthAvgTrendPercentage"
          :trendDirection="previousMonthVsThreeMonthAvgTrendDirection"
        />
        <StatCard title="Média Faturamento Últimos 3 Meses (R$)" :value="threeMonthAverageRevenueData.total_revenue" :isCurrency="true" />
      </div>
    </div>

    <div class="monthly-summary-card">
      <h2 class="summary-title">Análise Detalhada por Período</h2>
      <p class="page-description">Use os filtros abaixo para uma análise detalhada por período.</p>
      <div class="filter-bar">
        <CustomDatepicker id="start-date" label="Data de Início" v-model="filters.startDate" />
        <CustomDatepicker id="end-date" label="Data de Fim" v-model="filters.endDate" />
        <button @click="loadData" :disabled="loading" class="load-button">
          {{ loading ? 'Carregando...' : 'Carregar Dados' }}
        </button>
      </div>

      <div v-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>

      <div v-else-if="loading" class="loading-message">
        <p>Carregando dados do período...</p>
      </div>

      <div v-else-if="data" class="stats-wrapper">
        <div class="stats-container filterable-stats-container">
          <StatCard title="Faturamento Total (R$)" :value="data.total_revenue" :isCurrency="true" />
          <StatCard title="Total de Pedidos" :value="data.total_sales_count" :isNumberFormatted="true" />
          <StatCard title="Ticket Médio (R$)" :value="data.average_ticket_value" :isCurrency="true" />
        </div>
      </div>
      <div v-else class="no-data-message">
        <p>Nenhum dado disponível para o período selecionado.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getSalesOverview } from '../services/api';
import CustomDatepicker from '../components/CustomDatepicker.vue';
import StatCard from '../components/StatCard.vue';

const loading = ref(false);
const error = ref(null);
const data = ref(null);

const currentMonthRevenueData = ref(null);
const previousMonthRevenueData = ref(null);
const threeMonthAverageRevenueData = ref(null);

const previousMonthVsThreeMonthAvgTrendPercentage = ref(null);
const previousMonthVsThreeMonthAvgTrendDirection = ref('neutral');

const getDefaultEndDate = () => new Date().toISOString().split('T')[0];
const getDefaultStartDate = () => {
  const date = new Date();
  date.setDate(date.getDate() - 30);
  return date.toISOString().split('T')[0];
};

const filters = ref({
  startDate: getDefaultStartDate(),
  endDate: getDefaultEndDate()
});

const loadComparativeMonthlyRevenue = async () => {
  const today = new Date();
  const currentMonthFirstDay = new Date(today.getFullYear(), today.getMonth(), 1);
  const currentMonthEndDate = today;

  const previousMonthSameDay = new Date(today);
  previousMonthSameDay.setMonth(today.getMonth() - 1);
  if (previousMonthSameDay.getDate() !== today.getDate()) {
    previousMonthSameDay.setDate(0); 
  }
  const previousMonthFirstDay = new Date(previousMonthSameDay.getFullYear(), previousMonthSameDay.getMonth(), 1);

  let totalRevenueLast3FullMonths = 0;
  const promises = [];

  for (let i = 1; i <= 3; i++) {
    const monthEndDate = new Date(today.getFullYear(), today.getMonth() - i, 0);
    const monthStartDate = new Date(monthEndDate.getFullYear(), monthEndDate.getMonth(), 1);
    
    promises.push(getSalesOverview(
      monthStartDate.toISOString().split('T')[0],
      monthEndDate.toISOString().split('T')[0]
    ));
  }

  try {
    const [currentMonthResponse, previousMonthResponse, ...threeMonthResponses] = await Promise.all([
      getSalesOverview(
        currentMonthFirstDay.toISOString().split('T')[0],
        currentMonthEndDate.toISOString().split('T')[0]
      ),
      getSalesOverview(
        previousMonthFirstDay.toISOString().split('T')[0],
        previousMonthSameDay.toISOString().split('T')[0]
      ),
      ...promises
    ]);

    if (currentMonthResponse.data) {
      currentMonthRevenueData.value = currentMonthResponse.data;
    }

    if (previousMonthResponse.data) {
      previousMonthRevenueData.value = previousMonthResponse.data;
    }

    threeMonthResponses.forEach(response => {
      if (response.data && response.data.total_revenue) {
        totalRevenueLast3FullMonths += response.data.total_revenue;
      }
    });
    threeMonthAverageRevenueData.value = { total_revenue: totalRevenueLast3FullMonths / 3 };

    if (previousMonthRevenueData.value && threeMonthAverageRevenueData.value) {
      const previousMonthRevenue = previousMonthRevenueData.value.total_revenue || 0;
      const threeMonthAverageRevenue = threeMonthAverageRevenueData.value.total_revenue || 0;

      if (threeMonthAverageRevenue === 0) {
        previousMonthVsThreeMonthAvgTrendPercentage.value = null; 
        previousMonthVsThreeMonthAvgTrendDirection.value = 'neutral';
      } else {
        const diff = ((previousMonthRevenue - threeMonthAverageRevenue) / threeMonthAverageRevenue) * 100;
        previousMonthVsThreeMonthAvgTrendPercentage.value = diff;
        if (diff > 0) {
          previousMonthVsThreeMonthAvgTrendDirection.value = 'up';
        } else if (diff < 0) {
          previousMonthVsThreeMonthAvgTrendDirection.value = 'down';
        } else {
          previousMonthVsThreeMonthAvgTrendDirection.value = 'neutral';
        }
      }
    }

  } catch (err) {
    console.error("Failed to load comparative monthly revenue:", err);
  }
};

const loadData = async () => {
  loading.value = true;
  error.value = null;
  data.value = null;
  try {
    const response = await getSalesOverview(filters.value.startDate, filters.value.endDate);
    if (response.data && (response.data.total_revenue > 0 || response.data.total_sales_count > 0)) {
      data.value = response.data;
    } else {
      data.value = null;
    }
  } catch (err) {
    console.error("Failed to load sales overview:", err);
    error.value = "Falha ao carregar os dados do período.";
  }
  loading.value = false;
};

onMounted(() => {
  loadComparativeMonthlyRevenue();
  loadData();
});
</script>

<style scoped>
.sales-overview {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.monthly-summary-card, .filter-card {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.summary-title {
  text-align: center;
  margin-top: 0;
  margin-bottom: 10px;
  color: #2c3e50;
  font-size: 1.5rem; /* Standardized font size */
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

.stats-wrapper {
  width: 100%;
}

.stats-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: stretch;
  flex-wrap: wrap;
  gap: 20px;
  width: 100%;
}

.top-summary-stats-container .stat-card,
.filterable-stats-container .stat-card {
  width: calc((100% - 40px) / 3);
}

@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;
    align-items: center;
  }
  .top-summary-stats-container .stat-card,
  .filterable-stats-container .stat-card {
    width: 100%;
  }
}

.date-range-display {
  font-size: 1.1rem;
  color: #343a40;
  margin-bottom: 20px;
  text-align: center;
}

.error-message {
  color: #dc3545;
}

.loading-message {
  color: #495057;
}

.no-data-message {
  color: #6c757d;
}
</style>
