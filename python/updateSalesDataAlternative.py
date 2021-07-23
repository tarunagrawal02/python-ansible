import pandas as pd

#import pandas



# Loading the data

df = pd.read_csv('assignment data.csv', 

                        index_col='street',

                        header=0,

                        names=['street', 'city', 'zip', 'state', 'beds', 'baths', 'sq_ft', 'type', 'sale_date', 'price', 'latitude', 'longitude'])



# Remove data where sq_ft is 0, as it will result in error (infinity) as sq_ft is in denominator

df = df[df['sq_ft'] != 0]



# Creating a column based on price and sq_ft

df['per_sqr_ft'] = df['price']/df['sq_ft']



# Filtering the dataframe to include only the rows which are lesser than the mean of per_sqr_ft

df = df[df['per_sqr_ft'] < df['per_sqr_ft'].mean()]



df.to_csv('output.csv')


#        print('yes')







