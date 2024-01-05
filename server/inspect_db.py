from app import db, app, Submission

with app.app_context():
    submissions = Submission.query.all()
    for submission in submissions:
        print(submission.name, submission.email, submission.message, submission.timestamp)