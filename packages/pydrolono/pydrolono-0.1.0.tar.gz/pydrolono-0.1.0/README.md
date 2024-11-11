# Pydrolono

A Python client for accessing hydrological data from the Norwegian Water Resources and Energy Directorate (NVE) Hydrology API.

## Features

- Easy access to NVE's Hydrology API
- Support for retrieving stations, parameters, and observations
- Data conversion to Pandas DataFrames
- Type-safe with dataclass models
- Comprehensive error handling

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Setup

```python
from pydrolono.client import NVEHydroAPIClient

# Initialize client with API key from environment variable NVE_API_KEY
client = NVEHydroAPIClient()
```

### Get Available Parameters

```python
parameters = client.get_parameters()
if parameters:
    print(f"Retrieved {parameters.itemCount} parameters")
```

### Get Active Stations

```python
stations = client.get_stations(active=1)
if stations:
    print(f"Retrieved {stations.itemCount} active stations")
```

### Get Observations

```python
from pydrolono.client import ObservationsRequest

# Get data from the major flooding event in Voss, October 2014
request = ObservationsRequest(
    stationId="62.5.0",    # Bulken station in Vossovassdraget
    parameter="1000",      # Water level
    resolutionTime="60",   # Hourly data
    referenceTime="2014-10-27T00:00:00/2014-10-29T23:59:59"  # October 2014 flood
)

result = client.get_observations(request)
if result and result.data:
    print(f"Station: {result.data[0].stationName}")
    print(f"River: {result.data[0].stationId} - Vossovassdraget")
    print(f"Location: 60.63°N, 6.29°E")
    print(f"Elevation: 51 meters above sea level")
    print(f"Retrieved {result.data[0].observationCount} hourly measurements")
```

### Convert to DataFrame

```python
from pydrolono.client import observations_to_dataframe

if result and result.data:
    df = observations_to_dataframe(result.data)
    print(df.head())
```

## Interactive Demo App

The package includes a Flask web application that demonstrates the usage of pydrolono in a real-world context. The demo app provides:

- Interactive station search with autocomplete
- Station information display
- Time series visualization of water level and discharge data
- Responsive plotting using Plotly.js

To run the demo app:

```bash
# Install Flask if not already installed
pip install flask

# Start the Flask development server
python app/app.py
```

Then open your web browser to http://localhost:5000 to explore Norwegian hydrological data through an interactive interface.

## Authentication

The client requires an API key from NVE. You can provide it in two ways:

1. Set environment variable:
```bash
export NVE_API_KEY='your-api-key'
```

2. Pass directly to client:
```python
client = NVEHydroAPIClient(api_key='your-api-key')
```

## Testing

Run the test script to verify API connectivity and basic functionality:

```bash
python test_api.py
```

## License

This project is licensed under the MIT License.
