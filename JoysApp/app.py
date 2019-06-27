# to do: add in featured reviews

from flask import Flask, render_template

import requests
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
    full_df = pd.read_csv('data/2companyScoresDF.csv', header = 0)
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
    print(rankings)

    #get weighted company scores
    weighted_data = data*rankings
    total_score = np.sum(weighted_data, axis = 1)
    #print(total_score)
    ranked_companies_index = sorted(range(len(total_score)), key=lambda i: total_score[i], reverse=True)
    print(ranked_companies_index)
    #write it out as a loop
    #for i in range(3):
    #    rec_{}.format(i) #something like that =
    company_names =  full_df['company'][ranked_companies_index[0:8]]
    company_logo_paths = full_df['logo_image'][ranked_companies_index[0:8]]
    html_paths = full_df['company_website'][ranked_companies_index[0:8]]
    gd_stars = full_df['GlassdoorOverall'][ranked_companies_index[0:8]]
    ihs_stars = full_df['InHerSight_overall'][ranked_companies_index[0:8]]
    pto_reviews = full_df['pto_review'][ranked_companies_index[0:8]]
    print(pto_reviews)
    return render_template('results.html', company_names = company_names.values, company_logo_paths = company_logo_paths.values, html_paths = html_paths.values, gd_stars = gd_stars.values, ihs_stars = ihs_stars.values, pto_reviews = pto_reviews.values)
    #, linklist = linklist, etc)


##defines a new page
@app.route('/about', methods=['GET','POST'])
def display_about():
    return render_template('about.html')#, linklist = linklist, etc)




if __name__ == '__main__':
    #this runs your app locally
    app.run(host='0.0.0.0', port=5000, debug=True)
