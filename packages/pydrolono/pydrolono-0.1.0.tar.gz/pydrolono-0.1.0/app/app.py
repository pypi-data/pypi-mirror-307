from flask import (
    Flask,
    render_template,
    jsonify,
    request as flask_request
)
from pydrolono.client import NVEHydroAPIClient, ObservationsRequest
from datetime import datetime, timedelta

app = Flask(__name__)
client = NVEHydroAPIClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stations')
def get_stations():
    search_term = flask_request.args.get('term', flask_request.args.get('q', '')).lower()
    
    stations = client.get_stations(active=1)
    if stations and stations.data:
        # Filter stations that have water level or discharge measurements
        station_list = [
            {
                'id': station.stationId,
                'name': station.stationName,
                'latitude': station.latitude,
                'longitude': station.longitude,
                'elevation': station.masl,
                'river': station.riverName or 'Other'
            }
            for station in stations.data
            if station.seriesList and 
            any(param in str(station.seriesList) for param in ['1000', '1001'])
        ]
        
        # Apply search filter if search term is provided
        if search_term:
            station_list = [
                station for station in station_list
                if search_term in station['name'].lower() or
                   search_term in station['id'].lower() or
                   search_term in station['river'].lower()
            ]
            
        return jsonify(station_list)
    return jsonify([])

@app.route('/api/observations')
def get_observations():
    station_id = flask_request.args.get('station')
    date_str = flask_request.args.get('date')
    
    if not station_id or not date_str:
        return jsonify({'error': 'Missing parameters'}), 400
        
    try:
        center_date = datetime.strptime(date_str, '%Y-%m-%d')
        start_date = center_date - timedelta(days=3)
        end_date = center_date + timedelta(days=3)
        reference_time = f"{start_date.isoformat()}/{end_date.isoformat()}"
        
        # Get water level (1000) and discharge (1001) data
        observations = []
        for parameter in ['1000', '1001']:
            request = ObservationsRequest(
                stationId=station_id,
                parameter=parameter,
                resolutionTime='60',
                referenceTime=reference_time
            )
            result = client.get_observations(request)
            if result and result.data:
                observations.extend(result.data)
        
        # Format the response
        formatted_data = {
            'timestamps': [],
            'water_level': [],
            'discharge': []
        }
        
        for obs_data in observations:
            if obs_data.parameter == 1000:  # Water level
                for obs in obs_data.observations:
                    formatted_data['timestamps'].append(obs.time)
                    formatted_data['water_level'].append(obs.value)
            elif obs_data.parameter == 1001:  # Discharge
                for obs in obs_data.observations:
                    if obs.time not in formatted_data['timestamps']:
                        formatted_data['timestamps'].append(obs.time)
                    formatted_data['discharge'].append(obs.value)
                    
        return jsonify(formatted_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
