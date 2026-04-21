import json
import os
from langchain.tools import tool

OBD_PATH = os.path.join(os.path.dirname(__file__), "../data/obd_codes.json")


def load_obd_codes():
    with open(OBD_PATH, "r") as f:
        return json.load(f)


@tool
def obd_lookup(code: str) -> str:
    """Look up an OBD-II diagnostic trouble code and return full diagnosis details."""
    codes = load_obd_codes()
    code = code.strip().upper()

    if code in codes:
        entry = codes[code]
        severity_emoji = {
            "Low": "🟡",
            "Medium": "🟠",
            "High": "🔴",
            "Critical": "🚨"
        }.get(entry["severity"], "⚠️")

        pro_note = (
            "⚠️ PROFESSIONAL SERVICE REQUIRED"
            if entry["professional_required"] == "Yes"
            else "✅ Can be DIY with caution"
        )

        return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 OBD Code     : {code}
📋 Description  : {entry['description']}
🔧 System       : {entry['system']}
{severity_emoji} Severity     : {entry['severity']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧩 Possible Causes:
  • {("\n  • ").join(entry['causes'])}

🛠️ Suggested Fix:
  {entry['fix']}

{pro_note}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return (
        f"❌ Code '{code}' not found in database. "
        "Please double-check the code or consult a certified mechanic / official OBD documentation."
    )
