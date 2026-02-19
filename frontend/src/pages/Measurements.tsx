import { useEffect, useState } from 'react';
import api from '../services/api';
import { Measurement } from '../types';

const Measurements: React.FC = () => {
  const [measurements, setMeasurements] = useState<Measurement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMeasurements = async () => {
      try {
        const response = await api.get('/measurements?plant_id=1&limit=20');
        setMeasurements(response.data);
      } catch (error) {
        console.error('Error fetching measurements:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMeasurements();
  }, []);

  const phases = ['afluente', 'pretratamiento', 'reactor', 'clarificador', 'desinfeccion', 'lodos'];
  const phaseLabels: Record<string, string> = {
    afluente: 'Afluente',
    pretratamiento: 'Pretratamiento',
    reactor: 'Reactor',
    clarificador: 'Clarificador',
    desinfeccion: 'Desinfección',
    lodos: 'Lodos'
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
        <h1 className="text-2xl font-bold text-gray-800">Mediciones</h1>
        <button className="btn btn-primary">+ Nueva Medición</button>
      </div>

      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Fecha</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Fase</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">pH</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Temp (°C)</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Caudal</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">SST</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {measurements.map((m) => (
                <tr key={m.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm">
                    {new Date(m.timestamp).toLocaleDateString('es-CL')}
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                      {phaseLabels[m.phase] || m.phase}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm">{m.ph?.toFixed(2) || '-'}</td>
                  <td className="px-4 py-3 text-sm">{m.temperature?.toFixed(1) || '-'}</td>
                  <td className="px-4 py-3 text-sm">{m.caudal_effluent_m3h?.toFixed(1) || '-'}</td>
                  <td className="px-4 py-3 text-sm">{m.sst?.toFixed(0) || '-'}</td>
                  <td className="px-4 py-3 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      m.validated === 'validated' ? 'bg-green-100 text-green-700' :
                      m.validated === 'pending' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {m.validated === 'validated' ? 'Validado' : m.validated === 'pending' ? 'Pendiente' : 'Rechazado'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {measurements.length === 0 && (
          <p className="text-center py-8 text-gray-500">No hay mediciones registradas</p>
        )}
      </div>
    </div>
  );
};

export default Measurements;
