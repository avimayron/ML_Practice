import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns



df = pd.read_csv('data/data.csv')
df = df.fillna(0)
print(df.shape)


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score,mean_squared_error
import statsmodels.api as sm

# Pearson Coefficients for each ind var
print(df.corr(method='pearson')['SUS'].sort_values())


# fig = plt.figure(figsize=(16,9))

# ax1 = fig.add_subplot(121)
# sns.distplot(df.loc[df['Purchase'] == 1]['SUS'], color='c')
# ax1.set_title('Distribution of SUS for Intent Errors')

# ax2 = fig.add_subplot(122)
# sns.distplot(df.loc[df['Purchase'] == 0]['SUS'], color='b')
# ax2.set_title('Distribution of charges for non-smokers')

# plt.show()



# Setting variables
x = df.drop(columns=['Unnamed: 6','SUS']) # dependent vars
y = df["SUS"] # independent vars

    # OLS Regression, and Getting p-values
x2 = x
x2 = sm.add_constant(x2) # add constant to have y-intercept
model = sm.OLS(y, x2).fit() # OLS lr
print(model.summary()); # r square score, p-value's

# Significant indep vars
x2 = x2[["const","Intent_Error", "ASR_Error"]]
print(x.head())

# Print scatter plots of significant independent variables
sns.pairplot(df, x_vars=["Intent_Error", "ASR_Error", "Purchase"], y_vars="SUS", height=7, aspect=0.7)
# plt.show()

# Lines
x_train, x_test, y_train, y_test = train_test_split(x2, y) # train test split of data

lr = LinearRegression().fit(x_train,y_train) # trained linear regression model


y_train_pred = lr.predict(x_train)
y_test_pred = lr.predict(x_test)


print(lr.coef_) # prints lr coeff of each feature
print(lr.intercept_) # prints lr intercept value

print("The R square score of linear regression model is: ", lr.score(x_test,y_test))
print("The Mean squared error of linear regression model is: ", mean_squared_error(y, x['Intent_Error']))

# Scaling data
scale = PolynomialFeatures(degree=2) # 2nd order polynomial regression
scaledX = scale.fit_transform(x)

X_train,X_test,Y_train,Y_test = train_test_split(scaledX,y, random_state = 0)
plr = LinearRegression().fit(X_train,Y_train)

Y_train_pred = plr.predict(X_train)
Y_test_pred = plr.predict(X_test)

print(lr.coef_)

# Evaluation using R^2 -- to what extent are variations explained by model
print("The R square score of linear regression model is: ", plr.score(X_test,Y_test))
# print("The Mean-Squared error of linear regression model is: ", lr.mean_squared_error(y, y_test_pred))