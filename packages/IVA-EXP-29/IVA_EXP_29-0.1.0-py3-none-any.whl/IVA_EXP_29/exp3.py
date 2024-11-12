# exp1.py

def run():
    print("""Code for Experiment 3 alex,vggnet,lenet
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, Input, Model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
train_dir = "path to train"
test_dir =  "path to test"
batch_size = 32
img_width, img_height = 128, 128



train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    horizontal_flip=True,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2
)


train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode="sparse",
    shuffle=True
)


test_datagen = ImageDataGenerator(
    rescale=1./255
)


test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode="sparse",
    shuffle=False
)


print("Classes found in training set: ", train_generator.class_indices)
print("Classes found in test set: ", test_generator.class_indices)
          

ALEXnet code
          

          
def AlexNet():
    inp = layers.Input((img_width, img_height, 3))
    x = layers.Conv2D(96, kernel_size=11, strides=4, activation='relu')(inp)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=3, strides=2)(x)
    x = layers.Conv2D(256, kernel_size=5, padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=3, strides=2)(x)
    x = layers.Conv2D(384, kernel_size=3, padding='same', activation='relu')(x)
    x = layers.Conv2D(384, kernel_size=3, padding='same', activation='relu')(x)
    x = layers.Conv2D(256, kernel_size=3, padding='same', activation='relu')(x)
    x = layers.MaxPooling2D(pool_size=3, strides=2)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(4096, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(4096, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(7, activation='softmax')(x)

    model_Alex = models.Model(inputs=inp, outputs=x)

    return model_Alex

model_Alex = AlexNet()
model_Alex.summary()
model_Alex.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy']
)
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=5,
    min_lr=1e-6,
    verbose=1
)
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)
Alex_model = model_Alex.fit(
    train_generator,
    validation_data=test_generator,
    epochs=75,
    callbacks=[reduce_lr,early_stopping]
)
training_loss_alex = Alex_model.history['loss']
val_loss_alex = Alex_model.history['val_loss']
training_acc_alex = Alex_model.history['accuracy']
val_acc_alex = Alex_model.history['val_accuracy']
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(training_loss_alex, label='Training Loss')
plt.plot(val_loss_alex, label='Validation Loss')
plt.title('Loss during training and validation')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(training_acc_alex, label='Training Accuracy')
plt.plot(val_acc_alex, label='Validation Accuracy')
plt.title('Accuracy during training and validation')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()
          


code for VGGNEt
          


def VGGNet():
    inp = layers.Input((img_width, img_height, 3))
    x = layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same')(inp)
    x = layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    x = layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    x = layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    x = layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    x = layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    x = layers.Flatten()(x)
    x = layers.Dense(4096, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(4096, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(7, activation='softmax')(x)

    model_VGG = models.Model(inputs=inp, outputs=x)

    return model_VGG

model_VGG = VGGNet()
model_VGG.summary()
model_VGG.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy']
)
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=5,
    min_lr=1e-6,
    verbose=1
)
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)
VGG_model = model_VGG.fit(
    train_generator,
    validation_data=test_generator,
    epochs=75,
    callbacks=[reduce_lr,early_stopping]
)
training_loss_vgg = VGG_model.history['loss']
val_loss_vgg = VGG_model.history['val_loss']
training_acc_vgg = VGG_model.history['accuracy']
val_acc_vgg = VGG_model.history['val_accuracy']
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(training_loss_vgg, label='Training Loss')
plt.plot(val_loss_vgg, label='Validation Loss')
plt.title('Loss during training and validation')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(training_acc_vgg, label='Training Accuracy')
plt.plot(val_acc_vgg, label='Validation Accuracy')
plt.title('Accuracy during training and validation')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()
          


code for lenet 
          


import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt

def LeNet():
    inp = layers.Input(shape=(img_width, img_height, 1))
    x = layers.Conv2D(6, kernel_size=(5, 5), activation='relu')(inp)
    x = layers.AveragePooling2D()(x)
    
    x = layers.Conv2D(16, kernel_size=(5, 5), activation='relu')(x)
    x = layers.AveragePooling2D()(x)
    
    x = layers.Flatten()(x)
    x = layers.Dense(120, activation='relu')(x)
    x = layers.Dense(84, activation='relu')(x)
    x = layers.Dense(10, activation='softmax')(x)

    model_LeNet = models.Model(inputs=inp, outputs=x)
    return model_LeNet

# Define image dimensions
img_width, img_height = 32, 32

# Instantiate the LeNet model
model_LeNet = LeNet()
model_LeNet.summary()

# Compile the model
model_LeNet.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy']
)

# Set up callbacks
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=5,
    min_lr=1e-6,
    verbose=1
)
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

# Train the model
LeNet_model = model_LeNet.fit(
    train_generator,  # replace with your training data generator
    validation_data=test_generator,  # replace with your test/validation data generator
    epochs=75,
    callbacks=[reduce_lr, early_stopping]
)

# Extract training history
training_loss_lenet = LeNet_model.history['loss']
val_loss_lenet = LeNet_model.history['val_loss']
training_acc_lenet = LeNet_model.history['accuracy']
val_acc_lenet = LeNet_model.history['val_accuracy']

# Plot loss and accuracy
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(training_loss_lenet, label='Training Loss')
plt.plot(val_loss_lenet, label='Validation Loss')
plt.title('Loss during training and validation')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(training_acc_lenet, label='Training Accuracy')
plt.plot(val_acc_lenet, label='Validation Accuracy')
plt.title('Accuracy during training and validation')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()
""")
    # Add the actual code or details of Experiment 1 here
