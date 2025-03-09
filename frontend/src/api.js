import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api";

export const getInventory = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/inventory`);
    return response.data;
  } catch (error) {
    console.error("Error fetching inventory:", error);
    throw error;
  }
};

export const updateInventory = async (item) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/inventory`, item);
    return response.data;
  } catch (error) {
    console.error("Error updating inventory:", error);
    throw error;
  }
};

export const getRestockingAlerts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/alerts`);
    return response.data;
  } catch (error) {
    console.error("Error fetching alerts:", error);
    throw error;
  }
};

export const getSalesTrends = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/sales-trends`);
    return response.data;
  } catch (error) {
    console.error("Error fetching sales trends:", error);
    throw error;
  }
};

export const login = async (credentials) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
    return response.data;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
};
