from flask import Blueprint, render_template
from . import home_bp

# Define the homepage route
@home_bp.route('/')
def homepage():
    print("Homepage route called")
    return render_template('homepage.html')
