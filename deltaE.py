import pandas as pd
import math

# function to calculate the deltaE and finding the closest match to 
# RGB value in dataset

def deltaE(mongoCollection, r1, g1, b1):
    
    # loading mongoDB to pandas dataFrame 
    df = pd.DataFrame(list(mongoCollection.find()))
    
    # initializing return index with base values
    idx = [0, math.inf]
    
    # calculating lowest deltaE value
    # formula based off of https://en.wikipedia.org/wiki/Color_difference
    for index, row in df.iterrows():
        r2 = row['R']
        g2 = row['G']
        b2 = row['B']
        barR = (r1-r2)/2
        deltaR = r1-r2
        deltaG = g1-g2
        deltaB = b1-b2
        deltaC = math.sqrt(2*(deltaR**2)+(4*(deltaG**2)) +
                           (3*(deltaB**2)) + ((barR * (deltaR**2 - deltaB**2))/256))

        if deltaC < idx[1]:
            idx = [index, deltaC]
        else:
            continue
       
        rgb = [df.iloc[idx[0]]['R'], df.iloc[idx[0]]['G'], df.iloc[idx[0]]['B']]

    #returns rgb value with lowest deltaE in dataset
    return rgb
