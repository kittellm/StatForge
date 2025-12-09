import panel as pn
import requests
from statforge.config.settings import get_settings

pn.extension()

settings = get_settings()

def get_api_health():
    try:
        response = requests.get(f"{settings.API_BASE_URL}/health")
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "code": response.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def dashboard():
    health = get_api_health()
    
    return pn.Column(
        "# StatForge Dashboard",
        "## System Status",
        f"API URL: {settings.API_BASE_URL}",
        f"API Health: {health}",
    )

if __name__.startswith("bokeh"):
    dashboard().servable()
elif __name__ == "__main__":
    # For local testing
    dashboard().show()
