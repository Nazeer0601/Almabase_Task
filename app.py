import os
from flask import Flask, render_template, request, redirect, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db, User, Document
from utils.parser import extract_questions
from utils.chunker import chunk_text
from utils.exporter import export_answers
from rag.retriever import build_index, retrieve
from rag.generator import generate_answer
from pypdf import PdfReader

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "uploads"

db.init_app(app)

with app.app_context():
    db.create_all()

if not os.path.exists("uploads"):
    os.makedirs("uploads")

generated_results = []

# ---------- AUTH ----------

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ---------- UPLOAD QUESTIONNAIRE ----------

@app.route("/upload_questionnaire", methods=["POST"])
def upload_questionnaire():

    file = request.files["file"]

    # check file uploaded
    if not file or file.filename == "":
        return "No file uploaded"

    # allow only PDF
    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed"

    path = os.path.join("uploads", file.filename)
    file.save(path)

    doc = Document(filename=file.filename, doc_type="questionnaire")
    db.session.add(doc)
    db.session.commit()

    return redirect("/dashboard")


# ---------- UPLOAD REFERENCE DOCUMENT ----------

@app.route("/upload_reference", methods=["POST"])
def upload_reference():

    file = request.files["file"]

    if not file or file.filename == "":
        return "No file uploaded"

    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed"

    path = os.path.join("uploads", file.filename)
    file.save(path)

    # safe PDF reading
    try:
        reader = PdfReader(path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if not text.strip():
            return "PDF contains no readable text"

    except Exception:
        return "Invalid or corrupted PDF"

    chunks = chunk_text(text)
    build_index(chunks)

    doc = Document(filename=file.filename, doc_type="reference")
    db.session.add(doc)
    db.session.commit()

    return redirect("/dashboard")


# ---------- GENERATE ANSWERS ----------

@app.route("/generate_ui")
def generate_ui():
    global generated_results

    q_doc = Document.query.filter_by(doc_type="questionnaire").first()

    if not q_doc:
        return "Upload questionnaire first"

    file_path = os.path.join("uploads", q_doc.filename)

    questions = extract_questions(file_path)

    if not questions:
        return "Could not extract questions. Check your PDF."

    generated_results = []

    for q in questions:
        contexts = retrieve(q)
        answer, confidence = generate_answer(q, contexts)

        generated_results.append({
            "question": q,
            "answer": answer,
            "citation": contexts[0] if contexts else "None",
            "confidence": confidence,
            "evidence": contexts
        })

    answered = sum(1 for r in generated_results if "Not found" not in r["answer"])

    coverage = {
        "total": len(generated_results),
        "answered": answered,
        "missing": len(generated_results) - answered
    }

    return render_template("review.html", results=generated_results, coverage=coverage)


# ---------- EXPORT DOCUMENT ----------

@app.route("/export", methods=["POST"])
def export():
    global generated_results

    for i, r in enumerate(generated_results):
        r["answer"] = request.form.get(f"answer{i+1}")

    export_answers(generated_results)
    return send_file("output.docx", as_attachment=True)


# ---------- HOME ----------

@app.route("/")
def home():
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)