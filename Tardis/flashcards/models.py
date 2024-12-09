from extensions import db

class Flashcard_class(db.Model):
    __tablename__ = 'flashcards_table'
    id = db.Column(db.Integer, primary_key=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts_table.id'), nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey('features_table.id'), nullable=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard', name='difficulty_enum'), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
