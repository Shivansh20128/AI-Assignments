# Here I am importing the dataset 
import pandas as pd
data = pd.read_csv("wine.csv")
data

# This cell involves the preprocessing of the dataset
# For preprocessing, I am normalizing the dataset by using the MinMaxScaler tool library

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

normalize_columns = ['Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']

data[normalize_columns] = scaler.fit_transform(data[normalize_columns])

print(data)


# In this cell, I am making the dataset discrete since it has continious values due to which, if I try to make a bayesian network, 
# it will give with no edges to make a network

columns_to_discretize = ['Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
for col in columns_to_discretize:
    data[col] = pd.cut(data[col], bins=3)
    

# This cell is making the first (A) bayesian network using the prepared dataset which has now been normalized and discretized.
# I am using the method type "hc" (hill climbing) and score type "bic" as mentioned in the bnlearn documentation

import bnlearn as bn
structure = bn.structure_learning.fit(data, methodtype='hc', scoretype='bic')
parameter = bn.parameter_learning.fit(structure, data)

print(structure)

# This is the plot of the graph for the model.
bn.plot(structure)

# This is the plot of the graph of the model after parameter learning
bn.plot(parameter)

# Now I am using the model to make predictions for the class variable

prediction_A = bn.predict(parameter,data,"target")

print(prediction_A)

# In this cell, I will calculate the accuracy for this model by comparing the predicted values and the original values of the 
# target variable from the dataset

from sklearn.metrics import accuracy_score
original_values = data['target']
predicted_values = prediction_A['target']

accuracy_A = accuracy_score(original_values, predicted_values)

print(f'Accuracy value for A: {accuracy_A * 100:.2f}%')

# In this cell I am going to prune the branches one by one and calculate accuracy for all of them
#  Then I will choose the bayesian network having the best accuracy


# For that I have made a loop in which I am iterating through all the features and cheching if the model gets improved when one of the 
# features is removed


numerical_cols_all = ['target','Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
print(len(numerical_cols_all))


accuracy_B=0
pruned_index=0
for i in range (1,len(numerical_cols_all)):
    numerical_cols_new=[]
    for j in range (0,len(numerical_cols_all)):
        if(j!=i):
            numerical_cols_new.append(numerical_cols_all[j])
            
    new_data = data[numerical_cols_new]
    pruned_structure = bn.structure_learning.fit(new_data, methodtype='hc', scoretype='bds')
    pruned_parameter = bn.parameter_learning.fit(pruned_structure, new_data)

    pruned_predict = bn.predict(pruned_parameter,new_data,'target')

    predicted_values_pruned = pruned_predict['target']

    accuracy = accuracy_score(original_values, predicted_values_pruned)
    accuracy_B = max(accuracy_B,accuracy)
    if(accuracy==accuracy_B):
        pruned_index = i
    
    print(f'Accuracy value: {accuracy * 100:.2f}%')


# Here we can now see that we have recieved the best result with the following branch pruned. 
# The best accuracy is also mentioned.

print(accuracy_B)
print("Branch Pruned: ")
print(numerical_cols_all[pruned_index])

# This is another method that can improve our model. Here I am changing the scoring technique and getting a better accuracy than before.
structure_new = bn.structure_learning.fit(data, methodtype='hc', scoretype='bdeu')
parameter_new = bn.parameter_learning.fit(structure_new, data)

bn.plot(structure_new)
bn.plot(parameter_new)

prediction_A_new = bn.predict(parameter_new,data,"target")

original_values = data['target']
predicted_values_new = prediction_A_new['target']

accuracy_new = accuracy_score(original_values, predicted_values_new)

print(f'Accuracy value for new A: {accuracy_new * 100:.2f}%')


# In this cell I am preparing the dataset again in case there have been any changes in our old one.

data = pd.read_csv("wine.csv")

scaler = MinMaxScaler()

normalize_cols = ['Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']

data[normalize_columns] = scaler.fit_transform(data[normalize_columns])
per_column = data.values
columns_to_discretize = ['Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']

for col in columns_to_discretize:
    data[col] = pd.cut(data[col], bins=3)


# In this cell I am using the feature selection method to select a few features.
# In my solution, I am using the selection of feature on the basis of variance. Here, only features having a high variance value will be selected.
#  The threshold value here is 0.03 after trying different values.
#  This value gives us 11 columns. On increasing it, the number of columns will decrease

from sklearn.feature_selection import VarianceThreshold

sel = VarianceThreshold(threshold=(0.03))
feature_selection = sel.fit_transform(per_column)
df = pd.DataFrame(feature_selection, columns = data.columns[sel.get_support()])
print(df.columns)
selected_columns = df.columns


new_df = data[selected_columns]

# Now I am making a basian network with the new chosen features

structure_feature_selection = bn.structure_learning.fit(new_df, methodtype='hc', scoretype='bic')
parameter_feature_selection = bn.parameter_learning.fit(structure_feature_selection, new_df)


bn.plot(parameter_feature_selection)

# Making predictions
feature_selection_prediction = bn.predict(parameter_feature_selection, new_df,'target')

original_values_feature_selection = new_df['target']
predicted_values_feature_selection = feature_selection_prediction['target']

accuracy_C = accuracy_score(original_values_feature_selection, predicted_values_feature_selection)

print(f'Accuracy value with C: {accuracy_C * 100:.2f}%')

#  In this cell we will show the performances of the three bayesian networks in terms of their accuracy

print(f'Accuracy value with A: {accuracy_A * 100:.2f}%')
print(f'Accuracy value with B: {accuracy_B * 100:.2f}%')
print(f'Accuracy value with C: {accuracy_C * 100:.2f}%')

