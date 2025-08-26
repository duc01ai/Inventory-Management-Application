from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import pyodbc
import hashlib  # Dùng để hash mật khẩu
from datetime import datetime
from tkcalendar import DateEntry

class EmployeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x750+220+130")
        self.root.title("Employee Management")
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

        #All Variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_gender = StringVar()  # Khởi tạo StringVar
        self.var_gender.set('Male')    # Đặt giá trị mặc định

        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        # #Search frame
        
        SearchFrame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=2, border_width=2, border_color="gray", width=500, height=55)
        SearchFrame.place(x=300, y=60)


          # Label for the frame title
        SearchLabel = Label(SearchFrame, text="Search Employee", font=("Goudy Old Style", 12, "bold"), bg="white", fg="black", width=15)
        SearchLabel.place(x=10, y=-8)  # Điều chỉnh vị trí để hiển thị tiêu đề trong frame

        
        # Options
        cmb_search = ctk.CTkComboBox(SearchFrame, 
                                        variable=self.var_searchby,  # Gắn biến textvariable
                                        values=["Search by","Emp.No", "Name", "Email", "Highest Salary"],  # Các tùy chọn
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

        self.emp_infoframe= Frame(self.root, relief=GROOVE, bg="white")
        self.emp_infoframe.place(x=0, y=230, relwidth=1, height=420)


        #Title
        title= Label(self.root, text="Employee Details", font=("goudy old style",20), bg="#0f4d7d", fg="white").place(x=100, y=155, width=1300)

        #Content
        #==row 1==
        lbl_empid= Label(self.emp_infoframe, text="Emp.No", font=("goudy old style",18), bg="white").place(x=80, y=10)
        lbl_gender= Label(self.emp_infoframe, text="Gender", font=("goudy old style",18), bg="white").place(x=580, y=10)
        lbl_contact= Label(self.emp_infoframe, text="Contact", font=("goudy old style",18), bg="white").place(x=1150, y=10)

        txt_empid= ctk.CTkEntry(self.emp_infoframe, textvariable= self.var_emp_id, font=("Times new roman",18), fg_color="lightyellow", width=180, height=30).place(x=160, y=8)




        rbtn_gender_male = ctk.CTkRadioButton(
            self.emp_infoframe,
            text="Male",  # Nội dung hiển thị
            variable=self.var_gender,  # Biến ràng buộc
            value="Male",  # Giá trị khi được chọn
            font=("Goudy Old Style", 18),  # Font chữ
            radiobutton_width=20,  # Kích thước vòng tròn
            radiobutton_height=20,
            fg_color="#4CAF50",          # Màu vòng tròn khi chọn
            hover_color="#00FF00",       # Màu vòng tròn khi hover
            text_color="black"           # Màu chữ
        )
        rbtn_gender_male.place(x=580, y=10)

        rbtn_gender_female = ctk.CTkRadioButton(
            self.emp_infoframe,
            text="Female",  # Nội dung hiển thị
            variable=self.var_gender,  # Biến ràng buộc
            value="Female",  # Giá trị khi được chọn
            font=("Goudy Old Style", 18),  # Font chữ
            radiobutton_width=20,  # Kích thước vòng tròn
            radiobutton_height=20,
            fg_color="#4CAF50",          # Màu vòng tròn khi chọn
            hover_color="#00FF00",       # Màu vòng tròn khi hover
            text_color="black"           # Màu chữ
        )
        rbtn_gender_female.place(x=720, y=10)
      

        self.txt_contact = ctk.CTkEntry(self.emp_infoframe, textvariable=self.var_contact, font=("Times new roman", 18), fg_color="lightyellow", width=180, height=30)
        self.txt_contact.place(x=1000, y=8)

        #==row 2==
        lbl_name= Label(self.emp_infoframe, text="Emp Name", font=("goudy old style",18), bg="white").place(x=80, y=90)
        lbl_dob= Label(self.emp_infoframe, text="D.O.B", font=("goudy old style",18), bg="white").place(x=580, y=90)
        lbl_doj= Label(self.emp_infoframe, text="D.O.J", font=("goudy old style",18), bg="white").place(x=1030, y=90)

        txt_name= ctk.CTkEntry(self.emp_infoframe, textvariable= self.var_name, font=("Times new roman",18), fg_color="lightyellow",width=200, height=30).place(x=180, y=70)
        
        self.dob_date = DateEntry(self.emp_infoframe, 
                                    textvariable=self.var_dob, 
                                    font=("Times new Roman", 18), 
                                    background="#33CCFF", 
                                    foreground="black",
                                    date_pattern="dd-MM-yyy")
        self.dob_date.place(x=700, y=90, width=160)

        
        
        self.doj_date = DateEntry(self.emp_infoframe, 
                                    textvariable=self.var_doj, 
                                    font=("Times new Roman", 18), 
                                    background="#33CCFF", 
                                    foreground="black", 
                                    date_pattern="dd-MM-yyy")
        self.doj_date.place(x=1150, y=90, width=160)
        
        
        #==row 3==
        lbl_email= Label(self.emp_infoframe, text="Email", font=("goudy old style",18), bg="white").place(x=80, y=175)
        lbl_pass= Label(self.emp_infoframe, text="Password", font=("goudy old style",18), bg="white").place(x=580, y=175)
        lbl_utype= Label(self.emp_infoframe, text="Position", font=("goudy old style",18), bg="white").place(x=1150, y=175)

        txt_email= ctk.CTkEntry(self.emp_infoframe, textvariable= self.var_email, font=("Times new roman",18), fg_color="lightyellow", width=250, height=30).place(x=140, y=140)
        self.txt_pass= ctk.CTkEntry(self.emp_infoframe, textvariable= self.var_pass, font=("Times new roman",18), fg_color="lightyellow", width=200, height=30, show='*')
        self.txt_pass.place(x=550, y=140)
        
        # # CTkCheckBox for "Show Password"
        self.chk_show_pass = IntVar()
        show_pass = ctk.CTkCheckBox(
            self.emp_infoframe,
            text="Show",
            variable=self.chk_show_pass,

            onvalue=1,
            offvalue=0,
            command=self.toggle_show_pass,
            bg_color="white",
            fg_color="#0099FF",
            hover_color="#33CCFF",
            text_color="black",
            font=("goudy old style", 14, "italic"),
            )
        show_pass.place(x=760, y=145)


        cmb_utype = ctk.CTkComboBox(self.emp_infoframe, 
                                        variable=self.var_utype,  # Gắn biến textvariable
                                        values=["Manager", "Employee"],  # Các tùy chọn
                                        state="readonly",  # Chỉ đọc
                                        justify="center",  # Căn giữa
                                        font=("goudy old style", 18), width=140, height=20)  # Phông chữ
        cmb_utype.place(x=1000, y=140)
        cmb_utype.set('Manager')
        
       
        # #==row 4==
        lbl_address= Label(self.emp_infoframe, text="Address", font=("goudy old style",18), bg="white").place(x=80, y=270)
        lbl_salary= Label(self.emp_infoframe, text="Salary", font=("goudy old style",18), bg="white").place(x=800, y=270)


        self.txt_address = ctk.CTkTextbox(self.emp_infoframe, font=("Times new roman", 18), fg_color="lightyellow",
                                  border_color="gray",  # Màu viền
                                  border_width=2, width=320, height=70)
        
        self.txt_address.place(x=150, y=200)

        txt_salary= ctk.CTkEntry(self.emp_infoframe, textvariable= self.var_salary, font=("Times new roman",18), fg_color="lightyellow", width=180, height=30).place(x=710, y=215)

        # Buttons

        bnt_add = ctk.CTkButton(self.emp_infoframe, text="Save", command=self.add, font=("goudy old style", 18, "bold"),
                             fg_color="#2196f3",
                             text_color="White",
                             hover_color="#66CCFF",
                             corner_radius=8,
                             width=100, height=40)

        bnt_add.place(x=720, y=280)

        
        
    
        bnt_update = ctk.CTkButton(self.emp_infoframe, text="Update", command=self.update, font=("goudy old style", 18, "bold"),
                             fg_color="#4caf50",
                             text_color="White",
                             hover_color="#66CC00",
                             corner_radius=8,
                             width=100, height=40)

        bnt_update.place(x=830, y=280) 



         
        bnt_delete = ctk.CTkButton(self.emp_infoframe, text="Delete", command=self.delete, font=("goudy old style", 18, "bold"),
                             fg_color="#f44336",
                             text_color="White",
                             hover_color="#FF6633",
                             corner_radius=8,
                             width=100, height=40)

        bnt_delete.place(x=940, y=280)


        
        bnt_clear = ctk.CTkButton(self.emp_infoframe, text="Clear", command=self.clear, font=("goudy old style", 18, "bold"),
                             fg_color="#607d8b",
                             text_color="White",
                             hover_color="#BBBBBB",
                             corner_radius=8,
                             width=100, height=40)

        bnt_clear.place(x=1050, y=280)   

         # Employee details section
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=650, relwidth=1, height=280)

        # Scrollbars
        scrooly = Scrollbar(emp_frame, orient=VERTICAL, width=20)
        scroolx = Scrollbar(emp_frame, orient=HORIZONTAL, width=20)

        # Treeview widget
        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("Emp.No", "Name", "Gender", "Email", "Contact", "D.O.B", "D.O.J", "Password", "Position", "Address", "Salary"),
                                          yscrollcommand=scrooly.set, xscrollcommand=scroolx.set)

        #Pack scrollbars
        scroolx.pack(side=BOTTOM, fill=X)
        scrooly.pack(side=RIGHT, fill=Y)
        # Configure scrollbars to Treeview
        scroolx.config(command=self.EmployeeTable.xview)
        scrooly.config(command=self.EmployeeTable.yview)


        # Set up Treeview columns and headers
        self.EmployeeTable.heading("Emp.No", text="Emp.No")
        self.EmployeeTable.heading("Name", text="Name")
        self.EmployeeTable.heading("Gender", text="Gender")
        self.EmployeeTable.heading("Email", text="Email")
        self.EmployeeTable.heading("Contact", text="Contact")
        self.EmployeeTable.heading("D.O.B", text="D.O.B")
        self.EmployeeTable.heading("D.O.J", text="D.O.J")
        self.EmployeeTable.heading("Password", text="Password")
        self.EmployeeTable.heading("Position", text="Position")
        self.EmployeeTable.heading("Address", text="Address")
        self.EmployeeTable.heading("Salary", text="Salary")
        self.EmployeeTable["show"] = "headings"

          # Set column widths
        self.EmployeeTable.column("Emp.No", width=90)
        self.EmployeeTable.column("Name", width=180)
        self.EmployeeTable.column("Gender", width=150)
        self.EmployeeTable.column("Email", width=200)
        self.EmployeeTable.column("Contact", width=150)
        self.EmployeeTable.column("D.O.B", width=150)
        self.EmployeeTable.column("D.O.J", width=150)
        self.EmployeeTable.column("Password", width=150)
        self.EmployeeTable.column("Position", width=150)
        self.EmployeeTable.column("Address", width=230)
        self.EmployeeTable.column("Salary", width=150)

        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

 #===================================================================================    
    def toggle_show_pass(self):
        """Hiển thị hoặc ẩn mật khẩu cũ."""
        if self.chk_show_pass.get():  # Nếu checkbox được tick
            self.txt_pass.configure(show="")  # Hiển thị mật khẩu
        else:
            self.txt_pass.configure(show="*")  # Ẩn mật khẩu


    
#=========================def add===================================
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

            # Kiểm tra các trường bắt buộc
            if (self.var_emp_id.get() == "" or self.var_name.get() == "" or self.var_gender.get() == "" or
                self.var_email.get() == "" or self.var_contact.get() == "" or self.var_dob.get() == "" or
                self.var_doj.get() == "" or self.var_utype.get() == "" or self.var_salary.get() == ""):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            # Kiểm tra định dạng ngày
            try:
                dob = datetime.strptime(self.var_dob.get(), '%d-%m-%Y')
                doj = datetime.strptime(self.var_doj.get(), '%d-%m-%Y')
            except ValueError:
                messagebox.showerror("Error", "Date format must be DD-MM-YYYY", parent=self.root)
                return

            # Kiểm tra nhân viên đã tồn tại
            cursor.execute("SELECT * FROM Employee WHERE Emp_No = ?", (self.var_emp_id.get(),))
            row = cursor.fetchone()
            if row:
                messagebox.showerror("Error", "This Employee ID already exists", parent=self.root)
                return

            # Kiểm tra password
            if self.var_utype.get() == "Manager":
                if self.var_pass.get() == "":
                    messagebox.showerror("Error", "Password is required for Managers", parent=self.root)
                    return
                # Hash mật khẩu
                hashed_password = hashlib.sha256(self.var_pass.get().encode()).hexdigest()
            else:
                if self.var_pass.get() != "":
                    messagebox.showerror("Error", "Only Managers can set a password", parent=self.root)
                    return
                hashed_password = ""  # Không lưu mật khẩu nếu không phải Manager

            # Kiểm tra SĐT hoặc Email đã tồn tại
            cursor.execute("SELECT * FROM Employee WHERE Email = ? OR Contact = ?", (self.var_email.get(), self.var_contact.get()))
            row = cursor.fetchone()
            if row:
                messagebox.showerror("Error", "This Email or Contact number already exists", parent=self.root)
                return

            # Chèn dữ liệu vào cơ sở dữ liệu
            cursor.execute(
                "INSERT INTO Employee (Emp_No, Name, Gender, Contact, DOB, DOJ, Email, Password, Position, Address, Salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.var_emp_id.get(),
                    self.var_name.get(),
                    self.var_gender.get(),
                    self.var_contact.get(),
                    dob.strftime('%Y-%m-%d'),  # Chuyển sang YYYY-MM-DD cho SQL Server
                    doj.strftime('%Y-%m-%d'),
                    self.var_email.get(),
                    hashed_password,  # Lưu mật khẩu đã được hash
                    self.var_utype.get(),
                    self.txt_address.get('1.0', END).strip(),
                    self.var_salary.get()
                )
            )
            conn.commit()

            # Cập nhật giao diện Treeview với mật khẩu bị mã hóa thành '*'
            masked_password = "*" * len(self.var_pass.get()) if self.var_utype.get() == "Manager" else ""
            new_data = (
                self.var_emp_id.get(),
                self.var_name.get(),
                self.var_gender.get(),
                self.var_email.get(),
                self.var_contact.get(),
                self.var_dob.get(),
                self.var_doj.get(),
                masked_password,  # Hiển thị mật khẩu mã hóa trong Treeview
                self.var_utype.get(),
                self.txt_address.get('1.0', END).strip(),
                self.var_salary.get()
            )
            self.EmployeeTable.insert("", "end", values=new_data)

            messagebox.showinfo("Success", "Employee added successfully", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()


#=================Show==========================
    def show(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
                'charset=utf8'  # Đảm bảo kết nối với SQL Server sử dụng UTF-8
            )
            cursor = conn.cursor()

            # Truy vấn để lấy tất cả dữ liệu từ bảng Employee
            cursor.execute("SELECT Emp_No, Name, Gender, Email, Contact, DOB, DOJ, Password, Position, Address, Salary FROM Employee")
            rows = cursor.fetchall()

            # Xóa các dữ liệu cũ trong bảng hiển thị (nếu có)
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())

            for row in rows:
                # Chuyển đổi dữ liệu thành danh sách để dễ xử lý
                data_row = list(row)

                # Định dạng lại ngày tháng (DOB và DOJ)
                if isinstance(data_row[5], datetime):  # Giả định rằng DOB là cột thứ 6
                    data_row[5] = data_row[5].strftime('%d-%m-%Y')  # D.O.B
                if isinstance(data_row[6], datetime):  # Giả định rằng DOJ là cột thứ 7
                    data_row[6] = data_row[6].strftime('%d-%m-%Y')  # D.O.J

                # Hiển thị mật khẩu dưới dạng dấu '*'
                if len(data_row) > 7:  # Giả định rằng cột mật khẩu là cột thứ 8
                    data_row[7] = '*' * len(data_row[7]) if data_row[7] else ""

                # Kiểm tra xem dữ liệu có đủ để chèn vào Treeview không
                if len(data_row) == len(self.EmployeeTable["columns"]):
                    self.EmployeeTable.insert("", "end", values=data_row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()



#==============def get_data()====================
    def get_data(self, ev):
     try:
        # Lấy dòng hiện tại được chọn trong Treeview
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content['values']

        if row:
            # Kiểm tra giá trị của row[2] (Giới tính)
            gender_value = row[2].strip()  # Loại bỏ khoảng trắng dư thừa
            # Gán dữ liệu của dòng được chọn vào các biến
            self.var_emp_id.set(row[0])  # Emp.No
            self.var_name.set(row[1])    # Name
            self.var_email.set(row[3])   # Email
            self.var_contact.set(row[4]) # Contact

            # Kiểm tra giới tính và cập nhật giá trị cho Radiobutton
            if gender_value == "Male":
                self.var_gender.set("Male")  # Nếu là Male thì chọn Male
            elif gender_value == "Female":
                self.var_gender.set("Female")  # Nếu là Female thì chọn Female
            else:
                self.var_gender.set(None)  # Đảm bảo giá trị hợp lệ nếu có trường hợp khác

            # Cập nhật các biến khác
            contact_value = str(row[4])
            if contact_value and not contact_value.startswith('0'):
                contact_value = '0' + contact_value  # Chỉ thêm số 0 nếu chưa có
            self.var_contact.set(contact_value)  # Contact

            # Cập nhật các biến ngày sinh, ngày vào làm...
            if row[5]:
                try:
                    dob_date = datetime.strptime(row[5], '%Y-%m-%d')  # Chuyển từ YYYY-MM-DD sang object datetime
                    self.var_dob.set(dob_date.strftime('%d-%m-%Y'))    # Hiển thị định dạng DD-MM-YYYY
                except ValueError:
                    self.var_dob.set(row[5])  # Giữ nguyên nếu không chuyển được

            # Chuyển định dạng ngày vào làm (DOJ) từ YYYY-MM-DD sang DD-MM-YYYY
            if row[6]:
                try:
                    doj_date = datetime.strptime(row[6], '%Y-%m-%d')  # Chuyển từ YYYY-MM-DD sang object datetime
                    self.var_doj.set(doj_date.strftime('%d-%m-%Y'))    # Hiển thị định dạng DD-MM-YYYY
                except ValueError:
                    self.var_doj.set(row[6])  # Giữ nguyên nếu không chuyển được

            self.var_pass.set(row[7])  # Password
            self.var_utype.set(row[8])  # Position
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[9])  # Address
            self.var_salary.set(row[10])  # Salary

     except Exception as e:
        print(f"Error: {e}")



#=============UPDATE==================
    def update(self):
        try:
            # Kiểm tra các trường bắt buộc
            if (self.var_emp_id.get() == "" or self.var_name.get() == "" or self.var_gender.get() == "" or
                self.var_email.get() == "" or self.var_contact.get() == "" or self.var_dob.get() == "" or
                self.var_doj.get() == "" or self.var_utype.get() == "" or self.var_salary.get() == ""):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            # Kết nối SQL Server
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Kiểm tra định dạng ngày tháng
            try:
                dob = datetime.strptime(self.var_dob.get(), '%d-%m-%Y')
                doj = datetime.strptime(self.var_doj.get(), '%d-%m-%Y')
            except ValueError:
                messagebox.showerror("Error", "Date format must be DD-MM-YYYY", parent=self.root)
                return

            # Lấy dữ liệu hiện tại từ cơ sở dữ liệu
            cursor.execute("SELECT * FROM Employee WHERE Emp_No = ?", (self.var_emp_id.get(),))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "This Employee ID does not exist", parent=self.root)
                return

            # Lấy giá trị hiện tại
            original_password = row[6]  # Password cũ
            current_role = row[8]  # Vai trò hiện tại (Manager hoặc Employee)

            # Kiểm tra chuyển đổi vai trò
            if self.var_utype.get() == "Employee" and current_role == "Manager":  # Chuyển từ Manager -> Employee
                self.var_pass.set("")  # Xóa Password trên Entry
                sql_query = """
                    UPDATE Employee
                    SET Name=?, Gender=?, Contact=?, DOB=?, DOJ=?, Email=?, Position=?, Address=?, Salary=?, Password=NULL
                    WHERE Emp_No=?
                """
                params = (
                    self.var_name.get(),
                    self.var_gender.get(),
                    self.var_contact.get(),
                    dob.strftime('%Y-%m-%d'),
                    doj.strftime('%Y-%m-%d'),
                    self.var_email.get(),
                    self.var_utype.get(),
                    self.txt_address.get('1.0', END).strip(),
                    self.var_salary.get(),
                    self.var_emp_id.get()
                )
            elif self.var_utype.get() == "Manager" and current_role == "Employee":  # Chuyển từ Employee -> Manager
                if self.var_pass.get() == "":
                    messagebox.showerror("Error", "Password is required for Manager role", parent=self.root)
                    return

                # Mã hóa mật khẩu bằng hashlib (SHA-256)
                hashed_password = hashlib.sha256(self.var_pass.get().encode()).hexdigest()

                sql_query = """
                    UPDATE Employee
                    SET Name=?, Gender=?, Contact=?, DOB=?, DOJ=?, Email=?, Password=?, Position=?, Address=?, Salary=?
                    WHERE Emp_No=?
                """
                params = (
                    self.var_name.get(),
                    self.var_gender.get(),
                    self.var_contact.get(),
                    dob.strftime('%Y-%m-%d'),
                    doj.strftime('%Y-%m-%d'),
                    self.var_email.get(),
                    hashed_password,  # Lưu mật khẩu đã mã hóa
                    self.var_utype.get(),
                    self.txt_address.get('1.0', END).strip(),
                    self.var_salary.get(),
                    self.var_emp_id.get()
                )
            else:  # Không có thay đổi đặc biệt
                sql_query = """
                    UPDATE Employee
                    SET Name=?, Gender=?, Contact=?, DOB=?, DOJ=?, Email=?, Position=?, Address=?, Salary=?
                    WHERE Emp_No=?
                """
                params = (
                    self.var_name.get(),
                    self.var_gender.get(),
                    self.var_contact.get(),
                    dob.strftime('%Y-%m-%d'),
                    doj.strftime('%Y-%m-%d'),
                    self.var_email.get(),
                    self.var_utype.get(),
                    self.txt_address.get('1.0', END).strip(),
                    self.var_salary.get(),
                    self.var_emp_id.get()
                )

            # Thực thi câu lệnh SQL
            cursor.execute(sql_query, params)
            conn.commit()

            messagebox.showinfo("Success", "Employee updated successfully", parent=self.root)

            # Làm mới Treeview
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()





#===========delete==============
    def delete(self):
     try:
        # Lấy bản ghi hiện tại từ Treeview
        f = self.EmployeeTable.focus()
        if not f:  # Kiểm tra nếu không có bản ghi nào được chọn
            messagebox.showerror("Error", "Please select an employee to delete", parent=self.root)
            return

        # Lấy thông tin nhân viên từ bản ghi đã chọn
        content = self.EmployeeTable.item(f)
        row = content['values']

        if not row:  # Kiểm tra xem có dữ liệu trong hàng đã chọn hay không
            messagebox.showerror("Error", "Unable to retrieve the selected employee data.", parent=self.root)
            return

        emp_no =str(row[0])  # Giả sử Emp_No là cột đầu tiên trong Treeview

        # Xác nhận việc xóa
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Employee {emp_no}?", parent=self.root)
        if not confirm:
            return  # Dừng lại nếu người dùng không muốn tiếp tục xóa

        # Kết nối tới cơ sở dữ liệu
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )
        cursor = conn.cursor()

        # Kiểm tra xem nhân viên có tồn tại trước khi xóa
        cursor.execute("SELECT * FROM Employee WHERE Emp_No = ?", (emp_no,))
        result = cursor.fetchone()

        if not result:  # Nếu không tìm thấy nhân viên trong cơ sở dữ liệu
            messagebox.showerror("Error", f"Employee {emp_no} does not exist in the database.", parent=self.root)
            return

        # Thực hiện xóa bản ghi
        cursor.execute("DELETE FROM Employee WHERE Emp_No = ?", (emp_no,))
        conn.commit()

        # Kiểm tra số lượng bản ghi đã bị ảnh hưởng bởi câu lệnh DELETE
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Deletion failed. No records were deleted.", parent=self.root)
        else:
            # Xóa bản ghi từ Treeview sau khi xóa thành công trong DB
            self.EmployeeTable.delete(f)
            messagebox.showinfo("Success", f"Employee {emp_no} deleted successfully", parent=self.root)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        if conn:
            conn.close()

   
#============Clear==============
    def clear(self):
        self.var_emp_id.set("")          # Xóa Emp_ID
        self.var_name.set("")            # Xóa Tên
        self.var_gender.set("Male")          # Xóa Giới tính
        self.var_email.set("")           # Xóa Email
        self.var_contact.set("")         # Xóa Số điện thoại
        self.var_dob.set("")             # Xóa Ngày sinh
        self.var_doj.set("")             # Xóa Ngày vào làm
        self.var_pass.set("")            # Xóa Mật khẩu
        self.var_utype.set("Manager")           # Xóa Vị trí
        self.txt_address.delete('1.0', END)  # Xóa địa chỉ
        self.var_salary.set("")          # Xóa Lương
        self.var_searchtxt.set("")



#=============Search==============
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
        elif search_by == "Highest Salary":
            # Thực sự gọi hàm tìm mức lương cao nhất
            self.search_highest_salary()  # Thêm dấu ngoặc tròn () để gọi hàm
            return
        elif search_text == "":
            # Nếu chọn không phải "Highest Salary" và không nhập gì thì mới báo lỗi
            messagebox.showerror("Error", "Search input is required", parent=self.root)
            return
        
        # Xử lý tìm kiếm cho từng cột nếu không phải "Highest Salary"
        if search_by == "Emp.No":
            query = "SELECT * FROM Employee WHERE Emp_No LIKE ?"
            cursor.execute(query, f'%{search_text}%')
        elif search_by == "Name":
            query = "SELECT * FROM Employee WHERE Name LIKE ?"
            cursor.execute(query, f'%{search_text}%')
        elif search_by == "Email":
            query = "SELECT * FROM Employee WHERE Email LIKE ?"
            cursor.execute(query, f'%{search_text}%')
        else:
            messagebox.showerror("Error", "Invalid search option", parent=self.root)
            return

        # Lấy kết quả truy vấn
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ trong Treeview
        self.EmployeeTable.delete(*self.EmployeeTable.get_children())

        if rows:
            for row in rows:
                data_row = list(row)

                # Chuyển đổi định dạng ngày tháng từ YYYY-MM-DD về DD-MM-YYYY
                if isinstance(data_row[5], datetime):  # Giả định rằng D.O.B là cột thứ 6
                    data_row[5] = data_row[5].strftime('%d-%m-%Y')  # D.O.B
                if isinstance(data_row[6], datetime):  # Giả định rằng D.O.J là cột thứ 7
                    data_row[6] = data_row[6].strftime('%d-%m-%Y')  # D.O.J

                # Thêm dữ liệu vào Treeview
                if len(data_row) == len(self.EmployeeTable["columns"]):
                    self.EmployeeTable.insert("", "end", values=data_row)
        else:
            messagebox.showinfo("Info", "No records found", parent=self.root)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
     finally:
        if conn:
            conn.close()

   
#=================Highest salary===========================

    def search_highest_salary(self):
     try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )
        cursor = conn.cursor()

        # Truy vấn mức lương cao nhất
        query = "SELECT * FROM Employee WHERE Salary = (SELECT MAX(Salary) FROM Employee)"
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            messagebox.showinfo("Info", "No records found for highest salary.", parent=self.root)
            return
        self.display_data(rows)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
     finally:
        if conn:
            conn.close()

#=============Display===================

    def display_data(self, rows):
    # Xóa các dữ liệu cũ trong bảng hiển thị (nếu có)
     self.EmployeeTable.delete(*self.EmployeeTable.get_children())

     for row in rows:
        # Chuyển đổi dữ liệu thành danh sách để dễ xử lý
        data_row = list(row)

        # Nếu cần, chuyển đổi định dạng ngày tháng từ YYYY-MM-DD về DD-MM-YYYY
        if isinstance(data_row[5], datetime):  # Giả định rằng DOB là cột thứ 6
            data_row[5] = data_row[5].strftime('%d-%m-%Y')  # D.O.B
        if isinstance(data_row[6], datetime):  # Giả định rằng DOJ là cột thứ 7
            data_row[6] = data_row[6].strftime('%d-%m-%Y')  # D.O.J

        # Kiểm tra số lượng phần tử trong row có khớp với số cột không
        if len(data_row) == len(self.EmployeeTable["columns"]):
         self.EmployeeTable.insert("", "end", values=data_row)


# Khởi động ứng dụng
if __name__ == "__main__":
    root = ctk.CTk()
    obj = EmployeeClass(root)
    root.mainloop()