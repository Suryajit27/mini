import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
from pathlib import Path
import os.path
import matplotlib.pyplot as plt
from PIL import Image
import cv2
new_model = tf.keras.models.load_model('C:\\Users\\User\\Desktop\\Fruit_Vegetable_Recognition-master\\Fruit_Vegetable_Recognition-master\\FV.h5')
global counter
counter=0
def scanobj():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('python webcam screenshot app')
    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print('failed to grab frame')
            break
        cv2.imshow('test', frame)
        k  = cv2.waitKey(1)
        if k%256 == 27:
            print('escape hit, closing the app')
            counter=1
            break
        elif k%256  == 32:
            img_name = f'opencv_frame_{img_counter}.png'
            cv2.imwrite(img_name, frame)
            print('screenshot taken')
            img_counter += 1
            break
            
    cam.release()
    cv2.destroyAllWindows()
    return img_name

def output(location):
    labels ={0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}
    img=Image.open(location)
    img=img.resize((224,224)).convert('RGB')
    img=np.array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=new_model.predict(img)
    y_class = answer.argmax(axis=-1)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    return res
counter=0
while (counter!=1):
    currentimg = scanobj()
    str1="C:\\Users\\User\\Desktop\\Fruit_Vegetable_Recognition-master\\Fruit_Vegetable_Recognition-master\\opencv_frame_0.png"
    print(str1)
    result=output(str1)
    print(result)


