from google.colab import drive
drive.mount('/content/gdrive')

import numpy as np
import os
import keras
from keras.layers import Dense,GlobalAveragePooling2D
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam
from sklearn.utils import class_weight

base_model=keras.applications.vgg19.VGG19(weights='imagenet',include_top=False, input_shape=(224,224, 3))

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(256,activation='relu')(x)
x=Dense(128,activation='relu')(x)
x=Dense(64,activation='relu')(x)
preds=Dense(5,activation='softmax')(x)

model=Model(inputs=base_model.input,outputs=preds)

for layer in base_model.layers:
    layer.trainable=False

train_datagen=ImageDataGenerator(shear_range=0.2, horizontal_flip=True, zoom_range=0.2)

train_generator=train_datagen.flow_from_directory('gdrive/My Drive/flower_photos',
                                                 target_size=(224,224),
                                                 color_mode='rgb',
                                                 batch_size=4,
                                                 class_mode='categorical',
                                                 shuffle=True)

class_weights = class_weight.compute_class_weight(
           'balanced',
            np.unique(train_generator.classes), 
            train_generator.classes)

model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])

step_size_train=train_generator.n//train_generator.batch_size
model.fit_generator(generator=train_generator,
                   steps_per_epoch=step_size_train,
                   epochs=10, class_weight=class_weights)
