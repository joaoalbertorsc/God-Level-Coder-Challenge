<template>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!data || data.length === 0">
          <td :colspan="columns.length" class="no-data">Nenhum dado encontrado.</td>
        </tr>
        <tr v-for="(item, index) in data" :key="item.id || index">
          <td v-for="column in columns" :key="column.key" :title="getTooltip(item, column)">
            {{ formatValue(item, column) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  columns: { type: Array, required: true },
  data: { type: Array, required: true }
});

const formatValue = (item, column) => {
  const value = item[column.key];
  if (column.isCurrency) {
    return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  }
  return value;
};

const getTooltip = (item, column) => {
  if (column.tooltipKey) {
    return item[column.tooltipKey];
  }
  // Fallback to the display value if no specific tooltip key is provided
  const value = item[column.key];
  if (column.isCurrency) {
    return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  }
  return value;
};
</script>

<style scoped>
/* ... (existing styles) */
.table-container {
  width: 100%;
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  overflow: hidden;
}
th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}
thead th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #495057;
}
tbody tr:last-child td {
  border-bottom: none;
}
tbody tr:hover {
  background-color: #f1f3f5;
}
.no-data {
  text-align: center;
  padding: 30px;
  color: #6c757d;
}
</style>
