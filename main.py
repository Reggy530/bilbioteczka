from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)
# import sqlite3
#
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("INSERT INTO books VALUES(2, 'Garry Potter', 'J. K. Rowling', '9.3')")
# db.commit()



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        pass
    books = Book.query.all()

    return render_template("index.html", books=books)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    print(f"Generalnie usuwam {id}")
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/add",  methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        bookname = request.form.get("name")
        bookauthor = request.form.get("author")
        rating = request.form.get("rating")
        with app.app_context():
            db.create_all()
            new_book = Book(title=bookname, author=bookauthor, rating=rating)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    books = Book.query.all()
    if request.method == "POST":
        newrating = request.form.get("rating")
        book = Book.query.get(id) #ogarnięcie konkretnej książki po jego ID
        book.rating = newrating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", books=books, id=id)

if __name__ == "__main__":
    app.run(debug=True)

