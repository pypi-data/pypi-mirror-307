import tensorflow as tf
from tensorflow.keras.layers import Lambda, Conv2D, GlobalAveragePooling2D, GlobalMaxPooling2D, Dense, Multiply, Add, Concatenate, Activation, AveragePooling2D, MaxPooling2D

# Channel Attention Block
def channel_attention(X, ratio=8):
    channel_axis = -1
    channel = X.shape[channel_axis]
    
    shared_layer_one = Dense(channel // ratio,
                             activation='relu',
                             kernel_initializer='he_normal',
                             use_bias=True,
                             bias_initializer='zeros')
    shared_layer_two = Dense(channel,
                             kernel_initializer='he_normal',
                             use_bias=True,
                             bias_initializer='zeros')
    
    avg_pool = GlobalAveragePooling2D()(X)
    avg_pool = shared_layer_one(avg_pool)
    avg_pool = shared_layer_two(avg_pool)
    
    max_pool = GlobalMaxPooling2D()(X)
    max_pool = shared_layer_one(max_pool)
    max_pool = shared_layer_two(max_pool)
    
    cbam_feature = Add()([avg_pool, max_pool])
    cbam_feature = Activation('sigmoid')(cbam_feature)
    
    return Multiply()([X, cbam_feature])

# Spatial Attention Block
def spatial_attention(X):
    avg_pool = Lambda(lambda x: tf.reduce_mean(x, axis=-1, keepdims=True), 
                      output_shape=(X.shape[1], X.shape[2], 1))(X)
    max_pool = Lambda(lambda x: tf.reduce_max(x, axis=-1, keepdims=True), 
                      output_shape=(X.shape[1], X.shape[2], 1))(X)


    concat = Concatenate(axis=-1)([avg_pool, max_pool])
    
    cbam_feature = Conv2D(filters=1,
               kernel_size=(7,7),
               strides=(1,1),
               padding='same',
               activation='sigmoid',
               kernel_initializer='he_normal',
               use_bias=False)(concat)  # Apply convolution
    
    return Multiply()([X, cbam_feature])

# CBAM Block (Channel + Spatial Attention)
def cbam_block(input_feature, ratio=8):
    cbam_feature = channel_attention(input_feature, ratio)
    cbam_feature = spatial_attention(cbam_feature)
    return cbam_feature

if __name__ == "__main__":
    # Example usage
    input_layer = tf.keras.layers.Input(shape=(64, 64, 256))  # Example input shape
    output = cbam_block(input_layer)

    model = tf.keras.models.Model(inputs=input_layer, outputs=output)
    #model.summary()

    # model.save("cbam.h5")
    # model = tf.keras.models.load_model("cbam.h5", compile=False)
    model.summary()
