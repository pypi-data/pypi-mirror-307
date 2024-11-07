import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load the BCCD dataset
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.bccd.load_data()

# Show the number of training and testing images
print(f"Number of training images: {len(X_train)}")
print(f"Number of testing images: {len(X_test)}")

# Plot some sample images
fig, ax = plt.subplots(2, 3, figsize=(12, 8))
for i, image in enumerate(X_train[:6]):
    row, col = i // 3, i % 3
    ax[row, col].imshow(image, cmap='gray')
    ax[row, col].axis('off')
plt.show()

# Perform image augmentation
train_datagen = ImageDataGenerator(
    contrast_stretching=True,
    horizontal_flip=True,
    rotation_range=20
)

train_generator = train_datagen.flow(X_train, y_train, batch_size=32)

# Show the number of training and testing images after augmentation
print(f"Number of training images after augmentation: {len(train_generator)}")
print(f"Number of testing images: {len(X_test)}")

# Normalize the training data
X_train_norm = X_train / 255.0
X_test_norm = X_test / 255.0

# Build a convolutional neural network
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model without augmentation
history = model.fit(X_train_norm, tf.keras.utils.to_categorical(y_train),
                    epochs=10,
                    validation_data=(X_test_norm, tf.keras.utils.to_categorical(y_test)),
                    batch_size=32)

# Evaluate the model without augmentation
train_acc, test_acc = model.evaluate(X_train_norm, tf.keras.utils.to_categorical(y_train)), \
                      model.evaluate(X_test_norm, tf.keras.utils.to_categorical(y_test))
print(f"Training accuracy: {train_acc:.2f}")
print(f"Testing accuracy: {test_acc:.2f}")

# Train the model with augmentation
history = model.fit(train_generator,
                    epochs=10,
                    validation_data=(X_test_norm, tf.keras.utils.to_categorical(y_test)),
                    steps_per_epoch=len(train_generator))

# Evaluate the model with augmentation
train_acc, test_acc = model.evaluate(X_train_norm, tf.keras.utils.to_categorical(y_train)), \
                      model.evaluate(X_test_norm, tf.keras.utils.to_categorical(y_test))
print(f"Training accuracy (with augmentation): {train_acc:.2f}")
print(f"Testing accuracy (with augmentation): {test_acc:.2f}")

# Compare the training and testing accuracy before and after augmentation
print(f"Training accuracy before augmentation: {history.history['accuracy'][-1]:.2f}")
print(f"Testing accuracy before augmentation: {history.history['val_accuracy'][-1]:.2f}")
print(f"Training accuracy after augmentation: {train_acc:.2f}")
print(f"Testing accuracy after augmentation: {test_acc:.2f}")