from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, Add, ReLU, Concatenate
from tensorflow.keras.layers import BatchNormalization
from tf.keras.losses import MeanAbsoluteError
# Residual Block
def residual_block(X, filters, kernel_size=3, stride=1, conv_shortcut=True):
    """A residual block with or without a convolutional shortcut."""
    shortcut = X
    
    if conv_shortcut:  # If True, use a conv layer for the shortcut
        shortcut = Conv2D(filters, 1, strides=stride)(X)
        shortcut = BatchNormalization()(shortcut)
    
    X = Conv2D(filters, kernel_size, strides=stride, padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    X = Conv2D(filters, kernel_size, padding='same')(X)
    X = BatchNormalization()(X)
    
    X = Add([shortcut, X])
    X = ReLU()(X)
    return X

# Bottleneck Block
def bottleneck_block(X, filters, stride=1, conv_shortcut=True):
    """Bottleneck block with conv layers and a residual connection."""
    shortcut = X
    
    if conv_shortcut:  # If True, use a conv layer for the shortcut
        shortcut = Conv2D(4 * filters, 1, strides=stride)(X)
        shortcut = BatchNormalization()(shortcut)
    
    X = Conv2D(filters, 1, strides=stride)(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    X = Conv2D(filters, 3, padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    X = Conv2D(4 * filters, 1)(X)
    X = BatchNormalization()(X)

    X = Add([shortcut, X])
    X = ReLU()(X)
    return X

# ResNet-50 Model
def ResNet50(input_shape, gender_input_shape, classes=1000):
    X_input = Input(input_shape)
    gender_input = Input(gender_input_shape)

    # Initial Conv layer
    X = Conv2D(64, 7, strides=2, padding='same')(X_input)
    X = BatchNormalization()(X)
    X = ReLU()(X)
    X = MaxPooling2D(3, strides=2, padding='same')(X)

    # Conv2_X
    X = bottleneck_block(X, 64, conv_shortcut=False)
    X = bottleneck_block(X, 64)
    X = bottleneck_block(X, 64)

    # Conv3_X
    X = bottleneck_block(X, 128, stride=2)
    X = bottleneck_block(X, 128)
    X = bottleneck_block(X, 128)
    X = bottleneck_block(X, 128)

    # Conv4_X
    X = bottleneck_block(X, 256, stride=2)
    X = bottleneck_block(X, 256)
    X = bottleneck_block(X, 256)
    X = bottleneck_block(X, 256)
    X = bottleneck_block(X, 256)
    X = bottleneck_block(X, 256)

    # Conv5_X
    X = bottleneck_block(X, 512, stride=2)
    X = bottleneck_block(X, 512)
    X = bottleneck_block(X, 512)

    # Global Average Pooling
    X = GlobalAveragePooling2D()(X)

    # Fully connected layer for gender input
    gender_dense = Dense(16, activation='relu')(gender_input)

    # Concatenate gender input with the main output
    X = Concatenate()([X, gender_dense])
    
    # Fully connected (dense) layer
    if isinstance(classes, int):
        if classes == 1:
            X = Dense(classes, activation='sigmoid')(X)
        else:
            X = Dense(classes, activation='softmax')(X)
    else:
        X = Dense(1, activation='linear')(X)

    # Create model
    model = Model(inputs=[X_input, gender_input], outputs = X, name='ResNet50')
    return model


if __name__ == "__main__":
    # Create the ResNet18 model
    model = ResNet50(input_shape=(224, 224, 3), gender_input_shape=(1,), classes='regression')

    # Compile the model
    model.compile(optimizer='adam', loss=MeanAbsoluteError())

    # Print the model summary
    model.summary()
