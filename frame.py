import os
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import mysql.connector
import serial
import threading
from tkinter import *
from PIL import Image,ImageTk
top = Tk()
top.geometry("1020x400")
top.title("Automatic Weighing Machine")
ser = serial.Serial('COM7', 9600)
global float_data
float_data = 1.000
stable_counter = 0
l=[]
w=[]
p=[]

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
arr=['grapes','orange','apple']
thread = threading.Thread(target=weight_transfer_thread, daemon=True)
thread.start()
new_model = tf.keras.models.load_model('C:\\Users\\User\\Desktop\\Fruit_Vegetable_Recognition-master\\Fruit_Vegetable_Recognition-master\\FV.h5')
def scanobj():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('python webcam screenshot app')
    img_counter = 0
    img_name=""
    while True:
        ret, frame = cam.read()
        if not ret:
            print('failed to grab frame')
            break
        cv2.imshow('test', frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print('escape hit, closing the app')
            break
        elif k % 256 == 32:
            
            img_name = f'opencv_frame_{img_counter}.png'
            cv2.imwrite(img_name, frame)
            print('screenshot taken')
            img_counter += 1
            break
    cam.release()
    cv2.destroyAllWindows()
    return img_name
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
def scann(): 
    current_img=scanobj()
    arr=output(current_img,beam_width)
    rightframe(arr)


def rightframe(arr):
    column1_string=""
    #image1
    p1=Image.open(arr2[arr[0]])
    p1=p1.resize((70,70),Image.ANTIALIAS)
    photoimg1=ImageTk.PhotoImage(p1)
    lbl_img1=Label(image=photoimg1,background="white")
    lbl_img1.place(x=30,y=90,width=110,height=70)
    box1=Entry(f1,textvariable=n1,font=('Arial 20'),width=9,justify=CENTER)
    box1.delete(0,END)
    box1.insert(INSERT,arr[0])
    box1.config(state="disabled")
    box1.place(x=150,y=110)
    #unit price 
    box6=Entry(f1,font=('Arial 14'),width=5,justify=CENTER)
    box6.place(x=300,y=110)
    PRODUCT = arr[0]
    query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
    cursor.execute(query, (PRODUCT,))
    rows = cursor.fetchall()
    for row in rows:
        column1_value = row[0]
        column1_string=str(column1_value)
    box6.delete(0,END)
    box6.insert(INSERT,column1_string)
    b1=Button(f1,height=2,width=5,text="+",command=add1).place(x=370,y=110)

    #image2
    p2=Image.open(arr2[arr[1]])
    p2=p2.resize((70,70),Image.ANTIALIAS)
    photoimg2=ImageTk.PhotoImage(p2)
    lbl_img2=Label(image=photoimg2,background="white")
    lbl_img2.place(x=30,y=170,width=110,height=70)
    box2=Entry(f1,textvariable=n2,font=('Arial 20'),width=9,justify=CENTER)
    box2.delete(0,END)
    box2.insert(INSERT,arr[1])
    box2.config(state="disabled")
    box2.place(x=150,y=190)
    #unit  price
    box7=Entry(f1,font=('Arial 14'),width=5,justify=CENTER)
    box7.place(x=300,y=190)
    PRODUCT = arr[1]
    query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
    cursor.execute(query, (PRODUCT,))
    rows = cursor.fetchall()
    for row in rows:
        column1_value = row[0]
        column1_string=str(column1_value)
    box7.delete(0,END)
    box7.insert(INSERT,column1_string)
    b2=Button(f1,height=2,width=5,text="+",command=add2).place(x=370,y=190)

    #image3
    p3=Image.open(arr2[arr[2]])
    p3=p3.resize((70,70),Image.ANTIALIAS)
    photoimg3=ImageTk.PhotoImage(p3)
    lbl_img3=Label(image=photoimg3,background="white")
    lbl_img3.place(x=30,y=250,width=110,height=70)
    box3=Entry(f1,textvariable=n3,font=('Arial 20'),width=9,justify=CENTER)
    box3.delete(0,END)
    box3.insert(INSERT,arr[2])
    box3.config(state="disabled")
    box3.place(x=150,y=270)
    #unit price
    box8=Entry(f1,font=('Arial 14'),width=5,justify=CENTER)
    box8.place(x=300,y=270)
    PRODUCT = arr[2]
    query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
    cursor.execute(query, (PRODUCT,))
    rows = cursor.fetchall()
    for row in rows:
        column1_value = row[0]
        column1_string=str(column1_value)
    box8.delete(0,END)
    box8.insert(INSERT,column1_string)
    b3=Button(f1,height=2,width=5,text="+",command=add3).place(x=370,y=270)
     

arr2 ={'apple':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/apple.jpg",
       'banana':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/banana.jpg",
       'beetroot':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/beetroot.jpg",
       'bell pepper':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/bell pepper.jpg",
       'cabbage':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/cabbage.jpg",
       'capsicum':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/capsicum.jpg",
       'carrot':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/carrot.png",
       'cauliflower':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/cauliflower.jpg",
       'chilli pepper':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/chilli.jpg",
       'corn':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/corn.jpg",
       'cucumber':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/cucumber.jpg",
       'eggplant':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/eggplant.jpg",
       'garlic':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/garlic.jpg",
       'ginger':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/ginger.jpg",
       'grapes':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/grapes.jpg",
       'jalepeno':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/jalapeno.jpg",
       'kiwi':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/kiwi.jpg",
       'lemon':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/lemon.jpg",
       'lettuce':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/lettuce.jpeg",
       'mango':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/mango.png",
       'onion':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/onion.jpg",
       'orange':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/orange.jpg",
       'paprika':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/paprika.jpg",
       'pear':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/pear.jpg",
       'peas':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/peas.jpg",
       'pineapple':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/pineapple.jpg",
       'pomegranate':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/pomegranate.jpg",
       'potato':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/potato.jpg",
       'radish':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/radish.jpg",
       'soy beans':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/soy beans.jpg",
       'spinach':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/spinach.jpg",
       'sweetcorn':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/sweet corn.jpg",
       'sweet potato':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/sweet potato.jpg",
       'tomato':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/tomato.jpg",
       'turnip':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/turnip.jpg",
       'watermelon':"C:/Users/User/Desktop/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/images1/watermelon.jpg"}


name=StringVar()
n1=StringVar()
n2=StringVar()
n3=StringVar()
n4=StringVar()
#box9=Entry(font=('Arial 14'),width=0,justify=CENTER)
#box9.place(x=610,y=190)
def search():
       global search_result
       search_result=""
       f2=Frame(top,bg="green",width=230,height=250).place(x=450,y=80)
       column1_string=""
       #image4
       p4=Image.open(arr2[name.get()])
       p4=p4.resize((70,70),Image.ANTIALIAS)
       global photoimg4
       photoimg4=ImageTk.PhotoImage(p4)
       lbl_img4=Label(image=photoimg4,background="white")
       lbl_img4.place(x=510,y=90,width=110,height=70)
       box4=Entry(f2,textvariable=n4,font=('Arial 20'),width=9,justify=CENTER)
       box4.delete(0,END)
       box4.insert(INSERT,name.get())
       box4.config(state="disabled")
       box4.place(x=463,y=190)
       box9=Entry(f2,font=('Arial 14'),width=5,justify=CENTER)
       box9.place(x=610,y=190)
       PRODUCT = box4.get()
       query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
       cursor.execute(query, (PRODUCT,))
       rows = cursor.fetchall()
       for row in rows:
            column1_value = row[0]
            column1_string=str(column1_value)
       box9.delete(0,END)   
       box9.insert(INSERT,column1_string)
       search_result=box9.get()
       b6=Button(f2,height=2,width=5,text="+",command=add4).place(x=543,y=270)
def calculate():
     totalprice=sum(p)
     total.insert(INSERT,str(totalprice))

label1=Label(top,text="BILL",font=('Arial',20)).place(x=817,y=10)
box5=Listbox(top,width=15,height=14,justify=CENTER)
box5.place(x=700,y=80)
label2=Label(top,text="ITEMS",font=('Arial',10)).place(x=717,y=55)
box10=Listbox(top,width=15,height=14,justify=CENTER)
box10.place(x=800,y=80)
label3=Label(top,text="WEIGHTS",font=('Arial',10)).place(x=817,y=55)
box11=Listbox(top,width=15,height=14,justify=CENTER)
box11.place(x=900,y=80)
label4=Label(top,text="PRICE",font=('Arial',10)).place(x=917,y=55)
calc=Button(top,height=2,width=15,text="TOTAL",fg="white",activeforeground="blue",background="blue",command=calculate).place(x=700,y=350)
total=Entry(top,width=10,font=('Arial 20'))
total.place(x=825,y=350)

def add1():
       column1_value=0
       box10.delete(0,END)
       w.append(get_latest_weight()) 
       box11.delete(0,END)
       box5.delete(0,END)
       l.append(n1.get())
       PRODUCT = l[-1]
       query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
       cursor.execute(query, (PRODUCT,))
       rows = cursor.fetchall()
       for row in rows:
            column1_value = row[0]
       p.append(column1_value*w[-1])
       print("List: ",l)
       print("weight: ",w)
       print("price: ",p)
       global i
       for i in l:
              box5.insert(0,i)
       global j
       for j in w:
            box10.insert(0,j)
       global k
       for k in p:
            box11.insert(0,k)     
    

def add2():
       column1_value=0
       box10.delete(0,END)
       w.append(get_latest_weight()) 
       box11.delete(0,END)
       box5.delete(0,END)
       l.append(n2.get())
       PRODUCT = l[-1]
       query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
       cursor.execute(query, (PRODUCT,))
       rows = cursor.fetchall()
       for row in rows:
            column1_value = row[0]
       p.append(column1_value*w[-1])
       print("List: ",l)
       print("weight: ",w)
       print("price: ",p)
       global i
       for i in l:
              box5.insert(0,i)
       global j
       for j in w:
            box10.insert(0,j)  
       global k
       for k in p:
            box11.insert(0,k)           
    
def add3():
       column1_value=0
       box10.delete(0,END)
       w.append(get_latest_weight()) 
       box11.delete(0,END)
       box5.delete(0,END)
       l.append(n3.get())
       PRODUCT = l[-1]
       query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
       cursor.execute(query, (PRODUCT,))
       rows = cursor.fetchall()
       for row in rows:
            column1_value = row[0]
       p.append(column1_value*w[-1])
       print("List: ",l)
       print("weight: ",w)
       print("price: ",p)
       global i
       for i in l:
              box5.insert(0,i)
       global j
       for j in w:
            box10.insert(0,j)      
       global k
       for k in p:
            box11.insert(0,k)       

def add4():
       box10.delete(0,END)
       w.append(get_latest_weight())
       box11.delete(0,END)
       p.append(float(search_result)*w[-1]) 
       box5.delete(0,END)
       l.append(n4.get())
       print("List: ",l)
       print("weight: ",w)
       print("price: ",p)
       global i
       for i in l:
              box5.insert(0,i)
       global j
       for j in w:
            box10.insert(0,j)
       global k
       for k in p:
            box11.insert(0,k)             

textBox = Entry(top,textvariable=name,font=('Arial 20'),width=27,highlightbackground="green",highlightthickness=2).place(x=20,y=20)
b0=Button(top,bg="red",width=20,height=2,text="SEARCH",fg="white",activeforeground="red",command=search).place(x=450,y=20)
arr=['grapes','orange','apple']
b4=Button(top,width=6,height=2,bg="green",text="CAM",fg="white",activeforeground="green",command=scann).place(x=625,y=20)

f1=Frame(top,bg="red",width=410,height=250).place(x=20,y=80)
column1_string=""
#image1
p1=Image.open(arr2[arr[0]])
p1=p1.resize((70,70),Image.ANTIALIAS)
photoimg1=ImageTk.PhotoImage(p1)
lbl_img1=Label(image=photoimg1,background="white")
lbl_img1.place(x=30,y=90,width=110,height=70)
box1=Entry(f1,textvariable=n1,font=('Arial 20'),width=9,justify=CENTER)
box1.insert(INSERT,arr[0])
box1.config(state="disabled")
box1.place(x=150,y=110)
#unit price 
box6=Entry(f1,font=('Arial 14'),width=5,justify=CENTER)
box6.place(x=300,y=110)
PRODUCT = arr[0]
query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
cursor.execute(query, (PRODUCT,))
rows = cursor.fetchall()
for row in rows:
    column1_value = row[0]
    column1_string=str(column1_value)
box6.insert(INSERT,column1_string)
b1=Button(f1,height=2,width=5,text="+",command=add1).place(x=370,y=110)

#image2
p2=Image.open(arr2[arr[1]])
p2=p2.resize((70,70),Image.ANTIALIAS)
photoimg2=ImageTk.PhotoImage(p2)
lbl_img2=Label(image=photoimg2,background="white")
lbl_img2.place(x=30,y=170,width=110,height=70)
box2=Entry(f1,textvariable=n2,font=('Arial 20'),width=9,justify=CENTER)
box2.insert(INSERT,arr[1])
box2.config(state="disabled")
box2.place(x=150,y=190)
#unit  price
box7=Entry(f1,font=('Arial 14'),width=5,justify=CENTER)
box7.place(x=300,y=190)
PRODUCT = arr[1]
query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
cursor.execute(query, (PRODUCT,))
rows = cursor.fetchall()
for row in rows:
    column1_value = row[0]
    column1_string=str(column1_value)
box7.insert(INSERT,column1_string)
b2=Button(f1,height=2,width=5,text="+",command=add2).place(x=370,y=190)

#image3
p3=Image.open(arr2[arr[2]])
p3=p3.resize((70,70),Image.ANTIALIAS)
photoimg3=ImageTk.PhotoImage(p3)
lbl_img3=Label(image=photoimg3,background="white")
lbl_img3.place(x=30,y=250,width=110,height=70)
box3=Entry(f1,textvariable=n3,font=('Arial 20'),width=9,justify=CENTER)
box3.insert(INSERT,arr[2])
box3.config(state="disabled")
box3.place(x=150,y=270)
#unit price
box8=Entry(f1,font=('Arial 14'),width=5,justify=CENTER)
box8.place(x=300,y=270)
PRODUCT = arr[2]
query = 'SELECT PRICE FROM fruits_veg WHERE PROD_NAME = %s'
cursor.execute(query, (PRODUCT,))
rows = cursor.fetchall()
for row in rows:
    column1_value = row[0]
    column1_string=str(column1_value)
box8.insert(INSERT,column1_string)
b3=Button(f1,height=2,width=5,text="+",command=add3).place(x=370,y=270)

top.mainloop()
stop_thread=True
cursor.close()
connection.close()
ser.close()