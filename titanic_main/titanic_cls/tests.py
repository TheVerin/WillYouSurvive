from django.test import TestCase
from titanic_cls.ml_model import *
import pandas as pd



vector = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
df_vector = pd.DataFrame(vector, index=['first'], columns=['sex', 'age', 'fare',
                                                         'First', 'Second', 'Third',
                                                         'Crew', 'Kid', 'Miss', 'Mr', 'Mrs', 'Royality',
                                                         'Single', 'Small <5', 'Big >5'])

pred = classifier()



name = 'You'
sex = 'Male'
age = 78
classs = 'First'
cost = 35
title = 'Mr'
family = 'Single'



def preprocessing():
    for i in df_vector.columns.values:
        if i == 'sex':
            df_vector['sex'] = sex
            df_vector['sex'] = df_vector['sex'].map({'Male': 1, 'Female': 0})
        elif i == 'cost':
            df_vector.set_value('first', i, cost)
        elif i == 'age':
            df_vector.set_value('first', i, age)
        elif i == classs:
            df_vector.set_value('first', i, 1)
        elif i == title:
            df_vector.set_value('first', i, 1)
        elif i == family:
            df_vector.set_value('first', i, 1)
    return df_vector


print(preprocessing())


def predict():
    return pred.predict(preprocessing())


result_arr = predict()
result = result_arr[0]

print(result)