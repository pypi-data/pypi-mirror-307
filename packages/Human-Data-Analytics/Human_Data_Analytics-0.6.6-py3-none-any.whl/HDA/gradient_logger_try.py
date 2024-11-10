import tensorflow as tf

class GradientLogger(tf.keras.callbacks.Callback):
    def __init__(self, model, x_train, y_train):
        super(GradientLogger, self).__init__()
        self.model = model
        self.x_train = x_train
        self.y_train = y_train

    def on_train_batch_end(self, batch, logs=None):
        # Get the current batch of data
        inputs, labels = self.x_train[batch], self.y_train[batch]
        
        with tf.GradientTape() as tape:
            # Forward pass
            predictions = self.model(inputs, training=True)
            # Compute the loss
            loss = self.model.compiled_loss(labels, predictions)

        # Compute gradients
        gradients = tape.gradient(loss, self.model.trainable_variables)

        # Print gradients
        for var, grad in zip(self.model.trainable_variables, gradients):
            print(f'Variable: {var.name}, Gradient: {grad}')

# Define your model (example)
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(32,)),
    tf.keras.layers.Dense(10)
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# Sample training data (example)
x_train = tf.random.normal((100, 32))  # 100 samples, 32 features
y_train = tf.random.uniform((100,), maxval=10, dtype=tf.int32)  # 100 samples, 10 classes

# Fit the model and log gradients
model.fit(x_train, y_train, epochs=5, callbacks=[GradientLogger(model, x_train, y_train)])
