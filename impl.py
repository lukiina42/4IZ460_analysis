import pandas as pd
import sys

from cleverminer import cleverminer

adult = pd.read_csv ('./uvodniZprava/adult.data', encoding='cp1250', sep='\t')
print(adult.head(5))