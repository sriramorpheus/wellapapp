from extensions import db

class Feature_class(db.Model):
    """
    Represents a feature associated with a concept.
    """
    __tablename__ = 'features_table'
    id = db.Column(db.Integer, primary_key=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts_table.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    intent = db.Column(db.Text, nullable=True)
    parts = db.relationship('FeaturePart_class', backref='feature', lazy=True)


class Concept_class(db.Model):
    """
    Represents a concept, which can have multiple features.
    """
    __tablename__ = 'concepts_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    features = db.relationship('Feature_class', backref='concept', lazy=True)

class FeaturePart_class(db.Model):
    """
    Represents individual parts, spaces, options, and requirements for a feature.
    """
    __tablename__ = 'feature_parts_table'
    id = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('features_table.id'), nullable=False)
    part = db.Column(db.String(255))
    space = db.Column(db.String(255))
    option = db.Column(db.String(255))
    requirement = db.Column(db.String(255))