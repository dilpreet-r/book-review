import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker




engine = create_engine("ENTER YOUR DATABASE URL HERE")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f=open("books.csv")
    reader=csv.reader(f)
    for isbn_no,title,author,year in reader:
        db.execute(("INSERT INTO books(isbn_no,title,author,year) VALUES (:isbn_no,:title,:author,:year)"), {"isbn_no": isbn_no, "title": title, "author": author, "year": year})        
        print(f"Added {title} by {author} in {year} having isbn: {isbn_no}")
        
    db.commit()

if __name__ == "__main__":
    main()
