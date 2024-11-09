from image_utils import *
import os
from models.inception import Inceptionv4
from tensorflow.keras.utils import plot_model
import sys
old_stdout = sys.stdout

log_file = open("logs/train.log", "w")

sys.stdout = log_file

# Hyperparameters (a caso per ora)
batch_size = 32

# Load training data
train_path = os.path.join(os.environ.get("DATA_PATH"), "train")
image_train = load_images_from_folder(os.path.join(train_path, "images"), normalize = False, convert_to_tensor= False)
gender_train = load_labels(os.path.join(train_path, "labels.csv"), gender=True)
x_train = [image_train, gender_train]
y_train = load_labels(os.path.join(train_path, "labels.csv"))
train_length = y_train.shape[0]
train_steps = int(np.ceil(train_length/batch_size))

datagen_train = tf.keras.preprocessing.image.ImageDataGenerator(preprocessing_function=lambda x: x/255.,
                             horizontal_flip=True,  # randomly flip images
                             vertical_flip=True)  # randomly flip images

# Load validation data
val_path = os.path.join(os.environ.get("DATA_PATH"), "val")
x_val = load_images_from_folder(os.path.join(val_path, "images"), normalize = False, convert_to_tensor= False)
y_val = load_labels(os.path.join(val_path, "labels.csv"))
val_length = y_val.shape[0]
val_steps = int(np.ceil(val_length/batch_size))

datagen_val = tf.keras.preprocessing.image.ImageDataGenerator(preprocessing_function=lambda x: x/255.)

# define the model
model = Inceptionv4(input_shape = (224, 224, 3), gender_input_shape = (1,))
# model = ResNet18(input_shape = (224, 224, 3))
# model = ResNet18_CBAM(input_shape = (224, 224, 3))
model.summary()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.005)

# Compile the model
model.compile(optimizer=optimizer, loss=tf.keras.losses.MeanAbsoluteError) # not sure if this is the correct loss function

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=6)

print("Training model Inceptionv4 with batch size", batch_size)
model.fit(datagen_train.flow(x_train, y_train, batch_size=batch_size, shuffle=True),
          validation_data=datagen_val.flow(x_val, y_val, batch_size=batch_size, shuffle=False), 
          epochs=100,
          steps_per_epoch=train_steps,
          validation_steps=val_steps,
          callbacks=[callback])

model.save('my_inception_model.h5')
plot_model(model, to_file='models/inception_model.png', show_shapes=True)

sys.stdout = old_stdout

log_file.close()
