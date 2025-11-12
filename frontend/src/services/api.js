import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const getMonthlySummary = () => {
  return apiClient.get('/analytics/monthly-summary');
};

export const getSalesOverview = (startDate, endDate) => {
  return apiClient.get('/analytics/sales-overview', {
    params: { start_date: startDate, end_date: endDate }
  });
};

export const getTopProducts = (params) => {
  const cleanedParams = Object.entries(params).reduce((acc, [key, value]) => {
    if (value !== null && value !== '') {
      acc[key] = value;
    }
    return acc;
  }, {});
  return apiClient.get('/analytics/top-products', { params: cleanedParams });
};

export const getSalesBreakdown = (startDate, endDate, dimension) => {
  return apiClient.get('/analytics/sales-breakdown', {
    params: { 
      dimension: dimension, 
      start_date: startDate, 
      end_date: endDate 
    }
  });
};

export const getTicketTrend = (startDate, endDate) => {
  return apiClient.get('/analytics/ticket-trend', {
    params: { start_date: startDate, end_date: endDate }
  });
};

export const getTicketComposition = (startDate, endDate) => {
  return apiClient.get('/analytics/ticket-composition', {
    params: { start_date: startDate, end_date: endDate }
  });
};

export const getDeliveryPerformance = (params) => {
  const cleanedParams = Object.entries(params).reduce((acc, [key, value]) => {
    if (value !== null && value !== '') {
      acc[key] = value;
    }
    return acc;
  }, {});
  return apiClient.get('/analytics/delivery-performance', { params: cleanedParams });
};

export const getFilterOptions = () => {
  return apiClient.get('/filters/options');
};

export const getCustomerChurnRisk = (minPurchases, inactiveDays) => {
  return apiClient.get('/analytics/customer-churn-risk', {
    params: { min_purchases: minPurchases, inactive_days: inactiveDays }
  });
};

export const getAverageTicketGoal = () => {
  return apiClient.get('/goal/average-ticket-goal');
};

export const updateAverageTicketGoal = (goalValue) => {
  return apiClient.put('/goal/average-ticket-goal', { goal_value: goalValue });
};
