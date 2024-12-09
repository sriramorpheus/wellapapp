from flask import Blueprint, render_template, request, jsonify, url_for, flash, redirect
from extensions import db
import pandas as pd
from . import flashcards_bp
from flashcards.models import Flashcard_class

# Route: Display All Flashcards with Filters
@flashcards_bp.route('/')
def flashcards_home():
    concept_filter = request.args.get('concept')
    difficulty_filter = request.args.get('difficulty')

    query = Flashcard_class.query
    if concept_filter:
        query = query.filter_by(concept_id=concept_filter)
    if difficulty_filter:
        query = query.filter_by(difficulty=difficulty_filter)

    flashcards = query.all()
    return render_template('flashcards/home.html', flashcards=flashcards)


#favorite Flashcards Route
@flashcards_bp.route('/favorites')
def favorites():
    # Query all favorite flashcards
    favorite_flashcards = Flashcard_class.query.filter_by(is_favorite=True).all()
    return render_template('flashcards/favorites.html', flashcards=favorite_flashcards)


# Route: Add a New Flashcard
@flashcards_bp.route('/add', methods=['GET', 'POST'])
def add_flashcard():
    if request.method == 'POST':
        concept_id = request.form['concept_id']
        feature_id = request.form.get('feature_id')  # Optional
        question = request.form['question']
        answer = request.form['answer']
        difficulty = request.form['difficulty']

        new_flashcard = Flashcard_class(
            concept_id=concept_id,
            feature_id=feature_id,
            question=question,
            answer=answer,
            difficulty=difficulty
        )
        db.session.add(new_flashcard)
        db.session.commit()
        flash('Flashcard added successfully!', 'success')
        return redirect(url_for('flashcards.flashcards_home'))

    return render_template('flashcards/add_flashcard.html')

# Route: Edit a Flashcard
@flashcards_bp.route('/edit/<int:flashcard_id>', methods=['GET', 'POST'])
def edit_flashcard(flashcard_id):
    flashcard = Flashcard_class.query.get_or_404(flashcard_id)

    if request.method == 'POST':
        flashcard.question = request.form['question']
        flashcard.answer = request.form['answer']
        flashcard.difficulty = request.form['difficulty']
        db.session.commit()
        flash('Flashcard updated successfully!', 'success')
        return redirect(url_for('flashcards.flashcards_home'))

    return render_template('flashcards/edit_flashcard.html', flashcard=flashcard)

# Route: Delete a Flashcard
@flashcards_bp.route('/delete/<int:flashcard_id>', methods=['POST'])
def delete_flashcard(flashcard_id):
    flashcard = Flashcard_class.query.get_or_404(flashcard_id)
    db.session.delete(flashcard)
    db.session.commit()
    flash('Flashcard deleted successfully!', 'success')
    return redirect(url_for('flashcards.flashcards_home'))

# Route: Toggle favorite
@flashcards_bp.route('/toggle_favorite/<int:flashcard_id>', methods=['POST'])
def toggle_favorite(flashcard_id):
    flashcard = Flashcard_class.query.get_or_404(flashcard_id)
    flashcard.is_favorite = not flashcard.is_favorite
    db.session.commit()
    return jsonify({'status': 'success', 'is_favorite': flashcard.is_favorite})



#Flashcard Bulk Upload Route
flashcards_bp = Blueprint('flashcards', __name__)

@flashcards_bp.route('/upload', methods=['POST'])
def upload_flashcards():
    file = request.files['file']
    data = pd.read_excel(file)

    for _, row in data.iterrows():
        flashcard = Flashcard_class(
            concept_id=row['Concept ID'],
            feature_id=row['Feature ID'],
            question=row['Question'],
            answer=row['Answer'],
            difficulty=row['Difficulty'],
            is_favorite=False
        )
        db.session.add(flashcard)

    db.session.commit()
    return jsonify({"message": "Flashcards uploaded successfully"})

