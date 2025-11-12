<template>
  <div class="bullet-chart-card">
    <h3 class="card-title">{{ title }}</h3>
    <div class="chart-area">
      <div class="bullet-chart">
        <div class="bullet-bar" :style="{ width: barWidth + '%' }"></div>
        <div class="target-line" :style="{ left: targetPosition + '%' }"></div>
        <div class="reference-line" :style="{ left: referencePosition + '%' }"></div>
      </div>
      <div class="bullet-labels">
        <span>0</span>
        <span>{{ (maxValue / 2).toFixed(0) }}</span>
        <span>{{ maxValue.toFixed(0) }}</span>
      </div>
    </div>
    <div class="details-area">
      <div class="detail-item">
        <span class="label">Valor Atual:</span>
        <span class="value">{{ formatCurrency(currentValue) }}</span>
      </div>
      <div class="detail-item">
        <span class="label">Meta:</span>
        <input type="number" v-model.number="editableTarget" @change="saveTarget" class="target-input" />
      </div>
      <div class="detail-item">
        <span class="label">Referência:</span>
        <span class="value">{{ formatCurrency(referenceValue) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted} from 'vue';
import { getAverageTicketGoal, updateAverageTicketGoal } from '../services/api';

const props = defineProps({
  title: { type: String, required: true },
  currentValue: { type: Number, required: true },
  referenceValue: { type: Number, required: true },
  unit: { type: String, default: 'R$' }
});

const editableTarget = ref(0);

const maxValue = computed(() => {
  return Math.max(props.currentValue, editableTarget.value, props.referenceValue) * 1.2;
});

const barWidth = computed(() => (props.currentValue / maxValue.value) * 100);
const targetPosition = computed(() => (editableTarget.value / maxValue.value) * 100);
const referencePosition = computed(() => (props.referenceValue / maxValue.value) * 100);

const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
};

const saveTarget = async () => {
  try {
    await updateAverageTicketGoal(editableTarget.value);
  } catch (err) {
    console.error("Failed to update target:", err);
  }
};

onMounted(async () => {
  try {
    const response = await getAverageTicketGoal();
    editableTarget.value = response.data.goal_value;
  } catch (err) {
    console.error("Failed to load target:", err);
  }
});

</script>

<style scoped>
.bullet-chart-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-title {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.chart-area {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.bullet-chart {
  position: relative;
  width: 100%;
  height: 20px;
  background-color: #e9ecef;
  border-radius: 10px;
}

.bullet-bar {
  position: absolute;
  height: 100%;
  background-color: #42b983;
  border-radius: 10px;
}

.target-line {
  position: absolute;
  height: 120%;
  top: -10%;
  width: 2px;
  background-color: #dc3545;
}

.reference-line {
  position: absolute;
  height: 80%;
  top: 10%;
  width: 2px;
  background-color: #ffc107;
}

.bullet-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem; /* Standardized */
  color: #6c757d;
}

.details-area {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem; /* Standardized */
}

.label {
  font-weight: 600;
  color: #495057;
}

.value {
  color: #212529;
}

.target-input {
  width: 80px;
  text-align: right;
  border: 1px solid #ced4da;
  border-radius: 4px;
  padding: 5px;
  font-size: 0.9rem; /* Standardized */
}
</style>
