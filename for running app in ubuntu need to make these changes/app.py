# to do: add in featured reviews
import os

from flask import Flask, request, render_template

import pandas as pd
import numpy as np


#from sqlalchemy import create_engine
#from sqlalchemy_utils import database_exists, create_database
#import psycopg2
#from yelp_functions import *

#pd.options.display.max_columns=25
#Initialize app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


##defines a new page
@app.route('/results', methods=['GET','POST'])
def display_results():
    #print(request.form.get("items"))
    #if request.method == "GET":
    full_df = pd.read_csv("/home/ubuntu/JoysApp/data/2companyScoresDf.csv")
    #just getting the scores
    #update this since replaceing flexible hours w working remotely
    data = full_df[['Mentorship_predicted',
           'Management Opportunities_predicted',
           'Maternity Leave_predicted',
           'Learning Opportunities_predicted',
           'Salary Satisfaction_predicted',
          'Paid Time Off_predicted',
           'Flexible Hours_predicted']]

    categories = ['Mentorship Opportunities', 'Management Opportunities',
              'Maternity Leave', 'Learning Opportunities',
              'Salary Satisfaction', 'Paid Time Off', 'Flexible Hours']

    user_rankings = request.args.get('items')
    user_rankings = user_rankings.split(",")
    if user_rankings[0] == "":
        user_rankings = ['Management Opportunities', 'Mentorship Opportunities', 'Learning Opportunities', 'Maternity Leave', 'Salary Satisfaction', 'Paid Time Off', 'Flexible Hours']
    #print(user_rankings)
    rankings_dict = {key: i for i, key in enumerate(user_rankings)}
    #reverse score so that top ranked is more points
    rank1 = (7 - rankings_dict['Mentorship Opportunities'])/28
    rank2 = (7 - rankings_dict['Management Opportunities'])/28
    rank3 = (7 - rankings_dict['Maternity Leave'])/28
    rank4 = (7 - rankings_dict['Learning Opportunities'])/28
    rank5 = (7 - rankings_dict['Salary Satisfaction'])/28
    rank6 = (7 - rankings_dict['Paid Time Off'])/28
    rank7 = (7 - rankings_dict['Flexible Hours'])/28
    rankings = [rank1, rank2, rank3, rank4, rank5, rank6, rank7]

    #get weighted company scores
    weighted_data = data*rankings
    total_score = np.sum(weighted_data, axis = 1)
    #print(total_score)
    ranked_companies_index = sorted(range(len(total_score)), key=lambda i: total_score[i], reverse=True)
    #write it out as a loop
    #for i in range(3):
    #    rec_{}.format(i) #something like that =
    company_names =  full_df['company'][ranked_companies_index[0:8]]
    company_logo_paths = full_df['logo_image'][ranked_companies_index[0:8]]
    html_paths = full_df['company_website'][ranked_companies_index[0:8]]
    gd_stars = full_df['GlassdoorOverall'][ranked_companies_index[0:8]]
    ihs_stars = full_df['InHerSight_overall'][ranked_companies_index[0:8]]
    first_reviews = full_df['pto_review'][ranked_companies_index[0:6]]
    second_reviews = full_df['ml_review'][ranked_companies_index[0:6]]

    return render_template('results.html', company_names = company_names.values, company_logo_paths = company_logo_paths.values, html_paths = html_paths.values, gd_stars = gd_stars.values, ihs_stars = ihs_stars.values, first_reviews = first_reviews.values, second_reviews = second_reviews.values)


##defines a new page
@app.route('/about', methods=['GET','POST'])
def display_about():
    return render_template('about.html')
