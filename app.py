import os
import requests
from flask import Flask, session,render_template,request,redirect,g,url_for,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key=os.urandom(24)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
 #   raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
DATABASE_URL="ENTER YOUR DATABASE URL HERE"
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/",methods=['GET','POST'])
def index():
    if request.method=="GET":
        if session.get("user"):
            return render_template('search.html',user=session["user"])
        return render_template("index.html")
    else:
        session.pop('user',None)
        uname=request.form.get("username")
        pword=request.form.get("password")
        data=db.execute("select * from users where username=:username and password=:password",{"username":uname,"password":pword}).fetchall()
        if not data:
            return render_template("index.html",msg="Incorrect Username or Password or both")
        else:
            print(data)
            session["user"]=data[0][0]




@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        uname=request.form.get("username")
        pword=request.form.get("password")
        data=db.execute("SELECT * FROM users WHERE username=:username",{"username":uname}).fetchall()
        if not data:
            db.execute("INSERT INTO users(username,password) VALUES(:username,:password)",{"username":uname,"password":pword})
            db.commit()
            return render_template("index.html")
        else:
            return render_template("signup.html",msg="Username already taken")

@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="POST":
        if g.user:
            title=request.form.get("title")
            author=request.form.get("author")
            isbn_no=request.form.get("isbn_no")
            data=[]
            

            if title:
                ti=db.execute("SELECT * FROM books WHERE title LIKE :title",{"title":"%"+title+"%"}).fetchall()
                data.append(ti)
            if author:
                au=db.execute("SELECT * FROM books WHERE author LIKE :author",{"author":"%"+author+"%"}).fetchall()
                data.append(au)
            if isbn_no:
                isbn=db.execute("SELECT * FROM books WHERE isbn_no LIKE :isbn_no",{"isbn_no":"%"+isbn_no+"%"}).fetchall()
                data.append(isbn)
            if not data:
                return render_template("search.html",msg="Enter value in any column!")
            if not data[0]:
                return render_template("search.html",msg="No record found!")
            else:
                info=db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = 'books'").fetchall()
                return render_template("search.html",user=session['user'],dat=data,inf=info)
    return redirect(url_for('index'))

@app.route('/book/<int:bid>',methods=["GET","POST"])
def book(bid):
    if g.user:
        
        book_details=db.execute("SELECT * FROM books WHERE id=:id",{"id":bid}).fetchone()
        book_review=db.execute("SELECT review,username FROM users JOIN reviews ON reviews.user_id=users.id WHERE book_id=:id",{"id":bid}).fetchall()
        
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "OyCWQEsISMPuzo69fcnjg", "isbns": book_details[1]})
        if res.status_code==200:
            receive=res.json()
            ar=receive["books"][0]["average_rating"]
            rc=receive["books"][0]["work_ratings_count"]
        if request.method=="GET":   
            if not book_review:
                return render_template("book.html",book_det=book_details,msg="No Review Found",ar=ar,rc=rc)
            return render_template("book.html",book_det=book_details,book_review=book_review,ar=ar,rc=rc)
        else:

            rating=request.form.get('rating')
            review=request.form.get('review')
            userid=session["user"]
            check=db.execute("SELECT * FROM reviews WHERE user_id=:userid and book_id=:bid",{"userid":userid,"bid":bid}).fetchall()
            if check:
                return render_template("book.html",book_det=book_details,msg="Review Already Submitted",book_review=book_review,ar=ar,rc=rc)
            else:
                db.execute("INSERT INTO reviews(user_id,book_id,rating,review) VALUES(:userid,:bid,:rating,:review)",{"userid":userid,"bid":bid,"rating":rating,"review":review})
                db.commit()

            return render_template("book.html",book_det=book_details,book_review=book_review,ar=ar,rc=rc)

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user'] 

@app.route('/dropsession')
def dropsession():
   session.pop('user',None)
   return render_template("index.html")


@app.route('/api/<isbn>')
def api(isbn):
    isb=db.execute("SELECT * FROM books WHERE isbn_no= :isbn",{"isbn":isbn}).fetchone()
    if isb is None:
        return jsonify({"error":"Invalid ISBN"}), 404
        
    
    else:

        bookid=db.execute("SELECT id FROM books WHERE isbn_no=:isbn",{"isbn":isbn}).fetchone()
        val=db.execute("SELECT avg(rating) FROM reviews WHERE book_id=:bid",{"bid":bookid[0]}).fetchone()
        review=db.execute("SELECT count(review) FROM reviews WHERE book_id=:bid",{"bid":bookid[0]}).fetchone()
        return jsonify({
                "title":isb[2],
                "author":isb[3],
                "year":isb[4],
                "isbn":isb[1],
                "review_count":review[0],
                "average_score":val[0]
                })
if __name__ == '__main__':
    app.run()