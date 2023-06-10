import pandas as pd # for data manipulation 
import matplotlib.pyplot as plot # for visualizing dataSim

#Loading Data into a useable format 

users_df = pd.read_csv('data\\users.txt',sep=':',names=['UserID','BeneficiaryID'])
areas_df = pd.read_csv('data\\areas.csv', names=['BeneficiaryID', 'DistrictID'])
visits_df = pd.read_csv('data\\visits.csv', names=['Date', 'Type', 'BeneficiaryID'])

#print(users_df)
#print(areas_df)
#print (visits_df)

users_df['BeneficiaryID'] = users_df['BeneficiaryID'].apply(lambda x: x.split(',')) #make a list of strings thats has a new element based on each comma

users_df = users_df.explode('BeneficiaryID')#turns each element from the list into it own row 

# Making a final relational database with the use of merge  
df = pd.merge(users_df, areas_df, on='BeneficiaryID')
df = pd.merge(df, visits_df, on='BeneficiaryID')

# Convert Date to datetime so we can run date time functions on them
df['Date'] = pd.to_datetime(df['Date'])

# Count the number of visits for each district
district_counts = df.groupby('DistrictID')['Date'].count()

# Plot the number of visits for each district

"""
district_counts.plot(kind='bar')
plot.title('Number of Visits per District')
plot.xlabel('District')
plot.ylabel('Number of Visits')
plot.show()
"""



lwthreshold = df['DistrictID'].value_counts().quantile(0.25)
midthreshold = df['DistrictID'].value_counts().quantile(0.5)
upthreshold = df['DistrictID'].value_counts().quantile(0.75)

# Plotting the data
plot.figure(figsize=(10,6))
district_counts = df['DistrictID'].value_counts()
district_counts.plot(kind='bar')

# Add horizontal lines for each threshold
plot.axhline(y=lwthreshold, color='r', linestyle='-', label=f'Lower 25% of Visits/Care ({lwthreshold})')
plot.axhline(y=midthreshold, color='orange', linestyle='-', label=f'Middle 50% of Visits/Care ({midthreshold})')
plot.axhline(y=upthreshold, color='g', linestyle='-', label=f'Upper 75% of Visits/Care ({upthreshold})')

plot.title('Number of Visits by District')
plot.xlabel('District ID')
plot.ylabel('Number of Visits')
plot.legend()

plot.show()
