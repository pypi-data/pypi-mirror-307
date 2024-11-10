from tensorflow.keras.layers import Reshape, Conv2DTranspose, BatchNormalization, ReLU, Dense, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from .resnet18 import ResBlock

def ResNet18_encoder(input_shape):
    # Define the input tensor
    X_input = Input(input_shape)

    # Stage 1 (Initial Conv Layer)
    X = Conv2D(64, (7, 7), strides=(2, 2), padding='same')(X_input)
    X = BatchNormalization()(X)
    X = ReLU()(X)
    X = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(X)

    # Stage 2
    X = ResBlock(X, kernels=[3,3], filters=[64, 64], s=1)
    X = ResBlock(X, kernels=[3,3], filters=[64, 64], s=1)

    # Stage 3
    X = ResBlock(X, kernels=[3,3], filters=[128, 128], s=2)
    X = ResBlock(X, kernels=[3,3], filters=[128, 128], s=1)

    # Stage 4
    X = ResBlock(X, kernels=[3,3], filters=[256, 256], s=2)
    X = ResBlock(X, kernels=[3,3], filters=[256, 256], s=1)

    # Stage 5
    X = ResBlock(X, kernels=[3,3], filters=[512, 512], s=2)
    X = ResBlock(X, kernels=[3,3], filters=[512, 512], s=1)

    X = GlobalAveragePooling2D()(X)

    # Create model
    model = Model(inputs=[X_input], outputs = X, name='ResNet18_encoder')

    return model


# Define the decoder model
def ResNet18_decoder(encoded_shape):
    # Input for the decoder is the encoded output (512 nodes)
    encoded_input = Input(shape=encoded_shape)
    
    # Upsample to match the final feature map size before pooling in the encoder
    X = Dense(7 * 7 * 512, activation='relu')(encoded_input)
    X = Reshape((7, 7, 512))(X)

    # Decoder stages with transposed convolutions and upsampling layers
    X = Conv2DTranspose(256, (3, 3), strides=(2, 2), padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)
    
    X = Conv2DTranspose(128, (3, 3), strides=(2, 2), padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)
    
    X = Conv2DTranspose(64, (3, 3), strides=(2, 2), padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    # Additional upsampling to reach (224, 224, 3) shape
    X = Conv2DTranspose(64, (3, 3), strides=(2, 2), padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    # Final output layer with (224, 224, 3) shape
    X = Conv2DTranspose(3, (3, 3), strides=(2, 2), padding='same', activation='sigmoid')(X)

    return Model(inputs=encoded_input, outputs=X, name="Decoder")

# Define the Autoencoder by connecting the encoder and decoder
def ResNet18_Autoencoder(input_shape):
    # Encoder
    encoder = ResNet18_encoder(input_shape)
    
    # Decoder
    encoded_shape = (512,)
    decoder = ResNet18_decoder(encoded_shape)
    
    # Autoencoder
    X_input = Input(shape=input_shape)
    encoded_output = encoder(X_input)
    reconstructed_output = decoder(encoded_output)
    
    autoencoder = Model(inputs=X_input, outputs=reconstructed_output, name="ResNet18_Autoencoder")
    
    return autoencoder

if __name__ == "__main__":
    input_shape = (224, 224, 3)
    autoencoder = ResNet18_Autoencoder(input_shape)
    autoencoder.summary()
