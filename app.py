from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from summarizer import summarize
from flashcard import card_gen
from quiz import quiz_gen
import json

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)   

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        upload = Todo(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

    # Fetch files from the Todo table
    files = db.session.query(Todo).group_by(Todo.filename, Todo.data).all()
    return render_template("index.html", files=files)


@app.route("/process/<int:file_id>")
def process_file(file_id):
    file_data = Todo.query.get(file_id)
    if file_data is None:
        return "File not found", 404

    formatted_notes, summary = summarize(file_id, file_data.data, file_data.filename)

    return render_template("summarymenu.html", summary=formatted_notes, file_id=file_id)

@app.route("/flashcard/<int:file_id>")
def flashcard(file_id):
    file_data = Todo.query.get(file_id)
    if file_data is None:
        return "File not found", 404

    flashcards_json = card_gen(file_id)
    flashcards = json.loads(flashcards_json)
    

    return render_template("flashcard.html", flashcards=flashcards)

@app.route("/quiz/<int:file_id>", methods=["GET", "POST"])
def quiz(file_id):
    file_id = int(file_id)  
    quiz_json = quiz_gen(file_id)
    print("Quiz JSON:", quiz_json)
    quiz_data = json.loads(quiz_json).get("quiz", [])  # Convert JSON to Python list

    score = None
    results = []

    if request.method == "POST":
        score = 0
        total_questions = len(quiz_data)

        for i, q in enumerate(quiz_data, start=1):
            user_answer = request.form.get(f"answer_{i}", "").strip().lower()
            correct_answer = q["answer"].strip().lower()
            is_correct = user_answer == correct_answer

            if is_correct:
                score += 1

            results.append(
                {
                    "question": q["question"],
                    "your_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                }
            )

        return render_template(
            "quiz.html",
            quiz=quiz_data,
            score=score,
            total=total_questions,
            results=results,
        )

    return render_template(
        "quiz.html", quiz=quiz_data, score=None, total=None, results=None
    )

if __name__ == "__main__":
    app.run(debug=True)