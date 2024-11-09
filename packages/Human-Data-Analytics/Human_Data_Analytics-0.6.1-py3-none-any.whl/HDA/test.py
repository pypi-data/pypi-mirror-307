import os
from image_utils import *
from tensorflow.keras.models import load_model

# Hyperparameters (a caso per ora)
batch_size = 32
test_steps = 100

# Load test data
test_path = os.path.join(os.environ.get("DATA_PATH"), "test")
x_test = load_images_from_folder(os.path.join(test_path, "images"), normalize = False, convert_to_tensor= False)
y_test = load_labels(os.path.join(test_path, "labels.csv"))
test_length = y_test.shape[0]

datagen_test = tf.keras.preprocessing.image.ImageDataGenerator(preprocessing_function=lambda x: x/255.)

# Load the model
model = load_model('Inceptionv4.h5')

test_values = model.predict(datagen_test.flow(x_test, batch_size=batch_size, shuffle=False), steps=test_steps)[:test_length].squeeze()

mae = np.mean(np.abs(test_values - y_test))
print(f"Mean Absolute Error: {mae}")
