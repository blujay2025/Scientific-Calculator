import axios from "axios";

const runtimeApiBaseUrl = window?.__APP_CONFIG__?.VITE_API_BASE_URL;
const API_BASE_URL = runtimeApiBaseUrl || import.meta.env.VITE_API_BASE_URL || "/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  const isAuthRoute = config.url?.startsWith("/auth/");

  if (token && !isAuthRoute) {
    config.headers.Authorization = `Bearer ${token}`;
  } else if (config.headers?.Authorization) {
    delete config.headers.Authorization;
  }

  return config;
});

export default api;
