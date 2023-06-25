import pandas as pd
import numpy as np
import tensorflow as tf
from pathlib import Path

model = None


def load_model():
    global model
    model = tf.keras.models.load_model("models/grape_model")
    return model


def transform_image(image):
    image_dir = Path('src/leaves')

    image = tf.keras.preprocessing.image.load_img(f"{image_dir}/{image}", target_size=(224, 224))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


def get_leaves_predict(image):
    generator = tf.keras.preprocessing.image.ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input)

    label = 'ESC'

    test_df = pd.DataFrame({'Filepath': [image], 'Label': [label]})

    images = generator.flow_from_dataframe(
        dataframe=test_df, x_col='Filepath', y_col='Label', target_size=(224, 224), color_mode='rgb',
        class_mode='categorical', batch_size=1, shuffle=False)

    pred = model.predict(images)
    pred = np.argmax(pred, axis=1)

    labels = {0: 'Черная гниль', 1: 'Эска', 2: 'Здоровое ростение', 3: 'Листовая гниль'}
    prediction = labels[pred[0]]
    return pred[0], prediction


if __name__ == '__main__':
    load_model()
    print(get_leaves_predict("hel.JPG"))
