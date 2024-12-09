from flask import request, flash, redirect, url_for, render_template, send_file
from extensions import db
from reading_mode.models import Concept_class, Feature_class, FeaturePart_class
import pandas as pd
import json
from . import reading_mode_bp
from reading_mode.utils import convert_to_json

# Route: Display Reading Mode Home (Tiles)
@reading_mode_bp.route('/')
def reading_mode_home():
    concepts = Concept_class.query.all()  # Fetch all concepts
    return render_template('reading_mode/home.html', concepts=concepts)


@reading_mode_bp.route('/concept/<int:concept_id>')
def concept_details(concept_id):
    """
    Display details of a specific concept, grouped by features.
    """
    concept = Concept_class.query.get_or_404(concept_id)
    features = Feature_class.query.filter_by(concept_id=concept_id).all()
    
    ''' 
    # Debugging to confirm retrieved data
    print(f"Concept: {concept.name}")
    print(f"Features: {features}")
    '''

    feature_data = []
    for feature in features:
        parts = [
            {
                "part": part.part,
                "space": part.space,
                "option": part.option,
                "requirement": part.requirement,
            }
            for part in feature.parts
        ]
        feature_data.append({"name": feature.name, "intent": feature.intent, "parts": parts})

    grouped_data = {concept.name: feature_data}

    ''' 
    # Debugging to confirm grouped_data structure
    # Debugging output
    print(f"Concept: {concept.name}")
    print(f"Feature Data: {feature_data}")
    '''

    # Pass data to the template
    return render_template('reading_mode/concept_details.html', concept=concept, features=feature_data)


@reading_mode_bp.route('/feature-details/<int:feature_id>')
def feature_details(feature_id):
    feature = Feature_class.query.get_or_404(feature_id)
    return {
        "intent": feature.intent,
        "parts": json.loads(feature.parts),
        "spaces": json.loads(feature.space),
        "options": json.loads(feature.options),
        "requirements": json.loads(feature.requirements),
    }

@reading_mode_bp.route('/grouped-data')
def grouped_data():
    """
    Route to get grouped and formatted data for concepts and features.
    """
    grouped_features = Feature_class.get_grouped_features()
    return render_template('reading_mode/concept_details.html', grouped_data=grouped_data)

# Bulk upload route
@reading_mode_bp.route('/upload', methods=['GET', 'POST'])
def upload_reading_mode_data():
    if request.method == 'POST':
        file = request.files.get('file')
        upload_mode = request.form.get('upload_mode')

        if not file or not file.filename.endswith('.xlsx'):
            flash('Please upload a valid Excel file.', 'error')
            return redirect(url_for('reading_mode.upload_reading_mode_data'))

        try:
            data = pd.read_excel(file)

            # Validate required columns
            required_columns = ['Concept', 'Feature', 'Intent', 'Parts', 'Spaces', 'Options', 'Requirements']
            if not all(col in data.columns for col in required_columns):
                flash('Excel file is missing required columns.', 'error')
                return redirect(url_for('reading_mode.upload_reading_mode_data'))

            if upload_mode == 'erase':
                # Fully erase existing data
                FeaturePart_class.query.delete()
                Feature_class.query.delete()
                Concept_class.query.delete()
                db.session.commit()

            for _, row in data.iterrows():
                # Process concept
                concept = Concept_class.query.filter_by(name=row['Concept']).first()
                if not concept:
                    concept = Concept_class(name=row['Concept'])
                    db.session.add(concept)
                    db.session.flush()

                # Process feature
                feature = Feature_class.query.filter_by(name=row['Feature'], concept_id=concept.id).first()
                if not feature:
                    feature = Feature_class(name=row['Feature'], intent=row['Intent'], concept_id=concept.id)
                    db.session.add(feature)
                    db.session.flush()

                # Process parts
                feature_part = FeaturePart_class(
                    feature_id=feature.id,
                    part=row['Parts'],
                    space=row['Spaces'],
                    option=row['Options'],
                    requirement=row['Requirements']
                )
                db.session.add(feature_part)

            db.session.commit()
            flash('Data uploaded successfully!', 'success')
            return redirect(url_for('reading_mode.reading_mode_home'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error processing file: {e}", 'error')
            return redirect(url_for('reading_mode.upload_reading_mode_data'))

    return render_template('reading_mode/upload.html')

@reading_mode_bp.route('/download-template')
def download_template():
    template_path = 'static/templates/reading_mode_template.xlsx'
    return send_file(template_path, as_attachment=True, download_name='reading_mode_template.xlsx')
