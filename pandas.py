# Data Analysis using pandas
import pandas as pd

# 1. Requirement
print("Requirement \n Find out the top 10 companies that increased in \
marketcap from Mar'22 to Aug'22")

# 2. Data Collection - obtain datsets and convert them to dataframes
df_mar = pd.read_csv('Market_Cap-March-2022.csv')
df_aug = pd.read_csv('Market_Cap-Aug-2022.csv')

# 3. Exploratory Data Analysis
print("\nExploratory Data Analysis(EDA) - March'22 dataset \n")

# 3.1. Observe dataset - Determine the number of rows and columns
print("The dimension of the March-2022 dataframe is",df_mar.shape,"\n")

# 3.2. Understand variables/columns
print("The columns are, \n",df_mar.columns,"\n")
df_mar.dtypes
print("The columns are categorized as follows")
df_mar.info()

# 3.3. Find missing values
df_mar.isna().sum()
print("\nNo missing values found in the dataset\n")

# 3.4. Look at the data distribution
print("The first three rows of the dataset are \n",df_mar.head(3))
print("The last three rows of the dataset are \n",df_mar.tail(3))
pd.set_option('display.float_format',lambda x:'%0.1f'%x)
print("\nBasis Statistics\n", df_mar.describe(include = 'all'))

# 3.5. Identify relationships & Locate outliers

# 3.5.1. Numerical data
df_mar.corr()
df_mar.plot(kind = 'scatter', x = 'Rank', y = 'Marketcap')
df_mar.plot(kind = 'box',x = 'Rank')
print("\n Outliers observed but that is expected \n ")

# 3.5.2. Categorical data
# Company Name
df_mar['Name'].nunique()
df_mar[df_mar['Name'].duplicated() == True]

df_mar.loc[df_mar['Name'] == 'Cheniere Energy',['Rank','Name']]
df_mar.iloc[[517,759],[1,3]]

tup_dp =('Cheniere Energy','Central Bancompany','First Bancorp')
df_mar_dp = df_mar.query("Name in @tup_dp")
print("\n The duplicate names in the Mar'22 dataset are \n", df_mar_dp)

# Countries
ser_c = df_mar.groupby(['Country'])['Name'].count().sort_values(ascending = False)
ser_c.to_excel("Countries.xlsx")
print("\n Refer Countries.xlsx to see the total number of companies\
in each country\n")

# Repeat EDA for the Aug'22 dataset
print("Exploratory Data Analysis(EDA) - Aug'22 dataset \n")
df_aug.info()
df_aug.isna().sum()
df_aug_dp = df_aug[df_aug['Name'].duplicated() == True]
print("\n The duplicate names in the Aug'22 dataset are \n", df_aug_dp)

print("\n The takeaway from the Exploratory Data Analysis are,")
print(" - Two columns are categorized as object data type")
print(" - No missing values found")
print(" - Outliers found but those are expected")
print(" - Duplicate company names found")
print(" - Column labels should be renamed to improve clarity\n")

# 4. Data Wrangling or Data Munging is the translation of raw data
# into a more useful form

# 4.1. Data Cleaning is fixing the anomalies 
# 4.1.1. Categorize columns
df_mar['Name'] = df_mar['Name'].astype('string')
df_mar['Country'] = df_mar['Country'].astype('string')
df_aug['Name'] = df_aug['Name'].astype('string')
df_aug['country'] = df_aug['country'].astype('string')
df_mar.dtypes
df_aug.dtypes

# 4.1.2. Remove duplicates
df_mar = df_mar.drop_duplicates('Name', keep = 'first')
df_aug = df_aug.drop_duplicates('Name', keep = 'first')


# 4.1.3. Rename columns
df_mar.columns = ['rank-mar', 'name', 'marketcap_mar', 'country']
df_aug.columns = ['rank-aug', 'name', 'marketcap_aug', 'country']

# 4.1.4. Replace name
df_aug.replace('Meta Platforms (Facebook)', 'Meta (Facebook)', inplace = True)

# 4.2. Data Merging
df_merge = pd.merge(df_mar,df_aug, how = 'outer', left_on = ['name','country'],
                    right_on = ['name','country'])
df_merge.isna().sum()

df_merge['marketcap_mar'].fillna(df_merge['marketcap_aug'], inplace = True)
df_merge = df_merge.dropna()

# 4.3. Data Manipulation
df_merge['marketcap_delta (M)'] = (df_merge['marketcap_aug']-
                                   df_merge['marketcap_mar'])/1000000
df_merge = df_merge.sort_values('marketcap_delta (M)',ascending = False)
df_merge.set_index('name', inplace = True)
df_merge.drop(['rank-mar','rank-aug','marketcap_mar','marketcap_aug'],axis =1,
              inplace = True)

# 5. Result
df_result = df_merge.drop(df_merge.index[10:], axis = 0)
print("The top 10 companies that increased in marketcap from Mar'22 to Aug'22")
print(df_result)

# 6. Additional useful methods & functions
df_result['country'].where(df_result['country'] == 'United States')

df_result['deltaMC > 25(B)'] = df_result['marketcap_delta (M)'].apply(lambda
                        x: 'Yes' if x > 25000 else 'No')

df_merge.sample(n = 3)

pd.date_range('2022-03', periods = 6, freq ='M')







