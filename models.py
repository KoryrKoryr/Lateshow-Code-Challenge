# Import necessary modules
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


#Episode model
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False, unique=True)

    # Relationship with appearances
    appearances = db.relationship('Appearance', backref='episode', cascade="all, delete-orphan")
    
    # Serialization rules to avoid recursion
    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.id} - {self.number}>'

#Guest model
class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    # Relationship with appearances
    appearances = db.relationship('Appearance', backref='guest', cascade="all, delete-orphan")
    
    # Serialization rules to avoid recursion
    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.id} - {self.name}>'

#Appearance model
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    # Serialization rules to include related episode and guest
    serialize_rules = ('-episode.appearances', '-guest.appearances')

    # Validation for rating (must be between 1 and 5)
    @db.validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return value
    
    def __repr__(self):
        return f'<Appearance {self.id} - Rating: {self.rating}>'
