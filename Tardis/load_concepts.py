import csv
from extensions import db
from reading_mode.models import Concept_class
from app import create_app  # Import the factory function

# Initialize Flask app
def clear_concepts_table():
    with app.app_context():
        db.session.query(Concept_class).delete()
        db.session.commit()
        print("All existing concepts have been cleared.")

app = create_app()

def load_concepts_from_csv(file_path):
    with app.app_context():  # Use app context for database operations
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Check for existing concept
                    existing_concept = Concept_class.query.filter_by(id=row['id']).first()
                    if existing_concept:
                        print(f"Updating existing concept with ID {row['id']}: {row['name']}")
                        existing_concept.name = row['name']
                        existing_concept.description = row['description']
                    else:
                        print(f"Adding new concept: {row['name']}")
                        concept = Concept_class(
                            id=row['id'],
                            name=row['name'],
                            description=row['description']
                        )
                        db.session.add(concept)
                db.session.commit()
                print("Concepts successfully loaded into the database!")
        except Exception as e:
            print(f"Error loading concepts: {e}")

if __name__ == "__main__":
    load_concepts_from_csv('concepts.csv')  # Replace with the actual path to your CSV file
