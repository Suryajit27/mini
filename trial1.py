import os
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import mysql.connector
import serial
import threading

ser = serial.Serial('COM7', 9600)
global float_data
float_data = 1.000
stable_counter = 0

connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='TOMATO'
)
cursor = connection.cursor()
stop_thread=False
n = 0
counter=0
weight_available = threading.Event()


def weight_transfer_thread():
    global current_weight
    
    while True:
        # Read the weight from the weighing machine
        while not stop_thread:
            data = ser.readline().decode().strip()
            
            try:
                float_data = float(data)
                # Process the weight as needed
                
                # Update the current weight value
                current_weight = float_data
                
                # Set the event to signal the availability of a new weight value
                weight_available.set()
                
            except ValueError:
                print("Unable to convert the data to a float.")

def get_latest_weight():
    # Wait for the weight_available event to be set
    weight_available.wait()
    
    # Clear the event for future weight updates
    weight_available.clear()
    
    # Return the latest weight value
    return current_weight

thread = threading.Thread(target=weight_transfer_thread, daemon=True)
thread.start()


new_model = tf.keras.models.load_model('C:\\Users\\User\\Desktop\\Fruit_Vegetable_Recognition-master\\Fruit_Vegetable_Recognition-master\\FV.h5')

def scanobj():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('python webcam screenshot app')
    img_counter = 0
    img_name=""
    counter=0
    while True:
        ret, frame = cam.read()
        if not ret:
            print('failed to grab frame')
            break
        cv2.imshow('test', frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print('escape hit, closing the app')
            counter = 1
            break
        elif k % 256 == 32:
            
            img_name = f'opencv_frame_{img_counter}.png'
            cv2.imwrite(img_name, frame)
            print('screenshot taken')
            img_counter += 1
            break

    cam.release()
    cv2.destroyAllWindows()
    return img_name,counter

def output(location, beam_width):
    labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
              7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
              14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
              19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
              26: 'pomegranate', 27: 'potato', 28: 'radish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
              32: 'sweet potato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

    img = Image.open(location)
    img = img.resize((224, 224)).convert('RGB')
    img = np.array(img)
    img = img / 255
    img = np.expand_dims(img, [0])

    beam = [(1.0, [])]  # Initialize the beam with a single empty path

    while len(beam) < beam_width:
        candidates = []
        for prob, path in beam:
            answer = new_model.predict(img)
            topk_indices = answer.argsort()[0, -beam_width:]
            for idx in topk_indices:
                new_prob = prob * answer[0, idx]
                new_path = path + [idx]
                candidates.append((new_prob, new_path))

        candidates.sort(reverse=True, key=lambda x: x[0])

        unique_candidates = []
        for candidate in candidates:
            if candidate[1][-1] not in [path[-1] for _, path in unique_candidates]:
                unique_candidates.append(candidate)

        beam = unique_candidates[:len(beam) + 1]

    predictions = [path[-1] for _, path in beam]
    results = [labels[prediction] for prediction in predictions]
    return results

beam_width = 3
while counter != 1:
    currentimg,counter = scanobj()
    if counter!=1:
        str1 = "C:\\Users\\User\\Desktop\\Fruit_Vegetable_Recognition-master\\Fruit_Vegetable_Recognition-master\\opencv_frame_0.png"
        print(str1)
        results = output(str1, beam_width)
        print(results)
        n = int(input("enter the fruit number:"))
        PRODUCT = results[n - 1]
        data = get_latest_weight()
        print("weight: ",data)
        query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
        cursor.execute(query, (PRODUCT,))
        rows = cursor.fetchall()
        for row in rows:
            column1_value = float(row[0])
            price = column1_value * data
            print("Price: Rs",price)
stop_thread=True
cursor.close()
connection.close()
ser.close()
