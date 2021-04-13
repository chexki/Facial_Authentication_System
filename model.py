import os, time
import h5py
import numpy as npd
from keras.preprocessing.image import ImageDataGenerator,load_img,img_to_array
from keras import optimizers
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import callbacks
import keras
from keras.engine import  Model
from keras import backend as K

# K.common.set_image_dim_ordering('th')

if K.image_data_format() == 'th':
  input_tensor = Input(shape=(3, 299, 299))

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# vgg16 = keras.applications.vgg16.VGG16(include_top=False, weights='imagenet', input_tensor=None, input_shape=(96,96,3), pooling=None, classes=1000)
# vgg16.trainable = False
# vgg16.summary()

# top_model = Sequential()
# top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
# top_model.add(Dense(256, activation='relu'))
# top_model.add(Dropout(0.5))
# top_model.add(Dense(1, activation='sigmoid'))

# # add the model on top of the convolutional base
# #custom_vgg_model = Model(vgg16.input,top_model.output)

# model =  Sequential()
# model.add(vgg16)
# model.add(top_model)


# import os
# os.getcwd()
# os.chdir(r'C:\Users\Chexki\Downloads\Attend_Now\Face_authenticator\Transfer-Learning-Face-Anti-Spoofing-Attack-Model-master')
# model.load_weights(filepath='weights/main_weights.h5')

# img_width, img_height = (96,96)

# def predictions(input_):
# 	imgArray = img_to_array(img)
# 	imgArray = imgArray.reshape(1,img_width, img_height,3)
# 	imgArray = imgArray/float(255)
# 	outLabel = int(model.predict_classes(imgArray,verbose=0))
# 	# Real: 1    |  Fake: 0
# 	if outLabel == 1:
# 		return "Live"
# 	else:
# 		return "Not Live"


# # Testing
# img_width, img_height = (96,96)
# img = load_img(r'C:\Users\Chexki\Downloads\Attend_Now\Face_authenticator\data\Chetan\Chetan.jpg',target_size=(96,96))
# print(img)
# imgArray = img_to_array(img)
# print(type(imgArray))
# imgArray = imgArray.reshape(1,img_width, img_height,3)
# imgArray = imgArray/float(255)
# outLabel = int(model.predict_classes(imgArray,verbose=0))
# print(outLabel)
# print('Done')

