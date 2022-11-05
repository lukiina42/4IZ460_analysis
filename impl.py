import pandas as pd

import sys

from cleverminer import cleverminer

def filter_rows_by_values(df, col, values):
    return df[df[col].isin(values)]

def getUniqueValuesFromColumn(df, col):
    values = df[col].tolist()
    uniqueValues = []
    for i in values:
        if(i not in uniqueValues):
            uniqueValues.append(i)
    return uniqueValues

adult = pd.read_csv ('./data/adult.data', encoding='cp1250', sep=', ')
gdp = pd.read_csv ('./data/gdpStates.txt', encoding='cp1250', sep='\t')

#Drop column which is not needed
gdp.drop('Most Recent Year', inplace=True, axis=1)

uniqueCountryValues = getUniqueValuesFromColumn(adult, "country")

gdp = filter_rows_by_values(gdp, "country", uniqueCountryValues)

#merged tables
adultWithGdp = pd.merge(adult, gdp, on='country', how='outer')

print(adultWithGdp.dtypes)

#Create new attribute
adultWithGdp['AgeStatus'] = adultWithGdp.apply(lambda row: "Young" if row.Age < 30 else ("Middle aged" if row.Age >= 30 & row.Age < 60 else "Old"), axis=1)

print(adultWithGdp)