from typing import Dict, Any

from datazone.types.state import State

class ContextType:
    state: State
    resources: Dict[str, Any]
