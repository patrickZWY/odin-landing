from app import db, app
"""create a database before saving to a database"""
# context needed outside of flask
with app.app_context():
    db.create_all()

print("Database initialized successfully!")
