import random as rd
import os
import pandas as pd

dico = {"1":"liked", "0": "unliked"}

def like(pays):
     return pd.Series([dico[str(int(pays == "France"))]], index=['like'])
        

os.chdir(os.path.basename("Projet"))
dataframe = pd.read_json("../data_project/data2.json")

dataframe = pd.concat([dataframe, dataframe.pays.apply(like)], axis=1, join='inner')
print(dataframe)
dataframe.to_json("../data_project/data4.json")
print("Done !")