import random as rd
import os
import pandas as pd

dico = {"0":"liked", "1": "unliked"}

def like(_):

    return pd.Series([dico[str(rd.randint(0, 1))]], index=['like'])

os.chdir(os.path.basename("Projet"))
dataframe = pd.read_json("../data_project/data2.json")
print(dataframe)
dataframe = pd.concat([dataframe, dataframe.image.apply(like)], axis=1, join='inner')
print(dataframe)
dataframe.to_json("../data_project/data3.json")
print("Done !")