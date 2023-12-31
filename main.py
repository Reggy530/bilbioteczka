from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib

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


my_email = "dawaj.andrzeju@gmail.com"
password = "uzeyejbbivsfpsnr"




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
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="pawello454@gmail.com",
                            msg=f"Subject:O kurdebele! Usunieto ksiazke. :( \n\nO nie!")
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/add",  methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="pawello454@gmail.com",
                                msg=f"Subject:Dodano nowa ksiazke\n\nDodano nowa ksiazke. Sprawdz jaka. :) :) :)")
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
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="pawello454@gmail.com",
                                msg=f"Subject:Edytowano rating\n\nEdytowano rating dla ksiazki :) :) :)")
        newrating = request.form.get("rating")
        book = Book.query.get(id) #ogarnięcie konkretnej książki po jego ID
        book.rating = newrating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", books=books, id=id)

if __name__ == "__main__":
    app.run(debug=True)

