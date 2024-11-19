import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from playsound import playsound
#import smtplib


def detect_fire_in_img(img_path):
    model =load_model(r"/home/keerthana/Desktop/Fire Detection and Alarming System/fire-detection-master/model/acc_model_6.h5")
    prediction=predict_fire(img_path,model)
    if prediction==0:
        print("Fire")
        p = playsound(r"fire-detection-master/sound.mp3")
        p.start()
        input("press ENTER to stop playback")
        p.terminate()

def preprocess_img(img_path):
    image=cv2.imread(img_path)
    image=cv2.resize(image,(256,256))
    image=img_to_array(image)
    image=np.expand_dims(image,axis=0)
    image=image/255
    return image




def predict_fire(img_path,model):
    image=preprocess_img(img_path)
    prediction=model.predict(image)
    return prediction