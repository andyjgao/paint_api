import pandas as pd
import math
from colormath.color_diff import delta_e_cie1976
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
# function to calculate the deltaE and finding the closest match to 
# RGB value in dataset

def deltaE(mongoCollection, r1, g1, b1):
    
    # loading mongoDB to pandas dataFrame 
    df = pd.DataFrame(list(mongoCollection.find()))
    
    # initializing return index with base values
    idx = [0, math.inf]
    rgb1 = sRGBColor(r1,g1,b1,is_upscaled=True)
    lab1 = convert_color(rgb1,LabColor)
    # calculating lowest deltaE value
    # formula based off of https://en.wikipedia.org/wiki/Color_difference
    for index, row in df.iterrows():
        r2 = row['R']
        g2 = row['G']
        b2 = row['B']
        rgb2 = sRGBColor(r2,g2,b2,is_upscaled=True)
        lab2 = convert_color(rgb2,LabColor)

        delta_e = delta_e_cie1976(lab1, lab2)
        
        if delta_e < idx[1]:
            idx = [index,delta_e]
        else:
            continue
       
        rgb = [df.iloc[idx[0]]['R'], df.iloc[idx[0]]['G'], df.iloc[idx[0]]['B']]

    #returns rgb value with lowest deltaE in dataset
    return rgb
