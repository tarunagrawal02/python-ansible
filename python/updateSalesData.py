import pandas as pd
import pandas
import csv


infile = pd.read_csv("assignment data.csv")

a = infile['price']/infile['sq__ft']
#print (a)


avg_sq_ft= infile['sq__ft'].mean()

#print (avg)

avg_price= infile['price'].mean()

per_srq_ft = (avg_price)/(avg_sq_ft)

#print(per_srq_ft)

with open("assignment data.csv", "r") as f,open("modified10.csv", "w") as f_out:
          reader = csv.reader(f)
          writer = csv.writer(f_out)
          for row in reader:
              try:
                if int(row[9])/int(row[6]) < per_srq_ft:
                    writer.writerow(row)
              except:
                continue
