from typing import Dict, Any, List, Optional 
from datetime import datetime, timezone
import logging
logger = logging.getLogger("uvicorn.error")

class VehicleCache:

    def __init__(self):
        self._vehicles : Dict[str, Dict[str, Any]] = {}
        self._last_updated : datetime = None

    def _parse_int(self, value: Any) -> Optional[int]:
        "safe string/float -> int"
        if value is None or value == "":
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
        
    def _parse_float(self, value: Any) -> Optional[float]:
        """safe string -> float"""
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _parse_str(self, value: Any) -> Optional[str]:
        "safe float/int -> str"
        if value is None or value == "":
            return None
        try:
            return str(value)
        except(ValueError, TypeError):
            return None
        
    def _parse_bool(self, val: Any) -> Optional[bool]:
        "safe parsing of bool, specifically for monitored, vehicleatstop, so none scenarios dont default to actual values"
        return bool(val) if val is not None else None 

    def _clean_onward(self, vehicle_data) -> List[Dict[str, Any]]:
        sanitized_onward = []
        raw_onward = vehicle_data.get("onwardcalls", [])
        if isinstance(raw_onward, list):
                for call in raw_onward:
                    if isinstance(call, dict):
                        call_copy = dict(call)
                        call_copy["stoppointref"] = self._parse_str(call.get("stoppointref"))
                        sanitized_onward.append(call_copy)
        return sanitized_onward


    def _sanitize_vehicles(self, vehicle_id: str, vehicle_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        
        
        sanitized_onward = self._clean_onward(vehicle_data)
        return {
                    "vehicle_id": str(vehicle_id),
                    "vehicleref": str(vehicle_data.get("vehicleref", vehicle_id)),
                    "lineref": self._parse_str(vehicle_data.get("lineref")),
                    "publishedlinename": self._parse_str(vehicle_data.get("publishedlinename")),
                    "directionref": self._parse_str(vehicle_data.get("directionref")), #None for unknown direction, instead of inventing "0" using _parse_str
                    "latitude": self._parse_float(vehicle_data.get("latitude")),
                    "longitude": self._parse_float(vehicle_data.get("longitude")),
                    "percentage": self._parse_float(vehicle_data.get("percentage")),
                    "delaysecs": self._parse_int(vehicle_data.get("delaysecs")),
                    "recordedattime": self._parse_int(vehicle_data.get("recordedattime")),
                    "validuntiltime": self._parse_int(vehicle_data.get("validuntiltime")),
                    "vehicleatstop": self._parse_bool(vehicle_data.get("vehicleatstop")), #None if key is absent thru _parse_bool
                    
                    # Next stop details
                    "next_stoppointref": self._parse_str(vehicle_data.get("next_stoppointref")),
                    "next_stoppointname": self._parse_str(vehicle_data.get("next_stoppointname")),
                    "next_aimedarrivaltime": self._parse_int(vehicle_data.get("next_aimedarrivaltime")),
                    "next_expectedarrivaltime": self._parse_int(vehicle_data.get("next_expectedarrivaltime")),
                    "next_aimeddeparturetime": self._parse_int(vehicle_data.get("next_aimeddeparturetime")),
                    "next_expecteddeparturetime": self._parse_int(vehicle_data.get("next_expecteddeparturetime")),
                    
                    # stop calls
                    "onwardcalls": sanitized_onward,
                    
                    # attributes retained for downstream references
                    "originref": vehicle_data.get("originref"),
                    "destinationref": vehicle_data.get("destinationref"),
                    "destinationname": vehicle_data.get("destinationname"),
                    "monitored": self._parse_bool(vehicle_data.get("monitored")), #same as vehicleatstop
                    "tripref" : vehicle_data.get("__tripref"),
                    "routeref": vehicle_data.get("__routeref"),
                    "directionid": vehicle_data.get("__directionid"),
               

                }


    def update_vehicles(self, raw_vehicles: Dict[str, Dict[str, Any]]) -> None:
        new_store: Dict[str, Dict[str, Any]] = {}

        for vehicle_id, raw_data in raw_vehicles.items():
            if isinstance(raw_data, dict):
                sanitized = self._sanitize_vehicles(vehicle_id, raw_data)
                if sanitized is not None:
                    new_store[vehicle_id] = sanitized
        self._vehicles = new_store
        self._last_updated = datetime.now(timezone.utc)
        logger.info(
            f"Updated cache with {len(self._vehicles)} vehicles "
        )  


    def get_all_vehicles(self) -> List[Dict[str, Any]]:
            return list(self._vehicles.values())


    def get_vehicles_dict(self) -> Dict[str, Dict[str, Any]]:
            return dict(self._vehicles)

    def get_vehicle(self, vehicle_id) -> Optional[Dict[str, Any]]:
        vehicle = self._vehicles.get(str(vehicle_id))
        return dict(vehicle) if vehicle else None

    def get_last_updated(self) -> Optional[datetime]:

        return self._last_updated
        


# Singleton instance shared across poller, websocket, and geofence modules
vehicle_cache = VehicleCache()  