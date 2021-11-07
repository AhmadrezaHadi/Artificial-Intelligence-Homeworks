import pandas as pd
import numpy as np

def read_from_excel():
    df = pd.read_excel("ProvinceCenterDistances.xlsx")
    adj_matrix = np.zeros((31,31))
    for i in range(1,32):
        adj_matrix[:,i-1] = df[f"Unnamed: {i}"].to_numpy()[4:]
    return adj_matrix