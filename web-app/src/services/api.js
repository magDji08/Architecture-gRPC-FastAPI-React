import axios from "axios";

// Configuration de l'API - Utiliser variable d'environnement
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

console.log(`🌐 API Base URL: ${API_BASE_URL}`);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Intercepteur de requête pour logger
api.interceptors.request.use(
  (config) => {
    console.log(`📤 ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error("❌ Erreur de requête:", error);
    return Promise.reject(error);
  }
);

// Intercepteur de réponse pour gérer les erreurs
api.interceptors.response.use(
  (response) => {
    console.log(`📥 ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.code === "ECONNABORTED") {
      console.error("⏱️ Timeout: Le serveur ne répond pas");
    } else if (error.response) {
      console.error(`❌ Erreur ${error.response.status}:`, error.response.data);
    } else if (error.request) {
      console.error("❌ Aucune réponse du serveur. Vérifiez que le serveur est démarré.");
    } else {
      console.error("❌ Erreur:", error.message);
    }
    return Promise.reject(error);
  }
);

// API Methods
export const getUsers = () => api.get("/users");

export const getUser = (id) => api.get(`/users/${id}`);

export const createUser = (data) => api.post("/users", data);

export const updateUser = (id, data) => api.put(`/users/${id}`, data);

export const deleteUser = (id) => api.delete(`/users/${id}`);

// Health Check & Monitoring
export const getServicesStatus = () => api.get("/services/status");

export const checkGatewayHealth = () => api.get("/health");

export const checkGrpcHealth = () => api.get("/health/grpc");
