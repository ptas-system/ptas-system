import { useEffect, useState } from 'react';
import api from '../services/api';
import { Alert } from '../types';

const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await api.get('/alerts?plant_id=1&limit=20');
        setAlerts(response.data);
      } catch (error) {
        console.error('Error fetching alerts:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAlerts();
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-700 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-700 border-orange-200';
      case 'warning': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      default: return 'bg-blue-100 text-blue-700 border-blue-200';
    }
  };

  const handleResolve = async (alertId: number) => {
    try {
      await api.put(`/alerts/${alertId}/resolve`, { resolution_notes: 'Resuelto' });
      setAlerts(alerts.map(a => a.id === alertId ? { ...a, is_resolved: 'true' } : a));
    } catch (error) {
      console.error('Error resolving alert:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Alertas</h1>
      </div>

      <div className="space-y-4">
        {alerts.map((alert) => (
          <div key={alert.id} className={`card border-l-4 ${alert.severity === 'critical' ? 'border-l-red-500' : alert.severity === 'warning' ? 'border-l-yellow-500' : 'border-l-blue-500'}`}>
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`px-2 py-1 rounded-full text-xs ${getSeverityColor(alert.severity)}`}>
                    {alert.severity.toUpperCase()}
                  </span>
                  {alert.ds90_violation && (
                    <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs">DS90</span>
                  )}
                  {alert.ds609_violation && (
                    <span className="px-2 py-1 bg-orange-100 text-orange-700 rounded-full text-xs">DS609</span>
                  )}
                  {alert.is_resolved === 'true' && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs">Resuelto</span>
                  )}
                </div>
                <h3 className="font-semibold text-lg">{alert.title}</h3>
                <p className="text-gray-600 mt-1">{alert.message}</p>
                <p className="text-sm text-gray-400 mt-2">
                  {new Date(alert.created_at).toLocaleString('es-CL')}
                </p>
              </div>
              {alert.is_resolved !== 'true' && (
                <button
                  onClick={() => handleResolve(alert.id)}
                  className="btn btn-secondary text-sm"
                >
                  Resolver
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {alerts.length === 0 && (
        <div className="card text-center py-12">
          <p className="text-gray-500">No hay alertas</p>
        </div>
      )}
    </div>
  );
};

export default Alerts;
