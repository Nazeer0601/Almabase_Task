from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------- USER TABLE ----------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ---------- DOCUMENT TABLE ----------
class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    doc_type = db.Column(db.String(50))  # questionnaire or reference
    user_id = db.Column(db.Integer)

# ---------- ANSWERS TABLE ----------
class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    citation = db.Column(db.Text)
    confidence = db.Column(db.Float)
    user_id = db.Column(db.Integer)