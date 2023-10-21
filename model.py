import pandas as pd
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from datetime import datetime

class InventoryManagementModel:
    def __init__(self):
        self.product_df = pd.DataFrame()
        self.sales_df = pd.DataFrame()
        self.inventory_df = pd.DataFrame()
        self.model = None
        self.X_test = None
        self.y_test = None

    def generate_data(self):
        self.product_df = pd.read_csv('product_data.csv')
        self.sales_df = pd.read_csv('sales_data.csv')
        self.inventory_df = pd.read_csv('inventory_data.csv')

    def train_model_svm(self):
        inventory_agg = self.inventory_df.groupby(['ProductCode', 'InventoryDate'])['InventoryEnd'].mean().reset_index()
        merged_data = pd.merge(self.product_df['ProductCode'], inventory_agg, on=['ProductCode'])
        X = merged_data[['ProductCode']]
        y = merged_data['InventoryEnd']
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=39)
        self.model = SVR(kernel='linear')
        self.model.fit(X_train, y_train)

    def train_model_linear(self):
        inventory_agg = self.inventory_df.groupby(['ProductCode', 'InventoryDate'])['InventoryEnd'].mean().reset_index()
        merged_data = pd.merge(self.product_df['ProductCode'], inventory_agg, on=['ProductCode'])
        X = merged_data[['ProductCode']]
        y = merged_data['InventoryEnd']
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=39)
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

    def train_model_forest(self):
        inventory_agg = self.inventory_df.groupby(['ProductCode', 'InventoryDate'])['InventoryEnd'].mean().reset_index()
        merged_data = pd.merge(self.product_df['ProductCode'], inventory_agg, on=['ProductCode'])
        X = merged_data[['ProductCode']]
        y = merged_data['InventoryEnd']
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=39)
        self.model = RandomForestRegressor(n_estimators=100, random_state=39)
        self.model.fit(X_train, y_train)

    def evaluate_model(self):
        if self.model is None:
            print("Model has not been trained.")
            return
        y_pred = self.model.predict(self.X_test)
        r_squared = r2_score(self.y_test, y_pred)
        print(f"R-squared (Coefficient of Determination): {r_squared * 100:.2f}%")

    def predict_inventory(self, product_code):
        if self.model is None:
            print("Model has not been trained.")
            return
        input_data = pd.DataFrame({'ProductCode': [product_code]})
        predicted_inventory = self.model.predict(input_data)
        return predicted_inventory


inventory_model = InventoryManagementModel()
inventory_model.generate_data()
inventory_model.train_model_svm()
inventory_model.evaluate_model()
product_code = '1'
predicted_inventory = inventory_model.predict_inventory(product_code)
print(f"SVM  Inventory Prediction for Product {product_code}: {predicted_inventory}")
inventory_model.train_model_linear()
inventory_model.evaluate_model()
predicted_inventory = inventory_model.predict_inventory(product_code)
print(f"Linear Regression Inventory Prediction for Product {product_code}: {predicted_inventory}")
inventory_model.train_model_forest()
inventory_model.evaluate_model()
predicted_inventory = inventory_model.predict_inventory(product_code)
print(f"Random Forest Regression Inventory Prediction for Product {product_code}: {predicted_inventory}")