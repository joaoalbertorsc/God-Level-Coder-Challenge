<template>
  <div class="select-input-group">
    <label :for="id">{{ label }}</label>
    <select :id="id" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)" class="select-input">
      <option value="">{{ defaultOptionText }}</option>
      <option v-for="option in options" :key="option.id" :value="option.id">
        {{ option.name }}
      </option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, required: true },
  defaultOptionText: { type: String, default: 'Todos' } // e.g., "All Channels"
});
defineEmits(['update:modelValue']);
</script>

<style scoped>
.select-input-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 10px;
  /* Allow the component to shrink */
  min-width: 150px; 
}

.select-input-group label {
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 0.9rem;
}

.select-input {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  width: 100%; /* Make the select element take the full width of its container */
  box-sizing: border-box; /* Include padding and border in the element's total width */

  /* The following properties handle long text */
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>
