<template>
  <div class="date-input-group">
    <label :for="id">{{ label }}</label>
    <Datepicker 
      :id="id"
      v-model="date"
      format="dd/MM/yyyy"
      model-type="yyyy-MM-dd"
      :enable-time-picker="false"
      auto-apply
      placeholder="Selecione a data"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  modelValue: {
    type: String, // Expecting date in YYYY-MM-DD format
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const date = ref(props.modelValue);

// Watch for changes from the parent and update the datepicker
watch(() => props.modelValue, (newValue) => {
  date.value = newValue;
});

// Watch for changes in the datepicker and emit them to the parent
watch(date, (newValue) => {
  emit('update:modelValue', newValue);
});
</script>

<style scoped>
.date-input-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 10px;
}

.date-input-group label {
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 0.9rem;
}

/* You can customize the datepicker's appearance here */
</style>
