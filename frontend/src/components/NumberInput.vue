<template>
  <div class="number-input-group">
    <label :for="id">{{ label }}</label>
    <input 
      :id="id" 
      type="number" 
      :value="modelValue" 
      @input="$emit('update:modelValue', $event.target.value)" 
      :min="min" 
      :max="max" 
      class="number-input"
    />
  </div>
</template>

<script setup>
defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  modelValue: { type: [String, Number], default: '' },
  min: { type: Number, default: undefined },
  max: { type: Number, default: undefined }
});
defineEmits(['update:modelValue']);
</script>

<style scoped>
.number-input-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 10px;
}

.number-input-group label {
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 0.9rem;
}

.number-input {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  max-width: 150px;
}
</style>
