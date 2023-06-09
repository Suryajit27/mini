from tkinter import *
from tkinter import Tk,ttk
from PIL import Image,ImageTk

class Bill_App:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title('POS SOFTWARE')
        #image1
        img=Image.open("images/shop1.jpg")
        img=img.resize((500,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)
        lbl_img=Label(self.root,image=self.photoimg)
        lbl_img.place(x=0,y=0,width=500,height=100)
        #image2
        img_2=Image.open("images/shop2.jpg")
        img_2=img_2.resize((500,130),Image.ANTIALIAS)
        self.photoimg_2=ImageTk.PhotoImage(img_2)
        lbl_img_2=Label(self.root,image=self.photoimg_2)
        lbl_img_2.place(x=500,y=0,width=500,height=100)
        #image3
        img_3=Image.open("images/shop3.jpg")
        img_3=img_3.resize((500,130),Image.ANTIALIAS)
        self.photoimg_3=ImageTk.PhotoImage(img_3)
        lbl_img_3=Label(self.root,image=self.photoimg_3)
        lbl_img_3.place(x=1000,y=0,width=500,height=100)
        
        lbl_title=Label(self.root,text="Billing Software with Image Recognition",font=("times new roman",35,"bold"),bg="grey",fg="white")
        lbl_title.place(x=0,y=100,width=1530,height=50)

        Main_frame=Frame(self.root,bd=5,relief=GROOVE,bg="light grey")
        Main_frame.place(x=0,y=150,width=1530,height=620)
        #customer label
        Cust_Frame=LabelFrame(Main_frame,text="Customer",font=("times new roman",12,"bold"),bg="light grey",fg="grey")
        Cust_Frame.place(x=10,y=5,width=350,height=140)
        #mobile
        self.lbl_mob=Label(Cust_Frame,text="Mobile no",font=("arial",12,"bold"),bg="light grey",fg="black")
        self.lbl_mob.grid(row=0,column=0,stick=W,padx=5,pady=2)
        self.entry_mob=ttk.Entry(Cust_Frame,font=("arial",12,"bold"),width=24)
        self.entry_mob.grid(row=0,column=1)
        #name
        self.lbl_name=Label(Cust_Frame,text="Name",font=("arial",12,"bold"),bg="light grey",fg="black")
        self.lbl_name.grid(row=1,column=0,stick=W,padx=5,pady=2)
        self.entry_name=ttk.Entry(Cust_Frame,font=("arial",12,"bold"),width=24)
        self.entry_name.grid(row=1,column=1)
        #email
        self.lbl_email=Label(Cust_Frame,text="email",font=("arial",12,"bold"),bg="light grey",fg="black")
        self.lbl_email.grid(row=2,column=0,stick=W,padx=5,pady=2)
        self.entry_emaillbl_email=ttk.Entry(Cust_Frame,font=("arial",12,"bold"),width=24)
        self.entry_emaillbl_email.grid(row=2,column=1)
        #product label
        Product_Frame=LabelFrame(Main_frame,text="Product",font=("times new roman",12,"bold"),bg="light grey",fg="grey")
        Product_Frame.place(x=370,y=5,width=620,height=140)
        #Category
        self.lbl_Category=Label(Product_Frame,text="Select Categories",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_Category.grid(row=0,column=0,stick=W,padx=5,pady=2)
        self.Combo_Category=ttk.Combobox(Product_Frame,font=("arial",10,"bold"),width=15,state="readonly")
        self.Combo_Category.grid(row=0,column=1,stick=W,padx=5,pady=2)
        #subCatgegory
        self.lbl_subCategory=Label(Product_Frame,text="Select Sub Category",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_subCategory.grid(row=1,column=0,stick=W,padx=5,pady=2)
        self.Combo_subCategory=ttk.Combobox(Product_Frame,font=("arial",10,"bold"),width=15,state="readonly")
        self.Combo_subCategory.grid(row=1,column=1,stick=W,padx=5,pady=2)
        #price
        self.lbl_price=Label(Product_Frame,text="Price",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_price.grid(row=0,column=2,stick=W,padx=5,pady=2)
        self.Combo_price=ttk.Combobox(Product_Frame,font=("arial",10,"bold"),width=12,state="readonly")
        self.Combo_price.grid(row=0,column=3,stick=W,padx=5,pady=2)
        #qty
        self.lbl_Qty=Label(Product_Frame,text="Quantity",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_Qty.grid(row=1,column=2,stick=W,padx=5,pady=2)
        self.Combo_Qty=ttk.Combobox(Product_Frame,font=("arial",10,"bold"),width=12,state="readonly")
        self.Combo_Qty.grid(row=1,column=3,stick=W,padx=5,pady=2)
        #productid
        self.lbl_prodid=Label(Product_Frame,text="Product Id",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_prodid.grid(row=2,column=0,stick=W,padx=5,pady=2)
        self.entry_prodid=ttk.Entry(Product_Frame,font=("arial",12,"bold"),width=15)
        self.entry_prodid.grid(row=2,column=1)
        #productname
        self.lbl_prodname=Label(Product_Frame,text="Product name",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_prodname.grid(row=2,column=2,stick=W,padx=5,pady=2)
        self.entry_prodname=ttk.Entry(Product_Frame,font=("arial",12,"bold"),width=15)
        self.entry_prodname.grid(row=2,column=3)
        #search frame
        Search_Frame=LabelFrame(Main_frame,bd=2,bg="light grey")
        Search_Frame.place(x=1000,y=10,width=340,height=40)
        self.lbl_Bill=Label(Search_Frame,text="Bill Number",font=("arial",12,"bold"),bg="sky blue",fg="black")
        self.lbl_Bill.grid(row=0,column=0,sticky=W,padx=1)
        self.entry_search=ttk.Entry(Search_Frame,font=("arial",12,"bold"),width=15)
        self.entry_search.grid(row=0,column=1,sticky=W,padx=2)

        self.Search=Button(Search_Frame,text="Search",font=("arial",12,"bold"),bg="sky blue",fg="black",cursor="hand2")
        self.Search.grid(row=0,column=2)

        
        #rightframe Bill Area
        RightLabelFrame=LabelFrame(Main_frame,text='Bill Area',font=("times new roman",12,"bold"),bg="light grey",fg="grey")
        RightLabelFrame.place(x=1000,y=45,width=340,height=340)
        scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
        self.textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg="white",fg="blue",font=("times new roman",12,"bold"))
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)
        
        #BillCouter Frame
        Bottom_Frame=LabelFrame(Main_frame,text="Billcounter",font=("times new roman",12,"bold"),bg="light grey",fg="grey")
        Bottom_Frame.place(x=0,y=400,width=1520,height=125)

        self.lbl_Sbtotal=Label(Bottom_Frame,text="Sub Total",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_Sbtotal.grid(row=0,column=0,stick=W,padx=5,pady=2)
        self.entry_Sbtotal=ttk.Entry(Bottom_Frame,font=("arial",12,"bold"),width=15)
        self.entry_Sbtotal.grid(row=0,column=1)

        self.lbl_amountotal=Label(Bottom_Frame,text="Total Amount",font=("arial",12,"bold"),bd=4,bg="light grey")
        self.lbl_amountotal.grid(row=1,column=0,stick=W,padx=5,pady=2)
        self.entry_amountotal=ttk.Entry(Bottom_Frame,font=("arial",12,"bold"),width=15)
        self.entry_amountotal.grid(row=1,column=1)
        #ButtonFrame
        Btn_Frame=Frame(Bottom_Frame,bd=2,bg='light grey')
        Btn_Frame.place(x=320,y=0)

        self.BtnAddToCart=Button(Btn_Frame,text="Add to Cart",font=("arial",12,"bold"),bg="sky blue",fg="black",width=15,cursor="hand2")
        self.BtnAddToCart.grid(row=0,column=0)

        self.BtnGenBill=Button(Btn_Frame,text="Generate Bill",font=("arial",12,"bold"),bg="sky blue",fg="black",width=15,cursor="hand2")
        self.BtnGenBill.grid(row=0,column=1)

        self.BtnPrint=Button(Btn_Frame,text="Print Bill",font=("arial",12,"bold"),bg="sky blue",fg="black",width=15,cursor="hand2")
        self.BtnPrint.grid(row=0,column=2)

        self.BtnClear=Button(Btn_Frame,text="Clear",font=("arial",12,"bold"),bg="sky blue",fg="black",width=15,cursor="hand2")
        self.BtnClear.grid(row=0,column=3)

        self.BtnExit=Button(Btn_Frame,text="Exit",font=("arial",12,"bold"),bg="sky blue",fg="black",width=15,cursor="hand2")
        self.BtnExit.grid(row=0,column=4)





if __name__ == '__main__' :
    root=Tk()
    obj=Bill_App(root)
    root.mainloop()