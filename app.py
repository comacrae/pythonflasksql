"""NAME: Colin MacRae
FSUID: cm19be
DUE DATE: 2/16/21
The program in this file is the indivudal work of Colin MacRae
"""

from flask import Flask, render_template, request
import sqlite3 

app = Flask(__name__) # create instance of Flask object 

@app.route('/saveReview/', methods = ['POST', 'GET'])
def save_review():
    """This function gathers the info submitted to the addReview.html
    form and using the appropriate format executes two insert queries
    for the Ratings and Reviews tables in the reviewData.db
    """
    result = 'msg' # placeholder variable in case of an error in insertion
    if request.method == 'POST': 
        try: # attempt to get necessary info from addReview.html form
            un = request.form['username']
            rest = request.form['restaurant']
            fd = request.form['food']
            serv = request.form['service']
            amb = request.form['ambience']
            pr = request.form['price']
            rate = request.form['overall']
            review = request.form['review']

            with sqlite3.connect("reviewData.db") as db: #open db and get cursor
                cur = db.cursor()

                cur.execute("INSERT into Reviews(username,restaurant,reviewTime, rating,review) values (?,?,CURRENT_DATE,?,?)",(un,rest,rate,review) ) # query to insert review

                cur.execute("INSERT into Ratings(restaurant,food,service,ambience,price,overall) values (?,?,?,?,?,?)" , (rest,fd,serv,amb,pr,rate) ) # query to insert overall rating

                db.commit() #commit changes to database and report success
                result = "Review successfully added"
                return render_template("result.html", msg = result)
        except: # if failure
            db.rollback()  #revert changes
            result = "Unable to add review.\nDetails: save_review()" # report error 
            return render_template("error.html", msg = result)
        finally:
            db.close() # close db in either case

@app.route('/')
@app.route('/index')
def index():
    """Renders the index page containing links to 
    the addReview.html page, showReviews.html page, and
    showReports.html page
    """
    return render_template('index.html')

@app.route('/addReview/')
def add_review():
   """Renders the form to submit a review.""" 
   return render_template('addReview.html')

@app.route('/getReviews/')
def get_reviews():
    """Renders the form to get a list of reviews
    for a specific restaurant
    """
    return render_template('getReviews.html')

@app.route('/showReviews/', methods = ['POST'])
def show_reviews():
    """Attempts to get list of all reviews for a particular restaurant"""
    msg = None
    try:
        restaurant = request.form["restaurant"] # get info from html form
        con = sqlite3.connect("reviewData.db") # connect to database
        con.row_factory = sqlite3.Row # for creation of dictionaries

        cur = con.cursor() # get cursor of database

        query = "SELECT * FROM Reviews WHERE restaurant = \'%s\'"%restaurant
        cur.execute(query) #get all reviews for specific restaurant

        rows = cur.fetchall() # fetch dictionaries
        #return html page with full list
        return render_template('showReviews.html', rows = rows, restaurant = restaurant)
    except: # if failure, report error
        msg = "Unable to get reviews for %s.\nDetails:Failure in show_reviews()"%restaurant
        return render_template('error.html', msg = msg)
    finally: # close db in either case
        con.close()

@app.route('/showReport/')
def show_report():
    """Attempts to query the database in order to gather
    a list of the top ten restaurants with their avg
    ratings for various attributes (food, ambience, etc.)
    and list them in descending order of average overall 
    rating
    """
    msg = None #placeholder for error report msg
    try:
        con = sqlite3.connect("reviewData.db") #connect to db 
        con.row_factory = sqlite3.Row
        cur = con.cursor() # get cursor
        cur.execute("SELECT restaurant, AVG(food),AVG(service), AVG(ambience), AVG(price), AVG(overall) FROM Ratings GROUP BY restaurant ORDER BY AVG(overall) DESC LIMIT 10")
        
        rows = cur.fetchall() # get aforementioned list
        return render_template('showReport.html', rows = rows)
    except: # if failure, report error 
        msg = "Unable to get top ten list.\nDetails: failure in show_report()"
        return render_template('error.html', msg = msg)
    finally: # close db in either case
        con.close()

if __name__ == '__main__': # run app with debug mode
    app.run(debug = True)


