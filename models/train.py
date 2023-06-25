import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import PIL
from tensorflow import keras
from pathlib import Path
import os.path
from modules.helper_functions import create_tensorboard_callback, walk_through_dir

BATCH_SIZE = 32
IMAGE_SIZE = (300, 300)
dataset = "datasets"


def load_dataset():
    walk_through_dir(dataset)

    image_dir = Path(dataset)
    filepaths = list(image_dir.glob(r'**/*.JPG')) + list(image_dir.glob(r'**/*.jpg')) + \
                list(image_dir.glob(r'**/*.png')) + list(image_dir.glob(r'**/*.PNG'))
    labels = list(map(lambda x: os.path.split(os.path.split(x)[0])[1], filepaths))

    filepaths = pd.Series(filepaths, name='Filepath').astype(str)
    labels = pd.Series(labels, name='Label')
    image_df = pd.concat([filepaths, labels], axis=1)

    path = Path("../datasets").rglob("*.jpg")
    for img_p in path:
        try:
            PIL.Image.open(img_p)
        except PIL.UnidentifiedImageError:
            print(img_p)

    return image_df


def create_model():
    # Load Dataset
    image_df = load_dataset()

    train_df, test_df = train_test_split(image_df, test_size=0.2, shuffle=True, random_state=42)

    train_generator = keras.preprocessing.image.ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input, validation_split=0.2)

    test_generator = keras.preprocessing.image.ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input)

    train_images = train_generator.flow_from_dataframe(dataframe=train_df, x_col='Filepath', y_col='Label',
                                                       target_size=(224, 224), color_mode='rgb',
                                                       class_mode='categorical',
                                                       batch_size=32, shuffle=True, seed=42,
                                                       subset='training')

    val_images = train_generator.flow_from_dataframe(dataframe=train_df, x_col='Filepath', y_col='Label',
                                                     target_size=(224, 224), color_mode='rgb', class_mode='categorical',
                                                     batch_size=32,
                                                     shuffle=True, seed=42, subset='validation')

    test_images = test_generator.flow_from_dataframe(dataframe=test_df, x_col='Filepath', y_col='Label',
                                                     target_size=(224, 224), color_mode='rgb', class_mode='categorical',
                                                     batch_size=32, shuffle=False)

    resize_and_rescale = tf.keras.Sequential([
        keras.layers.experimental.preprocessing.Resizing(224, 224),
        keras.layers.experimental.preprocessing.Rescaling(1. / 255),
        keras.layers.experimental.preprocessing.RandomFlip("horizontal"),
        keras.layers.experimental.preprocessing.RandomRotation(0.1),
        keras.layers.experimental.preprocessing.RandomZoom(0.1),
        keras.layers.experimental.preprocessing.RandomContrast(0.1),
    ])

    pretrained_model = tf.keras.applications.efficientnet.EfficientNetB0(input_shape=(224, 224, 3),
                                                                         include_top=False, weights='imagenet',
                                                                         pooling='max')

    pretrained_model.trainable = False

    checkpoint_path = "grape_disease_classification_model_checkpoint"
    checkpoint_callback = keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True,
                                                          monitor="val_accuracy",
                                                          save_best_only=True)
    early_stopping = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

    inputs = pretrained_model.input
    x = resize_and_rescale(inputs)

    x = keras.layers.Dense(128, activation='relu')(pretrained_model.output)
    x = keras.layers.Dropout(0.45)(x)
    x = keras.layers.Dense(256, activation='relu')(x)
    x = keras.layers.Dropout(0.45)(x)

    outputs = keras.layers.Dense(4, activation='softmax')(x)

    model = keras.Model(inputs=inputs, outputs=outputs)

    model.compile(optimizer=keras.optimizers.Adam(0.00001), loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_images, steps_per_epoch=len(train_images), validation_data=val_images,
              validation_steps=len(val_images),
              epochs=10,
              callbacks=[early_stopping,
                         create_tensorboard_callback("../training_logs", "grape_classification"),
                         checkpoint_callback])
    model.save('models/grape_model_test')


if __name__ == '__main__':
    create_model()
