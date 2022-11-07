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

#Create new attribute
adultWithGdp['AgeStatus'] = adultWithGdp.apply(lambda row: "Young" if row.Age < 30 else ("Middle aged" if row.Age >= 30 & row.Age < 60 else "Old"), axis=1)

#jestlize je nekdo middle aged (30-60), pak je sance min 67%, ze bude mit plat mensi rovno nez 50k a zaroven takovych lidi je vice nez 10 000
clm = cleverminer(df=adultWithGdp, proc='4ftMiner',
               quantifiers= {'conf':0.67, 'Base':10000},
               ante ={
                    'attributes':[
                        {'name': 'AgeStatus', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'},
               succ ={
                    'attributes':[
                        {'name': 'income', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'}
               )

# #jestlize je nekdo young, pak je sance min 94%, ze bude mit plat mensi rovno nez 50k a zaroven takovych lidi je vice nez 9000
# clm = cleverminer(df=adultWithGdp, proc='4ftMiner',
#                quantifiers= {'conf':0.94, 'Base':9000},
#                ante ={
#                     'attributes':[
#                         {'name': 'AgeStatus', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'},
#                succ ={
#                     'attributes':[
#                         {'name': 'income', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'}
#                )

# #jestlize je nekdo middle aged (30-60) nebo young, pak je sance min 70%, ze bude mit plat mensi rovno nez 50k a zaroven takovych lidi je vice nez 18 000
# clm = cleverminer(df=adultWithGdp, proc='4ftMiner',
#                quantifiers= {'conf':0.7, 'Base':18000},
#                ante ={
#                     'attributes':[
#                         {'name': 'AgeStatus', 'type': 'subset', 'minlen': 1, 'maxlen': 2}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'},
#                succ ={
#                     'attributes':[
#                         {'name': 'income', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'}
#                )

# #jestlize je nekdo z Mexika, pak je 90% sance, ze tento clovek vydelava mene nez 50k a zaroven techto lidi je minimalne 600
# clm = cleverminer(df=adultWithGdp, proc='4ftMiner',
#                quantifiers= {'conf':0.90, 'Base':600},
#                ante ={
#                     'attributes':[
#                         {'name': 'country', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'},
#                succ ={
#                     'attributes':[
#                         {'name': 'income', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'}
#                )

# # jestlize je nekdo never-married, pak je 95% šance, že vydělává méně než 50k a zároveň je takových lidí více než 10000. Z tabulky zároveň vyplývá, že pokud si osoba v životě
# # již někoho vzala, pak je 33,5% šance, že má plat vyšší než 50k. Zajímavé :))))))))))))))))))))))))))))))))))))
# clm = cleverminer(df=adultWithGdp, proc='4ftMiner',
#                quantifiers= {'conf':0.95, 'Base':10000},
#                ante ={
#                     'attributes':[
#                         {'name': 'marital-status', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'},
#                succ ={
#                     'attributes':[
#                         {'name': 'income', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'}
#               )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)
