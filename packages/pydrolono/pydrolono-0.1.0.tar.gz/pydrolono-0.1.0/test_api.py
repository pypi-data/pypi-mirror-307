import os
from pydrolono.client import NVEHydroAPIClient, ObservationsRequest, observations_to_dataframe
from datetime import datetime, timedelta
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def test_api_connection():
    """Test basic API connectivity and parameter listing"""
    client = NVEHydroAPIClient()
    
    print("\n=== Testing Parameters Endpoint ===")
    parameters = client.get_parameters()
    if parameters:
        print(f"Successfully retrieved {parameters.itemCount} parameters")
        print("\nCommon measurement parameters:")
        common_params = [
            (0, "Nedbør"),
            (1000, "Vannstand"),
            (1001, "Vannføring"),
            (1003, "Vanntemperatur")
        ]
        for param_id, name in common_params:
            param = next((p for p in parameters.data if p.parameter == param_id), None)
            if param:
                print(f"- {param.parameter}: {param.parameterName} ({param.unit})")
            else:
                print(f"- {param_id}: Not found")
    else:
        print("Failed to retrieve parameters")

def test_stations():
    """Test station listing"""
    client = NVEHydroAPIClient()
    
    print("\n=== Testing Stations Endpoint ===")
    stations = client.get_stations(active=1)
    if stations:
        print(f"Successfully retrieved {stations.itemCount} active stations")
        print("\nFirst 5 stations:")
        for station in stations.data[:5]:
            print(f"- {station.stationId}: {station.stationName} ({station.latitude}, {station.longitude})")
    else:
        print("Failed to retrieve stations")

def test_observations():
    """Test observations retrieval for multiple stations and parameters"""
    client = NVEHydroAPIClient()
    
    # Example: Get last 24 hours of data
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    reference_time = f"{start_time.isoformat()}/{end_time.isoformat()}"
    
    # Test cases with station and desired parameters
    station_id = "12.209.0"  # Urula station
    parameters_to_test = [
        ("1000", "Vannstand"),
        ("1001", "Vannføring"),
        ("1003", "Vanntemperatur")
    ]
    
    print(f"\n=== Testing Observations Endpoint ===")
    print(f"Time range: {reference_time}")
    print(f"Testing station: {station_id}\n")
    
    # First get station details to check available parameters
    stations = client.get_stations(active=1)
    if not stations:
        print("Failed to retrieve station information")
        return
        
    station = next((s for s in stations.data if s.stationId == station_id), None)
    if not station:
        print(f"Station {station_id} not found")
        return
        
    # Get available series for the station
    series_list = station.seriesList
    if not series_list:
        print(f"No series information available for station {station_id}")
        return
        
    # Parse series list - extract parameter IDs from the series list
    if isinstance(series_list, str):
        available_parameters = set(series_list.split(','))
    elif isinstance(series_list, list):
        available_parameters = set(str(series.get('parameter')) for series in series_list)
    else:
        print(f"Unexpected series_list type: {type(series_list)}")
        return
    
    for parameter, param_name in parameters_to_test:
        if parameter not in available_parameters:
            print(f"\nSkipping {param_name} (parameter {parameter}) - not available at this station")
            continue
            
        print(f"\nTesting {param_name} (parameter {parameter})")
        
        request = ObservationsRequest(
            stationId=station_id,
            parameter=parameter,
            resolutionTime="60",  # hourly data
            referenceTime=reference_time
        )
        
        result = client.get_observations(request)
        if result and result.data:
            print(f"✓ Successfully retrieved {result.data[0].observationCount} observations")
            
            # Convert to DataFrame for better visualization
            df = observations_to_dataframe(result.data)
            if not df.empty:
                print("\nLatest measurements:")
                print(df.tail(3))
                
                # Basic statistics
                stats = df.describe()
                print("\nSummary statistics:")
                print(f"Mean: {stats.iloc[1].iloc[0]:.2f}")
                print(f"Min:  {stats.iloc[3].iloc[0]:.2f}")
                print(f"Max:  {stats.iloc[7].iloc[0]:.2f}")
            print("\n" + "-"*50 + "\n")
        else:
            print(f"✗ Failed to retrieve observations\n")

if __name__ == "__main__":
    test_api_connection()
    test_stations()
    test_observations()
