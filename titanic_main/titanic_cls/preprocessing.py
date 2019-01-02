import pandas as pd
import numpy as np

RawData = pd.read_csv('train.csv')


def sex():
    global RawData

    RawData['Sex'] = RawData['Sex'].map({'male': 1, 'female': 0})
    return RawData


RawData_sex = sex()


def get_title():
    global RawData_sex

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

    RawData_sex['Title'] = RawData_sex['Name'].map(lambda name: name.split(',')[1].split('.')[0].strip())
    RawData_sex['Title'] = RawData_sex.Title.map(title_dictionary)
    return RawData_sex


RawData_title = get_title()


grouped_train = RawData_title.iloc[:891].groupby(['Sex', 'Pclass', 'Title'])
grouped_median_train = grouped_train.median()
grouped_median_train = grouped_median_train.reset_index()[['Sex', 'Pclass', 'Title', 'Age']]


def fill_age(row):
    condition = (
            (grouped_median_train['Sex'] == row['Sex']) &
            (grouped_median_train['Title'] == row['Title']) &
            (grouped_median_train['Pclass'] == row['Pclass']))
    return grouped_median_train[condition]['Age'].values[0]


def process_age():
    global RawData_title
    RawData_title['Age'] = RawData_title.apply(lambda row: fill_age(row)
    if np.isnan(row['Age']) else row['Age'], axis=1)
    return RawData_title


RawData_age = process_age()


def process_fares():
    global RawData_age
    RawData_age.Fare.fillna(RawData_age.iloc[:].Fare.mean(), inplace=True)
    return RawData_age


RawData_fares = process_fares()


def process_class():
    global RawData_fares
    pclass_dummies = pd.get_dummies(RawData_fares['Pclass'], prefix='Pclass')
    RawData_fares = pd.concat([RawData_fares, pclass_dummies], axis=1)
    return RawData_fares


RawData_class = process_class()


def title_dummies():
    global RawData_class
    title_dummies = pd.get_dummies(RawData_class['Title'], prefix='Title')
    RawData_class = pd.concat([RawData_class, title_dummies], axis=1)
    RawData_class.drop('Title', axis=1, inplace=True)
    return RawData_class


RawData_title = title_dummies()


def adding_and_removing():
    global RawData_title

    '''Adding columns'''
    RawData_title['Family_size'] = RawData_title['SibSp'] + RawData_title['Parch'] + 1
    RawData_title['Single'] = RawData_title['Family_size'].map(lambda s: 1 if s == 1 else 0)
    RawData_title['Small'] = RawData_title['Family_size'].map(lambda s: 1 if 2 <= s <= 4 else 0)
    RawData_title['Big'] = RawData_title['Family_size'].map(lambda s: 1 if s >= 5 else 0)

    '''Removing columns'''
    RawData_title.drop(['PassengerId', 'Cabin', 'Embarked', 'Family_size',
                        'SibSp', 'Parch', 'Name', 'Ticket', 'Pclass'],
                       axis=1, inplace=True)
    return RawData_title


RawData_final = adding_and_removing()


def final_data():
    global RawData_final
    y = RawData_final.iloc[:, 0]
    x = RawData_final.iloc[:, 1:]
    return y, x
