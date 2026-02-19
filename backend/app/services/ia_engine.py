"""
IA Engine - Basic anomaly detection and recommendations.
Uses statistical methods (IQR, Z-score) for detection.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
from scipy import stats


@dataclass
class Anomaly:
    parameter: str
    value: float
    expected_range: tuple
    severity: str
    message: str
    method: str


class IAEngine:
    """Basic AI engine for PTAS anomaly detection."""
    
    def __init__(self):
        self.z_score_threshold = 3.0
        self.iqr_multiplier = 1.5
    
    def detect_anomalies(self, measurements: List[Dict[str, Any]], parameters: List[str]) -> List[Anomaly]:
        """Detect anomalies in measurements using multiple methods."""
        anomalies = []
        
        if len(measurements) < 10:
            return anomalies
        
        for param in parameters:
            values = [m.get(param) for m in measurements if m.get(param) is not None]
            
            if len(values) < 10:
                continue
            
            try:
                # Method 1: Z-score
                z_anomalies = self._detect_zscore(values, param)
                anomalies.extend(z_anomalies)
                
                # Method 2: IQR
                iqr_anomalies = self._detect_iqr(values, param)
                anomalies.extend(iqr_anomalies)
                
            except Exception:
                continue
        
        return anomalies
    
    def _detect_zscore(self, values: List[float], param: str) -> List[Anomaly]:
        """Detect anomalies using Z-score method."""
        anomalies = []
        
        values_array = np.array(values)
        mean = np.mean(values_array)
        std = np.std(values_array)
        
        if std == 0:
            return anomalies
        
        z_scores = np.abs((values_array - mean) / std)
        
        for i, z in enumerate(z_scores):
            if z > self.z_score_threshold:
                severity = "critical" if z > self.z_score_threshold * 1.5 else "warning"
                anomalies.append(Anomaly(
                    parameter=param,
                    value=values[i],
                    expected_range=(mean - 2 * std, mean + 2 * std),
                    severity=severity,
                    message=f"{param} presenta desviación estadísticamente significativa (z={z:.2f})",
                    method="z-score"
                ))
        
        return anomalies
    
    def _detect_iqr(self, values: List[float], param: str) -> List[Anomaly]:
        """Detect anomalies using IQR method."""
        anomalies = []
        
        values_array = np.array(values)
        q1 = np.percentile(values_array, 25)
        q3 = np.percentile(values_array, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - self.iqr_multiplier * iqr
        upper_bound = q3 + self.iqr_multiplier * iqr
        
        for value in values_array:
            if value < lower_bound or value > upper_bound:
                severity = "critical" if abs(value - np.median(values_array)) > 3 * iqr else "warning"
                anomalies.append(Anomaly(
                    parameter=param,
                    value=float(value),
                    expected_range=(float(lower_bound), float(upper_bound)),
                    severity=severity,
                    message=f"{param} está fuera del rango esperado (IQR)",
                    method="iqr"
                ))
        
        return anomalies
    
    def analyze_trend(self, values: List[float], window: int = 5) -> Dict[str, Any]:
        """Analyze trend direction using moving average."""
        if len(values) < window:
            return {"trend": "insufficient_data"}
        
        values_array = np.array(values)
        
        # Calculate moving average
        ma = np.convolve(values_array, np.ones(window) / window, mode='valid')
        
        # Simple linear trend
        if len(ma) >= 2:
            slope = (ma[-1] - ma[0]) / len(ma)
            
            if abs(slope) < 0.01:
                trend = "stable"
            elif slope > 0:
                trend = "increasing"
            else:
                trend = "decreasing"
            
            return {
                "trend": trend,
                "slope": float(slope),
                "last_value": float(values[-1]),
                "avg_value": float(np.mean(values))
            }
        
        return {"trend": "insufficient_data"}
    
    def generate_recommendations(self, anomalies: List[Anomaly], measurement: Dict[str, Any]) -> List[str]:
        """Generate operational recommendations based on anomalies."""
        recommendations = []
        
        for anomaly in anomalies:
            param = anomaly.parameter
            value = anomaly.value
            
            if param == "ph":
                if value < 6.0:
                    recommendations.append("⚠️ pH bajo: Verificar ingreso de aguas ácidas. Considerar neutralización con cal.")
                elif value > 9.0:
                    recommendations.append("⚠️ pH alto: Verificar vertidos alcalinos. Ajustar dosificación de químicos.")
            
            elif param == "sst":
                if value > 80:
                    recommendations.append("⚠️ SST elevado: Revisar funcionamiento del sedimentador. Posible sobrecarga.")
            
            elif param == "dbo5":
                if value > 60:
                    recommendations.append("⚠️ DBO5 alto: Posible sobrecarga orgánica. Verificar caudal y carga contaminantes.")
            
            elif param == "od":
                if value < 2.0:
                    recommendations.append("⚠️ OD bajo: Aumentar aireación. Revisar sopladores y difusores.")
                elif value > 6.0:
                    recommendations.append("ℹ️ OD alto: Considerar reducir aireación para ahorro energético.")
            
            elif param == "chlorine_free":
                if value < 0.5:
                    recommendations.append("⚠️ Cloro bajo: Aumentar dosificación de hipoclorito.")
                elif value > 2.0:
                    recommendations.append("⚠️ Cloro alto: Reducir dosificación para evitar subproductos.")
            
            elif param == "temperature":
                if value > 30:
                    recommendations.append("🌡️ Temperatura alta: Monitorear actividad biológica. Posible reducción de eficiencia.")
        
        if not recommendations:
            recommendations.append("✅ Sistema operando dentro de parámetros normales.")
        
        return recommendations
    
    def predict_maintenance(self, equipment_hours: List[Dict[str, Any]], max_hours: int = 10000) -> Dict[str, Any]:
        """Predict maintenance needs based on operating hours."""
        if not equipment_hours:
            return {"status": "no_data"}
        
        total_hours = sum(h.get("hours_run", 0) for h in equipment_hours)
        hours_remaining = max_hours - total_hours
        
        if hours_remaining < 0:
            return {
                "status": "overdue",
                "message": f"Mantenimiento overdue. Excedido por {abs(hours_remaining)} horas.",
                "priority": "critical"
            }
        elif hours_remaining < 500:
            return {
                "status": "imminent",
                "message": f"Mantenimiento recomendado en {hours_remaining} horas.",
                "priority": "high"
            }
        elif hours_remaining < 2000:
            return {
                "status": "upcoming",
                "message": f"Próximo mantenimiento en {hours_remaining} horas.",
                "priority": "medium"
            }
        else:
            return {
                "status": "ok",
                "message": f"Equipo en buen estado. {hours_remaining} horas restantes.",
                "priority": "low"
            }


# Singleton instance
ia_engine = IAEngine()
