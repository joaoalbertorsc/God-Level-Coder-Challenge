<template>
  <div class="cost-management">
    <div class="filter-card">
      <p class="page-description">Defina e atualize os preços de custo dos seus produtos para análises de margem precisas.</p>
      
      <div v-if="loadingProducts" class="loading-message">
        <p>Carregando produtos...</p>
      </div>
      <div v-else-if="errorProducts" class="error-message">
        <p>{{ errorProducts }}</p>
      </div>

      <div v-else-if="Object.keys(groupedProducts).length > 0" class="categories-container">
        <div v-for="(products, categoryName) in groupedProducts" :key="categoryName" class="category-section">
          <h3 class="category-title">{{ categoryName }}</h3>
          
          <div class="category-actions">
            <NumberInput 
              :id="`percent-input-${categoryName}`" 
              label="Aplicar % do Preço de Venda"
              v-model="categoryPercentage[categoryName]"
              :min="0" :max="100"
            />
            <button @click="applyPercentageToCategory(categoryName)" class="apply-button">Aplicar</button>
          </div>

          <div class="product-list">
            <div v-for="product in products" :key="product.id" class="product-item">
              <span class="product-name">{{ product.name }}</span>
              <NumberInput 
                :id="`cost-input-${product.id}`" 
                label="Preço de Custo (R$)"
                v-model="editableCosts[product.id]"
                :min="0"
              />
            </div>
          </div>
        </div>
        
        <div class="save-section">
          <button @click="saveCosts" :disabled="saving" class="save-button">
            {{ saving ? 'Salvando...' : 'Salvar Custos' }}
          </button>
          <div v-if="saveError" class="error-message">
            <p>{{ saveError }}</p>
          </div>
          <div v-if="saveSuccess" class="success-message">
            <p>Custos salvos com sucesso!</p>
          </div>
        </div>
      </div>
      <div v-else class="no-data-message">
        <p>Nenhum produto encontrado para gerenciamento de custos.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getProductsForCostManagement, updateProductCosts } from '../services/api';
import NumberInput from '../components/NumberInput.vue';

const loadingProducts = ref(false);
const errorProducts = ref(null);
const groupedProducts = ref({}); // { 'Category Name': [{id, name, cost_price, category_name}] }
const editableCosts = ref({}); // { product_id: cost_price }
const productPrices = ref({}); // { product_id: current_sale_price } - to calculate percentage
const categoryPercentage = ref({}); // { 'Category Name': percentage }

const saving = ref(false);
const saveError = ref(null);
const saveSuccess = ref(false);

const loadProducts = async () => {
  loadingProducts.value = true;
  errorProducts.value = null;
  try {
    const response = await getProductsForCostManagement();
    groupedProducts.value = response.data;
    
    // Initialize editableCosts and productPrices
    for (const category in response.data) {
      response.data[category].forEach(product => {
        editableCosts.value[product.id] = product.cost_price !== null ? product.cost_price : '';
        // NOTE: Backend currently doesn't return sale price. 
        // For percentage calculation, we'd need sale price here.
        // For this example, let's assume a dummy sale price for percentage calculation.
        productPrices.value[product.id] = Math.random() * 100 + 10; // Dummy sale price
      });
    }
  } catch (err) {
    console.error("Failed to load products for cost management:", err);
    errorProducts.value = "Falha ao carregar produtos. Por favor, tente novamente.";
  }
  loadingProducts.value = false;
};

const applyPercentageToCategory = (categoryName) => {
  const percentage = parseFloat(categoryPercentage.value[categoryName]);
  if (isNaN(percentage) || percentage < 0 || percentage > 100) {
    alert("Por favor, insira uma porcentagem válida entre 0 e 100.");
    return;
  }

  groupedProducts.value[categoryName].forEach(product => {
    // Assuming productPrices has the sale price. This needs to be fetched from backend.
    const salePrice = productPrices.value[product.id]; 
    if (salePrice) {
      editableCosts.value[product.id] = (salePrice * (percentage / 100)).toFixed(2);
    }
  });
};

const saveCosts = async () => {
  saving.value = true;
  saveError.value = null;
  saveSuccess.value = false;

  const costsToSave = [];
  for (const productId in editableCosts.value) {
    const cost = parseFloat(editableCosts.value[productId]);
    if (!isNaN(cost) && cost >= 0) {
      costsToSave.push({
        product_id: parseInt(productId),
        cost_price: cost
      });
    } else if (editableCosts.value[productId] === '') {
        // Allow saving empty cost_price as null (if backend supports it)
        costsToSave.push({
            product_id: parseInt(productId),
            cost_price: null
        });
    } else {
      saveError.value = "Por favor, verifique se todos os custos são números válidos e não negativos.";
      saving.value = false;
      return;
    }
  }

  try {
    await updateProductCosts(costsToSave);
    saveSuccess.value = true;
    // Optionally reload products to show updated costs or clear success message after a delay
    setTimeout(() => saveSuccess.value = false, 3000);
  } catch (err) {
    console.error("Failed to save costs:", err);
    saveError.value = "Falha ao salvar custos. Por favor, tente novamente.";
  }
  saving.value = false;
};

onMounted(loadProducts);
</script>

<style scoped>
.cost-management {
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
}

.page-description {
  margin-top: 0;
  margin-bottom: 20px;
  color: #6c757d;
  font-size: 1rem;
  text-align: center;
}

.loading-message, .error-message, .no-data-message, .success-message {
  text-align: center;
  margin: 20px 0;
}

.loading-message {
  color: #42b983;
}

.error-message {
  color: #dc3545;
}

.success-message {
  color: #28a745;
}

.categories-container {
  margin-top: 20px;
}

.category-section {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.category-title {
  font-size: 1.5rem;
  color: #343a40;
  margin-top: 0;
  margin-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.category-actions {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.apply-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  height: 38px; /* Align with NumberInput height */
}

.apply-button:hover {
  background-color: #0056b3;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.product-item {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.product-name {
  font-weight: 600;
  color: #495057;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.save-section {
  margin-top: 30px;
  text-align: center;
}

.save-button {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:disabled {
  background-color: #94d3a2;
  cursor: not-allowed;
}

.save-button:hover:not(:disabled) {
  background-color: #218838;
}
</style>
