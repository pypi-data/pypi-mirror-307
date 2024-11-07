import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Load the COCO dataset
coco_train_dir = 'coco_train2017'
coco_val_dir = 'coco_val2017'
coco_ann_dir = 'coco_ann2017/annotations/instances_val2017.json'

# Get the number of training and validation images
num_train_images = len(os.listdir(coco_train_dir))
num_val_images = len(os.listdir(coco_val_dir))
print(f"Number of training images: {num_train_images}")
print(f"Number of validation images: {num_val_images}")

# Plot some sample images
plt.figure(figsize=(12, 8))
for i in range(4):
    ax = plt.subplot(2, 2, i+1)
    img_path = os.path.join(coco_train_dir, os.listdir(coco_train_dir)[i])
    img = Image.open(img_path)
    plt.imshow(img)
    ax.set_title(f"Image {i+1}")
    ax.axis('off')
plt.show()

# Define image augmentation
data_gen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    contrast_stretch_range=(0.8, 1.2),
    fill_mode='nearest'
)

# Apply image augmentation
train_data_gen = data_gen.flow_from_directory(
    coco_train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_data_gen = data_gen.flow_from_directory(
    coco_val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Get the updated number of training and validation images
num_train_images = len(train_data_gen.filenames)
num_val_images = len(val_data_gen.filenames)
print(f"Number of training images after augmentation: {num_train_images}")
print(f"Number of validation images after augmentation: {num_val_images}")

# Normalize the training data
train_data_gen.rescale = 1./255
val_data_gen.rescale = 1./255

# Build a VGG16-based classification model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = Flatten()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(80, activation='softmax')(x)  # 80 classes in COCO dataset
model = Model(inputs=base_model.input, outputs=x)

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
epochs = 20
model.fit(train_data_gen, validation_data=val_data_gen, epochs=epochs, verbose=1)

# Evaluate the model
train_loss, train_acc = model.evaluate(train_data_gen)
val_loss, val_acc = model.evaluate(val_data_gen)

print(f"Training Accuracy: {train_acc:.2f}")
print(f"Validation Accuracy: {val_acc:.2f}")

# Build a Faster R-CNN model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential

frcnn_model = Sequential()
frcnn_model.add(VGG16(include_top=False, input_shape=(224, 224, 3)))
frcnn_model.add(Conv2D(512, (3, 3), activation='relu'))
frcnn_model.add(MaxPooling2D((2, 2)))
frcnn_model.add(Flatten())
frcnn_model.add(Dense(4096, activation='relu'))
frcnn_model.add(Dropout(0.5))
frcnn_model.add(Dense(4096, activation='relu'))
frcnn_model.add(Dropout(0.5))
frcnn_model.add(Dense(80, activation='softmax'))  # 80 classes in COCO dataset

frcnn_model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the Faster R-CNN model
frcnn_model.fit(train_data_gen, validation_data=val_data_gen, epochs=epochs, verbose=1)

# Evaluate the Faster R-CNN model
frcnn_train_loss, frcnn_train_acc = frcnn_model.evaluate(train_data_gen)
frcnn_val_loss, frcnn_val_acc = frcnn_model.evaluate(val_data_gen)

print(f"Faster R-CNN Training Accuracy: {frcnn_train_acc:.2f}")
print(f"Faster R-CNN Validation Accuracy: {frcnn_val_acc:.2f}")

# Compare the training and testing accuracy before and after augmentation
print("Accuracy before augmentation:")
print(f"Training Accuracy: {train_acc:.2f}")
print(f"Validation Accuracy: {val_acc:.2f}")

print("Accuracy after augmentation:")
print(f"Training Accuracy: {frcnn_train_acc:.2f}")
print(f"Validation Accuracy: {frcnn_val_acc:.2f}")
