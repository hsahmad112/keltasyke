from typing import Any, Dict, Optional
import copy

class PreferenceCache:

    def __init__(self):
        self._preferences: Dict[str, Any] = {}

    #set
    def set_preferences(self, prefs):
        self._preferences = prefs if prefs is not None else {}

    #get
    def get_preferences(self):
        return copy.deepcopy(self._preferences)
    
    #update
    def update_preferences(self, key: str, value: Any):
        self._preferences[key] = value


preferences_cache = PreferenceCache()