from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import pyodbc
import pandas as pd
class ProductClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x750+220+130")
        self.root.title("Products Management")
        self.root.config(bg="White")
        self.root.focus_force()
         # Set the window to always stay on top
        self.root.attributes("-topmost", True)
        
        # Tạo Frame giả để làm tiêu đề với màu nền đẹp, hiện đại
        self.title_frame = ctk.CTkFrame(self.root, fg_color="#0099FF", corner_radius=0)
        self.title_frame.pack(fill="x")

        # Tạo Label tiêu đề trong Frame, với phông chữ đẹp, dễ đọc
        self.title_label = Label(self.title_frame, text="Inventory Management System | Developed By Quang Vinh", 
                                 font=("Times new roman", 14, "bold"), background="#0099FF", foreground="white")
        self.title_label.pack(pady=14)

          # All Variables
        self.var_product_id = StringVar()
        self.var_product_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status= StringVar()
        self.var_Category_id = StringVar()
        self.var_searchby= StringVar()
        self.var_searchtxt= StringVar()
        self.row_list=[]

       
         #=============Image Load and Resize==========
        try:
            self.im1 = Image.open("C:\Đồ án Python\image\Asus Gaming.jpg")  # Đảm bảo tên file và đường dẫn chính xác
            self.im1 = self.im1.resize((360, 240), Image.LANCZOS)  # Sử dụng Image.LANCZOS thay cho ANTIALIAS
            self.im1 = ImageTk.PhotoImage(self.im1)

            self.lbl_im1 = Label(self.root, image=self.im1, bd=0, highlightthickness=0)
            self.lbl_im1.place(x=650, y=680)


            self.im2 = Image.open("C:\Đồ án Python\image\MSI Gaming.jpg")  # Đảm bảo tên file và đường dẫn chính xác
            self.im2 = self.im2.resize((330, 180), Image.LANCZOS)  # Sử dụng Image.LANCZOS thay cho ANTIALIAS
            self.im2 = ImageTk.PhotoImage(self.im2)

            self.lbl_im2 = Label(self.root, image=self.im2, bd=0, highlightthickness=0)
            self.lbl_im2.place(x=1160, y=700)

        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image. Error: {str(e)}", parent=self.root)


        product_frame= Frame(self.root, bd=2, relief= RIDGE, bg="white")
        product_frame.place(x=10, y=65, width=550, height=850)


        self.SearchFrame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=2, border_width=2, border_color="gray", width=520, height=60)
        self.SearchFrame.place(x=580, y=60)
        # Label for the frame title
        SearchLabel = Label(self.SearchFrame, text="Search Products", font=("Goudy Old Style", 12, "bold"), bg="white", fg="black", width=15)
        SearchLabel.place(x=10, y=-8)  # Điều chỉnh vị trí để hiển thị tiêu đề trong frame

        # Options
        cmb_search = ctk.CTkComboBox(self.SearchFrame, 
                                        variable=self.var_searchby,  # Gắn biến textvariable
                                        values=["Search by","Product.ID", "Product Name", "Status (Active)", "Status (Inactive)", "Quantity=0"],  # Các tùy chọn
                                        state="readonly",  # Chỉ đọc
                                        justify="center",  # Căn giữa
                                        font=("goudy old style", 16), width=140, height=20)  # Phông chữ
        cmb_search.place(x=10, y=20)
        cmb_search.set('Search by')
        
        txt_search = ctk.CTkEntry(self.SearchFrame, textvariable=self.var_searchtxt, font=("Times new roman", 16), fg_color="lightyellow", width=230, height=30).place(x=160, y=18)
        bnt_search = ctk.CTkButton(self.SearchFrame, text="Search", command=self.search, font=("goudy old style", 16), 
                fg_color="#00CC33", 
                hover_color="#00EE00",
                text_color="white",
                corner_radius=8, width=110, height=30)
        bnt_search.place(x=400, y=18)

        # Title
        title = Label(product_frame, text="Manage Products Details", font=("goudy old style", 25), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # Row 1
        lbl_product_id = Label(product_frame, text="Product.ID", font=("goudy old style", 18), bg="white").place(x=30, y=70)
        txt_product_id = ctk.CTkEntry(product_frame, textvariable=self.var_product_id, font=("goudy old style", 16), fg_color="lightyellow", width=120, height=30).place(x=160, y=55)

        # Row 2
        lbl_product_name = Label(product_frame, text="Product Name", font=("goudy old style", 18), bg="white").place(x=30, y=150)
        txt_product_name = ctk.CTkEntry(product_frame, textvariable=self.var_product_name, font=("Times new roman", 16), fg_color="lightyellow", width=230, height= 30).place(x=160, y=118)

         # Row 3
        lbl_price = Label(product_frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=230)
        txt_price = ctk.CTkEntry(product_frame, textvariable=self.var_price, font=("Times new roman", 16), fg_color="lightyellow", width=120, height=30).place(x=140, y=180)
        
        # Row 4
        lbl_quantity = Label(product_frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30, y=310)
        spin_quantity=Spinbox(product_frame, from_=0, to=1000, textvariable=self.var_quantity, font=("goudy old style", 16), bg="white").place(x=220, y=313, width=100, height=30)

        # Row 5
        lbl_status = Label(product_frame, text="Status", font=("goudy old style", 18), bg="white").place(x=30, y=388)

    # Thêm Radio Button cho "Active" và "Inactive"
      
        rbtn_active = ctk.CTkRadioButton(
            product_frame,
            text="Active",  # Nội dung hiển thị
            variable=self.var_status,  # Biến ràng buộc
            value="Active",  # Giá trị khi được chọn
            font=("Goudy Old Style", 18),  # Font chữ
            radiobutton_width=20,  # Kích thước vòng tròn
            radiobutton_height=20,
            fg_color="#4CAF50",          # Màu vòng tròn khi chọn
            hover_color="#00FF00",       # Màu vòng tròn khi hover
            text_color="black"           # Màu chữ
            )
        
        rbtn_active.place(x=155, y=313)


        rbtn_inactive = ctk.CTkRadioButton(
                product_frame,
                text="Inactive",  # Nội dung hiển thị
                variable=self.var_status,  # Biến ràng buộc
                value="Inactive",  # Giá trị khi được chọn
                font=("Goudy Old Style", 18),  # Font chữ
                radiobutton_width=20,  # Kích thước vòng tròn
                radiobutton_height=20,
                fg_color="#4CAF50",          # Màu vòng tròn khi chọn
                hover_color="#00FF00",       # Màu vòng tròn khi hover
                text_color="black"           # Màu chữ
                )
            
        rbtn_inactive.place(x=280, y=313) 
            
        self.var_status.set("Active")

       # Row 6: Tạo Listbox
        lbl_category_id = Label(product_frame, text="Category.ID", font=("goudy old style", 18), bg="white").place(x=30, y=470)
        # Tạo Listbox để hiển thị các Category_ID theo dạng lưới
        self.lst_category_id = Listbox(product_frame, font=("goudy old style", 16), selectmode=SINGLE, height=5, width=40)
        self.lst_category_id.place(x=230, y=435, width=180, height=125)

        # Thêm thanh cuộn dọc cho Listbox
        scroll_y = Scrollbar(product_frame, orient=VERTICAL, command=self.lst_category_id.yview)
        scroll_y.place(x=550, y=400, height=150)
        
        self.lst_category_id.configure( yscrollcommand=scroll_y.set)

       # Row 7: Thêm nút để upload hình ảnh
        lbl_upload_image = Label(product_frame, text="Images", font=("goudy old style", 18), bg="white").place(x=30, y=650)

#=====================Icon-Upload========================
        try:
            # Mở và chỉnh kích thước hình ảnh Sidebar icon
            self.icon_upload = Image.open("C:/Đồ án Python/image/Upload images.png")  # Đảm bảo đường dẫn đúng
            self.icon_upload = self.icon_upload.resize((70, 70), Image.LANCZOS)
            self.icon_upload = ImageTk.PhotoImage(self.icon_upload)

            # Tạo nút với icon và hành động Upload
            bnt_upload_image = Button(product_frame, image=self.icon_upload, command=self.upload_image, bg="White", fg="white", bd=0, cursor="hand2")
            bnt_upload_image.place(x=180, y=610, width=120, height=100)

        except Exception as e:
            print(f"Error loading image: {e}")

#============Button=============
        bnt_add = ctk.CTkButton(product_frame, text="Save", command=self.add, font=("goudy old style", 18, "bold"),
                             fg_color="#2196f3",
                             text_color="White",
                             hover_color="#66CCFF",
                             corner_radius=8,
                             width=100, height=40)

        bnt_add.place(x=10, y=630)    


        bnt_update = ctk.CTkButton(product_frame, text="Update", command=self.update, font=("goudy old style", 18, "bold"),
                             fg_color="#4caf50",
                             text_color="White",
                             hover_color="#66CC00",
                             corner_radius=8,
                             width=100, height=40)

        bnt_update.place(x=115, y=630)    


        
        bnt_delete = ctk.CTkButton(product_frame, text="Delete", command=self.delete, font=("goudy old style", 18, "bold"),
                             fg_color="#f44336",
                             text_color="White",
                             hover_color="#FF6633",
                             corner_radius=8,
                             width=100, height=40)

        bnt_delete.place(x=220, y=630)   



        bnt_clear = ctk.CTkButton(product_frame, text="Clear", command=self.clear, font=("goudy old style", 18, "bold"),
                             fg_color="#607d8b",
                             text_color="White",
                             hover_color="#BBBBBB",
                             corner_radius=8,
                             width=100, height=40)

        bnt_clear.place(x=325, y=630)   


        button_exportFrame= Frame(self.root, relief=RIDGE, bg="white")
        button_exportFrame.place(x=1380, y=75, width=150, height=85)


#=====================Icon-Upload Excel========================
        try:
            # Mở và chỉnh kích thước hình ảnh Sidebar icon
            self.icon_upload_button_excel = Image.open("C:\Đồ án Python\image\Excel.png")  # Đảm bảo đường dẫn đúng
            self.icon_upload_button_excel =   self.icon_upload_button_excel.resize((70, 70), Image.LANCZOS)
            self.icon_upload_button_excel = ImageTk.PhotoImage (self.icon_upload_button_excel)

            # Tạo nút với icon và hành động Upload
            bnt_upload_image = Button(button_exportFrame, image=  self.icon_upload_button_excel, command=self.export_inactive_products, bg="White", fg="white", bd=0, cursor="hand2")
            bnt_upload_image.place(x=20, y=0, width=120, height=80)

        except Exception as e:
            print(f"Error loading image: {e}")
         


        self.fetch_category_ids()
        # Product details section
        Product_frame = Frame(self.root, bd=3, relief=RIDGE)
        Product_frame.place(x=580, y=160, width=1030, height=500)

        # Scrollbars
        scrooly = Scrollbar(Product_frame, orient=VERTICAL, width=20)
        scroolx = Scrollbar(Product_frame, orient=HORIZONTAL, width=20)

        # Pack scrollbars
        scroolx.pack(side=BOTTOM, fill=X)
        scrooly.pack(side=RIGHT, fill=Y)

        # Treeview widget
        self.ProductTable = ttk.Treeview(Product_frame, columns=("Product.ID", "Product Name", "Price", "Quantity", "Status" ,"Category.ID", "Category Name", "Supplier Name"), yscrollcommand=scrooly.set, xscrollcommand=scroolx.set)

        # Configure scrollbars to Treeview
        scroolx.config(command=self.ProductTable.xview)
        scrooly.config(command=self.ProductTable.yview)

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
        self.ProductTable.column("Product Name", width=260, anchor=CENTER)
        self.ProductTable.column("Price", width=200, anchor= CENTER)
        self.ProductTable.column("Quantity", width=120, anchor= CENTER)
        self.ProductTable.column("Status", width=120, anchor= CENTER)
        self.ProductTable.column("Category.ID", width=120, anchor= CENTER)
        self.ProductTable.column("Category Name", width=260, anchor= CENTER)
        self.ProductTable.column("Supplier Name", width=120, anchor= CENTER)

        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()


#==================def fetch_category=================
    def fetch_category_ids(self):
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

            # Truy vấn lấy các Category_ID từ bảng Category
            query = "SELECT Category_ID FROM Category"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Xóa nội dung cũ (nếu có) trong Listbox
            self.lst_category_id.delete(0, END)

            # Hiển thị các Category_ID theo dạng lưới trong Listbox
            for row in rows:
                self.lst_category_id.insert(END, row[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            if conn:
                conn.close()

    
#=============def Upload-Image===============
    def upload_image(self):
     try:
        # Tạo cửa sổ Toplevel để chọn ảnh, sẽ nằm trên cửa sổ Product nhưng không thay đổi Product
        self.modal_window = ctk.CTkToplevel(self.root)  # Cửa sổ Product
        self.modal_window.withdraw()  # Ẩn cửa sổ Toplevel tạm thời
        self.modal_window.attributes("-topmost", True)  # Đặt cửa sổ Toplevel lên trên cùng (với Product)
        self.root.update()  # Cập nhật lại trạng thái của cửa sổ Dashboard

        # Mở hộp thoại chọn ảnh
        file_path = filedialog.askopenfilename(
            parent=self.modal_window,  # Đặt cửa sổ Toplevel làm parent
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.webp")]  # Chỉ hiển thị các loại ảnh
        )

        # Khi đã chọn xong ảnh, đóng cửa sổ Toplevel
        self.modal_window.grab_release()  # Giải phóng focus của Toplevel
        self.modal_window.destroy()  # Đóng cửa sổ Toplevel
        self.root.attributes("-topmost", True)  # Đảm bảo cửa sổ Dashboard vẫn trên cùng
        self.root.focus()  # Đảm bảo cửa sổ Dashboard giữ focus

        if file_path:  # Kiểm tra nếu người dùng chọn file
            # Lưu đường dẫn của ảnh
            self.image_path = file_path

            # Xử lý và hiển thị ảnh sau khi tải lên
            original_img = Image.open(file_path).convert("RGBA")
            datas = original_img.getdata()

            # Chuyển màu xám sáng thành trắng
            new_data = []
            for item in datas:
                if item[0] >= 215 and item[1] >= 210 and item[2] >= 210:
                    new_data.append((255, 255, 255, 255))  # Chuyển thành trắng
                else:
                    new_data.append(item)

            original_img.putdata(new_data)
            img_with_white_bg = original_img.convert("RGB")

            # Cắt 2 pixel từ dưới cùng của ảnh
            width, height = img_with_white_bg.size
            img_cropped = img_with_white_bg.crop((0, 0, width, height - 2))

            # Resize ảnh để vừa với không gian cần thiết
            img_resized = img_cropped.resize((190, 170), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img_resized)

            # Kiểm tra xem đã có label hiển thị ảnh chưa, nếu có thì cập nhật, nếu chưa thì tạo mới
            if hasattr(self, 'lbl_img'):
                self.lbl_img.configure(image=tk_img)
                self.lbl_img.image = tk_img
            else:
                # Tạo mới label hiển thị ảnh nếu chưa có
                self.lbl_img = Label(self.root, image=tk_img, bg="white")  # Hiển thị trong cửa sổ Product
                self.lbl_img.image = tk_img
                self.lbl_img.place(x=180, y=645)  # Vị trí ảnh trong cửa sổ Product

            # Cập nhật lại nút "Cập nhật" cho ảnh
            self.create_image_update_button()

     except Exception as e:
        # Xử lý lỗi trong trường hợp có sự cố khi tải ảnh
        print(f"Error uploading image: {e}")
        if hasattr(self, 'modal_window'):
            self.modal_window.destroy()
        self.root.attributes("-topmost", True)  # Đảm bảo cửa sổ Dashboard giữ focus
        self.root.focus()  # Đảm bảo cửa sổ Dashboard giữ focus




    
#==================def add===================
    def add(self):
        conn=None
        try:
            # Kiểm tra các trường bắt buộc đã được nhập chưa
            if (self.var_product_id.get() == "" or self.var_product_name.get() == "" or 
                self.var_price.get() == "" or self.var_quantity.get() == "" or 
                self.var_status.get() == "" or 
                not hasattr(self, 'image_path') or not self.image_path):
                messagebox.showerror("Error", "All fields and image are required", parent=self.root)
                return

            # Kiểm tra xem đã chọn mục nào trong Listbox chưa
            selected_category = self.lst_category_id.curselection()
            if not selected_category:
                messagebox.showerror("Error", "Please select a Category ID from the list", parent=self.root)
                return

            # Lấy Category_ID từ mục được chọn trong Listbox
            category_id = self.lst_category_id.get(selected_category[0])

            # Kết nối đến SQL Server
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Kiểm tra xem Product_ID có trùng lặp trong cơ sở dữ liệu không
            cursor.execute("SELECT * FROM Product WHERE Product_ID = ?", (self.var_product_id.get(),))
            row = cursor.fetchone()
            if row:
                messagebox.showerror("Error", "This Product_ID already exists", parent=self.root)
                return

            # Chèn dữ liệu vào bảng Products, lưu đường dẫn ảnh từ biến self.image_path
            cursor.execute(
                """
                INSERT INTO Product (Product_ID, Product_Name, Price, Quantity, Status, Category_ID, Image) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.var_product_id.get(),
                    self.var_product_name.get(),
                    float(self.var_price.get()),
                    int(self.var_quantity.get()),
                    self.var_status.get(),
                    category_id,
                    self.image_path
                )
            )
            conn.commit()

            # Cập nhật Treeview
            new_data = (
                self.var_product_id.get(),
                self.var_product_name.get(),
                self.var_price.get(),
                self.var_quantity.get(),
                self.var_status.get(),
                category_id,
            )
            self.ProductTable.insert("", "end", values=new_data)

            messagebox.showinfo("Success", "Product added successfully", parent=self.root)
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
                if conn:
                    conn.close()



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

        )
        cursor = conn.cursor()

        # Truy vấn lấy dữ liệu từ bảng Products, nối với bảng Category và Supplier để lấy thông tin Category Name và Supplier Name
        query = """
        SELECT P.Product_ID, P.Product_Name, P.Price, P.Quantity, P.Status, C.Category_ID, C.Category_Name, S.Sup_Name 
        FROM Product P
        JOIN Category C ON P.Category_ID = C.Category_ID
        JOIN Supplier S ON C.Sup_ID = S.Sup_ID
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

#===============================
    def get_data(self, ev):
     try:
        # Lấy dòng hiện tại được chọn trong Treeview
        f = self.ProductTable.focus()
        content = self.ProductTable.item(f)
        row = content['values']

        if row:
            # Gán dữ liệu của dòng được chọn vào các biến
            self.var_product_id.set(row[0])      # Product.ID
            self.var_product_name.set(row[1])    # Product Name
            self.var_price.set(row[2])           # Price
            self.var_quantity.set(row[3])        # Quantity
            self.var_status.set(row[4])          # Status
            self.var_Category_id.set(row[5])     # Category.ID
            self.lst_category_id.selection_clear(0, 'end')  # Xóa lựa chọn hiện tại trong Listbox

            # Duyệt qua các mục trong Listbox để tìm Category_ID tương ứng
            for i in range(self.lst_category_id.size()):
                if self.lst_category_id.get(i) == self.var_Category_id.get():
                    self.lst_category_id.selection_set(i)  # Chọn mục có Category_ID tương ứng
                    self.lst_category_id.activate(i)       # Kích hoạt mục
                    self.lst_category_id.see(i)            # Cuộn đến mục tương ứng
                    break

            # Kết nối đến cơ sở dữ liệu để lấy đường dẫn hình ảnh
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT Image FROM Product WHERE Product_ID = ?", (self.var_product_id.get(),))
            image_path = cursor.fetchone()

            if image_path and image_path[0]:
                # Mở hình ảnh từ đường dẫn và chuyển đổi thành RGBA
                img = Image.open(image_path[0]).convert("RGBA")

                # Xử lý nền xám thành nền trắng
                datas = img.getdata()
                new_data = []
                for item in datas:
                    # Kiểm tra pixel gần màu xám
                    if item[0] >= 215 and item[1] >= 210 and item[2] >= 210:
                        new_data.append((255, 255, 255, item[3]))  # Chuyển sang trắng
                    else:
                        new_data.append(item)
                img.putdata(new_data)

                # Cắt viền dưới cùng: Giữ lại phần trên của ảnh, cắt bỏ khoảng 2 pixel dưới cùng
                width, height = img.size
                img = img.crop((0, 0, width, height - 2))  # Cắt bỏ 2 pixel ở cạnh dưới

                # Resize ảnh cho phù hợp với giao diện
                img = img.resize((190, 170), Image.Resampling.LANCZOS)
                self.img = ImageTk.PhotoImage(img)

                # Tạo Label nếu chưa tồn tại để hiển thị ảnh
                if not hasattr(self, 'lbl_img'):
                    self.lbl_img = Label(self.root, image=self.img, bg="white", bd=0)
                    self.lbl_img.place(x=180, y=645)  # Thay đổi vị trí nếu cần
                else:
                    self.lbl_img.config(image=self.img)  # Cập nhật hình ảnh vào Label đã tồn tại
                    self.lbl_img.image = self.img  # Lưu tham chiếu ảnh để không bị garbage collected
            else:
                messagebox.showerror("Error", "Image path is empty or invalid", parent=self.root)
        
        # Gọi hàm để tạo nút cập nhật ảnh (nếu cần)
        self.create_image_update_button()

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
     finally:
            if conn:  # Đảm bảo rằng kết nối sẽ được đóng nếu nó đã được mở
             conn.close()

#========================def update=====================
    def update(self):
     try:
        # Kiểm tra các trường bắt buộc đã được nhập
        if (self.var_product_id.get() == "" or self.var_product_name.get() == "" or 
            self.var_price.get() == "" or self.var_quantity.get() == "" or 
            self.var_status.get() == "" or self.var_Category_id.get() == ""):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        # Lấy giá trị từ Listbox (nếu có lựa chọn mới)
        selected_category = self.lst_category_id.curselection()
        if selected_category:  # Nếu có mục được chọn trong Listbox
            self.var_Category_id.set(self.lst_category_id.get(selected_category[0]))

        # Kết nối đến SQL Server
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )
        cursor = conn.cursor()

        # Kiểm tra trùng lặp Product_Name và Status
        query = """SELECT Product_ID FROM Product 
                   WHERE Product_Name = ? AND Status = ? AND Product_ID != ?"""
        cursor.execute(query, (
            self.var_product_name.get(),
            self.var_status.get(),
            self.var_product_id.get()
        ))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Error", 
                                 f"Product with name '{self.var_product_name.get()}' and status '{self.var_status.get()}' already exists with a different ID.",
                                 parent=self.root)
            return

        # Cập nhật dữ liệu trong cơ sở dữ liệu
        if hasattr(self, 'image_path'):  # Nếu có ảnh mới
            cursor.execute(
                """UPDATE Product SET Product_Name = ?, Price = ?, Quantity = ?, Status = ?, Category_ID = ?, Image = ? 
                WHERE Product_ID = ?""",
                (
                    self.var_product_name.get(),
                    float(self.var_price.get()),
                    int(self.var_quantity.get()),
                    self.var_status.get(),
                    self.var_Category_id.get(),
                    self.image_path,
                    self.var_product_id.get()
                )
            )
        else:  # Không có ảnh mới
            cursor.execute(
                """UPDATE Product SET Product_Name = ?, Price = ?, Quantity = ?, Status = ?, Category_ID = ? 
                WHERE Product_ID = ?""",
                (
                    self.var_product_name.get(),
                    float(self.var_price.get()),
                    int(self.var_quantity.get()),
                    self.var_status.get(),
                    self.var_Category_id.get(),
                    self.var_product_id.get()
                )
            )

        conn.commit()

        # Cập nhật Treeview với thông tin mới
        selected_item = self.ProductTable.selection()
        self.ProductTable.item(selected_item, values=(
            self.var_product_id.get(),
            self.var_product_name.get(),
            self.var_price.get(),
            self.var_quantity.get(),
            self.var_status.get(),
            self.var_Category_id.get(),  # Cập nhật Category_ID mới
        ))

        # Cập nhật Listbox: Đặt lại lựa chọn cho mục tương ứng với Category_ID mới
        self.lst_category_id.selection_clear(0, 'end')
        for i in range(self.lst_category_id.size()):
            if self.lst_category_id.get(i) == self.var_Category_id.get():
                self.lst_category_id.selection_set(i)
                self.lst_category_id.activate(i)
                break

        # Thông báo thành công
        messagebox.showinfo("Success", "Product updated successfully", parent=self.root)

        # Gọi hàm show() để làm mới Treeview
        self.show()

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        if conn:
            conn.close()



#================def create_image_update_button==================
    def create_image_update_button(self):
    # Xóa nút cũ nếu đã tồn tại
     if hasattr(self, 'btn_update_image'):
        self.btn_update_image.destroy()

    # Tạo nút mới để cập nhật hình ảnh
     self.btn_update_image = Button(self.root, command= self.upload_image, text="Update Image")
     self.btn_update_image.place(x=420, y=660)  # Thay đổi vị trí nếu cần


#================def Delete========================
    def delete(self):
     try:
        # Kiểm tra nếu ID sản phẩm trống
        if self.var_product_id.get() == "":
            messagebox.showerror("Error", "Product ID is required to delete", parent=self.root)
            return

        # Kết nối đến SQL Server
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )
        cursor = conn.cursor()

        # Truy vấn tên sản phẩm dựa trên Product ID
        cursor.execute("SELECT Product_Name, Image FROM Product WHERE Product_ID = ?", (self.var_product_id.get(),))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Error", "Product not found", parent=self.root)
            return

        product_name = row[0]  # Lưu tên sản phẩm để hiển thị sau khi xóa
        self.image_path = row[1]  # Giữ lại đường dẫn ảnh để có thể add lại ngay lập tức

        # Xác nhận xóa sản phẩm
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?", parent=self.root)
        if not confirm:
            return

        # Xóa sản phẩm khỏi CSDL
        cursor.execute("DELETE FROM Product WHERE Product_ID = ?", (self.var_product_id.get(),))
        conn.commit()

        # Xóa sản phẩm khỏi Treeview nhưng giữ lại các thông tin trong các trường Entry
        selected_item = self.ProductTable.selection()
        if selected_item:
            self.ProductTable.delete(selected_item)

        # Thông báo sản phẩm đã được xóa
        messagebox.showinfo("Success", f"Product '{product_name}' deleted successfully", parent=self.root)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        if conn:
            conn.close()


#=================def Clear=====================
    def clear(self):
        # Xóa dữ liệu trong các trường nhập liệu
        self.var_product_id.set("")
        self.var_product_name.set("")
        self.var_price.set("")
        self.var_quantity.set("1")
        self.var_status.set("Active")
            
            # Xóa lựa chọn trong Listbox
        if hasattr(self, 'lst_category_id'):
            self.lst_category_id.selection_clear(0, END)  # Xóa mọi lựa chọn trong Listbox

        # Xóa đường dẫn ảnh
        if hasattr(self, 'image_path'):
            del self.image_path  # Xóa biến lưu đường dẫn ảnh

        # Đặt lại hình ảnh về biểu tượng mặc định
        try:
            # Mở và chỉnh kích thước hình ảnh Sidebar icon
            self.icon_upload = Image.open("C:/Đồ án Python/image/Upload images.png")  # Đảm bảo đường dẫn đúng
            self.icon_upload = self.icon_upload.resize((70, 70), Image.LANCZOS)
            self.icon_upload = ImageTk.PhotoImage(self.icon_upload)

            # Xóa lbl_img nếu đang hiển thị ảnh cũ
            if hasattr(self, 'lbl_img'):
                self.lbl_img.destroy()
                del self.lbl_img  # Xóa hoàn toàn biến `lbl_img`

            # Xóa nút `btn_update_image` nếu đang hiển thị
            if hasattr(self, 'btn_update_image'):
                self.btn_update_image.destroy()
                del self.btn_update_image  # Xóa hoàn toàn biến `btn_update_image`

            # Tạo lại button upload icon với hình ảnh mặc định
            self.bnt_upload_image = Button(self.root, image=self.icon_upload, command=self.upload_image, bg="White", fg="white", bd=0, cursor="hand2")
            self.bnt_upload_image.place(x=180, y=680, width=120, height=100)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading default icon: {str(e)}", parent=self.root)

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
        """

        # Thêm điều kiện WHERE vào truy vấn dựa trên tùy chọn tìm kiếm
        if search_by == "Product.ID":
            query += " WHERE P.Product_ID = ?"
            params = (search_text,)
        elif search_by == "Product Name":
            query += " WHERE P.Product_Name LIKE ?"
            params = (f'%{search_text}%',)
        elif search_by == "Status (Active)":
            query += " WHERE P.Status = 'Active'"
            params = ()
        elif search_by == "Status (Inactive)":
            query += " WHERE P.Status = 'Inactive'"
            params = ()
        elif search_by == "Quantity=0":
            query+= "WHERE P.Quantity=0"
            params = ()
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



#======================def export_inactive_products
    def export_inactive_products(self):
     try:
        # Tạo cửa sổ Toplevel để chọn ảnh, sẽ nằm trên cửa sổ Product nhưng không thay đổi Product
        self.modal_window = ctk.CTkToplevel(self.root)  # Cửa sổ Product
        self.modal_window.withdraw()  # Ẩn cửa sổ Toplevel tạm thời
        self.modal_window.attributes("-topmost", True)  # Đặt cửa sổ Toplevel lên trên cùng (với Product)
        self.root.update()  # Cập nhật lại trạng thái của cửa sổ Dashboard

        # Thiết lập kết nối đến SQL Server
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )

        # Truy vấn lấy các sản phẩm có Status="Inactive"
        query = """
        SELECT P.Product_ID, P.Product_Name, P.Price, P.Quantity, P.Status, C.Category_ID, C.Category_Name, S.Sup_Name 
        FROM Product P
        JOIN Category C ON P.Category_ID = C.Category_ID
        JOIN Supplier S ON C.Sup_ID = S.Sup_ID
        AND P.Status='Inactive'
        """
        df = pd.read_sql_query(query, conn)  # Đọc dữ liệu từ SQL Server vào DataFrame

        if df.empty:
            messagebox.showinfo("No Data", "No Inactive products found in the database.", parent=self.root)
            return

        # Chọn đường dẫn lưu file Excel
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            title="Save Excel File",
            parent=self.modal_window  # Đảm bảo hộp thoại mở trên cửa sổ Toplevel
        )
        if not save_path:  # Nếu người dùng hủy hộp thoại, thoát hàm
            return

        df.to_excel(save_path, index=False, engine='openpyxl')

        # Thông báo thành công
        messagebox.showinfo("Success", f"File exported successfully!\nLocation: {save_path}", parent=self.root)
        conn.close()  # Đóng kết nối

     except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)
     finally:
           if conn:
             conn.close()


if __name__ == "__main__":
    root = ctk.CTk()
    obj = ProductClass(root)
    root.mainloop()