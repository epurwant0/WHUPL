from flask import Flask
from flask import render_template,request
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import pickle


# Create an app object
app = Flask(__name__)

#Whenever this is called it will activate the function
@app.route('/')
def home(): 
	return render_template('index.html') 
# load the model
filename = 'model.pkl'
clf = pickle.load(open(filename, 'rb'))

def clean_data(df):
    new_df = df.dropna(how='any')
    new_df['formatted_sold_date'] = pd.to_datetime(new_df['sold_date'], format='%Y-%m-%d-%H.%M.%S.%f')
    cc_df = new_df.drop(columns=['sold_date'])
    cc_df['condition_grade'] = cc_df['condition_grade'].replace(
    {'SL': 0, 'RG': 20, 'PR': 10, 'EC':50, 'CL':40, 'C': 40, 'AV':30, 'A': 30})
    # convert to categorical using pd.get_dummies
    cc_df['sold_date_year'] = cc_df['formatted_sold_date'].dt.year
    cc_df['sold_date_month'] = cc_df['formatted_sold_date'].dt.month
    drop_df = cc_df.drop(columns=['formatted_sold_date', 'subseries'])

    # df_dummies = pd.get_dummies(drop_df, columns=['sold_date_year', 'sold_date_month'])

    return drop_df

def prep_features(result):
    vector = np.zeros(292) # Number of features in my dataset, dependent variables

    makez = 'Make_'+ result['Make'] #Make it return the column name e.g Make_BMW
    modelz = 'Model_'+ result['Model']
    fuelz = 'Fuel_' + result['fuel_type']
    gearz = 'Gear_'+ result['gear_type']

    make_index = features_final.columns.get_loc(str(makez)) # Get the index of the column using df.columns.get_loc()
    model_index = features_final.columns.get_loc(str(modelz))
    fuel_index = features_final.columns.get_loc(str(fuelz))
    gear_index = features_final.columns.get_loc(str(gearz))

    vector[0] = result['age'] # Input values into your np.zeros vector
    vector[1] = result['power']
    vector[2] = result['kms']
    vector[make_index]= 1 # this will put a 1 at the right position ( depending on what make is selected)
    vector[model_index]= 1
    vector[fuel_index]= 1
    vector[gear_index]= 1
    return vector


@app.route('/predictprice', methods=['POST','GET']) # this is the actual post request which will take the inputs run the model and hopefully return a prediction
def predict_price():
	print(request.__dict__) # test to check what it is being inputted into request
	if request.method=='POST':
	 	#Storage method for data (requests the web server to accept data)
		cars=request.form
		print(request.form.__dict__)# this form will take the inputs
		age=cars['age']
		power=cars['power']
		kms=cars['kms']
		make=cars['make']
		model=cars['model']
		gear_type=cars['gear_type']
		fuel_type=cars['fuel_type']

		# the function from above will convert this result dict into a vector of 292 values
		result = {'age':age, 'power':power, 'kms':kms,'Make':make, 'Model':model,'gear_type':gear_type,'fuel_type':fuel_type}

		print("hey")
		test = prep_features(result)
		print(test)
		prediction = rand_est.predict([test])
		# calls result.html which displays the output from the random forest
	return render_template('result.html',prediction=prediction) # returns prediction

app.run(debug=True)