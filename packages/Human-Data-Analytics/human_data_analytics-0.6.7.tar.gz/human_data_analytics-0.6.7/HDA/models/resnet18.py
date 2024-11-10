from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, Add, ReLU, Concatenate
from tensorflow.keras.layers import BatchNormalization
from .cbam import cbam_block, channel_attention

# Convolutional Block with downsampling (used in ResNet)
def ResBlock(X, kernels, filters, s=2, network_type='vannila'):
    F1, F2 = filters
    k1, k2 = kernels

    # Save the input value for shortcut
    X_shortcut = X

    # First component of main path
    X = Conv2D(F1, (k1, k1), strides=(s, s), padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    # Second component of main path
    X = Conv2D(F2, (k2, k2), strides=(1, 1), padding='same')(X)
    X = BatchNormalization()(X)

    if network_type.lower() == 'cbam':
        X = cbam_block(X)
    elif network_type.lower() == 'channel_attention':
        X = channel_attention(X)

    if s > 1:
        X_shortcut = Conv2D(F2, (1, 1), strides=(s, s))(X_shortcut)
        X_shortcut = BatchNormalization()(X_shortcut)
    
    # Add shortcut to main path
    X = Add()([X, X_shortcut])
    X = ReLU()(X)

    return X


# Build ResNet18 model
def ResNet18(input_shape, gender_input_shape, classes=1000, network_type='vannila'):
    # Define the input tensor
    X_input = Input(input_shape)
    gender_input = Input(gender_input_shape)

    # Stage 1 (Initial Conv Layer)
    X = Conv2D(64, (7, 7), strides=(2, 2), padding='same')(X_input)
    X = BatchNormalization()(X)
    X = ReLU()(X)
    if network_type.lower() == 'cbam':
        X = cbam_block(X)
    elif network_type.lower() == 'channel_attention':
        X = channel_attention(X)
    X = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(X)

    # Stage 2
    X = ResBlock(X, kernels=[3,3], filters=[64, 64], s=1, network_type=network_type)
    X = ResBlock(X, kernels=[3,3], filters=[64, 64], s=1, network_type=network_type)

    # Stage 3
    X = ResBlock(X, kernels=[3,3], filters=[128, 128], s=2, network_type=network_type)
    X = ResBlock(X, kernels=[3,3], filters=[128, 128], s=1, network_type=network_type)

    # Stage 4
    X = ResBlock(X, kernels=[3,3], filters=[256, 256], s=2, network_type=network_type)
    X = ResBlock(X, kernels=[3,3], filters=[256, 256], s=1, network_type=network_type)

    # Stage 5
    X = ResBlock(X, kernels=[3,3], filters=[512, 512], s=2, network_type=network_type)
    X = ResBlock(X, kernels=[3,3], filters=[512, 512], s=1, network_type=network_type)

    # Average Pooling
    X = GlobalAveragePooling2D()(X)

    # Fully connected layer for gender input
    gender_dense = Dense(16, activation='relu')(gender_input)

    # Concatenate gender input with the main output
    X = Concatenate()([X, gender_dense])
   
    # Output layer (fully connected)
    if isinstance(classes, int):
        if classes == 1:
            X = Dense(classes, activation='sigmoid')(X)
        else:
            X = Dense(classes, activation='softmax')(X)
    else:
        X = Dense(1, activation='linear')(X)

     # Create model
    model = Model(inputs=[X_input, gender_input], outputs = X, name='ResNet18')

    return model


if __name__ == "__main__":
    # Create the ResNet18 model
    model = ResNet18(input_shape=(224, 224, 3), gender_input_shape=(1,), classes='regression', net_type='cbam') 

    # Compile the model
    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mean_absolute_error'])

    # Print the model summary
    model.summary()
