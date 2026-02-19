// TypeScript interfaces for PTAS Frontend

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  role: 'administrador' | 'supervisor' | 'operador';
  plant_id: number | null;
  is_active: boolean;
  created_at: string;
}

export interface Plant {
  id: number;
  name: string;
  code: string;
  address?: string;
  region?: string;
  capacity_m3d?: number;
  population_equiv?: number;
  treatment_type?: string;
  status: string;
  ds90_enabled: boolean;
  ds609_enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface Measurement {
  id: number;
  plant_id: number;
  user_id: number;
  timestamp: string;
  phase: string;
  caudal_affluent_m3h?: number;
  caudal_effluent_m3h?: number;
  ph?: number;
  temperature?: number;
  conductivity?: number;
  turbidity?: number;
  od?: number;
  chlorine_free?: number;
  sst?: number;
  dbo5?: number;
  dqo?: number;
  level_sludge_m?: number;
  notes?: string;
  validated: string;
  validated_by?: number;
  validated_at?: string;
  created_at: string;
}

export interface Equipment {
  id: number;
  plant_id: number;
  name: string;
  code?: string;
  equipment_type: string;
  brand?: string;
  model?: string;
  serial_number?: string;
  power_kw?: number;
  status: string;
  install_date?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Alert {
  id: number;
  plant_id: number;
  measurement_id?: number;
  equipment_id?: number;
  alert_type: string;
  severity: string;
  title: string;
  message: string;
  ds90_violation: boolean;
  ds609_violation: boolean;
  norm_reference?: string;
  is_resolved: string;
  resolved_by?: number;
  resolved_at?: string;
  resolution_notes?: string;
  created_at: string;
}

export interface DashboardSummary {
  plant: { id: number; name: string; code: string };
  last_measurement: {
    timestamp: string;
    phase: string;
    caudal_effluent_m3h?: number;
    ph?: number;
    temperature?: number;
    chlorine_free?: number;
    sst?: number;
    dbo5?: number;
  } | null;
  compliance: {
    ds90_compliant: boolean;
    ds609_compliant: boolean;
    last_violation: string | null;
  };
  alerts: {
    active: number;
    critical: number;
    warning: number;
  };
  equipment: {
    total: number;
    active: number;
    maintenance: number;
    broken: number;
  };
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  user: User;
}

export interface AlertStats {
  total: number;
  active: number;
  resolved: number;
  critical: number;
  warning: number;
  ds90_violations: number;
  ds609_violations: number;
}
