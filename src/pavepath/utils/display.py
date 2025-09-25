# pavepath/utils/display.py

from typing import Optional

def mask_key(v: Optional[str]) -> str:
    if not v:
        return "None"
    return (v[:4] + "..." + v[-4:]) if len(v) > 8 else "set"
