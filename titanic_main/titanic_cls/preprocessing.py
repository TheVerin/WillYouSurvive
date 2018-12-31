import pandas as pd
import numpy as np

RawData = pd.read_csv('train.csv')


def sex():
    global RawData

    RawData['Sex'] = RawData['Sex'].map({'male': 1, 'female': 0})
    return RawData


RawData = sex()


def get_title():
    global RawData

    title_dictionary = {'Rev': 'Crew',
                        'Miss': 'Miss',
                        'Dr': 'Crew',
                        'Master': 'Kid',
                        'Don': 'Royality',
                        'Major': 'Crew',
                        'Col': 'Crew',
                        'Capt': 'Crew',
                        'the Countess': 'Royality',
                        'Mme': 'Mrs',
                        'Lady': 'Royality',
                        'Mr': 'Mr',
                        'Jonkheer': 'Royality',
                        'Mlle': 'Miss',
                        'Ms': 'Mrs',
                        'Mrs': 'Mrs',
                        'Sir': 'Royality'}

    RawData['Title'] = RawData['Name'].map(lambda name: name.split(',')[1].split('.')[0].strip())
    RawData['Title'] = RawData.Title.map(title_dictionary)
    return RawData


RawData = get_title()


grouped_train = RawData.iloc[:891].groupby(['Sex', 'Pclass', 'Title'])
grouped_median_train = grouped_train.median()
grouped_median_train = grouped_median_train.reset_index()[['Sex', 'Pclass', 'Title', 'Age']]


def fill_age(row):
    condition = (
            (grouped_median_train['Sex'] == row['Sex']) &
            (grouped_median_train['Title'] == row['Title']) &
            (grouped_median_train['Pclass'] == row['Pclass']))
    return grouped_median_train[condition]['Age'].values[0]


def process_age():
    global RawData
    RawData['Age'] = RawData.apply(lambda row: fill_age(row)
    if np.isnan(row['Age']) else row['Age'], axis=1)
    return RawData


RawData = process_age()


def process_fares():
    global RawData
    RawData.Fare.fillna(RawData.iloc[:].Fare.mean(), inplace=True)
    return RawData


RawData = process_fares()


def process_class():
    global RawData
    pclass_dummies = pd.get_dummies(RawData['Pclass'], prefix='Pclass')
    RawData = pd.concat([RawData, pclass_dummies], axis=1)
    return RawData


RawData = process_class()


def title_dummies():
    global RawData
    title_dummies = pd.get_dummies(RawData['Title'], prefix = 'Title')
    RawData = pd.concat([RawData, title_dummies], axis = 1)
    RawData.drop('Title', axis = 1, inplace = True)
    return RawData


RawData = title_dummies()


def adding_and_removing():
    global RawData

    '''Adding columns'''
    RawData['Family_size'] = RawData['SibSp'] + RawData['Parch'] + 1
    RawData['Single'] = RawData['Family_size'].map(lambda s: 1 if s == 1 else 0)
    RawData['Small'] = RawData['Family_size'].map(lambda s: 1 if 2 <= s <= 4 else 0)
    RawData['Big'] = RawData['Family_size'].map(lambda s: 1 if s >= 5 else 0)

    '''Removing columns'''
    RawData.drop(['PassengerId', 'Cabin', 'Embarked', 'Family_size', 'SibSp', 'Parch', 'Name', 'Ticket'], axis=1, inplace=True)
    return RawData


RawData = adding_and_removing()


def final_data():
    global RawData
    y = RawData.iloc[:, 0]
    x = RawData.iloc[:, 1:]
    return y, x

