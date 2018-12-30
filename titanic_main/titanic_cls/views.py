from django.shortcuts import render
import pandas as pd

RawData = pd.read_csv('train.csv')
print(RawData.head(5))