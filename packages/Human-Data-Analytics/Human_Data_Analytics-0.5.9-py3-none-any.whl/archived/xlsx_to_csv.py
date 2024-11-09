import os

path = os.path.join("dataset_boneage", "test", "Bone age ground truth.xlsx")
print(path)

import pandas as pd

df = pd.read_excel(path)
print(df.head())

df.to_csv("dataset_boneage/test/Bone_age_ground_truth.csv", index=False)
