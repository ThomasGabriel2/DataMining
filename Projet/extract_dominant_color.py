from PIL import Image
import numpy
from sklearn.cluster import KMeans
import pandas as pd
import os
import math

os.chdir(os.path.basename("Projet"))
dataframe = pd.read_json("../data_project/data.json")
print(dataframe)

def extract_color(image_path):
    try:
        imgfile = Image.open("../images_project/" + image_path)
        numarray = numpy.array(imgfile.getdata(), numpy.uint8)
        clusters = KMeans(n_clusters=4, n_init='auto')
        clusters.fit(numarray)
        dominant_color = clusters.cluster_centers_[0]
        vectorize_ceil = numpy.vectorize(math.ceil)
        dominant_color = vectorize_ceil(dominant_color[0:3])
        res = pd.Series(dominant_color, index=['red', 'green', 'blue'])
    except:
        res = pd.Series([0, 0, 0], index=['red', 'green', 'blue'])
    return res

dataframe = pd.concat([dataframe, dataframe.image.apply(extract_color)], axis=1, join='inner')
print(dataframe)
dataframe.to_json("../data_project/data2.json")
print("Done !")