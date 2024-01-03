import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pathlib
import sys
from tensorflow import keras 
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Permet de réduire au silence certains warnings de TF



def get_local_data(file_path, val_split=0.15, batch_size = 40, height = 240, width = 240):
	#Return les datasets de training et de validation depuis le dataset local complet
	
	data_dir = pathlib.Path(file_path)
	print('Number of JPEG in dataset:',len(list(data_dir.glob('*/*.jpg')))) #print the total amount of images
	train_ds = tf.keras.preprocessing.image_dataset_from_directory(
		data_dir,
		validation_split = val_split, 
		subset="training",
		seed=710,
		image_size=(height, width),
		batch_size=batch_size)

	val_ds = tf.keras.preprocessing.image_dataset_from_directory(
		data_dir,
		validation_split = val_split,
		subset="validation",
		seed=710,
		image_size=(height, width),
		batch_size=batch_size)

	class_names = train_ds.class_names
	print('Pokemon in set:', class_names[:3], ' ... ', class_names[-3:])

	return train_ds, val_ds, class_names

def configure_ds(train_ds, val_ds):
	AUTOTUNE = tf.data.experimental.AUTOTUNE
	train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
	val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
	return train_ds, val_ds

def create_model(num_classes = 4, height = 240, width = 240):

	#Ajout de la data augmentation pour une meilleure performance
	data_augmentation = keras.Sequential(
		[layers.experimental.preprocessing.RandomFlip("horizontal",
		    input_shape=(height,width,3)),
			layers.experimental.preprocessing.RandomRotation(0.1),
			layers.experimental.preprocessing.RandomContrast(0.2),  # Modification de la luminosité (contraste)
			layers.experimental.preprocessing.RandomZoom(0.1)]
		)

	model = Sequential([

		data_augmentation,
		#Normalisation du model avec une remise à l'echelle
		layers.experimental.preprocessing.Rescaling(1./255, input_shape=(height, width, 3)),

		layers.Conv2D(32, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Conv2D(64, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Conv2D(128, 3, padding='same', activation='relu'), #uncomment for entire data set
		layers.MaxPooling2D(), #uncomment for entire data set
		layers.Dropout(0.15),
		layers.Flatten(),
		layers.Dense(256, activation='relu'), #uncomment for entire data set
		layers.Dropout(0.5),
		layers.Dense(128, activation='relu'), 
		layers.Dense(num_classes)

	])

	#Compilation du modèle
	model.compile(optimizer='adam',
		loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
		metrics=['accuracy'])

	return model

#model = create_model()

#model.save("/workspaces/Steam-games-overview-Prj/bloc 4 DL")

def train_model(model, train_ds, val_ds, epochs= 40):
	history = model.fit(
		train_ds,
		validation_data=val_ds,
		epochs=epochs
		)
	return history, epochs

def make_prediction(model, picture_path, class_names, height = 240, width = 240):

	img = keras.preprocessing.image.load_img(
    	picture_path, target_size=(height, width)
	)
	img_array = keras.preprocessing.image.img_to_array(img)
	img_array = tf.expand_dims(img_array, 0) # Create a batch

	predictions = model.predict(img_array)
	score = tf.nn.softmax(predictions[0])

	result_str = " {} avec {:.2f}% confidence.".format(class_names[np.argmax(score)], 100 * np.max(score))
	img_to_print = Image.open(picture_path)
	draw = ImageDraw.Draw(img_to_print)
	font = ImageFont.load_default()
	draw.text((0, 0),result_string,(0,255,0),font=font)
	img_to_print.show()

	return result_str

if __name__ == "__main__":

	#Récuperation du dataset
	train_ds, val_ds = get_local_data("/workspaces/Steam-games-overview-Prj/bloc 4 DL/Who_s_that_Champ/Dataset champion")
	class_names = train_ds.class_names

	#Entraînement du modèle
	train_ds, val_ds = configure_ds(train_ds, val_ds)
	model = create_model()
	print(model.summary())
	history, epochs = train_model(model, train_ds, val_ds)

	model.save("/workspaces/Steam-games-overview-Prj/bloc 4 DL")

    #Tester le modèle


