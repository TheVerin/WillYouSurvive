from django.shortcuts import render
import pandas as pd
from . import ml_model
from titanic_cls.models import Titanic

model = ml_model.classifier()
vector = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
df_vector = pd.DataFrame(vector, index=['first'], columns=['sex', 'age', 'fare',
                                                         'First', 'Second', 'Third',
                                                         'Crew', 'Kid', 'Miss', 'Mr', 'Mrs', 'Royality',
                                                         'Single', 'Small <5', 'Big >5'])


def final(request):
    name = 'You'
    sex = 'Male'
    age = 0
    classs = 'First'
    cost = 0
    title = 'Mr'
    family = 'Single'
    result = 0

    if request.GET.get('name'):
        name = request.GET.get('name')
        sex = request.GET.get('sex')
        age_x = request.GET.get('age')
        age = int(age_x)
        classs = request.GET.get('classs')
        cost_x = request.GET.get('cost')
        cost = int(cost_x)
        title = request.GET.get('title')
        family = request.GET.get('family')

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

    def predict():
        return model.predict(preprocessing())

    result_arr = predict()
    result = result_arr[0]

    obj = Titanic.objects.create(
        title=title,
        name=name,
        sex=sex,
        cls=classs,
        age=age,
        family=family,
        fare=cost,
        result=result
    )
    obj.save()

    return render(
        request,
        'index.html',
        {
            'name': name,
            'sex': sex,
            'age': age,
            'classs': classs,
            'cost': cost,
            'title': title,
            'family': family,
            'result': result
        }

    )
