import csv
from models import db, Episode, Guest, Appearance
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_database(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        for index, row in enumerate(reader):
            # Check if the episode already exists
            episode = Episode.query.filter_by(number=index + 1).first()
            if not episode:
                episode = Episode(number=index + 1, date=row['Show'])
                db.session.add(episode)
                db.session.commit()  # Commit to ensure the episode is saved

            # Check if the guest already exists
            guest = Guest.query.filter_by(name=row['Raw_Guest_List']).first()
            if not guest:
                guest = Guest(name=row['Raw_Guest_List'], occupation=row['GoogleKnowlege_Occupation'])
                db.session.add(guest)
                db.session.commit()  # Commit to ensure the guest is saved

            # Ensure the episode and guest exist before creating an appearance
            if episode and guest:
                # Create the appearance
                appearance = Appearance(rating=5, episode_id=episode.id, guest_id=guest.id)
                db.session.add(appearance)

        db.session.commit()

# Usage
if __name__ == '__main__':
    with app.app_context():
        seed_database('seed.csv')
        print("Your database has been seeded successfully!")