from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import pyodbc
from datetime import datetime

class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700+220+130")
        self.root.title("Category Management")
        self.root.config(bg="White")
        self.root.focus_force()
         # Set the window to always stay on top
        self.root.attributes("-topmost", True)

       # Tạo Frame giả để làm tiêu đề với màu nền đẹp, hiện đại
        self.title_frame = ctk.CTkFrame(self.root, fg_color="#0099FF", corner_radius=0)
        self.title_frame.pack(fill="x")

        # Tạo Label tiêu đề trong Frame, với phông chữ đẹp, dễ đọc
        self.title_label = Label(self.title_frame, text="Inventory Management System | Developed By Quang Vinh", 
                                 font=("Times new roman", 16, "bold"), background="#0099FF", foreground="white")
        self.title_label.pack(pady=10)

        # All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_category_id = StringVar()
        self.var_category_name = StringVar()
        self.var_sup_id = StringVar()

        
        Category_frame= Frame(self.root, bd=2, relief= RIDGE, bg="white")
        Category_frame.place(x=10, y=50, width=535, height=500)

        SearchFrame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=2, border_width=2, border_color="gray", width=500, height=55)
        SearchFrame.place(x=600, y=60)

          # Title
        title = Label(Category_frame, text="Category Details", font=("goudy old style", 20), bg="#4AA02C", fg="white").pack(side=TOP, fill=X)


          # Label for the frame title
        SearchLabel = Label(SearchFrame, text="Search Category", font=("Goudy Old Style", 12, "bold"), bg="white", fg="black", width=15)
        SearchLabel.place(x=10, y=-8)  # Điều chỉnh vị trí để hiển thị tiêu đề trong frame

        
        # Options
        cmb_search = ctk.CTkComboBox(SearchFrame, 
                                        variable=self.var_searchby,  # Gắn biến textvariable
                                        values=["Category.ID", "Category Name"],  # Các tùy chọn
                                        state="readonly",  # Chỉ đọc
                                        justify="center",  # Căn giữa
                                        font=("goudy old style", 16), width=140, height=20)  # Phông chữ
        cmb_search.place(x=10, y=15)
        cmb_search.set('Search by')
        
        txt_search = ctk.CTkEntry(SearchFrame, textvariable=self.var_searchtxt, font=("Times new roman", 16), fg_color="lightyellow", width=210, height=30).place(x=160, y=13)
        bnt_search = ctk.CTkButton(SearchFrame, text="Search", command=self.search, font=("goudy old style", 16), 
                fg_color="#00CC33", 
                hover_color="#00EE00",
                text_color="white",
                corner_radius=8, width=110, height=30)
        bnt_search.place(x=380, y=13)


        # Row 1
        lbl_supplier_categoryid = Label(Category_frame, text="Category.ID", font=("goudy old style", 18), bg="white").place(x=40, y=60)
        txt_supplier_categoryid = ctk.CTkEntry(Category_frame, textvariable=self.var_category_id, font=("goudy old style", 16), fg_color="lightyellow", width=150, height=30).place(x=160, y=48)

        # # Row 2
        lbl_categoryname = Label( Category_frame,text="Category Name", font=("goudy old style", 18), bg="white").place(x=40, y=150)
        txt_categoryname = ctk.CTkEntry(Category_frame, textvariable=self.var_category_name, font=("Times new roman", 16), fg_color="lightyellow", width=210, height=30).place(x=180, y=120)

        # # Row 3
        lbl_supplier_SupID = Label(Category_frame, text="Supplier.ID", font=("goudy old style", 18), bg="white").place(x=40, y=250)
        

         # Options
        self.cmb_supplier = ctk.CTkComboBox(Category_frame, 
                                        variable=self.var_sup_id,  # Gắn biến textvariable
                                        values=[""],  # Các tùy chọn
                                        state="readonly",  # Chỉ đọc
                                        justify="center",  # Căn giữa
                                        font=("goudy old style", 16), width=180, height=30)  # Phông chữ
        self.cmb_supplier.place(x=160, y=200)
        
        self.fetch_supplier_ids()
        # Buttons

        bnt_add = ctk.CTkButton(Category_frame, text="Save", command=self.add, font=("goudy old style", 18, "bold"),
                             fg_color="#2196f3",
                             text_color="White",
                             hover_color="#66CCFF",
                             corner_radius=8,
                             width=100, height=40)

        bnt_add.place(x=5, y=350)

        
        
        
        bnt_update = ctk.CTkButton(Category_frame, text="Update", command=self.update, font=("goudy old style", 18, "bold"),
                             fg_color="#4caf50",
                             text_color="White",
                             hover_color="#66CC00",
                             corner_radius=8,
                             width=100, height=40)

        bnt_update.place(x=110, y=350) 



         
        bnt_delete = ctk.CTkButton(Category_frame, text="Delete", command=self.delete, font=("goudy old style", 18, "bold"),
                             fg_color="#f44336",
                             text_color="White",
                             hover_color="#FF6633",
                             corner_radius=8,
                             width=100, height=40)

        bnt_delete.place(x=215, y=350)


        
        bnt_clear = ctk.CTkButton(Category_frame, text="Clear", command=self.clear, font=("goudy old style", 18, "bold"),
                             fg_color="#607d8b",
                             text_color="White",
                             hover_color="#BBBBBB",
                             corner_radius=8,
                             width=100, height=40)

        bnt_clear.place(x=320, y=350)   
         

        try:
            self.im1 = Image.open("C:\Đồ án Python\image\Category1.jpg")  # Đảm bảo tên file và đường dẫn chính xác
            self.im1 = self.im1.resize((360, 240), Image.LANCZOS)  # Sử dụng Image.LANCZOS thay cho ANTIALIAS
            self.im1 = ImageTk.PhotoImage(self.im1)

            self.lbl_im1 = Label(self.root, image=self.im1, bd=0, highlightthickness=0)
            self.lbl_im1.place(x=630, y=600)


            self.im2 = Image.open("C:\Đồ án Python\image\Category2.jpg")  # Đảm bảo tên file và đường dẫn chính xác
            self.im2 = self.im2.resize((330, 200), Image.LANCZOS)  # Sử dụng Image.LANCZOS thay cho ANTIALIAS
            self.im2 = ImageTk.PhotoImage(self.im2)

            self.lbl_im2 = Label(self.root, image=self.im2, bd=0, highlightthickness=0)
            self.lbl_im2.place(x=1100, y=620)



            self.im3 = Image.open("C:\Đồ án Python\image\Category3.jpeg")  # Đảm bảo tên file và đường dẫn chính xác
            self.im3 = self.im3.resize((380, 280), Image.LANCZOS)  # Sử dụng Image.LANCZOS thay cho ANTIALIAS
            self.im3 = ImageTk.PhotoImage(self.im3)

            self.lbl_im3 = Label(self.root, image=self.im3, bd=0, highlightthickness=0)
            self.lbl_im3.place(x=130, y=600)


        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image. Error: {str(e)}", parent=self.root)
 

      
        # Supplier details section
        categorytree_frame = Frame(self.root, bd=3, relief=RIDGE)
        categorytree_frame.place(x=600, y=170, width=800, height=390)

        # Scrollbars
        scrooly = Scrollbar(categorytree_frame, orient=VERTICAL, width=20)
        scroolx = Scrollbar(categorytree_frame, orient=HORIZONTAL, width=20)

        # Pack scrollbars
        scroolx.pack(side=BOTTOM, fill=X)
        scrooly.pack(side=RIGHT, fill=Y)

        # Treeview widget
        self.CategoryTable = ttk.Treeview(categorytree_frame, columns=("Category.ID", "Category Name", "Supplier.ID", "Supplier Name"), yscrollcommand=scrooly.set, xscrollcommand=scroolx.set)

        # Configure scrollbars to Treeview
        scroolx.config(command=self.CategoryTable.xview)
        scrooly.config(command=self.CategoryTable.yview)

        # Set up Treeview columns and headers
        self.CategoryTable.heading("Category.ID", text="Category.ID")
        self.CategoryTable.heading("Category Name", text="Category Name")
        self.CategoryTable.heading("Supplier.ID", text="Supplier.ID")
        self.CategoryTable.heading("Supplier Name", text="Supplier Name")
        self.CategoryTable["show"] = "headings"

        # Set column widths
        self.CategoryTable.column("Category.ID", width=180, anchor= CENTER)
        self.CategoryTable.column("Category Name", width=300, anchor= CENTER)
        self.CategoryTable.column("Supplier.ID", width=180, anchor= CENTER)
        self.CategoryTable.column("Supplier Name", width=200, anchor= CENTER)

        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

      
        self.show()

#==================def fetch_category=================
    def fetch_supplier_ids(self):
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

        # Truy vấn lấy các Sup_ID từ bảng Supplier
        query = "SELECT Sup_ID FROM Supplier"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Danh sách thứ tự mong muốn
        desired_order = [
            "Sup.ASUS.001",
            "Sup.MSI.002",
            "Sup.LENOVO.003",
            "Sup.ACER.004",
            "Sup.HP.005",
            "Sup.DELL.006"
        ]

        # Lấy danh sách các Sup_ID từ cơ sở dữ liệu
        supplier_ids = [row[0] for row in rows]

        # Sắp xếp các Sup_ID theo thứ tự mong muốn
        sorted_supplier_ids = sorted(supplier_ids, key=lambda x: desired_order.index(x) if x in desired_order else len(desired_order))

        # Cập nhật giá trị cho combobox
        self.cmb_supplier.configure(values=sorted_supplier_ids)

        # Đặt giá trị mặc định nếu giá trị đầu tiên trong desired_order có trong danh sách
        if sorted_supplier_ids:
            self.cmb_supplier.set(sorted_supplier_ids[0])  # Đặt giá trị mặc định là phần tử đầu tiên sau khi sắp xếp
        else:
            self.cmb_supplier.set("No Suppliers")  # Nếu danh sách rỗng, hiển thị thông báo

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        if conn:
            conn.close()

#================def add================
    def add(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Kiểm tra xem các trường bắt buộc đã được nhập chưa
            if (self.var_category_id.get() == "" or self.var_category_name.get() == "" or self.var_sup_id.get() == "" ):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            # Kiểm tra xem mặt hàng với Category_ID đã tồn tại chưa
            cursor.execute("SELECT * FROM Category WHERE Category_ID = ?", (self.var_category_id.get(),))
            row = cursor.fetchone()
            if row:
                messagebox.showerror("Error", "This Category.ID already exists", parent=self.root)
                return

            # Kiểm tra xem có bản ghi nào có Category_Name và Sup_ID giống nhau không
            cursor.execute(
                "SELECT * FROM Category WHERE Category_Name = ? AND Sup_ID = ?",
                (self.var_category_name.get(), self.var_sup_id.get())
            )
            existing_record = cursor.fetchone()
            if existing_record:
                messagebox.showerror("Error", "This Category already exists", parent=self.root)
                return

            # Chèn dữ liệu vào bảng Category, đảm bảo đúng số cột
            cursor.execute(
                "INSERT INTO Category (Category_ID, Category_Name, Sup_ID) VALUES (?, ?, ?)",
                (
                    self.var_category_id.get(),
                    self.var_category_name.get(),
                    self.var_sup_id.get()
                )
            )
            conn.commit()
            
            # Cập nhật Treeview
            new_data = (
                self.var_category_id.get(),
                self.var_category_name.get(),
                self.var_sup_id.get(),
                "",  # Bạn có thể thay bằng tên nhà cung cấp nếu cần
            )
            self.CategoryTable.insert("", "end", values=new_data)

            messagebox.showinfo("Success", "Category added successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

#===================show===================
    def show(self):
     try:
        # Kết nối tới cơ sở dữ liệu SQL Server với mã hóa UTF-8
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
            'CHARSET=UTF8;'  # Đảm bảo sử dụng UTF-8
        )
        cursor = conn.cursor()

        # Truy vấn lấy dữ liệu từ bảng Category và Supplier qua Sup_ID
        query = """
            SELECT C.Category_ID, C.Category_Name, C.Sup_ID, S.Sup_Name 
            FROM Category C
            LEFT JOIN Supplier S ON C.Sup_ID = S.Sup_ID
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ trong bảng Treeview (nếu có)
        self.CategoryTable.delete(*self.CategoryTable.get_children())

        # Duyệt qua từng dòng dữ liệu và chèn vào Treeview
        for row in rows:
            # Chuyển đổi dữ liệu sang định dạng UTF-8 nếu cần thiết
            row_utf8 = [str(item) if isinstance(item, str) else item for item in row]
            self.CategoryTable.insert("", "end", values=row_utf8)

     except Exception as ex:
        # Hiển thị lỗi nếu có vấn đề xảy ra
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        # Đóng kết nối cơ sở dữ liệu
        if conn:
            conn.close()




#=================def get_data()====================
    def get_data(self, ev):
    # Lấy dòng hiện tại được chọn trong Treeview
     f = self.CategoryTable.focus()
     content = self.CategoryTable.item(f)
     row = content['values']
    
     if row:
        # Gán dữ liệu của dòng được chọn vào các biến (không lấy cột "Supplier Name")
        self.var_category_id.set(row[0])    # Category.ID
        self.var_category_name.set(row[1])  # Category Name
        self.var_sup_id.set(row[2])         # Supplier.ID

        
 #=============UPDATE==================
    def update(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Kiểm tra các trường bắt buộc
            if (self.var_category_id.get() == "" or self.var_category_name.get() == "" or self.var_sup_id.get() == ""):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            # Kiểm tra xem Category_ID có tồn tại hay không
            cursor.execute("SELECT * FROM Category WHERE Category_ID = ?", (self.var_category_id.get(),))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Invalid Category.ID", parent=self.root)
                return

            # Cập nhật dữ liệu cho bản ghi có Category_ID tương ứng
            cursor.execute(
                "UPDATE Category SET Category_Name = ?, Sup_ID = ? WHERE Category_ID = ?",
                (
                    self.var_category_name.get(),
                    self.var_sup_id.get(),
                    self.var_category_id.get()
                )
            )
            conn.commit()
            
            messagebox.showinfo("Success", "Category updated successfully", parent=self.root)
            self.show()  # Tải lại dữ liệu vào Treeview
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()


#================def delete================
    def delete(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Kiểm tra nếu Category_ID không được nhập
            if self.var_category_id.get() == "":
                messagebox.showerror("Error", "Category.ID is required", parent=self.root)
                return

            # Kiểm tra xem Category_ID có tồn tại hay không
            cursor.execute("SELECT * FROM Category WHERE Category_ID = ?", (self.var_category_id.get(),))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Invalid Category.ID", parent=self.root)
                return
                
                # Xác nhận xóa sản phẩm
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{self.var_category_name.get()}'?", parent=self.root)
            if not confirm:
                return

            # Xóa bản ghi có Category_ID tương ứng
            cursor.execute("DELETE FROM Category WHERE Category_ID = ?", (self.var_category_id.get(),))
            conn.commit()

            messagebox.showinfo("Success", "Category deleted successfully", parent=self.root)
            self.show()  # Tải lại dữ liệu vào Treeview
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()



#============Clear==============
    def clear(self):
        self.var_category_id.set("")         
        self.var_category_name.set("")            
        self.var_sup_id.set("Sup.AUS.001")          
    

#================def search===============
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
            self.show() # Gọi hàm show để lấy lại tất cả dữ liệu
            return
        # Tạo truy vấn dựa trên tùy chọn tìm kiếm
        query = ""
        if search_by == "Category.ID":
            query = "SELECT C.Category_ID, C.Category_Name, C.Sup_ID, S.Sup_Name FROM Category C LEFT JOIN Supplier S ON C.Sup_ID = S.Sup_ID WHERE C.Category_ID = ?"
        elif search_by == "Category Name":
            query = "SELECT  C.Category_ID, C.Category_Name, C.Sup_ID, S.Sup_Name FROM Category C LEFT JOIN Supplier S ON C.Sup_ID = S.Sup_ID WHERE C.Category_Name LIKE ?"
        else:
            messagebox.showerror("Error", "Invalid search option", parent=self.root)
            return

        # Thực thi truy vấn
        cursor.execute(query, search_text if search_by == "Category.ID" else f'%{search_text}%')

        # Lấy kết quả truy vấn
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ trong Treeview
        self.CategoryTable.delete(*self.CategoryTable.get_children())

        if rows:
            for row in rows:
                # Chuyển đổi dữ liệu sang định dạng UTF-8 nếu cần thiết
                row_utf8 = [str(item).encode('utf-8').decode('utf-8') if isinstance(item, str) else item for item in row]
                
                # Thêm dữ liệu vào Treeview
                self.CategoryTable.insert("", "end", values=row_utf8)
        else:
            messagebox.showinfo("Info", "No records found", parent=self.root)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
     finally:
        if conn:
            conn.close()


# Khởi động ứng dụng
if __name__ == "__main__":
    root = ctk.CTk()
    obj = CategoryClass(root)
    root.mainloop()
