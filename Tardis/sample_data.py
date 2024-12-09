from app import create_app
from extensions import db
from reading_mode.models import Concept_class, Feature_class
from flashcards.models import Flashcard_class

app = create_app()
app.app_context().push()

# Add Concepts
concepts = [
    Concept_class(name="Fundamentals", description="Overview of WELL Processes and Portfolio."),
    Concept_class(name="Air", description="Air quality requirements."),
    Concept_class(name="Water", description="Water quality requirements."),
    # Add more WELL concepts as needed
]

db.session.add_all(concepts)
db.session.commit()

# Add Features
features = [
    Feature_class(
        concept_id=2,  # Air
        name="Ventilation",
        parts="{'Part 1': 'Minimum Ventilation Rates', 'Part 2': 'Indoor Air Quality'}",
        space="{'Type 1': 'Office', 'Type 2': 'Home'}",
        options="{'Path A': 'Natural Ventilation', 'Path B': 'Mechanical Ventilation'}",
        requirements="Maintain CO2 levels below 800 ppm"
    ),
    Feature_class(
        concept_id=3,  # Water
        name="Water Quality",
        parts="{'Part 1': 'Drinking Water Quality', 'Part 2': 'Water Testing'}",
        space="{'Type 1': 'Public Building'}",
        options="{'Path A': 'Filtration', 'Path B': 'Treatment'}",
        requirements="Meet WHO drinking water guidelines"
    ),
]

db.session.add_all(features)
db.session.commit()

# Add Flashcards
flashcards = [
    Flashcard_class(
        concept_id=2,  # Air
        feature_id=1,  # Ventilation
        question="What is the recommended CO2 level for indoor air quality?",
        answer="CO2 levels should remain below 800 ppm.",
        difficulty="Medium",
        is_favorite=False
    ),
    Flashcard_class(
        concept_id=3,  # Water
        feature_id=2,  # Water Quality
        question="Which standard should drinking water meet?",
        answer="WHO drinking water guidelines.",
        difficulty="Hard",
        is_favorite=False
    ),
]

db.session.add_all(flashcards)
db.session.commit()
