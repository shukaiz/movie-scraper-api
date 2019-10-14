#!flask/bin/python
# coding=utf-8
import pandas as pd
from flask import Flask, jsonify, abort, make_response, request
from graph import *


app = Flask(__name__)


@app.route('/actors', methods=['GET'])
def get_actors_filter():
    """
    Get actors in JSON format with filter.
    Example: /actors?attr={attr_value}
    Filters out all actors that don’t have {attr_value} in attr.
    """
    if 'name' in request.args:
        name_id = request.args['name']
        return df_actor[df_actor['name'] != name_id].to_json(orient='records')
    elif 'age' in request.args:
        age_id = request.args['age']
        return df_actor[df_actor['age'] != int(age_id)].to_json(orient='records')
    elif 'total_gross' in request.args:
        total_gross_id = request.args['total_gross']
        return df_actor[df_actor['total_gross'] != int(total_gross_id)].to_json(orient='records')
    elif 'num_movies' in request.args:
        num_movies_id = request.args['num_movies']
        return df_actor[df_actor['num_movies'] != int(num_movies_id)].to_json(orient='records')
    else:
        abort(400)


@app.route('/movies', methods=['GET'])
def get_movies_filter():
    """
    Get movies in JSON format with filter.
    Example: /movies?attr={attr_value}
    Filters out all movies that don’t have {attr_value} in attr.
    """
    if 'name' in request.args:
        name_id = request.args['name']
        return df_movie[df_movie['name'] != name_id].to_json(orient='records')
    elif 'year' in request.args:
        year_id = request.args['year']
        return df_movie[df_movie['year'] != int(year_id)].to_json(orient='records')
    elif 'box_office' in request.args:
        box_office_id = request.args['box_office']
        return df_movie[df_movie['box_office'] != int(box_office_id)].to_json(orient='records')
    elif 'num_actors' in request.args:
        num_actors_id = request.args['num_actors']
        return df_movie[df_movie['num_actors'] != int(num_actors_id)].to_json(orient='records')
    else:
        abort(400)


@app.route('/actors/<path:actor_id>', methods=['GET'])
def get_actors(actor_id):
    """Returns the first Actor object that has name “Bruce Willis”, displays actor attributes and metadata"""
    return df_actor[df_actor['name'] == actor_id].to_json(orient='records')


@app.route('/movies/<path:movie_id>', methods=['GET'])
def get_movies(movie_id):
    """Returns the first Movie object that has correct name, displays movie attributes and metadata"""
    return df_movie[df_movie['name'] == movie_id].to_json(orient='records')


@app.route('/actors', methods=['POST'])
def create_actor():  # Leverage POST requests to ADD content to backend
    if not request.json or 'name' not in request.json:
        abort(400)
    graph.df_actor = df_actor.append([request.json['name'], 0, 0, 0])
    return jsonify({'name': request.json['name']}), 201


@app.route('/movies', methods=['POST'])
def create_movie():  # Leverage POST requests to ADD content to backend
    if not request.json or 'name' not in request.json:
        abort(400)
    graph.df_movie = df_movie.append([request.json['name'], 0, 0, 0])
    return jsonify({'name': request.json['name']}), 201


@app.route('/actors/<path:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):  # Leverage DELETE requests to REMOVE content from backend
    if len(actor_id) == 0:
        abort(404)
    graph.df_actor = df_actor[df_actor['name'] != actor_id]
    return jsonify({'result': True})


@app.route('/movies/<path:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):  # Leverage DELETE requests to REMOVE content from backend
    if len(movie_id) == 0:
        abort(404)
    graph.df_movie = df_movie[df_movie['name'] != movie_id]
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):  # Handles not found request if user inputs an URL that's not recognized.
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
