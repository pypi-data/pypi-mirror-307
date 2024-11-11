import pandas as pd

# test
df = pd.read_csv("dataset_boneage/test/Bone_age_ground_truth.csv")
# print(df.head())

df.rename(columns={'Case ID': 'Image ID', "Sex": "male"}, inplace=True)

df['male'] = df['male'].map({'M': True, 'F': False})

df.to_csv("dataset_boneage/test/test.csv", index=False)

#train
df = pd.read_csv("dataset_boneage/train/train_old.csv")
# print(df.head())

df.rename(columns={'id':'Image ID', "boneage": "Bone Age (months)"}, inplace=True)

cols = ['Image ID', 'male', 'Bone Age (months)']
df = df[cols]

df.to_csv("dataset_boneage/train/train.csv", index=False)

# val
df = pd.read_csv("dataset_boneage/val/Validation Dataset.csv")

#df['male'] = df['male'].map({'TRUE': True, 'FALSE': False})

df.to_csv("dataset_boneage/val/val.csv", index=False)
