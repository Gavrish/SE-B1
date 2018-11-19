import pandas as pd  
import numpy as np  
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
    

#train = pd.read_csv('/home/nicco/SE-B1/4sale.com/db/input_csv_files/train.csv')
#test = pd.read_csv('/home/nicco/SE-B1/4sale.com/db/input_csv_files/test.csv')

# A class to carry out property price estimation
class price_est:
    # initialize with training data 
	def __init__(self,pred):
		self.train = pd.read_csv('db/input_csv_files/train.csv')
		self.pred = pred	

	# Use RandomForestRegressor to predict price value
	def est(self, pred):
		#y = dataset.iloc[:, 4].values
		
		X_test = []
		X_test.append(pred)
		print(X_test)
		X_train = self.train.iloc[:, 0:6].values  
		y_train = self.train.iloc[:, 6].values 

		#y = dataset.iloc[:, 4].values

		regressor = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
			   max_features='auto', max_leaf_nodes=None,
			   min_impurity_decrease=0.0, min_impurity_split=None,
			   min_samples_leaf=1, min_samples_split=2,
			   min_weight_fraction_leaf=0.0, n_estimators=100,
			   oob_score=False, random_state=0, verbose=0, warm_start=False) 

		regressor.fit(X_train, y_train)  
		y_pred = regressor.predict(X_test) 
		r2 = regressor.score(X_train, y_train)
		return y_pred



