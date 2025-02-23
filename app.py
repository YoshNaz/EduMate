from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import BytesIO

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

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        file = request.files["file"]
        upload = Todo(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return render_template('index.html')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)