import pandas as pd
# Create a dataframe from csv


df = pd.read_csv('/home/Modbus/template.csv', delimiter=',',header=0)

#eg. passing 1 as template, row 0 must be indexed,
def selector(tp):
    tp=int(tp)
    tp-=1
    #Get the row based on template choice
    row = df.iloc[tp]
    # Treat row as a tuple
    my_tuple = tuple(row)
    print("Template tuple")
    print(my_tuple)
    return my_tuple