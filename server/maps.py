from flask_restx import Namespace, Resource
from flask import request, jsonify
import requests
import os

maps = Namespace('maps', description='Maps Management')

@maps.route('/fetch_places', methods=['POST'])
class FetchPlaces(Resource):
    def post(self):
        data = request.get_json()
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        base_url = data.get('baseUrl')
        radius = data.get('radius')
        type = data.get('type')
        keyword = data.get('keyword')
        location = data.get('location')

        # Append the API key to the URL
        url_with_api_key = f"{base_url}?location={location['lat']},{location['lng']}&radius={radius}&type={type}&keyword={keyword}&key={api_key}"
        payload={}
        headers={}
        # Fetch the JSON data from Google Places API
        response = requests.request("GET", url_with_api_key, headers=headers, data=payload)
        # Check if the request was successful
        if response.ok:
            json_data = response.text
            return (json_data), 200
        else:
            return {'message': 'Failed to fetch places'}, 500
        

@maps.route('/get_api_key', methods=['POST'])
class  Getapikey(Resource):
    def post(self):
        api_key=os.getenv('GOOGLE_MAPS_API_KEY')
        return jsonify({'key': api_key})

