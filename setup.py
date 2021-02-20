"""NAME: Colin MacRae
FSUID: cm19be
DUE DATE: 2/16/21
The program in this file is the indivudal work of Colin MacRae
"""
from flask import Flask
import sqlite3

conn = sqlite3.connect('reviewData.db') # connect to db

print("Opened database successfully") # print success msg to terminal

reviews = """CREATE TABLE Reviews( 
                        username CHAR(40), 
                        restaurant CHAR(50),
                        reviewTime DATE, 
                        rating FLOAT, 
                        review CHAR(500))""" #query for creating Reviews table

conn.execute(reviews) 

ratings = """CREATE TABLE  Ratings(
                            restaurant CHAR(50), 
                            food FLOAT, 
                            service FLOAT, 
                            ambience FLOAT, 
                            price FLOAT, 
                            overall FLOAT)""" # query for creating Ratings table
conn.execute(ratings)

print('table created successfully') #print message to terminal to report success

conn.close() # close db

