import pytest
from PIL import Image
from src.layout import DashboardLayout
from src.config import Config

def test_layout_creation(monkeypatch):
    # Mock Config to ensure consistent data
    monkeypatch.setattr(Config, "CITY_NAME", "TestCity")
    
    layout = DashboardLayout()
    
    # Mock data
    data = {
        "weather": {"temp": "20.0", "desc": "Sunny", "icon": "Clear"},
        "github_commits": 10,
        "vps_usage": 50,
        "btc_price": {"usd": 50000, "usd_24h_change": 5.0},
        "week_progress": 75
    }
    
    # Generate image
    img = layout.create_image(800, 480, data)
    
    assert isinstance(img, Image.Image)
    assert img.size == (800, 480)
    assert img.mode == "1"
