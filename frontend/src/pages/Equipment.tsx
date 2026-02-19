import { useEffect, useState } from 'react';
import api from '../services/api';
import { Equipment } from '../types';

const EquipmentPage: React.FC = () => {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEquipment = async () => {
      try {
        const response = await api.get('/equipment?plant_id=1');
        setEquipment(response.data);
      } catch (error) {
        console.error('Error fetching equipment:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchEquipment();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-700';
      case 'maintenance': return 'bg-yellow-100 text-yellow-700';
      case 'broken': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active': return 'Activo';
      case 'maintenance': return 'Mantenimiento';
      case 'broken': return 'Fuera de servicio';
      default: return status;
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
        <h1 className="text-2xl font-bold text-gray-800">Equipos</h1>
        <button className="btn btn-primary">+ Nuevo Equipo</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {equipment.map((eq) => (
          <div key={eq.id} className="card hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-semibold text-lg">{eq.name}</h3>
                <p className="text-sm text-gray-500">{eq.equipment_type}</p>
              </div>
              <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(eq.status)}`}>
                {getStatusLabel(eq.status)}
              </span>
            </div>
            
            <div className="space-y-2 text-sm">
              {eq.code && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Código:</span>
                  <span className="font-medium">{eq.code}</span>
                </div>
              )}
              {eq.brand && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Marca:</span>
                  <span className="font-medium">{eq.brand}</span>
                </div>
              )}
              {eq.power_kw && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Potencia:</span>
                  <span className="font-medium">{eq.power_kw} kW</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {equipment.length === 0 && (
        <div className="card text-center py-12">
          <p className="text-gray-500">No hay equipos registrados</p>
          <button className="btn btn-primary mt-4">Agregar primer equipo</button>
        </div>
      )}
    </div>
  );
};

export default EquipmentPage;
