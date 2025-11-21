import requests
import datetime
import logging
from .config import Config

logger = logging.getLogger(__name__)


def get_weather():
    if not Config.OPENWEATHER_API_KEY:
        return {"temp": "13.9", "desc": "Sunny", "icon": "Clear"}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={Config.CITY_NAME}&appid={Config.OPENWEATHER_API_KEY}&units=metric"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return {
            "temp": str(round(data["main"]["temp"], 1)),
            "desc": data["weather"][0]["main"],
            "icon": data["weather"][0]["main"],
        }
    except Exception as e:
        logger.error(f"Weather API Error: {e}")
        return {"temp": "--", "desc": "NetErr", "icon": ""}


def get_github_commits():
    if not Config.GITHUB_USERNAME:
        return 0

    url = f"https://api.github.com/users/{Config.GITHUB_USERNAME}/events"
    headers = {}
    if Config.GITHUB_TOKEN:
        headers["Authorization"] = f"token {Config.GITHUB_TOKEN}"

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        events = res.json()

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        count = 0
        for e in events:
            if e.get("type") == "PushEvent" and e.get("created_at", "").startswith(
                today
            ):
                count += e.get("payload", {}).get("size", 1)
        return count
    except Exception as e:
        logger.error(f"GitHub API Error: {e}")
        return 0


def get_vps_info():
    if not Config.VPS_API_KEY:
        return 0
    try:
        url = f"https://api.64clouds.com/v1/getServiceInfo?veid=1550095&api_key={Config.VPS_API_KEY}"
        res = requests.get(url, timeout=10)
        data = res.json()
        if data.get("error") != 0:
            return 0
        return int((data["data_counter"] / data["plan_monthly_data"]) * 100)
    except Exception as e:
        logger.error(f"VPS API Error: {e}")
        return 0


def get_btc_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return res.json().get("bitcoin", {"usd": 0, "usd_24h_change": 0})
    except Exception as e:
        logger.error(f"BTC API Error: {e}")
    return {"usd": "---", "usd_24h_change": 0}


def get_week_progress():
    now = datetime.datetime.now()
    total_hours = 7 * 24
    passed_hours = now.weekday() * 24 + now.hour
    return int((passed_hours / total_hours) * 100)

