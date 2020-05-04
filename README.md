# Project 1

Web Programming with Python and JavaScript

OBJECTIVES:
 =>Become more comfortable with Python.
 =>Gain experience with Flask.
 =>Learn to use SQL to interact with databases.

OVERVIEW:
In this project, I have built a book review website. Users will be able to register for this website and then log in using username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. I have also used the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via website’s API.

DESCRIPTION:

Tables that I have made using models.py followed by create_all() method in create.py are:
users,books and reviews

Import:File called books.csv is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py, a program that will take the books and import them into my PostgreSQL database is written.

Registration: Users can register for my website, providing a username and password. HTML page signup.html provides the view of registration front end view.

Login: Users, once registered, can log in to website with their username and password. HTML page associated with it is index.html.

Logout: Logged in users can log out of the site.

Search: Once a user has logged in, they can search for a book. Users can type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, a list of possible matching results, or some sort of message if there were no matches is displayed. If the user typed in only part of a title, ISBN, or author name, matches for those are displayed as well!

Book Page: When users click on a book from the results of the search page, they are taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on the website.

Review Submission: On the book page, users can submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users cannot submit multiple reviews for the same book.

Goodreads Review Data: On book page, the average rating and number of ratings the work has received from Goodreads are also provided.

API Access: If users make a GET request to website’s /api/<isbn> route, where <isbn> is an ISBN number, JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score is displayed.