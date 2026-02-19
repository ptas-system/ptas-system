import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { DashboardSummary } from '../types';

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/dashboard/summary?plant_id=1');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching summary:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, []);

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
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <span className="text-gray-500">{summary?.plant?.name || 'Cargando...'}</span>
      </div>

      {/* Alerts Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className={`stat-card ${summary?.alerts?.critical ? 'stat-card-danger' : 'stat-card-success'}`}>
          <p className="text-sm text-gray-500">Alertas Críticas</p>
          <p className="text-3xl font-bold">{summary?.alerts?.critical || 0}</p>
        </div>
        <div className="stat-card stat-card-warning">
          <p className="text-sm text-gray-500">Advertencias</p>
          <p className="text-3xl font-bold">{summary?.alerts?.warning || 0}</p>
        </div>
        <div className="stat-card stat-card-info">
          <p className="text-sm text-gray-500">Equipos Activos</p>
          <p className="text-3xl font-bold">{summary?.equipment?.active || 0}/{summary?.equipment?.total || 0}</p>
        </div>
        <div className="stat-card stat-card-success">
          <p className="text-sm text-gray-500">Cumplimiento</p>
          <p className="text-3xl font-bold">{summary?.compliance?.ds90_compliant ? '✓' : '✗'}</p>
        </div>
      </div>

      {/* Last Measurement */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Última Medición</h2>
        {summary?.last_measurement ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-500">Fecha</p>
              <p className="font-medium">{new Date(summary.last_measurement.timestamp).toLocaleString('es-CL')}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">pH</p>
              <p className="font-medium">{summary.last_measurement.ph?.toFixed(2) || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Caudal (m³/h)</p>
              <p className="font-medium">{summary.last_measurement.caudal_effluent_m3h?.toFixed(1) || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Cloro (mg/L)</p>
              <p className="font-medium">{summary.last_measurement.chlorine_free?.toFixed(2) || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">SST (mg/L)</p>
              <p className="font-medium">{summary.last_measurement.sst?.toFixed(1) || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">DBO5 (mg/L)</p>
              <p className="font-medium">{summary.last_measurement.dbo5?.toFixed(1) || '-'}</p>
            </div>
          </div>
        ) : (
          <p className="text-gray-500">No hay mediciones registradas</p>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/measurements" className="card hover:shadow-md transition-shadow">
          <h3 className="font-semibold text-primary-600">📊 Mediciones</h3>
          <p className="text-sm text-gray-500 mt-1">Registrar y ver mediciones</p>
        </Link>
        <Link to="/equipment" className="card hover:shadow-md transition-shadow">
          <h3 className="font-semibold text-primary-600">⚙️ Equipos</h3>
          <p className="text-sm text-gray-500 mt-1">Gestión de equipos</p>
        </Link>
        <Link to="/alerts" className="card hover:shadow-md transition-shadow">
          <h3 className="font-semibold text-primary-600">🔔 Alertas</h3>
          <p className="text-sm text-gray-500 mt-1">Ver alertas activas</p>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
