import pytest
import pandas as pd
from datetime import datetime, timedelta
from pydrolono.client import (
    NVEHydroAPIClient, 
    ObservationsRequest,
    observations_to_dataframe
)
from pydrolono.exceptions import ValidationError, APIError, AuthenticationError

@pytest.fixture
def client():
    """Create a client instance for testing."""
    return NVEHydroAPIClient()

def test_client_initialization():
    """Test client initialization with invalid API key."""
    with pytest.raises(ValueError, match="Invalid API key provided"):
        NVEHydroAPIClient(api_key="invalid_key")
    
    with pytest.raises(ValueError, match="API key must be a string"):
        NVEHydroAPIClient(api_key=123)

def test_get_parameters(client):
    """Test parameters endpoint."""
    result = client.get_parameters()
    assert result is not None
    assert result.itemCount > 0
    assert len(result.data) > 0

def test_get_stations(client):
    """Test stations endpoint."""
    result = client.get_stations(active=1)
    assert result is not None
    assert result.itemCount > 0
    assert len(result.data) > 0

def test_get_observations(client):
    """Test observations endpoint."""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    reference_time = f"{start_time.isoformat()}/{end_time.isoformat()}"
    
    request = ObservationsRequest(
        stationId="12.209.0",
        parameter="1000",
        resolutionTime="60",
        referenceTime=reference_time
    )
    
    result = client.get_observations(request)
    assert result is not None
    assert result.itemCount > 0
    assert len(result.data) > 0

def test_invalid_station(client):
    """Test handling of invalid station ID."""
    request = ObservationsRequest(
        stationId="invalid.station.id",
        parameter="1000",
        resolutionTime="60",
        referenceTime="2024-01-01/2024-01-02"
    )
    
    with pytest.raises(APIError) as exc_info:
        client.get_observations(request)
    assert "API request failed" in str(exc_info.value)

def test_invalid_api_key(monkeypatch):
    """Test handling of invalid API key."""
    with pytest.raises(ValueError, match="No API key provided"):
        # Ensure environment variable is not set
        monkeypatch.delenv("NVE_API_KEY", raising=False)
        NVEHydroAPIClient(api_key=None)

def test_observations_to_dataframe(client):
    """Test conversion of observations to DataFrame."""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    reference_time = f"{start_time.isoformat()}/{end_time.isoformat()}"
    
    request = ObservationsRequest(
        stationId="12.209.0",
        parameter="1000",
        resolutionTime="60",
        referenceTime=reference_time
    )
    
    result = client.get_observations(request)
    df = observations_to_dataframe(result.data)
    
    assert not df.empty
    assert isinstance(df.index, pd.DatetimeIndex)
    assert len(df.columns) > 0

def test_load_api_key_from_env(monkeypatch):
    """Test loading API key from environment variable."""
    monkeypatch.setenv("NVE_API_KEY", "test_key")
    client = NVEHydroAPIClient()
    assert client.headers["X-API-Key"] == "test_key"

def test_get_observations_with_invalid_time(client):
    """Test observations with invalid time format."""
    request = ObservationsRequest(
        stationId="12.209.0",
        parameter="1000",
        resolutionTime="60",
        referenceTime="invalid_time"
    )
    
    with pytest.raises(APIError):
        client.get_observations(request)

def test_invalid_parameter(client):
    """Test handling of invalid parameter."""
    request = ObservationsRequest(
        stationId="12.209.0",
        parameter="invalid",
        resolutionTime="60",
        referenceTime="2024-01-01/2024-01-02"
    )
    
    with pytest.raises(APIError) as exc_info:
        client.get_observations(request)
    assert "API request failed" in str(exc_info.value)
