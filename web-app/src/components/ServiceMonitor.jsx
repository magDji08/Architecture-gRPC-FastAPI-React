import React, { useState, useEffect } from 'react';
import { getServicesStatus } from '../services/api';
import './ServiceMonitor.css';

function ServiceMonitor() {
  const [services, setServices] = useState([]);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchServicesStatus = async () => {
    try {
      const response = await getServicesStatus();
      setServices(response.data.services);
      setLastUpdate(new Date());
      setIsLoading(false);
    } catch (error) {
      console.error('Erreur lors de la récupération du statut des services:', error);
      // En cas d'erreur, marquer les services comme indisponibles
      setServices([
        {
          name: "API Gateway",
          type: "rest",
          status: "unhealthy",
          port: 8000,
          url: "http://localhost:8000",
          error: "Impossible de contacter le service"
        },
        {
          name: "gRPC Server",
          type: "grpc",
          status: "unhealthy",
          port: 50051,
          url: "localhost:50051",
          error: "Impossible de contacter le service"
        },
        {
          name: "React Frontend",
          type: "web",
          status: "healthy",
          port: 3000,
          url: "http://localhost:3000"
        }
      ]);
      setLastUpdate(new Date());
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Récupération initiale
    fetchServicesStatus();

    // Récupération toutes les 10 secondes
    const interval = setInterval(() => {
      fetchServicesStatus();
    }, 10000);

    // Nettoyage à la destruction du composant
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return '✅';
      case 'unhealthy':
        return '❌';
      case 'unknown':
        return '❓';
      default:
        return '⚪';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return '#10b981';
      case 'unhealthy':
        return '#ef4444';
      case 'unknown':
        return '#f59e0b';
      default:
        return '#6b7280';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'rest':
        return '🌐';
      case 'grpc':
        return '⚡';
      case 'web':
        return '💻';
      default:
        return '📡';
    }
  };

  const formatTime = (date) => {
    if (!date) return 'Jamais';
    return date.toLocaleTimeString('fr-FR');
  };

  const handleRefresh = () => {
    setIsLoading(true);
    fetchServicesStatus();
  };

  const healthyCount = services.filter(s => s.status === 'healthy').length;
  const unhealthyCount = services.filter(s => s.status === 'unhealthy').length;

  return (
    <div className="service-monitor">
      <div className="monitor-header">
        <div className="header-left">
          <h3>📊 Monitoring des Services</h3>
          <span className="update-time">
            Dernière mise à jour: {formatTime(lastUpdate)}
          </span>
        </div>
        <div className="header-right">
          <div className="status-summary">
            <span className="summary-item healthy">
              ✅ {healthyCount} actif{healthyCount > 1 ? 's' : ''}
            </span>
            <span className="summary-item unhealthy">
              ❌ {unhealthyCount} inactif{unhealthyCount > 1 ? 's' : ''}
            </span>
          </div>
          <button onClick={handleRefresh} className="refresh-btn" disabled={isLoading}>
            {isLoading ? '⏳' : '🔄'} Actualiser
          </button>
        </div>
      </div>

      <div className="services-grid">
        {services.map((service, index) => (
          <div 
            key={index} 
            className={`service-card ${service.status}`}
            style={{ '--status-color': getStatusColor(service.status) }}
          >
            <div className="service-header">
              <div className="service-title">
                <span className="type-icon">{getTypeIcon(service.type)}</span>
                <h4>{service.name}</h4>
              </div>
              <span className="status-badge" style={{ backgroundColor: getStatusColor(service.status) }}>
                {getStatusIcon(service.status)} {service.status.toUpperCase()}
              </span>
            </div>

            <div className="service-details">
              <div className="detail-row">
                <span className="label">Type:</span>
                <span className="value">{service.type.toUpperCase()}</span>
              </div>
              <div className="detail-row">
                <span className="label">Port:</span>
                <span className="value">{service.port}</span>
              </div>
              <div className="detail-row">
                <span className="label">URL:</span>
                <span className="value url">{service.url}</span>
              </div>
              {service.users_count !== undefined && (
                <div className="detail-row">
                  <span className="label">Utilisateurs:</span>
                  <span className="value">{service.users_count}</span>
                </div>
              )}
              {service.error && (
                <div className="detail-row error">
                  <span className="label">Erreur:</span>
                  <span className="value">{service.error}</span>
                </div>
              )}
            </div>

            <div className="service-footer">
              <div className="pulse-indicator" style={{ backgroundColor: getStatusColor(service.status) }}></div>
              <span className="timestamp">
                {service.timestamp ? new Date(service.timestamp).toLocaleTimeString('fr-FR') : 'N/A'}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="monitor-info">
        <p>
          ℹ️ Les services sont vérifiés automatiquement toutes les 10 secondes
        </p>
      </div>
    </div>
  );
}

export default ServiceMonitor;
