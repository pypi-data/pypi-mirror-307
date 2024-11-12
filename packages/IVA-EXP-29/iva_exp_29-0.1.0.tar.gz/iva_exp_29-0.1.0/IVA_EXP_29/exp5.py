def run():
    print(""" EXP 5 GAN
import keras
import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
from keras.applications import vgg19

# Load images
base_image_path = cv2.imread("/content/istockphoto-1345426734-612x612.jpg")
style_reference_image_path = cv2.imread("/content/istockphoto-1345426734-612x612.jpg")
result_prefix = "paris_generated"
total_variation_weight = 1e-6
style_weight = 1e-6  # Corrected 'le-6' to '1e-6'
content_weight = 2.5e-8

# Get image dimensions and resize base image
width, height, channels = base_image_path.shape
img_nrows = 400
img_ncols = int(width * img_nrows / height)
base_image_path = cv2.cvtColor(base_image_path, cv2.COLOR_BGR2RGB)

# Display the images for visualization
plt.imshow(base_image_path)
plt.show()
plt.imshow(style_reference_image_path)
plt.show()

# Preprocess images for VGG19 model
def preprocess_image(image_path):
    img = keras.utils.load_img(image_path, target_size=(img_nrows, img_ncols))
    img = keras.utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return tf.convert_to_tensor(img)

def deprocess_image(x):
    x = x.reshape((img_nrows, img_ncols, 3))
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    x = x[:, :, ::-1]  # Convert from 'BGR' to 'RGB'
    x = np.clip(x, 0, 255).astype("uint8")
    return x

# Gram matrix function for style loss
def gram_matrix(x):
    x = tf.transpose(x, (2, 0, 1))
    features = tf.reshape(x, (tf.shape(x)[0], -1))
    gram = tf.matmul(features, tf.transpose(features))
    return gram

# Style loss function
def style_loss(style, combination):
    S = gram_matrix(style)
    C = gram_matrix(combination)
    size = img_nrows * img_ncols
    return tf.reduce_sum(tf.square(S / (size ** 2) - C)) / (4.0 * (3 ** 2))

# Content loss function
def content_loss(base, combination):
    return tf.reduce_sum(tf.square(combination - base))

# Total variation loss function
def total_variation_loss(x):
    a = tf.square(x[:, :-1, :-1, :] - x[:, 1:, :-1, :])
    b = tf.square(x[:, :-1, :-1, :] - x[:, :-1, 1:, :])
    return tf.reduce_sum(tf.pow(a + b, 1.25))

# Load VGG19 model
model = vgg19.VGG19(weights="imagenet", include_top=False)

# Feature extractor model
outputs_dict = {layer.name: layer.output for layer in model.layers}
feature_extractor = keras.Model(inputs=model.inputs, outputs=outputs_dict)

# Layers for style and content loss
style_layer_names = [
    "block1_conv1", "block2_conv1", "block3_conv1", "block4_conv1", "block5_conv1"
]
content_layer_name = "block5_conv2"

# Compute total loss (content loss, style loss, and total variation loss)
def compute_loss(combination_image, base_image, style_reference_image):
    input_tensor = tf.concat([base_image, style_reference_image, combination_image], axis=0)
    features = feature_extractor(input_tensor)

    loss = tf.zeros(shape=())
    # Content loss
    layer_features = features[content_layer_name]
    base_image_features = layer_features[0, :, :, :]
    combination_features = layer_features[2, :, :, :]
    loss += content_weight * content_loss(base_image_features, combination_features)

    # Style loss
    for layer_name in style_layer_names:
        layer_features = features[layer_name]
        style_reference_features = layer_features[1, :, :, :]
        combination_features = layer_features[2, :, :, :]
        sl = style_loss(style_reference_features, combination_features)
        loss += (style_weight / len(style_layer_names)) * sl

    # Total variation loss
    loss += total_variation_weight * total_variation_loss(combination_image)

    return loss

# Compute loss and gradients for optimization
@tf.function
def compute_loss_and_grads(combination_image, base_image, style_reference_image):
    with tf.GradientTape() as tape:
        loss = compute_loss(combination_image, base_image, style_reference_image)
    grads = tape.gradient(loss, combination_image)
    return loss, grads

# Initialize optimizer
optimizer = keras.optimizers.SGD(keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=100.0, decay_steps=100, decay_rate=0.96))

# Load and preprocess images
base_image = preprocess_image("/content/istockphoto-1345426734-612x612.jpg")
style_reference_image = preprocess_image("/content/images (5).jpeg")
combination_image = tf.Variable(preprocess_image("/content/istockphoto-1345426734-612x612.jpg"))

iterations = 5
for i in range(1, iterations + 1):
    loss, grads = compute_loss_and_grads(combination_image, base_image, style_reference_image)
    optimizer.apply_gradients([(grads, combination_image)])

    if i % 100 == 0:
        print(f"Iteration {i}: loss={loss.numpy()}")

    img = deprocess_image(combination_image.numpy())
    fname = result_prefix + f"_at_iteration_{i}.png"
    keras.utils.save_img(fname, img)

# Display generated image at iteration 100
from IPython.display import Image
Image(filename=result_prefix + "_at_iteration_5.png")""")
