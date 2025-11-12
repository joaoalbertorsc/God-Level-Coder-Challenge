<template>
  <div class="ticket-trend">
    <div v-if="currentMonthAverageTicketData && previousMonthAverageTicketData && threeMonthAverageTicketData && sixMonthAverageTicketData && twelveMonthAverageTicketData" class="monthly-summary-card">
      <h2 class="summary-title">Ticket Médio Mensal</h2>
      <p class="page-description">Visão geral do ticket médio do mês atual em comparação com períodos anteriores.</p>
      <div class="stats-container top-summary-stats-container">
        <StatCard 
          title="Ticket Médio Mês Atual"
          :value="currentMonthAverageTicketData.average_ticket_value" 
          :isCurrency="true"
          :trendPercentage="currentVsPreviousMonthTrendPercentage"
          :trendDirection="currentVsPreviousMonthTrendDirection"
        />
        <StatCard 
          title="Ticket Médio Mês Passado"
          :value="previousMonthAverageTicketData.average_ticket_value" 
          :isCurrency="true"
          :trendPercentage="previousVsThreeMonthAvgTrendPercentage"
          :trendDirection="previousVsThreeMonthAvgTrendDirection"
        />
        <StatCard 
          title="Média T.M. Últimos 3 Meses"
          :value="threeMonthAverageTicketData.average_ticket_value" 
          :isCurrency="true"
          :trendPercentage="threeMonthAvgVsSixMonthAvgTrendPercentage"
          :trendDirection="threeMonthAvgVsSixMonthAvgTrendDirection"
        />
        <StatCard 
          title="Média T.M. Últimos 6 Meses"
          :value="sixMonthAverageTicketData.average_ticket_value" 
          :isCurrency="true"
          :trendPercentage="sixMonthAvgVsTwelveMonthAvgTrendPercentage"
          :trendDirection="sixMonthAvgVsTwelveMonthAvgTrendDirection"
        />
        <StatCard title="Média T.M. Último Ano" :value="twelveMonthAverageTicketData.average_ticket_value" :isCurrency="true" />
      </div>

      <div class="charts-within-card-container">
        <BulletChartCard
          v-if="currentMonthAverageTicketData && previousMonthAverageTicketData"
          title="Meta de Ticket Médio (Mês Atual)"
          :currentValue="currentMonthAverageTicketData.average_ticket_value"
          :referenceValue="previousMonthAverageTicketData.average_ticket_value"
          unit="R$"
          class="bullet-chart-container-within-card"
        />
      </div>
    </div>

    <div class="monthly-summary-card">
      <h2 class="summary-title">Análise de Tendência do Ticket Médio</h2>
      <p class="page-description">Utilize os filtros para visualizar a evolução do ticket médio em diferentes períodos.</p>
      
      <div class="filter-bar">
        <CustomDatepicker id="start-date" label="Data de Início" v-model="filters.startDate" />
        <CustomDatepicker id="end-date" label="Data de Fim" v-model="filters.endDate" />
        <button @click="loadFilteredData" :disabled="loading" class="load-button">
          {{ loading ? 'Carregando...' : 'Analisar' }}
        </button>
      </div>

      <div v-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>

      <div v-else-if="loading" class="loading-message">
        <p>Carregando dados...</p>
      </div>

      <div v-else class="side-by-side-charts">
        <div class="chart-container">
          <div v-if="chartData">
            <LineChart :chartData="chartData" />
          </div>
          <div v-else class="no-data-message">
            <p>Nenhum dado de tendência disponível para o período selecionado.</p>
          </div>
        </div>

        <div class="doughnut-chart-container">
          <DoughnutChartCard 
            v-if="doughnutChartData"
            title="Composição por Categoria"
            :chartData="doughnutChartData"
          />
          <div v-else class="no-data-message">
            <p>Nenhum dado de composição disponível para o período selecionado.</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getTicketTrend, getSalesOverview, getTicketComposition } from '../services/api';
import CustomDatepicker from '../components/CustomDatepicker.vue';
import LineChart from '../components/LineChart.vue';
import StatCard from '../components/StatCard.vue';
import BulletChartCard from '../components/BulletChartCard.vue';
import DoughnutChartCard from '../components/DoughnutChartCard.vue';
import { formatDateForDisplay } from '../utils/formatters';

const loading = ref(false);
const error = ref(null);
const trendData = ref([]);
const ticketCompositionData = ref(null);

const currentMonthAverageTicketData = ref(null);
const previousMonthAverageTicketData = ref(null);
const threeMonthAverageTicketData = ref(null);
const sixMonthAverageTicketData = ref(null);
const twelveMonthAverageTicketData = ref(null);

const currentVsPreviousMonthTrendPercentage = ref(null);
const currentVsPreviousMonthTrendDirection = ref('neutral');

const previousVsThreeMonthAvgTrendPercentage = ref(null);
const previousVsThreeMonthAvgTrendDirection = ref('neutral');

const threeMonthAvgVsSixMonthAvgTrendPercentage = ref(null);
const threeMonthAvgVsSixMonthAvgTrendDirection = ref('neutral');

const sixMonthAvgVsTwelveMonthAvgTrendPercentage = ref(null);
const sixMonthAvgVsTwelveMonthAvgTrendDirection = ref('neutral');

const filters = ref({
  startDate: new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split('T')[0],
  endDate: new Date().toISOString().split('T')[0],
});

const chartData = computed(() => {
  if (!trendData.value || trendData.value.length === 0) return null;
  return {
    labels: trendData.value.map(d => formatDateForDisplay(d.date)),
    datasets: [
      {
        label: 'Ticket Médio (R$)',
        backgroundColor: '#42b983',
        borderColor: '#42b983',
        data: trendData.value.map(d => d.value),
        tension: 0.1
      }
    ]
  };
});

const doughnutChartData = computed(() => {
  if (!ticketCompositionData.value || ticketCompositionData.value.composition.length === 0) return null;

  const labels = ticketCompositionData.value.composition.map(item => item.category_name);
  const data = ticketCompositionData.value.composition.map(item => item.total_revenue);

  const backgroundColors = labels.map((_, index) => `hsl(${index * 60}, 70%, 60%)`);

  return {
    labels: labels,
    datasets: [
      {
        backgroundColor: backgroundColors,
        data: data,
      }
    ]
  };
});

const calculateTrend = (currentValue, comparativeValue) => {
  if (comparativeValue === null || comparativeValue === 0) {
    return { percentage: null, direction: 'neutral' };
  }
  const diff = ((currentValue - comparativeValue) / comparativeValue) * 100;
  let direction = 'neutral';
  if (diff > 0) direction = 'up';
  else if (diff < 0) direction = 'down';
  return { percentage: diff, direction: direction };
};

const loadComparativeMonthlyAverageTickets = async () => {
  const today = new Date();
  const currentMonthFirstDay = new Date(today.getFullYear(), today.getMonth(), 1);
  const currentMonthEndDate = today;

  const previousMonthSameDay = new Date(today);
  previousMonthSameDay.setMonth(today.getMonth() - 1);
  if (previousMonthSameDay.getDate() !== today.getDate()) {
    previousMonthSameDay.setDate(0); 
  }
  const previousMonthFirstDay = new Date(previousMonthSameDay.getFullYear(), previousMonthSameDay.getMonth(), 1);

  const getMonthlyOverviewPromises = (numMonths) => {
    const promises = [];
    for (let i = 1; i <= numMonths; i++) {
      const monthEndDate = new Date(today.getFullYear(), today.getMonth() - i, 0); 
      const monthStartDate = new Date(monthEndDate.getFullYear(), monthEndDate.getMonth(), 1); 
      promises.push(getSalesOverview(
        monthStartDate.toISOString().split('T')[0],
        monthEndDate.toISOString().split('T')[0]
      ));
    }
    return promises;
  };

  const threeMonthPromises = getMonthlyOverviewPromises(3);
  const sixMonthPromises = getMonthlyOverviewPromises(6);
  const twelveMonthPromises = getMonthlyOverviewPromises(12);

  try {
    const [currentMonthResponse, previousMonthResponse, ...allOtherResponses] = await Promise.all([
      getSalesOverview(
        currentMonthFirstDay.toISOString().split('T')[0],
        currentMonthEndDate.toISOString().split('T')[0]
      ),
      getSalesOverview(
        previousMonthFirstDay.toISOString().split('T')[0],
        previousMonthSameDay.toISOString().split('T')[0]
      ),
      ...threeMonthPromises,
      ...sixMonthPromises,
      ...twelveMonthPromises
    ]);

    if (currentMonthResponse.data) {
      currentMonthAverageTicketData.value = currentMonthResponse.data;
    }

    if (previousMonthResponse.data) {
      previousMonthAverageTicketData.value = previousMonthResponse.data;
    }

    let totalAverageTicketLast3FullMonths = 0;
    const threeMonthResponses = allOtherResponses.slice(0, 3);
    threeMonthResponses.forEach(response => {
      if (response.data && response.data.average_ticket_value) {
        totalAverageTicketLast3FullMonths += response.data.average_ticket_value;
      }
    });
    threeMonthAverageTicketData.value = { average_ticket_value: totalAverageTicketLast3FullMonths / 3 };

    let totalAverageTicketLast6FullMonths = 0;
    const sixMonthResponses = allOtherResponses.slice(3, 9);
    sixMonthResponses.forEach(response => {
      if (response.data && response.data.average_ticket_value) {
        totalAverageTicketLast6FullMonths += response.data.average_ticket_value;
      }
    });
    sixMonthAverageTicketData.value = { average_ticket_value: totalAverageTicketLast6FullMonths / 6 };

    let totalAverageTicketLast12FullMonths = 0;
    const twelveMonthResponses = allOtherResponses.slice(9, 21);
    twelveMonthResponses.forEach(response => {
      if (response.data && response.data.average_ticket_value) {
        totalAverageTicketLast12FullMonths += response.data.average_ticket_value;
      }
    });
    twelveMonthAverageTicketData.value = { average_ticket_value: totalAverageTicketLast12FullMonths / 12 };

    if (currentMonthAverageTicketData.value && previousMonthAverageTicketData.value) {
      const { percentage, direction } = calculateTrend(
        currentMonthAverageTicketData.value.average_ticket_value,
        previousMonthAverageTicketData.value.average_ticket_value
      );
      currentVsPreviousMonthTrendPercentage.value = percentage;
      currentVsPreviousMonthTrendDirection.value = direction;
    }

    if (previousMonthAverageTicketData.value && threeMonthAverageTicketData.value) {
      const { percentage, direction } = calculateTrend(
        previousMonthAverageTicketData.value.average_ticket_value,
        threeMonthAverageTicketData.value.average_ticket_value
      );
      previousVsThreeMonthAvgTrendPercentage.value = percentage;
      previousVsThreeMonthAvgTrendDirection.value = direction;
    }

    if (threeMonthAverageTicketData.value && sixMonthAverageTicketData.value) {
      const { percentage, direction } = calculateTrend(
        threeMonthAverageTicketData.value.average_ticket_value,
        sixMonthAverageTicketData.value.average_ticket_value
      );
      threeMonthAvgVsSixMonthAvgTrendPercentage.value = percentage;
      threeMonthAvgVsSixMonthAvgTrendDirection.value = direction;
    }

    if (sixMonthAverageTicketData.value && twelveMonthAverageTicketData.value) {
      const { percentage, direction } = calculateTrend(
        sixMonthAverageTicketData.value.average_ticket_value,
        twelveMonthAverageTicketData.value.average_ticket_value
      );
      sixMonthAvgVsTwelveMonthAvgTrendPercentage.value = percentage;
      sixMonthAvgVsTwelveMonthAvgTrendDirection.value = direction;
    }

  } catch (err) {
    console.error("Failed to load comparative monthly average tickets:", err);
  }
};

const loadFilteredData = async () => {
  loading.value = true;
  error.value = null;
  trendData.value = [];
  ticketCompositionData.value = null;

  try {
    const [trendResponse, compositionResponse] = await Promise.all([
      getTicketTrend(filters.value.startDate, filters.value.endDate),
      getTicketComposition(filters.value.startDate, filters.value.endDate)
    ]);

    if (trendResponse.data && trendResponse.data.trend && trendResponse.data.trend.length > 0) {
      trendData.value = trendResponse.data.trend;
    }

    if (compositionResponse.data) {
      ticketCompositionData.value = compositionResponse.data;
    }

  } catch (err) {
    console.error("Failed to load filtered data:", err);
    error.value = "Falha ao carregar os dados filtrados. Por favor, tente novamente.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadComparativeMonthlyAverageTickets();
  loadFilteredData();
});

</script>

<style scoped>
.ticket-trend {
  width: 100%;
  max-width: 1400px;
}

.monthly-summary-card {
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

.side-by-side-charts {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.chart-container {
  flex: 2;
  min-width: 0;
  height: 150px; 
}

.doughnut-chart-container {
  flex: 1;
  min-width: 0;
}

.bullet-chart-container-within-card {
  margin-top: 20px;
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

.top-summary-stats-container .stat-card {
  width: calc((100% - 80px) / 5);
}

@media (max-width: 992px) {
  .side-by-side-charts {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;
    align-items: center;
  }
  .top-summary-stats-container .stat-card {
    width: 100%;
  }
}
</style>
