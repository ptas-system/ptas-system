"""
Normativity service - DS90 and DS609 compliance checking.
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class NormType(str, Enum):
    DS90 = "ds90"
    DS609 = "ds609"


@dataclass
class Violation:
    norm: str
    parameter: str
    value: float
    limit: float
    severity: str
    message: str
    reference: str


class NormativityService:
    """Service to check compliance with Chilean norms DS90 and DS609."""
    
    # DS90 Limits (DS 90/2000 - Norma de Emisión)
    DS90_LIMITS = {
        "ph": {"min": 6.0, "max": 9.0, "unit": "pH", "severity": "critical"},
        "temperature": {"max": 35.0, "unit": "°C", "severity": "critical"},
        "sst": {"max": 80.0, "unit": "mg/L", "severity": "critical"},
        "dbo5": {"max": 60.0, "unit": "mg/L", "severity": "critical"},
        "dqo": {"max": 200.0, "unit": "mg/L", "severity": "warning"},
        "greases": {"max": 100.0, "unit": "mg/L", "severity": "critical"},
        "coliformes_fecales": {"max": 1000.0, "unit": "NMP/100mL", "severity": "critical"},
    }
    
    # DS609 Limits (DS 609/1998 - Agua Potable)
    DS609_LIMITS = {
        "ph": {"min": 6.5, "max": 8.5, "unit": "pH", "severity": "critical"},
        "chlorine_free": {"min": 0.5, "max": 5.0, "unit": "mg/L", "severity": "critical"},
        "turbidity": {"max": 2.0, "unit": "NTU", "severity": "warning"},
        "color": {"max": 20.0, "unit": "UC", "severity": "warning"},
    }
    
    def check_ds90(self, measurement: Dict[str, Any]) -> List[Violation]:
        """Check DS90 compliance for a measurement."""
        violations = []
        
        for param, limits in self.DS90_LIMITS.items():
            value = measurement.get(param)
            if value is None:
                continue
            
            value = float(value)
            
            # Check min
            if "min" in limits and value < limits["min"]:
                violations.append(Violation(
                    norm="DS90",
                    parameter=param,
                    value=value,
                    limit=limits["min"],
                    severity=limits["severity"],
                    message=f"{param} está bajo el límite DS90 ({limits['min']} {limits['unit']})",
                    reference=self._get_ds90_reference(param)
                ))
            
            # Check max
            if "max" in limits and value > limits["max"]:
                violations.append(Violation(
                    norm="DS90",
                    parameter=param,
                    value=value,
                    limit=limits["max"],
                    severity=limits["severity"],
                    message=f"{param} excede el límite DS90 ({limits['max']} {limits['unit']})",
                    reference=self._get_ds90_reference(param)
                ))
        
        return violations
    
    def check_ds609(self, measurement: Dict[str, Any]) -> List[Violation]:
        """Check DS609 compliance for a measurement."""
        violations = []
        
        for param, limits in self.DS609_LIMITS.items():
            value = measurement.get(param)
            if value is None:
                continue
            
            value = float(value)
            
            # Check min
            if "min" in limits and value < limits["min"]:
                violations.append(Violation(
                    norm="DS609",
                    parameter=param,
                    value=value,
                    limit=limits["min"],
                    severity=limits["severity"],
                    message=f"{param} está bajo el límite DS609 ({limits['min']} {limits['unit']})",
                    reference=self._get_ds609_reference(param)
                ))
            
            # Check max
            if "max" in limits and value > limits["max"]:
                violations.append(Violation(
                    norm="DS609",
                    parameter=param,
                    value=value,
                    limit=limits["max"],
                    severity=limits["severity"],
                    message=f"{param} excede el límite DS609 ({limits['max']} {limits['unit']})",
                    reference=self._get_ds609_reference(param)
                ))
        
        return violations
    
    def check_all(self, measurement: Dict[str, Any], ds90_enabled: bool = True, ds609_enabled: bool = True) -> Dict[str, Any]:
        """Check all applicable norms."""
        violations = []
        
        if ds90_enabled:
            violations.extend(self.check_ds90(measurement))
        
        if ds609_enabled:
            violations.extend(self.check_ds609(measurement))
        
        return {
            "compliant": len(violations) == 0,
            "violations": [
                {
                    "norm": v.norm,
                    "parameter": v.parameter,
                    "value": v.value,
                    "limit": v.limit,
                    "severity": v.severity,
                    "message": v.message,
                    "reference": v.reference
                }
                for v in violations
            ]
        }
    
    def _get_ds90_reference(self, param: str) -> str:
        """Get DS90 article reference."""
        refs = {
            "ph": "DS 90, Art. 3.a",
            "temperature": "DS 90, Art. 3.a",
            "sst": "DS 90, Art. 3.a",
            "dbo5": "DS 90, Art. 3.a",
            "dqo": "DS 90, Art. 3.a",
            "greases": "DS 90, Art. 3.a",
            "coliformes_fecales": "DS 90, Art. 3.b",
        }
        return refs.get(param, "DS 90")
    
    def _get_ds609_reference(self, param: str) -> str:
        """Get DS609 article reference."""
        refs = {
            "ph": "DS 609, Art. 5.a",
            "chlorine_free": "DS 609, Art. 5.c",
            "turbidity": "DS 609, Art. 5.b",
            "color": "DS 609, Art. 5.b",
        }
        return refs.get(param, "DS 609")


# Singleton instance
normativity = NormativityService()
