import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Getting all transactions for the user
    transactions = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total_value = cash

    # Calculating the current price and total value of each stock
    for transaction in transactions:
        quote = lookup(transaction["symbol"])
        transaction["price"] = usd(quote["price"])
        transaction["total"] = usd(quote["price"] * transaction["total_shares"])
        total_value += quote["price"] * transaction["total_shares"]

    return render_template("index.html", transactions=transactions, cash=usd(cash), total=usd(total_value))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol or not lookup(symbol):
            return apology("Invalid symbol", 400)

        try:
            shares = int(request.form.get("shares"))
            if shares < 1:
                raise ValueError
        except ValueError:
            return apology("Invalid number of shares", 400)

        quote = lookup(symbol)
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        cost = quote["price"] * shares

        if user_cash < cost:
            return apology("Can't afford", 400)

        # Update cash in users table
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)

        # Add transaction to transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol.upper(), shares, quote["price"])

        flash('Bought!')
        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", user_id)

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must symbol")

        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Symbol does not exist")
        return render_template("quoted.html",
                                name = stock["name"],
                                price = stock["price"],
                                symbol = stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Ensure confirmation password was submitted and matches password
        elif not confirmation or password != confirmation:
            return apology("passwords must match", 403)

        # Query database to check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) == 1:
            return apology("username already exists", 403)

        # Hash the password and insert the new user into the database
        hash = generate_password_hash(password)
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        if not new_user_id:
            return apology("registration failed", 403)

        # Log the user in automatically after registering
        session["user_id"] = new_user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        # Retrieve the symbols of stocks the user owns.
        stocks = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)

    else:
        symbol = request.form.get("symbol")
        if not symbol or not lookup(symbol):
            return apology("Invalid symbol", 400)

        try:
            shares = int(request.form.get("shares"))
            if shares < 1:
                raise ValueError
        except ValueError:
            return apology("Invalid number of shares", 400)

        # Validate if the user has enough shares to sell
        rows = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        if rows[0]["total_shares"] < shares:
            return apology("Not enough shares", 400)

        # Get current price of the stock
        quote = lookup(symbol)

        # Calculate the total sale value
        sale_value = quote["price"] * shares

        # Update the user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, session["user_id"])

        # Insert the sell transaction with negative shares to denote a sell
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol.upper(), -shares, quote["price"])

        flash('Sold!')
        return redirect("/")

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Let user add more cash to their account."""
    if request.method == "POST":
        amount = request.form.get("amount")

        # Validate the amount
        try:
            amount = float(amount)
            if amount <= 0:
                return apology("Must provide a positive amount", 400)
        except ValueError:
            return apology("Invalid amount", 400)

        # Update the user's cash amount in the database
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])

        flash("Cash added successfully!")
        return redirect("/")

    else:
        return render_template("add_cash.html")
