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

#jestlize je nekdo middle aged (30-60) nebo young, pak je sance min 70%, ze bude mit plat mensi rovno nez 50k a zaroven takovych lidi je vice nez 18 000
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
#                 )

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

# jestlize je nekdo never-married, pak je 95% ??ance, ??e vyd??l??v?? m??n?? ne?? 50k a z??rove?? je takov??ch lid?? v??ce ne?? 10000. Z tabulky z??rove?? vypl??v??, ??e pokud si osoba v ??ivot??
# ji?? n??koho vzala, pak je 33,5% ??ance, ??e m?? plat vy?????? ne?? 50k. Zaj??mav??
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

# print(getUniqueValuesFromColumn(adultWithGdp, "race"))

# Bohuzel je z tohoto tezke cokoliv vycist, protoze ve vypsanem histogramu neni napsano, ktera hodnota se radi ke ktere rase..
# clm = cleverminer(df=adultWithGdp,target='race',proc='CFMiner',
#                quantifiers= {'Base':200, 'RelMax': 0.8},
#                cond ={
#                     'attributes':[
#                         {'name': 'income', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'}
#                )

# # Minim??ln?? 90% lid?? s rasou specifikovanou jako "Other" vyd??l??v?? m??n?? ne?? 50k
# clm = cleverminer(df=adultWithGdp,target='income',proc='CFMiner',
#                quantifiers= {'Base':200, 'RelMax': 0.9},
#                cond ={
#                     'attributes':[
#                         {'name': 'race', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
#                     ], 'minlen':1, 'maxlen':1, 'type':'con'}
#                )

# # Pokud m?? ??lov??k d??t?? a nikdy nebyl v man??elstv??, pak m?? 99% ??anci, ??e vyd??l??v?? m??n?? ne?? 50k za rok a z??rove?? takov??ch lid?? je v datasetu minim??ln?? 4400.
# # V histogramu vid??me: [4451, 34] - pouze 34 takov??ch lid?? z celkov??ch 4485 vyd??l??v?? v??ce ne?? 50k za rok
# clm = cleverminer(df=adultWithGdp,target='income',proc='CFMiner',
#     quantifiers= {'Base':4400, 'RelMax': 0.99},
#     cond ={
#             'attributes':[
#                 {'name': 'marital-status', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
#                 {'name': 'relationship', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
#             ], 'minlen':1, 'maxlen':2, 'type':'con'}
# )

clm = cleverminer(df=adultWithGdp,target='education',proc='CFMiner',
    quantifiers= {'S_Up_ANY': 8, 'Base':10, 'RelMax': 0.10},
    cond ={
        'attributes':[
            {'name': 'income', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
        ], 'minlen':1, 'maxlen':1, 'type':'con'}
)

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)
