from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from customtkinter import CTkLabel
from pathlib import Path
import customtkinter as ctk
import time
import os
import tempfile
import subprocess
import platform
import re
import datetime
import pyodbc
import sys
import random

class ExportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Exported")

        # Đặt kích thước cửa sổ để phù hợp với kích thước màn hình 
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Đặt cửa sổ ở kích thước toàn màn hình và che thanh taskbar 
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.overrideredirect(True)  # Sử dụng `overrideredirect` để loại bỏ thanh tiêu đề và viền
        # Nút để chuyển đổi chế độ toàn màn hình
        self.root.bind("<F11>", self.toggle_fullscreen)  # Dùng phím F11 để chuyển chế độ toàn màn hình
        self.root.bind("<Escape>", self.exit_fullscreen)  # Dùng phím Esc để thoát toàn màn hình

        # Tạo Frame giả để làm tiêu đề với màu nền đẹp, hiện đại
        self.title_frame = ctk.CTkFrame(self.root, fg_color="#0099FF", corner_radius=0)
        self.title_frame.pack(fill="x")

        # Tạo Label tiêu đề trong Frame, với phông chữ đẹp, dễ đọc
        self.title_label = Label(self.title_frame, text="Inventory Management System | Developed By Quang Vinh", 
                                 font=("Times new roman", 16, "bold"), background="#0099FF", foreground="white")
        self.title_label.pack(pady=20)

        self.btn_back= ctk.CTkButton(self.title_frame, text="Back", command=self.exit_fullscreen, font=ctk.CTkFont(family="Goudy Old Style", size=18, weight="bold"),  # Font chữ
            fg_color="#FF9900",  
            hover_color="#FFAA33",
            text_color="white",
            corner_radius=8, width=110, height=40 )
        self.btn_back.place(x=1420, y=5)

           # All Variables
        self.var_product_id = StringVar()
        self.var_product_name = StringVar()
        self.var_price = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status= StringVar()
        self.var_Category_id = StringVar()
        self.var_searchby= StringVar()
        self.var_searchtxt= StringVar()
        self.var_cal_input= StringVar()

        # Khởi tạo các biến cho thông tin của cửa hàng
        self.var_store_id = StringVar()
        self.var_store_name = StringVar()
        self.var_address = StringVar()
        self.var_contact = StringVar()
        
        self.row_list=[]
        self.cart_list=[]
        
        # Product Frame 1
        ProductFrame1 = Frame(self.root, bd=6, relief=RIDGE, bg='#FFFFFF')
        ProductFrame1.place(x=6, y=70, width=530, height=1000)

        # Title
        title = Label(ProductFrame1, text="All Products", font=("goudy old style", 28, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)

        # Product Frame 2
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg='#FFFFFF')
        ProductFrame2.place(x=0, y=60, width=515, height=133)

        # Label search
        lbl_search = Label(ProductFrame2, text="Search Product | By ID or Name", font=("Times new roman", 15, "bold"), bg="white", fg="green").place(x=10, y=5)

        # Button Show All
        self.btn_show_all = ctk.CTkButton(ProductFrame2, text="Show All", command=self.show, font=ctk.CTkFont(family="goudy old style", size=15, weight="bold"), 
            fg_color="#083531", 
            hover_color="#009933",
            text_color="white",
           corner_radius=8, width=90, height=30 ).place(x=315, y=10)

        self.btn_search= ctk.CTkButton(ProductFrame2, text="Search", command=self.search, font=ctk.CTkFont(family="Goudy Old Style", size=15, weight="bold"),  # Font chữ
            fg_color="#2196f3",  
            hover_color="#3EAEF4",
            text_color="white",
            corner_radius=8, width=90, height=30 )
        self.btn_search.place(x=315, y=55)


        # Tạo ComboBox bằng CTkComboBox
        cmb_search = ctk.CTkComboBox(ProductFrame2, 
                                    variable=self.var_searchby,  # Gắn biến textvariable
                                    values=["Product.ID", "Product Name"],  # Các tùy chọn
                                    state="readonly",  # Chỉ đọc
                                    justify="center",  # Căn giữa
                                    font=("goudy old style", 15), width=125)  # Phông chữ

        cmb_search.place(x=3, y=55)  # Đặt vị trí và kích thước
        cmb_search.set("Product.ID")  # Thiết lập giá trị mặc định

        # Cập nhật Entry sử dụng customtkinter
        self.txt_search = ctk.CTkEntry(ProductFrame2, textvariable=self.var_searchtxt, font=("Times new roman", 16), 
                            fg_color="lightyellow", width=175, height=30)
        self.txt_search.place(x=135, y=55)

        # Product Frame 3
        ProductFrame3 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg='#FFFFFF')
        ProductFrame3.place(x=0, y=210, width=520, height=550)

        # Scrollbars
        scrooly = Scrollbar(ProductFrame3, orient=VERTICAL, width=20)
        scroolx = Scrollbar(ProductFrame3, orient=HORIZONTAL, width=20)

        # Pack scrollbars
        scroolx.pack(side=BOTTOM, fill=X)
        scrooly.pack(side=RIGHT, fill=Y)
   
        # Treeview widget
        self.ProductTable = ttk.Treeview(ProductFrame3, columns=("Product.ID", "Product Name", "Price", "Quantity", "Status" ,"Category.ID", "Category Name", "Supplier Name"), yscrollcommand=scrooly.set, xscrollcommand=scroolx.set)

        # Cấu hình sự kiện để hiển thị hình ảnh khi chọn dòng
        # Configure scrollbars to Treeview
        scroolx.configure(command=self.ProductTable.xview)
        scrooly.configure(command=self.ProductTable.yview)
    
        # Set up Treeview columns and headers
        self.ProductTable.heading("Product.ID", text="Product.ID")
        self.ProductTable.heading("Product Name", text="Product Name")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("Quantity", text="Quantity")
        self.ProductTable.heading("Status", text="Status")
        self.ProductTable.heading("Category.ID", text="Category.ID")
        self.ProductTable.heading("Category Name", text="Category Name")
        self.ProductTable.heading("Supplier Name", text="Supplier Name")
        self.ProductTable["show"] = "headings"
    
        
        # Set column widths
        self.ProductTable.column("Product.ID", width=120, anchor=CENTER)
        self.ProductTable.column("Product Name", width=240, anchor=CENTER)
        self.ProductTable.column("Price", width=140, anchor= CENTER)
        self.ProductTable.column("Quantity", width=120, anchor= CENTER)
        self.ProductTable.column("Status", width=120, anchor= CENTER)
        self.ProductTable.column("Category.ID", width=120, anchor= CENTER)
        self.ProductTable.column("Category Name", width=220, anchor= CENTER)
        self.ProductTable.column("Supplier Name", width=120, anchor= CENTER)

        self.ProductTable.pack(fill=BOTH, expand=1)
        # Binding to display image on row selection
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        # Cập nhật Label sử dụng customtkinter
        lbl_Note = CTkLabel(ProductFrame3, text="Note: Enter 0 Quantity to remove Product from Cart", 
                            font=("Goudy Old Style", 16), text_color="red", anchor="w", 
                            fg_color="white")
        lbl_Note.pack(side=BOTTOM, fill=X)

    
        # Store Frame
        StoreFrame = Frame(self.root, bd=7, relief=RIDGE, bg='#FFFFFF')
        StoreFrame.place(x=540, y=70, width=765, height=180)

        # Title
        title_store = Label(StoreFrame, text="Store Details", font=("goudy old style", 22), bg="light gray").pack(side=TOP, fill=X)

        self.fetch_store_data(StoreFrame)

        #Cal_Cart Frame
        Cal_CartFrame = Frame(self.root, bd=12, relief=RIDGE, bg='#FFFFFF')
        Cal_CartFrame.place(x=540, y=250, width=765, height=610)

        #Cal Frame
        Cal_Frame = Frame(Cal_CartFrame, bd=14, relief=RIDGE, bg='#FFFFFF')
        Cal_Frame.place(x=0, y=0, width=380, height=595)

        # Tạo một Frame chứa Text widget và nút DEL
        text_frame = Frame(Cal_Frame, bg="#FFFFFF")
        text_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        # Text widget (vùng hiển thị đầu vào)
        self.txt_cal_input = Text(text_frame, font=("Arial", 20, "bold"), bg="white", bd=11, width=19, height=4, relief=GROOVE, state='disable')
        self.txt_cal_input.grid(row=0, column=0)


        #Button Cal
        bnt_parentheses=Button(Cal_Frame, text= '(', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input('('), bd=9, padx=3, pady=15,
                                cursor="hand2").grid(row=1, column=0, sticky="nsew")
        bnt_other_parenthese=Button(Cal_Frame, text= ')', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(')'), padx=3, bd=9, pady=15, cursor="hand2").grid(row=1, column=1, sticky="nsew")
        bnt_percent=Button(Cal_Frame, text= '%', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input('%'), bd=9, padx=3, pady=15, cursor="hand2").grid(row=1, column=2, sticky="nsew")
        bnt_decimal=Button(Cal_Frame, text= '.', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input('.'), bd=9, padx=3, pady=15, cursor="hand2").grid(row=1, column=3, sticky="nsew")

        bnt_7=Button(Cal_Frame, text= '7', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(7), padx=3, bd=9, pady=15, cursor="hand2").grid(row=2, column=0, sticky="nsew")
        bnt_8=Button(Cal_Frame, text= '8', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(8), padx=3, bd=9, pady=15, cursor="hand2").grid(row=2, column=1, sticky="nsew")
        bnt_9=Button(Cal_Frame, text= '9', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(9), padx=3, bd=9, pady=15, cursor="hand2").grid(row=2, column=2, sticky="nsew")
        bnt_multip=Button(Cal_Frame, text= 'x', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input('x'), padx=3, bd=9, pady=15, cursor="hand2").grid(row=2, column=3, sticky="nsew")

        bnt_4=Button(Cal_Frame, text= '4', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(4), bd=9, padx=3, pady=15, cursor="hand2").grid(row=3, column=0, sticky="nsew")
        bnt_5=Button(Cal_Frame, text= '5', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(5), bd=9, padx=3, pady=15, cursor="hand2").grid(row=3, column=1, sticky="nsew")
        bnt_6=Button(Cal_Frame, text= '6', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(6), bd=9, padx=3, pady=15, cursor="hand2").grid(row=3, column=2, sticky="nsew")
        bnt_substraction=Button(Cal_Frame, text= '-', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input('-'), bd=9, pady=15, cursor="hand2").grid(row=3, column=3, sticky="nsew")

        bnt_1=Button(Cal_Frame, text= '1', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(1), bd=9, padx=3, pady=15, cursor="hand2").grid(row=4, column=0, sticky="nsew")
        bnt_2=Button(Cal_Frame, text= '2', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(2), bd=9, padx=3, pady=15, cursor="hand2").grid(row=4, column=1, sticky="nsew")
        bnt_3=Button(Cal_Frame, text= '3', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(3), bd=9, padx=3, pady=15, cursor="hand2").grid(row=4, column=2, sticky="nsew")
        bnt_sum=Button(Cal_Frame, text= '+', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input('+'), bd=9, padx=3, pady=15, cursor="hand2").grid(row=4, column=3, sticky="nsew")

        bnt_0=Button(Cal_Frame, text= '0', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input(0), bd=9, padx=3, pady=15, cursor="hand2").grid(row=5, column=0, sticky="nsew")
        bnt_AC=Button(Cal_Frame, text= 'AC', font=("Arial", 16, "bold"), width=4, command=self.clear_cal, bd=9, pady=15, padx=3, cursor="hand2").grid(row=5, column=1, sticky="nsew")
        bnt_equal=Button(Cal_Frame, text= '=', font=("Arial", 16, "bold"), width=4, command=self.performance, bd=9, padx=3, pady=15, cursor="hand2").grid(row=5, column=2, sticky="nsew")
        bnt_0=Button(Cal_Frame, text= '÷', font=("Arial", 16, "bold"), width=4, command=lambda:self.get_input('÷'), padx=3, bd=9, pady=15, cursor="hand2").grid(row=5, column=3, sticky="nsew")

        # Nút "DEL" để xóa ký tự cuối cùng, nằm cạnh Text widget
        btn_clear_last = Button(text_frame, text="DEL", font=("Arial", 10, "bold"), command=self.delete_last_char ,bd=9, width=3, height=5 , cursor="hand2", relief=GROOVE)
        btn_clear_last.grid(row=0, column=1, sticky="nsew")

        #Cart Frame
        Cart_Frame = Frame(Cal_CartFrame, bd=11, relief=RIDGE, bg='#FFFFFF')
        Cart_Frame.place(x=380, y=0, width=370, height=595)

        # Title
        self.title_Cart = Label(Cart_Frame, text="Cart \t Total Product: [0]", font=("goudy old style", 18), bg="light gray")
        self.title_Cart.pack(side=TOP, fill=X)

        # Scrollbars
        scrooly = Scrollbar(Cart_Frame, orient=VERTICAL, width=18)
        scroolx = Scrollbar(Cart_Frame, orient=HORIZONTAL, width=18)

         # Pack scrollbars
        scroolx.pack(side=BOTTOM, fill=X)
        scrooly.pack(side=RIGHT, fill=Y)

       # Treeview widget
        self.CartTable = ttk.Treeview(Cart_Frame, columns=("Product.ID", "Product Name", "Total Price", "Quantity", "Status", "Discount"), yscrollcommand=scrooly.set, xscrollcommand=scroolx.set)

        # Configure scrollbars to Treeview
        scroolx.config(command=self.CartTable.xview)
        scrooly.config(command=self.CartTable.yview)

        # Set up Treeview columns and headers
        self.CartTable.heading("Product.ID", text="Product.ID")
        self.CartTable.heading("Product Name", text="Product Name")
        self.CartTable.heading("Total Price", text="Total Price")
        self.CartTable.heading("Quantity", text="Quantity")
        self.CartTable.heading("Status", text="Status")
        self.CartTable.heading("Discount", text="Discount")
        self.CartTable["show"] = "headings"

        # Set column widths
        self.CartTable.column("Product.ID", width=120, anchor=CENTER)
        self.CartTable.column("Product Name", width=220, anchor=CENTER)
        self.CartTable.column("Total Price", width=130, anchor=CENTER)
        self.CartTable.column("Quantity", width=110, anchor=CENTER)
        self.CartTable.column("Status", width=120, anchor=CENTER)
        self.CartTable.column("Discount", width=120, anchor=CENTER)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        self.var_pName= StringVar()
        self.var_pPrice= StringVar()
        self.var_pQuantity= StringVar()
        self.var_pDiscount= StringVar()
        self.var_pStatus= StringVar()
        self.var_empNo= StringVar()
        self.var_empName= StringVar()
        self.var_stock= StringVar()




        #Cart Frame
        Add_Cart_Frame = Frame(self.root, bd=6, relief=RIDGE, bg='#FFFFFF')
        Add_Cart_Frame.place(x=540, y=860, width=765, height=210)

       
        #Emp.No
        Emp_No=Label(Add_Cart_Frame, text="Emp.No",font=("goudy old style", 16), bg="#FFFFFF").place(x=30, y=10)
        txt_Emp_No = ctk.CTkEntry(Add_Cart_Frame, textvariable=self.var_empNo, font=("Times new roman", 18), fg_color="light yellow", width=150, height=28).place(x=100, y=8)

        #Emp Name
        Emp_Name=Label(Add_Cart_Frame, text="Emp Name",font=("goudy old style", 16), bg="#FFFFFF").place(x=370, y=10)
        txt_Emp_Name = ctk.CTkEntry(Add_Cart_Frame, textvariable=self.var_empName, font=("Times new roman", 18), fg_color="light yellow", width=180, height=30).place(x=400, y=8)
        
        
        #Product Name
        productName= Label(Add_Cart_Frame, text="Product Name",font=("goudy old style", 16), bg="white").place(x=30, y=65)
        txt_productName = ctk.CTkEntry(Add_Cart_Frame, textvariable=self.var_pName, font=("Times new roman", 16), fg_color="light gray", state='readonly', width=210, height=25).place(x=5, y=80)
        
        #Price per Quantity
        product_Price= Label(Add_Cart_Frame, text="Price Per Quantity",font=("goudy old style", 16), bg="white").place(x=360, y=65)
        txt_product_price = ctk.CTkEntry(Add_Cart_Frame, textvariable=self.var_pPrice, font=("Times new roman", 16), fg_color="light gray", state='readonly', width=160 , height=25).place(x=280, y=80)

        #Quantity
        product_Quantity=Label(Add_Cart_Frame, text="Quantity",font=("goudy old style", 16), bg="white").place(x=610, y=65)
        txt_productName = ctk.CTkEntry(Add_Cart_Frame, textvariable=self.var_pQuantity, font=("Times new roman", 16), fg_color="light yellow", width=130, height=25).place(x=470, y=80)

        #Stock
        self.lbl_Stock=Label(Add_Cart_Frame, text="In Stock [100]",font=("goudy old style", 16), bg="white")
        self.lbl_Stock.place(x=10, y=160)

        # Discount
        self.lbl_Discount=Label(Add_Cart_Frame, text="Discount",font=("goudy old style", 16), bg="white")
        self.lbl_Discount.place(x=160, y=160)
   
        spin_discount=Spinbox(Add_Cart_Frame, from_=0, to=100, textvariable=self.var_pDiscount, font=("goudy old style", 16), bg="light yellow").place(x=250, y=160, width=90, height=30)
        #Button Clear
        bnt_clear = ctk.CTkButton(Add_Cart_Frame, text="Clear", font=("Goudy Old Style", 15, "bold"), command=self.clear_cart,
                     fg_color="light gray", 
                     text_color="Black",
                     hover_color="#B3B3B3",  # Màu khi hover
                     corner_radius=8,
                     width=130, height=30)
        
        bnt_clear.place(x=290, y=123)


        #Button Add| Update Cart
        bnt_add_upadate_Cart = ctk.CTkButton(Add_Cart_Frame, text="Add|Update Cart", command=self.add_updatecart, font=("goudy old style", 15, "bold"),
                             fg_color="Orange",
                             text_color="Black",
                             hover_color="#FFCC33",
                             corner_radius=8,
                             width=140, height=30)

        bnt_add_upadate_Cart.place(x=450, y=123)                                                                                             

        # Store Frame
        StoreBill_Frame = Frame(self.root, bd=8, relief=RIDGE, bg='#FFFFFF')
        StoreBill_Frame.place(x=1305, y=70, width=610, height=1000)

        # Title
        title = Label(StoreBill_Frame, text="Store Bill Area", font=("goudy old style", 28, "bold"), bg="red", fg="white", padx=23, pady=9)
        title.pack(side=TOP, fill=X)
        
        # Thanh cuộn dọc
        scrooly_y = Scrollbar(StoreBill_Frame, orient=VERTICAL)
        # Thanh cuộn ngang
        scrooly_x = Scrollbar(StoreBill_Frame, orient=HORIZONTAL)

        # Text widget (với padding, căn sát bên trái, wrap=NONE để cho phép cuộn ngang)
        self.txt_bill_area = Text(StoreBill_Frame, yscrollcommand=scrooly_y.set, xscrollcommand=scrooly_x.set, 
                                wrap=NONE, padx=10, pady=10, font=("Courier New", 10), width=50, height=20)
        self.txt_bill_area.pack(fill=BOTH, expand=1)

        # Cấu hình thanh cuộn dọc
        scrooly_y.config(command=self.txt_bill_area.yview)
        scrooly_y.pack(side=RIGHT, fill=Y)

        # Cấu hình thanh cuộn ngang
        scrooly_x.config(command=self.txt_bill_area.xview)
        scrooly_x.pack(side=BOTTOM, fill=X)

        #Billing button
        btn_Store_Frame= Frame(StoreBill_Frame, bd=7, relief=RIDGE, bg='#FFFFFF')
        btn_Store_Frame.place(x=0, y=768, width=600, height=220)

        self.lbl_billing_amount= Label(btn_Store_Frame, text="Total Price\n[0]", font=("goudy old style", 18, "bold"), bg="#3f51b5", fg="white")
        self.lbl_billing_amount.place(x=0, y=0, width=200, height=100)

        self.lbl_discount= Label(btn_Store_Frame, text="Discount\n[0%]", font=("goudy old style", 18, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=200, y=0, width=190, height=100)

        self.lbl_netpay= Label(btn_Store_Frame, text="Net Pay\n[0]", font=("goudy old style", 18, "bold"), bg="#607d8b", fg="white")
        self.lbl_netpay.place(x=390, y=0, width=200, height=100)

        self.btn_print =ctk.CTkButton(btn_Store_Frame, text="Print", command=self.print_bill,
                           font=("Goudy Old Style", 18, "bold"), 
                           fg_color="#33CC00", text_color="white", 
                           hover_color="#339900",  # Màu khi hover
                           corner_radius=8,  # Bo góc cho nút
                           cursor="hand2", width=160, height=80)
        self.btn_print.place(x=0, y=85)


        self.btn_ClearAll = ctk.CTkButton(btn_Store_Frame, text="Clear All", command=self.clear_all,
                                    font=("Goudy Old Style", 18, "bold"), 
                                    fg_color="gray", text_color="white", 
                                    hover_color="#B3B3B3",  # Màu khi hover
                                    corner_radius=8,  # Bo góc cho nút
                                    cursor="hand2", width=150, height=80)
        self.btn_ClearAll.place(x=165, y=85)



        self.btn_Generate= ctk.CTkButton(btn_Store_Frame, text="Generate/Save Bill", command=self.generate_bill, font=("goudy old style", 18, "bold"),
                                    fg_color="#009688",
                                    text_color="white", 
                                    hover_color='#00695C',
                                    corner_radius=8,
                                    cursor="hand2" , width=130, height=80)
        self.btn_Generate.place(x=320, y=85)  

#=============def Calculator================
    # Hàm xử lý nhập liệu (cập nhật giá trị vào cuối nội dung)
    def get_input(self, num):
        self.txt_cal_input.config(state='normal')  # Chuyển trạng thái thành 'normal' để cập nhật
        current_input = self.txt_cal_input.get("1.0", "end-1c")  # Lấy giá trị hiện tại trong Text widget
        new_input = current_input + str(num)  # Thêm giá trị nút bấm vào
        self.txt_cal_input.delete("1.0", "end")  # Xóa toàn bộ văn bản hiện tại
        self.txt_cal_input.insert("end", new_input)  # Thêm giá trị mới vào cuối

        # Đặt con trỏ vào cuối văn bản
        self.txt_cal_input.mark_set("insert", "end")
        self.txt_cal_input.see("end")

        self.txt_cal_input.config(state='disable')  # Chuyển lại trạng thái thành 'disable'


#==================def delete last characters===================
    def delete_last_char(self):
        self.txt_cal_input.config(state='normal')  # Mở khóa Text widget
        current_input = self.txt_cal_input.get("1.0", "end-1c")  # Lấy giá trị hiện tại
        if current_input:  # Nếu không trống
            new_input = current_input[:-1]  # Xóa ký tự cuối cùng
            self.txt_cal_input.delete("1.0", "end")  # Xóa toàn bộ văn bản hiện tại
            self.txt_cal_input.insert("end", new_input)  # Thêm giá trị mới vào
        self.txt_cal_input.config(state='disable')  # Khóa lại Text widget


#===============;l===def clear calculator=====================
    def clear_cal(self):
        self.txt_cal_input.config(state='normal')  # Mở khóa Text widget
        self.txt_cal_input.delete("1.0", "end")    # Xóa toàn bộ nội dung
        self.txt_cal_input.config(state='disabled')  # Khóa lại Text widget sau khi xóa

#==================def Performamce=====================
    def performance(self):
        self.txt_cal_input.config(state='normal')  # Mở khóa Text widget để thực hiện thao tác
        current_input = self.txt_cal_input.get("1.0", "end-1c").strip()  # Lấy giá trị hiện tại trong Text widget và xóa khoảng trắng

        # Thêm dấu '*' giữa số và dấu '(' hoặc dấu ')' và số nếu cần thiết
        current_input = self.add_multiplication_sign(current_input)

        # Kiểm tra lỗi nếu ký hiệu '%' được dùng không hợp lệ, chỉ cho phép 9%(3) nhưng không cho phép 9%3
        if re.search(r'\d+\s*%\s*\d+(?!\()', current_input):  # Phát hiện trường hợp 9%3 mà không có dấu ngoặc sau
            self.txt_cal_input.delete("1.0", "end")
            self.txt_cal_input.insert("end", "Error: Invalid % operation")
            self.txt_cal_input.config(state='disabled')
            return

        # Kiểm tra lỗi nếu không có phép toán giữa các dấu ngoặc hoặc số (ví dụ: (8+1)(5+3))
        if re.search(r'\)\s*\(', current_input):
            current_input = re.sub(r'\)\s*\(', ')*(', current_input)

        # Thay thế các ký hiệu nhân và chia bằng các ký hiệu mà Python hiểu được
        current_input = current_input.replace('x', '*').replace('÷', '/')

        # Kiểm tra các phép toán không hợp lệ như **, //, */, /*
        if re.search(r'\d\s*(\*\*|//|\*/|/\*)\s*\d', current_input):
            self.txt_cal_input.delete("1.0", "end")
            self.txt_cal_input.insert("end", "Error:")
            self.txt_cal_input.config(state='disabled')
            return

        try:
            # Tính toán kết quả
            result = eval(current_input)

            # Xóa toàn bộ nội dung hiện tại để chỉ giữ lại kết quả
            self.txt_cal_input.delete("1.0", "end")

            # Hiển thị kết quả đã căn phải
            formatted_result = str(result)
            self.txt_cal_input.insert("end", formatted_result)

            # Lưu kết quả để có thể tiếp tục tính toán
            self.last_result = result

            # Đặt con trỏ vào cuối văn bản
            self.txt_cal_input.mark_set("insert", "end")
            self.txt_cal_input.see("end")

            # Đặt cờ đánh dấu đã hiển thị kết quả
            self.result_displayed = True
        except Exception as e:
            # Hiển thị lỗi nếu biểu thức không hợp lệ
            self.txt_cal_input.delete("1.0", "end")
            self.txt_cal_input.insert("end", f"Error:")

        self.txt_cal_input.config(state='disabled')  # Khóa lại Text widget sau khi tính toán


#===============def add_multiplication_sign================: Hàm tự đông hiểu 7(5+3) hoặc (5+3)7 là 7*(5+3)
    def add_multiplication_sign(self, expression):
         # Thêm dấu '*' giữa số và dấu '('
        expression = re.sub(r'(\d)(\()', r'\1*\2', expression)
        
        # Thêm dấu '*' giữa dấu ')' và số
        expression = re.sub(r'(\))(\d)', r'\1*\2', expression)
        
        # Thay thế '%' thành '/100' nếu cần thiết
        expression = expression.replace('%', '/100')

        return expression

#====================def fetch_store_data======================
    def fetch_store_data(self, StoreFrame):
        try:
            # Kết nối tới SQL Server
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT Store_ID, Store_Name, Address, Phone_number FROM Store")
            rows = cursor.fetchall()

            # Khung chứa Listbox và thanh cuộn
            listbox_frame = Frame(StoreFrame)
            listbox_frame.place(x=0, y=40, width=750, height=125)

            # Tạo thanh cuộn dọc và ngang
            scrollbar_y = Scrollbar(listbox_frame, orient=VERTICAL)
            scrollbar_x = Scrollbar(listbox_frame, orient=HORIZONTAL)

            # Tạo Listbox với thanh cuộn
            self.listbox = Listbox(
                listbox_frame, font=("Times new roman", 18), bg="white", selectmode=SINGLE,
                yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, width=80
            )
            self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

            # Cấu hình thanh cuộn
            scrollbar_y.config(command=self.listbox.yview)
            scrollbar_y.pack(side=RIGHT, fill=Y)
            scrollbar_x.config(command=self.listbox.xview)
            scrollbar_x.pack(side=BOTTOM, fill=X)

            # Thêm từng hàng chứa Store_ID, Store_Name, Address, Contact vào Listbox với khoảng cách giữa các dòng
            for row in rows:
                store_info = f"{row[0]} - {row[1]} - {row[2]} - {row[3]}"
                self.listbox.insert(END, store_info)

            # Đóng kết nối
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")

#=================def show===================
    def show(self):
        try:
            # Kết nối đến SQL Server với mã hóa UTF-8
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
                'charset=UTF8;'  # Thêm chỉ định mã hóa UTF-8
            )
            cursor = conn.cursor()

            # Truy vấn lấy dữ liệu từ bảng Products, nối với bảng Category và Supplier để lấy thông tin Category Name và Supplier Name
            # Chỉ lấy những sản phẩm có trạng thái 'Active'
            query = """
            SELECT P.Product_ID, P.Product_Name, P.Price, P.Quantity, P.Status, C.Category_ID, C.Category_Name, S.Sup_Name 
            FROM Product P
            JOIN Category C ON P.Category_ID = C.Category_ID
            JOIN Supplier S ON C.Sup_ID = S.Sup_ID
            WHERE P.Status = 'Active'
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Xóa tất cả dữ liệu cũ trong Treeview
            self.ProductTable.delete(*self.ProductTable.get_children())

            # Thêm dữ liệu vào Treeview
            for row in rows:
                # Chuyển dữ liệu sang UTF-8 nếu cần thiết
                utf8_row = tuple(str(item).encode('utf-8', 'ignore').decode('utf-8') if isinstance(item, str) else item for item in row)
                self.ProductTable.insert("", "end", values=utf8_row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            if conn:
                conn.close()


#=================def get_data()====================
    def get_data(self, ev):
     conn=None
     try:
        # Lấy dòng hiện tại được chọn trong Treeview
        f = self.ProductTable.focus()
        content = self.ProductTable.item(f)
        row = content['values']

        if row:
            self.var_product_id.set(row[0])  # Đảm bảo Product_ID được lấy từ Treeview
            self.var_pName.set(row[1])       # Thiết lập Product Name
            self.var_pPrice.set(row[2])      # Thiết lập Price
            stock_quantity = row[3]          # Lấy số lượng hàng tồn kho
            self.lbl_Stock.config(text=f"In Stock [{str(stock_quantity)}]")  # Hiển thị số lượng hàng tồn kho

            # Kết nối đến cơ sở dữ liệu để lấy đường dẫn hình ảnh
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Truy vấn đường dẫn hình ảnh dựa trên Product_ID
            cursor.execute("SELECT Image FROM Product WHERE Product_ID = ?", (self.var_product_id.get(),))
            image_path = cursor.fetchone()

            # Kiểm tra kết quả truy vấn
            if image_path and image_path[0]:
                image_path = image_path[0]  # Đường dẫn ảnh
                try:
                    # Mở hình ảnh và xử lý
                    img = Image.open(image_path).convert("RGBA")

                    # Xử lý nền xám thành nền trắng
                    datas = img.getdata()
                    new_data = []
                    for item in datas:
                        if item[0] >= 215 and item[1] >= 210 and item[2] >= 210:
                            new_data.append((255, 255, 255, item[3]))  # Chuyển sang trắng
                        else:
                            new_data.append(item)
                    img.putdata(new_data)

                    # Cắt viền dưới cùng và resize ảnh
                    width, height = img.size
                    img = img.crop((0, 0, width, height - 2))
                    img = img.resize((210, 170), Image.Resampling.LANCZOS)
                    self.img = ImageTk.PhotoImage(img)

                    # Hiển thị ảnh
                    if not hasattr(self, 'lbl_img'):
                        self.lbl_img = Label(self.root, image=self.img, bg="#FFFFFF", bd=0)
                        self.lbl_img.place(x=150, y=860)  # Thay đổi vị trí nếu cần
                    else:
                        self.lbl_img.config(image=self.img)
                        self.lbl_img.image = self.img
                except Exception as img_err:
                    messagebox.showerror("Error", f"Failed to open or process image: {img_err}", parent=self.root)
            else:
                # Thông báo nếu không có đường dẫn hình ảnh hợp lệ
                messagebox.showerror("Error", "No image found for the selected product ID", parent=self.root)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    
     finally:
            # Đảm bảo đóng kết nối sau khi truy vấn xong
              if conn:
                    conn.close()

#===================def Search================
    def search(self):
     try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )
        cursor = conn.cursor()

        search_by = self.var_searchby.get()
        search_text = self.var_searchtxt.get().strip()  # Xóa khoảng trắng thừa

        # Kiểm tra tùy chọn tìm kiếm
        if search_by == "Search by":
            self.show()  # Gọi hàm show để lấy lại tất cả dữ liệu
            return

        # Tạo truy vấn với JOIN để lấy đầy đủ thông tin từ các bảng
        query = """
            SELECT P.Product_ID, P.Product_Name, P.Price, P.Quantity, P.Status, 
                   P.Category_ID, C.Category_Name, S.Sup_Name
            FROM Product P
            LEFT JOIN Category C ON P.Category_ID = C.Category_ID
            LEFT JOIN Supplier S ON C.Sup_ID = S.Sup_ID
            WHERE P.Status = 'Active'
        """

        # Thêm điều kiện WHERE vào truy vấn dựa trên tùy chọn tìm kiếm
        if search_by == "Product.ID":
            query += " AND P.Product_ID = ?"
            params = (search_text,)
        elif search_by == "Product Name":
            query += " AND P.Product_Name LIKE ?"
            params = (f'%{search_text}%',)
        elif search_by == "Status (Active)":
            params = ()  # Already filtering active products in the main query
        else:
            messagebox.showerror("Error", "Invalid search option", parent=self.root)
            return

        # Thực thi truy vấn
        cursor.execute(query, params)

        # Lấy kết quả truy vấn
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ trong Treeview
        self.ProductTable.delete(*self.ProductTable.get_children())

        if rows:
            for row in rows:
                # Chuyển đổi dữ liệu sang định dạng UTF-8 nếu cần thiết
                row_utf8 = [str(item).encode('utf-8').decode('utf-8') if isinstance(item, str) else item for item in row]
                
                # Thêm dữ liệu vào Treeview
                self.ProductTable.insert("", "end", values=row_utf8)
        else:
            messagebox.showinfo("Info", "No records found", parent=self.root)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
     finally:
        if conn:
            conn.close()


#================def add|update cart=============
    def add_updatecart(self):
        if self.var_product_id.get() == '':
            messagebox.showerror('Error', "Please select a product from the list", parent=self.root)

        elif self.var_pQuantity.get() == '':
            messagebox.showerror('Error', "Quantity is required", parent=self.root)
        else:
            try:
                # Kết nối đến SQL Server
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                    'DATABASE=QuanLyTonKho;'
                    'UID=sa;'
                    'PWD=182003;'
                )
                cursor = conn.cursor()

                # Truy vấn số lượng tồn kho từ cơ sở dữ liệu
                cursor.execute("SELECT Quantity FROM Product WHERE Product_ID = ?", (self.var_product_id.get(),))
                result = cursor.fetchone()

                if result:
                    stock_quantity = int(result[0])  # Số lượng tồn kho trong kho
                    requested_quantity = int(self.var_pQuantity.get())  # Số lượng người dùng nhập

                    # Kiểm tra số lượng yêu cầu có lớn hơn số lượng tồn kho không
                    if requested_quantity > stock_quantity:
                        messagebox.showerror('Error', f"Insufficient stock! Only {stock_quantity} items available.", parent=self.root)
                        return
                    else:
                        # Tính toán giá tiền (giá chưa giảm)
                        price_cal = requested_quantity * float(self.var_pPrice.get())
                        
                        # Lấy giá trị discount từ Spinbox và tính toán
                        discount_percentage = float(self.var_pDiscount.get())  # Giá trị Discount từ Spinbox
                        discount_amount = (discount_percentage / 100) * price_cal  # Số tiền giảm
                        net_price = price_cal - discount_amount  # Giá cuối cùng sau discount

                        # Tạo cart_data bao gồm giá ban đầu (price_cal) và giá giảm (net_price)
                        cart_data = [
                            self.var_product_id.get(),  # Product ID
                            self.var_pName.get(),        # Product Name
                            f"{price_cal:.2f}",          # Tổng tiền (giá ban đầu, trước khi giảm giá)
                            self.var_pQuantity.get(),    # Số lượng
                            self.var_status.get(),       # Trạng thái
                            f"{discount_percentage}%"    # Phần trăm giảm giá
                        ]

                        # ============== Update Cart =================
                        present = 'no'
                        index = 0
                        for row in self.cart_list:
                            if self.var_product_id.get() == row[0]:
                                present = 'yes'
                                break
                            index += 1

                        if present == 'yes':
                            op = messagebox.askyesno('Confirm', "Product already present! \nDo you want to update or remove it from the Cart List?", parent=self.root)
                            if op:
                                if self.var_pQuantity.get() == '0':
                                    self.cart_list.pop(index)  # Xóa sản phẩm nếu số lượng là 0
                                else:
                                    # Cập nhật số lượng và giá tiền
                                    self.cart_list[index][3] = self.var_pQuantity.get()  # Cập nhật số lượng
                                    self.cart_list[index][2] = f"{price_cal:.2f}"  # Cập nhật giá ban đầu
                                    self.cart_list[index][5] = f"{discount_percentage}%"  # Cập nhật phần trăm giảm giá
                        else:
                            self.cart_list.append(cart_data)  # Thêm sản phẩm mới vào giỏ hàng

                        self.show_cart()  # Hiển thị lại giỏ hàng
                        self.bill_update()  # Cập nhật hóa đơn
                else:
                    messagebox.showerror('Error', "Product not found in database!", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
            finally:
                if conn:
                    conn.close()



#===============def showw cart====================
    def show_cart(self):
        # Clear the current content in the CartTable Treeview
        self.CartTable.delete(*self.CartTable.get_children())

        # Sort the cart_list by Product.ID in ascending order
        sorted_cart_list = sorted(self.cart_list, key=lambda item: item[0])  # Sort by Product.ID (item[0])

        # Loop through the sorted cart_list and insert each item into the Treeview
        for item in sorted_cart_list:
            product_id = item[0]        # Product ID
            product_name = item[1]      # Product Name
            total_price = float(item[2])  # Total Price (calculated after discount)
            quantity = int(item[3])     # Quantity
            status = "Active"           # Assuming all items are available; adjust based on your logic if needed
            discount = item[5]          # Discount Percentage (e.g., "10%")

            # Insert data into the CartTable
            self.CartTable.insert("", "end", values=(product_id, product_name, f"{total_price:.2f}", quantity, status, discount))


#======================def get_data_cart===================
    def get_data_cart(self, event):
        # Lấy hàng được chọn từ Treeview CartTable
        selected_row = self.CartTable.focus()  # Lấy ID của hàng được chọn
        content = self.CartTable.item(selected_row)  # Lấy nội dung của hàng
        row = content['values']  # Trích xuất giá trị từ hàng

        if row:
            # Gán giá trị cho các biến liên quan đến Entry/Spinbox
            self.var_product_id.set(row[0])      # Gán Product ID
            self.var_pName.set(row[1])          # Gán Product Name
            self.var_pQuantity.set(row[3])      # Gán Quantity

            # Lấy giá trị discount từ hàng (giả định cột Discount là cột thứ 6 - index 5)
            try:
                discount_value = row[5]  # Discount nằm ở cột thứ 6
                if discount_value is None or discount_value == "":
                    self.var_pDiscount.set(0)  # Gán giá trị mặc định là 0 nếu không có dữ liệu
                else:
                    # Loại bỏ ký tự '%' nếu tồn tại và chuyển đổi giá trị thành số
                    discount_cleaned = discount_value.replace('%', '').strip()
                    discount = int(float(discount_cleaned))  # Chuyển đổi thành số nguyên
                    self.var_pDiscount.set(discount)  # Hiển thị discount trên Spinbox
            except (ValueError, IndexError) as e:
                messagebox.showerror("Error", "Invalid discount value in cart", parent=self.root)
                self.var_pDiscount.set(0)  # Đặt giá trị mặc định nếu lỗi xảy ra
                return

            # Tính toán và gán giá trị giá tiền/đơn vị (Price per unit)
            try:
                total_price = float(row[2])  # Lấy Total Price
                quantity = int(row[3])       # Lấy Quantity
                if quantity > 0:
                    initial_price = total_price / quantity
                    self.var_pPrice.set(f"{initial_price:.2f}")  # Hiển thị giá mỗi sản phẩm
                else:
                    self.var_pPrice.set("0.00")  # Xử lý trường hợp quantity = 0
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Invalid price or quantity in cart", parent=self.root)
                self.var_pPrice.set("0.00")  # Đặt giá trị mặc định nếu lỗi xảy ra
                return

            # Lấy và hiển thị hình ảnh, số lượng tồn kho dựa vào Product ID
            product_id = row[0]
            try:
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                    'DATABASE=QuanLyTonKho;'
                    'UID=sa;'
                    'PWD=182003;'
                )
                cursor = conn.cursor()

                # Truy vấn để lấy đường dẫn ảnh và số lượng tồn kho từ Product
                cursor.execute("SELECT Image, Quantity FROM Product WHERE Product_ID = ?", (product_id,))
                result = cursor.fetchone()

                if result:
                    image_path, stock_quantity = result
                    self.lbl_Stock.config(text=f"In Stock [{stock_quantity}]")  # Hiển thị số lượng tồn kho

                    if image_path:  # Nếu có đường dẫn ảnh
                        try:
                            # Xử lý hình ảnh
                            img = Image.open(image_path).convert("RGBA")
                            datas = img.getdata()
                            new_data = [
                                (255, 255, 255, item[3]) if item[0] >= 215 and item[1] >= 210 and item[2] >= 210 else item
                                for item in datas
                            ]
                            img.putdata(new_data)
                            img = img.resize((200, 160), Image.Resampling.LANCZOS)
                            self.img = ImageTk.PhotoImage(img)

                            # Hiển thị ảnh trong Label
                            if not hasattr(self, 'lbl_img'):
                                self.lbl_img = Label(self.root, image=self.img, bg="white", bd=0)
                                self.lbl_img.place(x=130, y=680)
                            else:
                                self.lbl_img.config(image=self.img)
                                self.lbl_img.image = self.img
                        except Exception as img_err:
                            messagebox.showerror("Error", f"Failed to open or process image: {img_err}", parent=self.root)
                    else:
                        messagebox.showwarning("Warning", "No image found for the selected product ID", parent=self.root)
                else:
                    messagebox.showwarning("Warning", "Product data not found", parent=self.root)
            except Exception as db_err:
                messagebox.showerror("Error", f"Database error: {db_err}", parent=self.root)
            finally:
                if conn:
                    conn.close()



#=================def bill update================      
    def bill_update(self):
        # Đặt lại giá trị ban đầu
        self.bill_amt = 0.0  # Tổng tiền chưa giảm
        self.netpay = 0.0    # Tổng thanh toán sau giảm giá
        self.total_quantity = 0  # Tổng số lượng sản phẩm
        self.discount_amount = 0.0  # Tổng tiền giảm giá

        # Kiểm tra nếu TreeView giỏ hàng rỗng
        if not self.CartTable.get_children():  # Nếu không có sản phẩm trong TreeView
            self.lbl_billing_amount.config(text="Total Price\n0.00")
            self.lbl_discount.config(text="Discount\n0.00")
            self.lbl_netpay.config(text="Net Pay\n0.00")
            self.title_Cart.config(text="Cart \t Total Product: [0]")
            return

        # Tính toán lại giá trị từ TreeView
        for child in self.CartTable.get_children():
            row = self.CartTable.item(child, 'values')  # Lấy giá trị của từng hàng
            try:
                # Ép kiểu dữ liệu từ TreeView
                price_per_unit = float(row[2]) if row[2] else 0.0  # Giá mỗi sản phẩm (Total Price từ TreeView)
                quantity = int(row[3]) if row[3] else 0  # Số lượng
                discount_percentage = float(row[5].replace('%', '')) if row[5] else 0.0  # Discount (%)

                # Tính tổng giá trị từng sản phẩm và các giá trị khác
                total_price_product = price_per_unit  # Tổng giá trị lấy trực tiếp từ cột Total Price
                discount_amount_product = total_price_product * (discount_percentage / 100)  # Số tiền giảm giá
                final_price_product = total_price_product - discount_amount_product  # Giá cuối sau giảm giá

                # Cộng dồn các giá trị
                self.bill_amt += total_price_product  # Tổng giá trị từ TreeView
                self.discount_amount += discount_amount_product  # Tổng tiền giảm giá
                self.netpay += final_price_product  # Tổng tiền sau giảm giá
                self.total_quantity += quantity  # Tổng số lượng sản phẩm
            except (ValueError, TypeError) as e:
                print(f"Error parsing row: {row}, Error: {e}")  # Debug thông tin lỗi

        # Cập nhật các Label
        self.lbl_billing_amount.config(text=f"Total Price\n{self.bill_amt:.2f}")  # Tổng giá trị
        self.lbl_discount.config(text=f"Discount\n{self.discount_amount:.2f}")  # Tổng tiền giảm giá
        self.lbl_netpay.config(text=f"Net Pay\n{self.netpay:.2f}")  # Tổng tiền sau giảm giá
        self.title_Cart.config(text=f"Cart \t Total Product: [{self.total_quantity}]")  # Tổng sản phẩm


#=======================def generate_bill===================
    def generate_bill(self):
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please add products to Cart!", parent=self.root)
            return

        try:
            # Kết nối đến SQL Server
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Tạo mã hóa đơn ngẫu nhiên
            invoice = f"{random.randint(100000, 999999)}"

            # Lấy mã số nhân viên và tên nhân viên từ Entry
            Emp_No = self.var_empNo.get()
            emp_name = self.var_empName.get()

            # Tạo header cho hóa đơn
            bill_top_temp = f'''Invoice.No: {invoice}
Emp.No: {Emp_No}
Employee Name: {emp_name}
Date: {time.strftime("%d/%m/%Y")}
Time: {time.strftime("%H:%M:%S")}
{'='*95}
'''

            # Lấy chỉ mục cửa hàng từ Listbox
            selected_index = self.listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a store from the Listbox!", parent=self.root)
                return

            selected_store = self.listbox.get(selected_index[0])
            store_info = selected_store.split(' - ')

            # Thông tin cửa hàng
            store_details = f'''Store.ID: {store_info[0]}
Store Name: {store_info[1]}
Address: {store_info[2]}
Phone number: {store_info[3]}
{'='*95}
Product Name                                     Price               Quantity         Discount
'''

            # Hiển thị xác nhận trước khi tạo hóa đơn
            confirm = messagebox.askyesno("Confirm", "Are you sure to generate bill?", parent=self.root)
            if not confirm:
                return  # Dừng nếu người dùng chọn "No"

            # Xóa nội dung cũ và in phần đầu hóa đơn
            self.txt_bill_area.delete("1.0", END)
            self.txt_bill_area.tag_configure("left", justify="left", lmargin1=0, lmargin2=0, spacing1=1)
            self.txt_bill_area.tag_configure("default_font", font=("Courier New", 10))
            self.txt_bill_area.insert("1.0", bill_top_temp, ("left", "default_font"))
            self.txt_bill_area.insert("end", store_details, ("left", "default_font"))

                # ==================== Phần giữa hóa đơn ====================
            name_width = 30
            price_width = 20  # Tăng chiều rộng của cột Price
            quantity_width = 15  # Tăng chiều rộng của cột Quantity
            discount_width = 15  # Tăng chiều rộng của cột Discount

            sorted_cart_list = sorted(self.cart_list, key=lambda row: row[0])  # Sắp xếp theo Product.ID

            for row in sorted_cart_list:
                # Lấy dữ liệu từ cart_list
                product_id = row[0]  # Product ID
                name = row[1]  # Product Name
                quantity = int(row[3])  # Quantity
                price = float(row[2])  # Tổng giá
                discount = float(row[5].replace('%', '').strip())  # Xử lý Discount để loại bỏ ký tự %

                # Tính giá trị sau giảm giá
                discounted_price = price - (price * discount / 100)

                # Đảm bảo các cột đều thẳng hàng với nhau
              # Thêm khoảng trắng vào trước các giá trị Quantity và Discount để chúng nhích về bên trái một chút
                formatted_line = f"{name:<{name_width}}{price:>{price_width+8}.2f}{' ' * (quantity_width - 14)}{quantity:>{quantity_width}}{' ' * (discount_width - 13)}{discount:>{discount_width}}%"


                # Thêm dòng sản phẩm vào 'txt_bill_area'
                self.txt_bill_area.insert("end", "\n" + formatted_line, ("left", "default_font"))

                # Cập nhật số lượng trong bảng Product
                cursor.execute(
                    "UPDATE Product SET Quantity = Quantity - ? WHERE Product_ID = ? AND Quantity >= ?",
                    (quantity, product_id, quantity)
                )

                # Kiểm tra và cập nhật số lượng tồn kho
                cursor.execute("SELECT Quantity FROM Product WHERE Product_ID = ?", (product_id,))
                updated_quantity = cursor.fetchone()
                if updated_quantity:
                    self.lbl_Stock.config(text=f"In Stock [{updated_quantity[0]}]")

                # Kiểm tra nếu sản phẩm không đủ tồn kho
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", f"Product ID {product_id} does not have enough in stock.", parent=self.root)
                    conn.rollback()
                    return


            # ==================== Phần cuối hóa đơn ====================
            bill_bottom_temp = f'''
\n\n\n{'='*95}
Total Price: \t\t\t{self.bill_amt:.2f}
Discount: \t\t\t-{self.discount_amount:.2f}
Net Pay: \t\t\t{self.netpay:.2f}
'''
            self.txt_bill_area.insert("end", bill_bottom_temp, ("left", "default_font"))

            # Đường dẫn thư mục và file
            bill_folder = Path("C:/Đồ án Python/bill_exported")
            bill_path = bill_folder / f"Invoice.No.{invoice}.txt"

            # Kiểm tra và tạo thư mục nếu chưa tồn tại
            try:
                bill_folder.mkdir(parents=True, exist_ok=True)  # Tạo thư mục (nếu chưa tồn tại)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create folder '{bill_folder}' due to: {str(e)}", parent=self.root)
                return

            # Ghi nội dung từ Text Widget vào file
            try:
                with open(bill_path, 'w', encoding='utf-8') as bill_file:
                    bill_content = self.txt_bill_area.get("1.0", "end-1c")  # Lấy nội dung từ Text Widget
                    bill_file.write(bill_content)  # Ghi nội dung vào file
                    self.bill_file_path = bill_path  # Lưu đường dẫn file để in sau này
                messagebox.showinfo("Success", f"Invoice saved successfully", parent=self.root)

                # Lưu hóa đơn vào bảng Export_Bill
                date_exported = time.strftime("%Y-%m-%d")
                time_exported = time.strftime("%H:%M:%S")
                invoice_sql = f"Invoice.No.{invoice}"
                cursor.execute(
                    """
                    INSERT INTO Export_Bill (Invoice_No, Date_Exported, Time_Exported, Emp_No, Store_ID)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (invoice_sql, date_exported, time_exported, Emp_No, store_info[0])
                )

                conn.commit()
                self.show()

            except Exception as e:
                messagebox.showerror("Error", f"Error while saving file: {str(e)}", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Đảm bảo kết nối được đóng sau khi tất cả thao tác đã hoàn tất
            if conn:
                conn.close()



#=======================def Print========================
    def print_bill(self):
        try:
            # Tạo cửa sổ Toplevel và đảm bảo nó nằm trên cửa sổ Export
            self.modal_window = ctk.CTkToplevel(self.root)
            self.modal_window.geometry("600x400")  # Kích thước cửa sổ Toplevel
            self.modal_window.attributes("-topmost", True)  # Đặt cửa sổ Toplevel lên trên cùng
            self.modal_window.grab_set()  # Giữ focus cho cửa sổ này
            self.modal_window.lift()  # Đảm bảo cửa sổ modal luôn nằm trên cửa sổ chính
            self.modal_window.deiconify()  # Chắc chắn cửa sổ Toplevel được hiển thị

            # Cập nhật giao diện trước khi mở hộp thoại chọn file
            self.root.update_idletasks()  # Cập nhật giao diện trước khi mở hộp thoại
            # Mở hộp thoại để chọn file
            bill_file_path = filedialog.askopenfilename(
                parent=self.modal_window,  # Đặt hộp thoại thuộc Toplevel tạm thời
                title="Select Bill File",
                initialdir="C:/Đồ án Python/bill_exported",  # Đường dẫn đến thư mục hóa đơn
                filetypes=[("Text files", "*.txt")]  # Lọc chỉ hiển thị file .txt
            )

            # Sau khi chọn file, đóng cửa sổ modal và tiếp tục xử lý
            self.modal_window.grab_release()  # Giải phóng focus của cửa sổ Toplevel
            self.modal_window.destroy()  # Đóng cửa sổ Toplevel

            if bill_file_path:  # Nếu người dùng chọn file
                if os.path.exists(bill_file_path):  # Kiểm tra file có tồn tại không
                    # Mở và đọc nội dung file
                    with open(bill_file_path, "r", encoding="utf-8") as file:
                        file_content = file.read()

                    # Hiển thị nội dung file trong widget Text
                    self.txt_bill_area.delete(1.0, "end")  # Xóa nội dung cũ (nếu có)
                    self.txt_bill_area.insert("end", file_content)  # Chèn nội dung file vào widget Text

                    # Mở file để in
                    os.startfile(bill_file_path, "print")

                    # Hiển thị thông báo thông tin sau khi mở file
                    self.root.after(300, lambda: messagebox.showinfo('Print', f"Printing bill from {bill_file_path}...", parent=self.root))
                    
                    # Thông báo in thành công
                    self.root.after(100, lambda: messagebox.showinfo('Success', "Bill printed successfully!", parent=self.root))
                else:
                    messagebox.showerror('Error', "Bill file not found. Please generate the bill first.", parent=self.root)
            else:
                messagebox.showerror('Error', "No file selected. Please select a bill file to print.", parent=self.root)

        except Exception as e:
            # Hiển thị thông báo lỗi nếu xảy ra lỗi trong quá trình
            messagebox.showerror(
                'Error',
                f"An error occurred while printing: {str(e)}",
                parent=self.root
            )

   
#====================def clear_cart=====================
    def clear_cart(self):
        self.var_product_id.set('')
        self.var_pName.set('')
        self.var_pPrice.set('')
        self.var_pQuantity.set('')
        self.var_pDiscount.set("0")
        self.lbl_Stock.configure(text='In Stock')
        self.var_stock.set('')

#====================def clear_all=======================
    def clear_all(self):
        # Kiểm tra nếu Text Widget txt_bill_area trống
        if not self.txt_bill_area.get('1.0', 'end-1c').strip():  # Kiểm tra nội dung trong Text Widget
            messagebox.showerror("Error", "No bill data to clear!", parent=self.root)
            return

        # Xóa toàn bộ sản phẩm trong giỏ hàng
        self.cart_list.clear()  # Xóa danh sách sản phẩm trong giỏ hàng

        # Xóa dữ liệu trong Text Widget hóa đơn
        self.txt_bill_area.delete('1.0', END)  # Xóa toàn bộ nội dung từ đầu đến cuối

        # Xóa chọn trong Listbox (nếu Listbox tồn tại)
        if hasattr(self, "listbox"):  # Kiểm tra nếu self.listbox đã được tạo
            self.listbox.selection_clear(0, END)  # Xóa toàn bộ lựa chọn trong Listbox
        
            # Xóa tất cả các mục trong Treeview (CartTable)
        for item in self.CartTable.get_children():
            self.CartTable.delete(item)  # Xóa mỗi mục trong Treeview
         # Xóa đường dẫn ảnh
        if hasattr(self, 'image_path'):
            del self.image_path  # Xóa biến lưu đường dẫn ảnh

        # Đặt lại hình ảnh về biểu tượng mặc định
        try:
            # Xóa lbl_img nếu đang hiển thị ảnh cũ
            if hasattr(self, 'lbl_img'):
                self.lbl_img.destroy()
                del self.lbl_img  # Xóa hoàn toàn biến `lbl_img

        except Exception as e:
            messagebox.showerror("Error", f"Error loading default icon: {str(e)}", parent=self.root)

        # Reset lại dữ liệu giỏ hàng và cập nhật giao diện
        self.clear_cart()

        # Đặt lại các giá trị liên quan đến hóa đơn
        self.bill_amt = 0
        self.netpay = 0
        self.total_quantity = 0
        self.discount_amount = 0

        # Cập nhật các Label hiển thị trên giao diện
        self.lbl_billing_amount.config(text='Total Price\n[0]')  # Tổng tiền = 0
        self.lbl_netpay.config(text='Net Pay\n[0]')  # Giá trị sau giảm giá = 0
        self.title_Cart.config(text="Cart \t Total Product: [0]")  # Không còn sản phẩm trong giỏ

        # Hiển thị thông báo hoàn tất xóa dữ liệu
        messagebox.showinfo("Clear All", "All data has been cleared successfully!", parent=self.root)
        self.show()
        self.show_cart()

       

#==============sTạo Fullscreen===============
    def toggle_fullscreen(self, event=None): 
        is_fullscreen = self.root.attributes('-fullscreen') 
        self.root.attributes('-fullscreen', not is_fullscreen) 
        self.root.overrideredirect(not is_fullscreen) 
        if not is_fullscreen: 
            screen_width = self.root.winfo_screenwidth() 
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_width}x{screen_height}+0+0") 
        else:
            self.root.state('normal')
    
    
    def exit_fullscreen(self, event=None):
       self.root.attributes('-fullscreen', False) 
       self.root.overrideredirect(False) 
       self.root.state('normal')
    

if __name__ == "__main__":
 
    # Khởi chạy CTk ứng dụng
    root = ctk.CTk()
    obj = ExportClass(root)  # Truyền emp_no vào
    root.mainloop()