from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from models import db, Episode, Guest, Appearance
from flask_migrate import Migrate

# Initialize the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration tool
db.init_app(app)
migrate = Migrate(app, db)

#Initialize Flask-RESTful API
api = Api(app)

# GET /  Return welcome message
class HomeResource(Resource):
    def get(self):
        return jsonify({'message': 'Welcome to Lateshow Code Challenge API!'})

# GET /episodes  Return all episodes
class EpisodesResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        return jsonify([{
            "id": episode.id,
            "date": episode.date,
            "number": episode.number
        }for episode in episodes])

# GET /episodes/<int:episode_id>  Return a specific episode and its appearance
class EpisodeDetailResource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if episode:
            return jsonify({
                "id": episode.id,
                "date": episode.date,
                "number": episode.number,
                "appearances":[
                    {
                        "id": appearance.id,
                        "rating": appearance.rating,
                        "episode_id": appearance.episode_id,
                        "guest_id": appearance.guest_id,
                        "guest": {
                            "id": appearance.guest.id,
                            "name": appearance.guest.name,
                            "occupation": appearance.guest.occupation
                        }   
                    } for appearance in episode.appearances
                ]    
            })
        return ({"error": "Episode not found"}), 404
    
    def delete(self, id):
        episode = Episode.query.get(id)
        if episode:
            db.session.delete(episode)
            db.session.commit()
            return {"message": f"Episode {id} deleted successfully"}, 200
        return {"error": "Episode not found"}, 404 

# GET /guests Fetch all guest
class GuestsResource(Resource):
    def get(self):
        guests = Guest.query.all()
        return jsonify([{
            "id": guest.id,
            "name": guest.name,
            "occupation": guest.occupation
        } for guest in guests])
    
# POST /appearances Create a new appearance for an episode and guest
class AppearanceResource(Resource):
    def post(self):
        data = request.get_json()
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        # Validate rating
        if not (1 <= rating <= 5):
            return {"errors": ["Rating must be between 1 and 5"]}, 400

        # Check if episode and guest exist
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)
        if not episode or not guest:
            return {"errors": ["Episode or Guest not found"]}, 404

        # Create and save appearance
        appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
        db.session.add(appearance)
        db.session.commit()

        # Return the created appearance data
        return {
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": appearance.guest_id,
            "episode_id": appearance.episode_id,
            "episode": {
                "id": episode.id,
                "date": episode.date,
                "number": episode.number
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
        }, 201
    
# Register API resource routes
api.add_resource(HomeResource, '/')
api.add_resource(EpisodesResource, '/episodes')
api.add_resource(EpisodeDetailResource, '/episodes/<int:id>')
api.add_resource(GuestsResource, '/guests')
api.add_resource(AppearanceResource, '/appearances')

#Run the application
if __name__ == '__main__':
    app.run(debug=True)
