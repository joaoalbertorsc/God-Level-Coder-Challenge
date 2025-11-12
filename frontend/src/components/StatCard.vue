<template>
  <div class="stat-card" :title="tooltipText">
    <h3 class="stat-title">{{ title }}</h3>
    <p class="stat-value">{{ formattedValue }}</p>
    <div v-if="trendPercentage !== null" class="comparison-details">
      <span :class="trendClass">
        <i :class="trendIcon"></i> {{ formattedTrendPercentage }}
      </span>
    </div>
    <p v-if="subValue" class="stat-sub-value">{{ subValue }}</p>
    <p v-if="subValue2" class="stat-sub-value-small">{{ subValue2 }}</p>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    title: { type: String, required: true },
    value: { type: [String, Number], required: true },
    subValue: { type: [String, Number], default: '' },
    subValue2: { type: [String, Number], default: '' },
    isCurrency: { type: Boolean, default: false },
    isNumberFormatted: { type: Boolean, default: false },
    trendPercentage: { type: [Number, null], default: null },
    trendDirection: { type: String, default: 'neutral' }
  },
  computed: {
    formattedValue() {
      const numValue = Number(this.value);
      if (isNaN(numValue)) {
        return this.value;
      }
      if (this.isCurrency) {
        return numValue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
      } else if (this.isNumberFormatted) {
        return numValue.toLocaleString('pt-BR');
      }
      return this.value;
    },
    formattedTrendPercentage() {
      if (this.trendPercentage === null) return '';
      const diff = this.trendPercentage;
      const sign = diff > 0 ? '+' : '';
      return `${sign}${diff.toFixed(2)}%`;
    },
    trendClass() {
      if (this.trendDirection === 'up') return 'trend-up';
      if (this.trendDirection === 'down') return 'trend-down';
      return 'trend-neutral';
    },
    trendIcon() {
      if (this.trendDirection === 'up') return 'fas fa-arrow-up';
      if (this.trendDirection === 'down') return 'fas fa-arrow-down';
      return 'fas fa-minus';
    },
    tooltipText() {
      let text = String(this.formattedValue);
      if (this.subValue) text += ` - ${this.subValue}`;
      if (this.subValue2) text += ` - ${this.subValue2}`;
      if (this.trendPercentage !== null) text += ` (${this.formattedTrendPercentage})`;
      return text;
    }
  }
}
</script>

<style scoped>
.stat-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-title {
  font-size: 1.2rem; /* Standardized */
  font-weight: 600;
  color: #6c757d;
  margin-top: 0;
  margin-bottom: 10px;
}

.stat-value {
  font-weight: 700;
  color: #343a40;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: clamp(1.3rem, 2.5vw, 1.8rem);
}

.stat-sub-value {
  font-size: 1.1rem;
  font-weight: 500;
  color: #495057;
  margin: 5px 0 0;
}

.stat-sub-value-small {
  font-size: 0.9rem; /* Standardized */
  font-style: italic;
  color: #6c757d;
  margin: 3px 0 0;
}

.comparison-details {
  margin-top: 10px;
  font-size: 0.9rem; /* Standardized */
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.trend-up {
  color: #28a745;
}

.trend-down {
  color: #dc3545;
}

.trend-neutral {
  color: #6c757d;
}
</style>
