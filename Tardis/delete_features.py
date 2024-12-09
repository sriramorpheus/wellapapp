from extensions import db
from reading_mode.models import Feature_class
from app import create_app

# Initialize the app context
app = create_app()

def delete_all_features():
    with app.app_context():
        try:
            # Delete all records from the features_table
            db.session.query(Feature_class).delete()
            db.session.commit()
            print("All records in features_table have been deleted.")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting records: {e}")

if __name__ == "__main__":
    delete_all_features()
