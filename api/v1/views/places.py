#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Gets the places with their linked city id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Gets plalce by place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(city_id=city_id, **data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all place place objects dep on json"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if not data or (not data.get('states') and not data.get('cities') and not data.get('amenities')):
        places = storage.all(Place).values()
    else:
        places = set()
        if 'states' in data:
            for state_id in data['states']:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.update(city.places)
        if 'cities' in data:
            for city_id in data['cities']:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)
        if not data.get('states') and not data.get('cities'):
            places = storage.all(Place).values()
        if 'amenities' in data:
            amenities_ids = data['amenities']
            filtered_places = []
            for place in places:
                place_amenities_ids = [amenity.id for amenity in place.amenities]
                if all(amenity_id in place_amenities_ids for amenity_id in amenities_ids):
                    filtered_places.append(place)
                places = filtered_places
    return jsonify([place.to_dict() for place in places])
