from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import sys
import os
import pyodbc
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
from datetime import datetime
from employee import EmployeeClass
from category import CategoryClass
from products import ProductClass
from export import ExportClass
from login import Login_System
from Import import ImportClass
class IMS:
    def __init__(self, root,emp_no,emp_name):
        self.root = root
        self.root.title("Dashboard")
        self.product_open = False  # Biến để theo dõi trạng thái cửa sổ Product
        self.root.config(bg="White")

        # Đặt kích thước cửa sổ để phù hợp với kích thước màn hình 
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Đặt cửa sổ ở kích thước toàn màn hình và che thanh taskbar 
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.overrideredirect(True)  # Sử dụng `overrideredirect` để loại bỏ thanh tiêu đề và viền
    
        # Nút để chuyển đổi chế độ toàn màn hình
        self.root.bind("<F11>", self.toggle_fullscreen)  # Dùng phím F11 để chuyển chế độ toàn màn hình
        self.root.bind("<Escape>", self.exit_fullscreen)  # Dùng phím Esc để thoát toàn màn hình

        # Tạo Frame giả để làm tiêu đề với màu nền xanh
        self.title_frame = Frame(self.root, bg="#00688B")
        self.title_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        # Tạo Label tiêu đề trong Frame
        self.title_label = Label(self.title_frame, text="Inventory Management System | Developed By Quang Vinh", 
                                 font=("Times new roman", 18, "bold"), background="#00688B", foreground="white")
        self.title_label.pack(pady=8)

        # Mở và chỉnh kích thước hình ảnh Logo1
        image = Image.open("C:\Đồ án Python\image\Logo1.jpg")
        image = image.resize((60, 60), Image.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(image)

        # Tạo Label chính với hình ảnh và nội dung
        self.icon_label = Label(self.root, text="Inventory Management System", image=self.icon_title, 
                                compound=LEFT, font=("Times new roman", 40, "bold"), 
                                background="#010c48", foreground="white", anchor="w", padx=30)
        self.icon_label.place(relx=0, rely=0.1, relwidth=1)


        # # Tạo label mới cho thông tin thời gian và ngày tháng
        self.lbl_time = Label(self.title_frame, text="Welcome Manager to go to Inventory Management System", font=("Times new roman", 16), background="#00688B", foreground="white")
        self.lbl_time.pack(pady=10)  # Bạn có thể điều chỉnh vị trí và các thuộc tính khác của label

        self.update_clock()

        self.bnt_logoutframe = Frame(self.root, bd=0, relief=RIDGE, bg="#010c48")
        self.bnt_logoutframe.place(x=1710, y=109, width=210, height=65)

            
        welcome_label = ctk.CTkLabel(
        self.title_frame,
        text=f"Welcome Manager {emp_name}!",  # Nội dung chào mừng
        font=("Times new roman", 20, "italic"),  # In nghiêng
        text_color="#FFD700",  # Màu chữ vàng
        fg_color="#00688B"     # Màu nền xanh giống Frame
    )
        welcome_label.place(x=20, y=55)  # Đặt gần góc trái của Frame, dưới tiêu đề chính

        # Button Logout
        self.btn_logout = ctk.CTkButton(self.bnt_logoutframe, text="Logout", command=self.logout, font=ctk.CTkFont(family="goudy old style", size=18, weight="bold"), 
            fg_color="#FBB117", 
            hover_color="#FDD017",
            text_color="white",
            #border_color="#0099FF",
            #border_width=3,
            cursor="hand2", 
           corner_radius=8, width=110, height=45 )
        self.btn_logout.place(x=45, y=4)


        # self.btn_logout= ctk.CTkButton(self.title_frame, text="Back", command=self.exit_fullscreen, font=ctk.CTkFont(family="Goudy Old Style", size=18, weight="bold"),  # Font chữ
        #     fg_color="#FF9900",  
        #     hover_color="#FFAA33",
        #     text_color="white",
        #     corner_radius=8, width=110, height=40 )
        # self.btn_logout.place(x=1420, y=5)


        # Tạo Menu và logo bên trái
        self.MenuLogo = Image.open("C:\Đồ án Python\image\Hình 1.png")  # Sửa lại tên file hình ảnh nếu cần
        self.MenuLogo = self.MenuLogo.resize((150, 150), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, width=500, bg="white")
        LeftMenu.place(x=0, y=175,height=630)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        # Thêm tiêu đề Menu
        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688")
        lbl_menu.pack(side=TOP, fill=X)

        # Mở và chỉnh kích thước hình ảnh Sidebar icon
        self.icon_side = Image.open("C:\Đồ án Python\image\Side.jpeg")  # Đường dẫn hình ảnh
        self.icon_side = self.icon_side.resize((40, 40), Image.LANCZOS)
        self.icon_side = ImageTk.PhotoImage(self.icon_side)

        self.var_empNo= StringVar(value=emp_no)
        self.var_empName=StringVar(value=emp_name)

        # Điều chỉnh các nút để căn đều
        button_width = 150

        
       # Thêm nút Employee có kèm hình ảnh với CustomTkinter (ctk)
        btn_employee = ctk.CTkButton(LeftMenu, 
                                    text="Employee", 
                                    command=self.employee, 
                                    image=self.icon_side, 
                                    compound="left",  # Tương tự với compound=LEFT trong tkinter
                                    font=("Times New Roman", 18, "bold"), 
                                    fg_color="white",  # Màu nền của nút
                                    hover_color="#F5FFFA",  # Màu khi hover qua nút
                                    border_color="#0099FF",  # Màu viền của nút
                                    border_width=2, 
                                    cursor="hand2", 
                                    width=button_width, 
                                    anchor="w",
                                    corner_radius=8,  # Bán kính góc
                                    text_color="black")  # Màu chữ trong nút
        btn_employee.pack(side="top", fill="x", pady=10)


        # Thêm nút Import có kèm hình ảnh với CustomTkinter (ctk)
        btn_import = ctk.CTkButton(LeftMenu, 
                                    text="Import", 
                                    image=self.icon_side, command=self.Import,
                                    compound="left",  # Tương tự với compound=LEFT trong tkinter
                                    font=("Times New Roman", 18, "bold"), 
                                    fg_color="white",  # Màu nền của nút
                                    hover_color="#FFFAF0",  # Màu khi hover qua nút
                                    border_color="#0099FF",  # Màu viền của nút
                                    border_width=2, 
                                    cursor="hand2", 
                                    width=button_width, 
                                    anchor="w",
                                    corner_radius=8,  # Bán kính góc
                                    text_color="black")  # Màu chữ trong nút
        btn_import.pack(side="top", fill="x", pady=5)



        # Thêm nút Category có kèm hình ảnh với CustomTkinter (ctk)
        btn_category = ctk.CTkButton(LeftMenu, 
                                    text="Category", 
                                    command=self.category, 
                                    image=self.icon_side, 
                                    compound="left",  # Tương tự với compound=LEFT trong tkinter
                                    font=("Times New Roman", 18, "bold"), 
                                    fg_color="white",  # Màu nền của nút
                                    hover_color="#F5FFFA",  # Màu khi hover qua nút
                                    border_color="#0099FF",  # Màu viền của nút
                                    border_width=2, 
                                    cursor="hand2", 
                                    width=button_width, 
                                    anchor="w",
                                    corner_radius=8,  # Bán kính góc
                                    text_color="black")  # Màu chữ trong nút
        btn_category.pack(side="top", fill="x", pady=10)




        # Thêm nút Product có kèm hình ảnh với CustomTkinter (ctk)
        btn_product = ctk.CTkButton(LeftMenu, 
                                    text="Products", 
                                    command=self.products, 
                                    image=self.icon_side, 
                                    compound="left",  # Tương tự với compound=LEFT trong tkinter
                                    font=("Times New Roman", 18, "bold"), 
                                    fg_color="white",  # Màu nền của nút
                                    hover_color="#FFFAF0",  # Màu khi hover qua nút
                                    border_color="#0099FF",  # Màu viền của nút
                                    border_width=2, 
                                    cursor="hand2", 
                                    width=button_width, 
                                    anchor="w",
                                    corner_radius=8,  # Bán kính góc
                                    text_color="black")  # Màu chữ trong nút
        btn_product.pack(side="top", fill="x", pady=10)



    # Thêm nút Export có kèm hình ảnh với CustomTkinter (ctk)
        btn_export = ctk.CTkButton(LeftMenu, 
                                    text="Export", 
                                    command=self.Export, 
                                    image=self.icon_side, 
                                    compound="left",  # Tương tự với compound=LEFT trong tkinter
                                    font=("Times New Roman", 18, "bold"), 
                                    fg_color="white",  # Màu nền của nút
                                    hover_color="#F5FFFA",  # Màu khi hover qua nút
                                    border_color="#0099FF",  # Màu viền của nút
                                    border_width=2, 
                                    cursor="hand2", 
                                    width=button_width, 
                                    anchor="w",
                                    corner_radius=8,  # Bán kính góc
                                    text_color="black")  # Màu chữ trong nút
        btn_export.pack(side="top", fill="x", pady=10)




        # Thêm nút Import có kèm hình ảnh với CustomTkinter (ctk)
        btn_exit = ctk.CTkButton(LeftMenu, 
                                    text="Exit", 
                                    command=self.exit, 
                                    image=self.icon_side, 
                                    compound="left",  # Tương tự với compound=LEFT trong tkinter
                                    font=("Times New Roman", 18, "bold"), 
                                    fg_color="white",  # Màu nền của nút
                                    hover_color="#FFFAF0",  # Màu khi hover qua nút
                                    border_color="#0099FF",  # Màu viền của nút
                                    border_width=2, 
                                    cursor="hand2", 
                                    width=button_width, 
                                    anchor="w",
                                    corner_radius=8,  # Bán kính góc
                                    text_color="black")  # Màu chữ trong nút
        btn_exit.pack(side="top", fill="x", pady=5)


         # Content

#========================Employee==========================
        self.Emp_Frame= Frame(self.root, bd=3, bg="#2C3E50", relief=RIDGE)
        self.Emp_Frame.place(x=300, y=180, height=200, width=300)
 
        # Tải và chỉnh kích thước icon
        icon_path = r"C:\Đồ án Python\image\total_emp.png"  # Đường dẫn hình ảnh
        self.icon_side_emp = Image.open(icon_path)  # Mở hình ảnh
        self.icon_side_emp = self.icon_side_emp.resize((55, 55), Image.LANCZOS)  # Chỉnh kích thước
        self.icon_side_emp = ImageTk.PhotoImage(self.icon_side_emp)  # Chuyển đổi thành PhotoImage

        # Thêm icon vào Frame
        total_emp_icon = Label(self.Emp_Frame, image=self.icon_side_emp, bg="#2C3E50")
        total_emp_icon.pack(pady=10)  # Khoảng cách padding bên trên (tuỳ chỉnh theo ý thích)

        # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        label_title_emp = Label(self.Emp_Frame, text="Total Employee", font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        label_title_emp.pack(pady=5)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        self.label_count_emp = Label(self.Emp_Frame, text="0", font=("Arial", 22, "bold"), bg="#2C3E50", fg="white")
        self.label_count_emp.pack(pady=(8, 0))

        
#=============================Supplier==========================
        self.supplier_Frame= Frame(self.root, bd=3, bg="#ff5722", relief=RIDGE)
        self.supplier_Frame.place(x=650, y=180, height=200, width=300)

        
        # Tải và chỉnh kích thước icon
        icon_path = r"C:\Đồ án Python\image\total_sup.png"  # Đường dẫn hình ảnh
        self.icon_side_supplier = Image.open(icon_path)  # Mở hình ảnh
        self.icon_side_supplier = self.icon_side_supplier.resize((60, 60), Image.LANCZOS)  # Chỉnh kích thước
        self.icon_side_supplier = ImageTk.PhotoImage(self.icon_side_supplier)  # Chuyển đổi thành PhotoImage

         # Thêm icon vào Frame
        total_supplier_icon = Label(self.supplier_Frame, image=self.icon_side_supplier, bg="#ff5722")
        total_supplier_icon.pack(pady=10)  # Khoảng cách padding bên trên (tuỳ chỉnh theo ý thích)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        label_title_supplier = Label(self.supplier_Frame, text="Total Supplier", font=("Arial", 18, "bold"), bg="#ff5722", fg="white")
        label_title_supplier.pack(pady=5)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        self.label_count_supplier = Label(self.supplier_Frame, text="0", font=("Arial", 22, "bold"), bg="#ff5722", fg="white")
        self.label_count_supplier.pack(pady=(8, 0))


#================Category====================
        self.category_Frame= Frame(self.root, bd=3, bg="#009688", relief=RIDGE)
        self.category_Frame.place(x=1000, y=180, height=200, width=300)

        
        # Tải và chỉnh kích thước icon
        icon_path = r"C:\Đồ án Python\image\total_cat.png"  # Đường dẫn hình ảnh
        self.icon_side_category = Image.open(icon_path)  # Mở hình ảnh
        self.icon_side_category = self.icon_side_category.resize((60, 60), Image.LANCZOS)  # Chỉnh kích thước
        self.icon_side_category = ImageTk.PhotoImage(self.icon_side_category)  # Chuyển đổi thành PhotoImage

         # Thêm icon vào Frame
        total_category_icon = Label(self.category_Frame, image=self.icon_side_category, bg="#009688")
        total_category_icon.pack(pady=10)  # Khoảng cách padding bên trên (tuỳ chỉnh theo ý thích)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        label_title_category = Label(self.category_Frame, text="Total Category", font=("Arial", 18, "bold"), bg="#009688", fg="white")
        label_title_category.pack(pady=5)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        self.label_count_category = Label(self.category_Frame, text="0", font=("Arial", 22, "bold"), bg="#009688", fg="white")
        self.label_count_category.pack(pady=(8, 0))

#======================Products======================
        self.product_Frame= Frame(self.root, bd=3, bg="#607d8b", relief=RIDGE)
        self.product_Frame.place(x=300, y=500, height=200, width=300)

        
        # Tải và chỉnh kích thước icon
        icon_path = r"C:\Đồ án Python\image\total_prod.png"  # Đường dẫn hình ảnh
        self.icon_side_product = Image.open(icon_path)  # Mở hình ảnh
        self.icon_side_product = self.icon_side_product.resize((60, 60), Image.LANCZOS)  # Chỉnh kích thước
        self.icon_side_product = ImageTk.PhotoImage(self.icon_side_product)  # Chuyển đổi thành PhotoImage

         # Thêm icon vào Frame
        total_product_icon = Label(self.product_Frame, image=self.icon_side_product, bg="#607d8b")
        total_product_icon.pack(pady=10)  # Khoảng cách padding bên trên (tuỳ chỉnh theo ý thích)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        label_title_product = Label(self.product_Frame, text="Total Products", font=("Arial", 18, "bold"), bg="#607d8b", fg="white")
        label_title_product.pack(pady=5)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        self.label_count_product = Label(self.product_Frame, text="0", font=("Arial", 22, "bold"), bg="#607d8b", fg="white")
        self.label_count_product.pack(pady=(8, 0))

    
#========================Bill Imported======================
        self.Bill_ImporedFrame= Frame(self.root, bd=3, bg="#00BFFF", relief=RIDGE)
        self.Bill_ImporedFrame.place(x=650, y=500, height=200, width=300)

        
        # Tải và chỉnh kích thước icon
        icon_path = r"C:\Đồ án Python\image\total_import.jpg"  # Đường dẫn hình ảnh
        self.icon_side_bill_imp = Image.open(icon_path)  # Mở hình ảnh
        self.icon_side_bill_imp = self.icon_side_bill_imp.resize((60, 60), Image.LANCZOS)  # Chỉnh kích thước
        self.icon_side_bill_imp = ImageTk.PhotoImage(self.icon_side_bill_imp)  # Chuyển đổi thành PhotoImage

         # Thêm icon vào Frame
        bill_imp_icon = Label(self.Bill_ImporedFrame, image=self.icon_side_bill_imp, bg="#00BFFF")
        bill_imp_icon.pack(pady=10)  # Khoảng cách padding bên trên (tuỳ chỉnh theo ý thích)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        label_title_bill_imp = Label(self.Bill_ImporedFrame, text="Total Bill Imported", font=("Arial", 18, "bold"), bg="#00BFFF", fg="white")
        label_title_bill_imp.pack(pady=5)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        self.label_count_bill_imp = Label(self.Bill_ImporedFrame, text="0", font=("Arial", 22, "bold"), bg="#00BFFF", fg="white")
        self.label_count_bill_imp.pack(pady=(8, 0))

#=========================Bill Exported=============================

        self.Bill_ExportedFrame= Frame(self.root, bd=3, bg="#FF4500", relief=RIDGE)
        self.Bill_ExportedFrame.place(x=1000, y=500, height=200, width=300)

        
        # Tải và chỉnh kích thước icon
        icon_path = r"C:\Đồ án Python\image\total_sales.png"  # Đường dẫn hình ảnh
        self.icon_side_bill_export = Image.open(icon_path)  # Mở hình ảnh
        self.icon_side_bill_export = self.icon_side_bill_export.resize((60, 60), Image.LANCZOS)  # Chỉnh kích thước
        self.icon_side_bill_export = ImageTk.PhotoImage(self.icon_side_bill_export)  # Chuyển đổi thành PhotoImage

         # Thêm icon vào Frame
        bill_export_icon = Label(self.Bill_ExportedFrame, image=self.icon_side_bill_export, bg="#FF4500")
        bill_export_icon.pack(pady=10)  # Khoảng cách padding bên trên (tuỳ chỉnh theo ý thích)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        label_title_bill_export = Label(self.Bill_ExportedFrame, text="Total Bill Exported", font=("Arial", 18, "bold"), bg="#FF4500", fg="white")
        label_title_bill_export.pack(pady=5)

         # (Tuỳ chọn) Thêm tiêu đề hoặc chú thích vào Frame
        self.label_count_bill_export = Label(self.Bill_ExportedFrame, text="0", font=("Arial", 22, "bold"), bg="#FF4500", fg="white")
        self.label_count_bill_export.pack(pady=(8, 0))
#================================Diagram===============================
        # self.Diagram_Frame= Frame(self.root, relief=RIDGE)
        # self.Diagram_Frame.place(x=1350, y=180, width=400, height=500)

        self.DiagramFrame = Frame(self.root, relief="flat", bd=0)
        self.DiagramFrame.place(x=1330, y=180, width=580, height=800)

        self.update_diagram()


 #====================================================      
        # Thêm footer
        self.lbl_footer = Label(self.root, text="IMS-Inventory Management System | Developed by Quang Vinh\nContact me: Zalo:0901381780 && Email: zquangvinh359@gmail.com", 
                                font=("Times new roman", 15, "bold"), background="#4d636d", foreground="white")
        self.lbl_footer.pack(side=BOTTOM, fill=X)
        self.update_content()

#====================================================================================================    
    def exit(self):
        sys.exit()

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
 
    
    def update_clock(self):
        now = time.strftime("%d-%m-%Y")
        current_time = time.strftime("%H:%M:%S")
        
        # Cập nhật label thời gian và ngày tháng mới
        self.lbl_time.config(text=f"\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tDate: {now}\t\t\t\tTime: {current_time}")
        
        # Gọi lại sau mỗi 1000 ms (1 giây)
        self.root.after(1000, self.update_clock)  


    def employee(self):
         # Kiểm tra nếu cửa sổ con chưa được mở
        if not hasattr(self, 'new_win') or not self.new_win.winfo_exists():
            self.new_win = ctk.CTkToplevel(self.root)  # Tạo cửa sổ con
            self.new_win.title("Employee Management")  # Đặt tiêu đề cho cửa sổ con

            # Đặt kích thước cửa sổ con
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.new_win.geometry(f"{screen_width}x{screen_height}+0+0")

            # Cho phép thanh tiêu đề và các nút minimize/maximize/close
            self.new_win.overrideredirect(False)
            self.new_win.attributes('-topmost', False)  # Không bắt buộc đặt trên cùng

            # Xử lý sự kiện đóng cửa sổ
            self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)

            # Ràng buộc sự kiện minimize (tùy chọn)
            self.new_win.bind("<Unmap>", self.on_minimize)
            self.new_win.bind("<Map>", self.on_restore)

            # Tạo đối tượng ProductClass và gắn cửa sổ con
            self.new_obj = EmployeeClass(self.new_win)

    
   
   
    def category(self):
       # Kiểm tra nếu cửa sổ con chưa được mở
        if not hasattr(self, 'new_win') or not self.new_win.winfo_exists():
            self.new_win = ctk.CTkToplevel(self.root)  # Tạo cửa sổ con
            self.new_win.title("Category Management")  # Đặt tiêu đề cho cửa sổ con

            # Đặt kích thước cửa sổ con
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.new_win.geometry(f"{screen_width}x{screen_height}+0+0")

            # Cho phép thanh tiêu đề và các nút minimize/maximize/close
            self.new_win.overrideredirect(False)
            self.new_win.attributes('-topmost', False)  # Không bắt buộc đặt trên cùng

            # Xử lý sự kiện đóng cửa sổ
            self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)

            # Ràng buộc sự kiện minimize (tùy chọn)
            self.new_win.bind("<Unmap>", self.on_minimize)
            self.new_win.bind("<Map>", self.on_restore)

            # Tạo đối tượng ProductClass và gắn cửa sổ con
            self.new_obj = CategoryClass(self.new_win)

    
    
    def products(self):
        """
        Tạo cửa sổ con Product nhưng đảm bảo Dashboard luôn hiển thị.
        """
        if not hasattr(self, 'new_win') or not self.new_win.winfo_exists():
            self.new_win = ctk.CTkToplevel(self.root)  # Tạo cửa sổ con
            self.new_win.title("Product Management")  # Tiêu đề cửa sổ con

            # Đặt kích thước cửa sổ con
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.new_win.geometry(f"{screen_width}x{screen_height}+0+0")

            # Đảm bảo cửa sổ Dashboard không bị ẩn
            self.root.attributes('-topmost', True)
            self.new_win.attributes('-topmost', True)

            # Xử lý sự kiện minimize và đóng cửa sổ con
            self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)
            self.new_win.bind("<Unmap>", self.on_minimize)
            self.new_win.bind("<Map>", self.on_restore)  # Khi khôi phục từ minimize
                # Tạo đối tượng ProductClass
            self.new_obj = ProductClass(self.new_win)

            
            
    
    def Import(self):
        """
        Tạo cửa sổ con Import nhưng đảm bảo Dashboard luôn hiển thị mà không bị minimize.
        """
        # Kiểm tra nếu cửa sổ con chưa tồn tại hoặc đã bị đóng
        if not hasattr(self, 'new_win') or not self.new_win.winfo_exists():
            # Tạo cửa sổ con
            self.new_win = ctk.CTkToplevel(self.root)
            self.new_win.title("Import Management")
            
            # Đặt kích thước cửa sổ con bằng toàn màn hình
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.new_win.geometry(f"{screen_width}x{screen_height}+220+30")

            # Đảm bảo Dashboard và cửa sổ Import không bị ẩn
            self.root.attributes('-topmost', True)
            self.new_win.attributes('-topmost', True)

            # Sử dụng `deiconify` để đảm bảo cửa sổ con không bị minimize
            self.new_win.deiconify()

            # Xử lý sự kiện minimize và đóng cửa sổ con
            self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)
            #self.new_win.bind("<Unmap>", self.on_minimize)
            self.new_win.bind("<Map>", self.on_restore)
            
            emp_no= self.var_empNo.get()
            emp_name= self.var_empName.get()
            # Tạo đối tượng ImportClass
            self.new_obj = ImportClass(self.new_win, emp_no, emp_name)

        else:
            # Nếu cửa sổ con đã tồn tại, hiển thị nó
            self.new_win.deiconify()
            self.new_win.lift()  # Đưa cửa sổ con lên trên cùng
            self.new_win.attributes('-topmost', True)  # Đảm bảo không bị ẩn


        

    def Export(self):
        """
        Tạo cửa sổ con Export, đảm bảo có thể minimize mà không mất giao diện.
        """
        if not hasattr(self, 'new_win') or not self.new_win.winfo_exists():
            # Tạo cửa sổ con
            self.new_win = ctk.CTkToplevel(self.root)
            self.new_win.title("Export Management")

            # Đặt kích thước cửa sổ con (full screen)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.new_win.geometry(f"{screen_width}x{screen_height}+0+0")

            # Sử dụng thanh tiêu đề mặc định, không dùng `overrideredirect`
            self.new_win.overrideredirect(False)

            # Đảm bảo Export luôn trên cùng
            self.new_win.attributes('-topmost', True)

            # Xử lý sự kiện đóng hoặc minimize
            self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)
            #self.new_win.bind("<Unmap>", self.on_minimize)  # Sự kiện minimize
            self.new_win.bind("<Map>", self.on_restore)  # Sự kiện khôi phục từ minimize

                # Truyền giá trị emp_no từ Dashboard vào ExportClass
            emp_no = self.var_empNo.get()  # Lấy giá trị emp_no từ Dashboard
            emp_name=self.var_empName.get()
            self.new_obj = ExportClass(self.new_win,emp_no, emp_name)  # Truyền emp_no
            # Đảm bảo thao tác trên Dashboard bị khóa khi Export mở
            self.new_win.grab_set()

    


    def on_restore(self, event=None):
        """
        Xử lý sự kiện khi cửa sổ con được khôi phục từ trạng thái minimize
        """
        if hasattr(self, 'new_win') and self.new_win.winfo_exists():
            # Khi cửa sổ Product được khôi phục, đảm bảo nó hiển thị trên Dashboard
            self.new_win.deiconify()
            self.new_win.lift()  # Đưa cửa sổ con lên trên cùng nếu bị ẩn dưới cửa sổ khác
   
   
    def on_close(self):
            # Đóng cửa sổ con (Export) và hiển thị lại Dashboard
            if hasattr(self, 'new_win') and self.new_win.winfo_exists():
                self.new_win.destroy()  # Đóng cửa sổ Export
            if hasattr(self, 'root') and self.root.winfo_exists():
                self.root.deiconify()  # Hiển thị lại cửa sổ Dashboard 

    def on_minimize(self, event=None):
        """
        Xử lý sự kiện khi cửa sổ con bị minimize.
        """
        if hasattr(self, 'new_win') and self.new_win.winfo_exists():
            self.new_win.iconify()  # Thu nhỏ cửa sổ con
        self.root.attributes('-topmost', True)  # Dashboard vẫn hiển thị trên cùng



#==========================def update content========================
    def update_content(self):
     try:
        # Kết nối đến SQL Server
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )
        cursor = conn.cursor()

        # Truy vấn số lượng sản phẩm
        query1 = "SELECT COUNT(*) FROM Product"
        cursor.execute(query1)
        product_count = cursor.fetchone()[0]  # Lấy số lượng sản phẩm
        self.label_count_product.config(text=f"{str(product_count)}")

        # Truy vấn số lượng nhân viên
        query2 = "SELECT COUNT(*) FROM Employee"
        cursor.execute(query2)
        employee_count = cursor.fetchone()[0]  # Lấy số lượng nhân viên
        self.label_count_emp.config(text=f"{str(employee_count)}")

        # Truy vấn số lượng nhà cung cấp
        query3 = "SELECT COUNT(*) FROM Supplier"
        cursor.execute(query3)
        supplier_count = cursor.fetchone()[0]  # Lấy số lượng nhà cung cấp
        self.label_count_supplier.config(text=f"{str(supplier_count)}")

        # Truy vấn số lượng hóa đơn xuất
        query4 = "SELECT COUNT(*) FROM Export_Bill"
        cursor.execute(query4)
        bill_exported_count = cursor.fetchone()[0]  # Lấy số lượng hóa đơn xuất
        self.label_count_bill_export.config(text=f"{str(bill_exported_count)}")

        # Truy vấn số lượng danh mục sản phẩm
        query5 = "SELECT COUNT(*) FROM Category"
        cursor.execute(query5)
        category_count = cursor.fetchone()[0]  # Lấy số lượng danh mục
        self.label_count_category.config(text=f"{str(category_count)}")

        # Truy vấn số lượng hóa đơn nhập (nếu có bảng hóa đơn nhập)
        query6 = "SELECT COUNT(*) FROM Import_Bill"
        cursor.execute(query6)
        bill_imported_count = cursor.fetchone()[0]  # Lấy số lượng hóa đơn nhập
        self.label_count_bill_imp.config(text=f"{str(bill_imported_count)}")

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
            if conn:
             conn.close()



    def get_monthly_data(self):
        try:
            # Kết nối SQL Server
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Lấy tháng hiện tại và năm
            current_month = datetime.now().month
            current_year = datetime.now().year

            # Truy vấn số lượng hóa đơn xuất theo tháng
            query1 = f"""
                SELECT COUNT(*) 
                FROM Export_Bill 
                WHERE MONTH(Date_Exported) = {current_month} AND YEAR(Date_Exported) = {current_year}
            """
            cursor.execute(query1)
            export_count = cursor.fetchone()[0]

            # Truy vấn số lượng hóa đơn nhập theo tháng
            query2 = f"""
                SELECT COUNT(*) 
                FROM Import_Bill 
                WHERE MONTH(Date_Imported) = {current_month} AND YEAR(Date_Imported) = {current_year}
            """
            cursor.execute(query2)
            import_count = cursor.fetchone()[0]

            return export_count, import_count

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            return 0, 0
        finally:
            if conn:
                conn.close()

    def update_diagram(self):
        """Cập nhật biểu đồ cột."""
        # Xóa các widget cũ trong DiagramFrame
        for widget in self.DiagramFrame.winfo_children():
            widget.destroy()

        # Lấy dữ liệu hóa đơn
        export_count, import_count = self.get_monthly_data()

        # Tạo biểu đồ cột
        fig = Figure(figsize=(5, 7), dpi=100)
        ax = fig.add_subplot(111)
        categories = ['Export', 'Import']
        values = [max(1, export_count), max(1, import_count)]  # Đảm bảo giá trị ít nhất là 1

        # Vẽ biểu đồ
        bars = ax.bar(categories, values, color=['blue', 'orange'])
        ax.set_title(f"Monthly Export & Import Bills\n({datetime.now().strftime('%B %Y')})")
        ax.set_ylabel("Count")
        ax.set_xlabel("Bill Type")

        # Thiết lập trục tung (y-axis)
        ax.yaxis.set_major_locator(MultipleLocator(1))  # Bước nhảy của trục tung là 1
        ax.set_ylim(0, max(values) + 1)  # Đặt giới hạn trục tung từ 0 đến giá trị lớn nhất + 1

        # Hiển thị số lượng trên cột (Đã xóa đoạn này)
        # for bar in bars:
        #     yval = bar.get_height()
        #     ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom')

        # Nhúng biểu đồ vào DiagramFrame
        canvas = FigureCanvasTkAgg(fig, self.DiagramFrame)
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        canvas.draw()

        # Đặt lịch cập nhật lại biểu đồ mỗi 60 giây (tùy chỉnh thời gian theo nhu cầu)
        self.root.after(480000, self.update_diagram)



#=======================def Logout===================
    def logout(self):
        # Đóng cửa sổ Dashboard hiện tại
        self.root.destroy()

        # Khởi động lại tệp login.py
        os.system("python login.py")  # Gọi lại tệp login.py để mở lại cửa sổ Login


   
if __name__ == "__main__":

    # Nhận tham số từ login.py
    if len(sys.argv) > 2:
        emp_no = sys.argv[1]      # Lấy mã nhân viên (emp_no)
        emp_name = sys.argv[2]    # Lấy tên nhân viên (emp_name)
    else:
        emp_no = "Unknown"        # Giá trị mặc định nếu không có mã nhân viên
        emp_name = "User"         # Giá trị mặc định nếu không có tên

    root = ctk.CTk()
    obj = IMS(root, emp_no, emp_name)  # Truyền cả emp_no và emp_name
    root.mainloop()
