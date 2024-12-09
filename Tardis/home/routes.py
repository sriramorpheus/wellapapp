from flask import Blueprint, render_template, request, session, jsonify
from . import home_bp

# Define the homepage route
@home_bp.route('/')
def homepage():
    print("Homepage route called")
    return render_template('homepage.html')

@home_bp.route('/toggle-dark-mode', methods=['POST'])
def toggle_dark_mode():
    """
    Handle dark mode toggle.
    Update the session based on the user's choice.
    """
    data = request.get_json()
    session['dark_mode'] = data.get('darkMode', False)
    return jsonify({"status": "success"})
