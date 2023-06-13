from sklearn import tree
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import graphviz
import pydotplus
from IPython.display import Image, display
import os

os.chdir(os.path.basename("Projet"))
dataframe = pd.read_json("../data_project/data4.json")

resultframe = dataframe[["like"]]
dataframe = dataframe[["type","pays", "red", "green", "blue"]]
print(dataframe)
print(resultframe)

# generating numerical labels
le1 = LabelEncoder()
dataframe["type"] = le1.fit_transform(dataframe["type"])

le2 = LabelEncoder()
dataframe["pays"] = le2.fit_transform(dataframe["pays"])

le3 = LabelEncoder()
resultframe["like"] = le3.fit_transform(resultframe["like"])

# Use of decision tree classifiers
dtc = tree.DecisionTreeClassifier()
dtc = dtc.fit(dataframe.values, resultframe)

dot_data = tree.export_graphviz(
    dtc,
    out_file=None,
    feature_names=dataframe.columns,
    filled=True,
    rounded=True,
    class_names=le3.inverse_transform(resultframe.like.unique()),
)
graph = graphviz.Source(dot_data)

graph = graphviz.Source(dot_data)
pydot_graph = pydotplus.graph_from_dot_data(dot_data)
img = Image(pydot_graph.create_png())
with open("DecisionTree2.png", 'wb') as png:
    png.write(pydot_graph.create_png())