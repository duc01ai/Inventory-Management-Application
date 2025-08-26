from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import sys
import os
import hashlib 
import smtplib
from email.mime.text import MIMEText
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import pyodbc
import customtkinter as ctk

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x600+220+130")
        self.root.title("Login")
        self.root.config(bg="#fafafa")
        self.root.focus_force()
        
        self.username = StringVar()
        self.password = StringVar()
        self.is_otp_verified= False
        self.otp=''

# Lấy kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Load ảnh gốc và resize với độ phân giải cao
        self.login_image = Image.open("C:\Đồ án Python\image\Login.jpg")  # Đảm bảo ảnh gốc có độ phân giải cao
        self.login_image = self.login_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.login_image = ImageTk.PhotoImage(self.login_image)

        # Hiển thị ảnh làm nền
        self.label_login_image = Label(self.root, image=self.login_image, bd=0)
        self.label_login_image.place(x=0, y=0, relwidth=1, relheight=1)

        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=900, y=130, width=580, height=420)
                
        self.title = Label(login_frame, text="Login System", font=("Elephant", 25, "bold"), bg="white").pack(side=TOP, fill=X)

        lbl_user = Label(login_frame, text="Username", font=("Times new roman", 20, "bold"), bg="white", fg="#FF5722").place(x=50, y=100)

        self.txt_user = ctk.CTkEntry(login_frame, textvariable=self.username, font=("times new roman", 18), fg_color="lightgray", width=240, height=30).place(x=160, y=83)

        lbl_pass = Label(login_frame, text="Password", font=("Times new roman", 20, "bold"), bg="white", fg="#FF5722").place(x=50, y=180)

        self.txt_pass = ctk.CTkEntry(login_frame, textvariable=self.password, font=("times new roman", 18), fg_color="lightgray", width=220, height=30, show="*")
        self.txt_pass.place(x=160, y=145)

        bnt_login = ctk.CTkButton(login_frame, text="Login", command=self.login, font=("goudy old style", 20, "bold"),
                                fg_color="#2196f3", text_color="White", hover_color="#66CCFF", corner_radius=8,
                                width=120, height=40)
        bnt_login.place(x=200, y=200)

        # CTkCheckBox for "Show Password"
        self.chk_show_pass = IntVar()
        show_pass = ctk.CTkCheckBox(
            login_frame,
            text="Show Password",
            variable=self.chk_show_pass,
            onvalue=1,
            offvalue=0,
            command=self.toggle_show_pass,
            bg_color="white",
            fg_color="#FF5722",
            hover_color="#FF7043",
            text_color="black",
            font=("goudy old style", 18, "italic"),
        )
        show_pass.place(x=160, y=260)

        forgot_pass = ctk.CTkButton(
            login_frame, command=self.forgot_windown,
            text="Forgot password?",
            font=("times new roman", 14, "italic"),
            fg_color="white",
            text_color="#FF5722",
            hover_color="#F5FFFA",
            border_width=0,
            corner_radius=5
        )
        forgot_pass.place(x=180, y=300)

#======================def Login========================
    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                # Kết nối tới SQL Server
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                    'DATABASE=QuanLyTonKho;'
                    'UID=sa;'
                    'PWD=182003;'
                )
                cursor = conn.cursor()

                # Hash mật khẩu người dùng nhập (mã hóa mật khẩu)
                hashed_password = hashlib.sha256(self.password.get().encode()).hexdigest()

                # Kiểm tra username và hashed password trong bảng Employee
                query = "SELECT * FROM Employee WHERE Emp_No = ? AND Password = ?"
                cursor.execute(query, (self.username.get(), hashed_password))
                user = cursor.fetchone()

                if user is None:
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                else:
                    # Lấy tên nhân viên từ dữ liệu trả về
                    self.emp_name = user[1]  # Giả sử tên nhân viên là cột thứ 2 trong bảng (index 1)
                    self.emp_no= self.username.get()
                  # Giả sử mã nhân viên ở cột thứ 1 (index 0)
                    messagebox.showinfo("Success", f"Welcome {self.emp_name}!", parent=self.root)

                    # Đóng cửa sổ đăng nhập hiện tại
                    self.root.destroy()

                    # Chạy dashboard và truyền tên nhân viên
                    subprocess.Popen(['python', 'dashboard.py', self.emp_no, self.emp_name])
                    #subprocess.Popen(['python', 'export.py', self.emp_no])

            except pyodbc.Error as ex:
                messagebox.showerror("Error", f"Error connecting to database: {str(ex)}", parent=self.root)

            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

            finally:
                 if conn:
                    conn.close()

#=========================def toggle_password====================

    def toggle_show_pass(self):
        """Hiển thị hoặc ẩn mật khẩu cũ."""
        if self.chk_show_pass.get():  # Nếu checkbox được tick
            self.txt_pass.configure(show="")  # Hiển thị mật khẩu
        else:
            self.txt_pass.configure(show="*")  # Ẩn mật khẩu

    def toggle_show_new_pass(self):
        """Hiển thị hoặc ẩn mật khẩu mới."""
        if self.chk_show_pass1.get():  # Nếu checkbox được tick
            self.txt_new_pass.configure(show="")  # Hiển thị mật khẩu
        else:
            self.txt_new_pass.configure(show="*")  # Ẩn mật khẩu

    def toggle_show_confirm_new_pass(self):
        """Hiển thị hoặc ẩn mật khẩu xác nhận mới."""
        if self.chk_show_pass2.get():  # Nếu checkbox được tick
            self.txt_confirm_new_pass.configure(show="")  # Hiển thị mật khẩu
        else:
            self.txt_confirm_new_pass.configure(show="*")  # Ẩn mật khẩu

#=======================def forgot========================

    def forgot_windown(self):
     try:
        # Kết nối tới SQL Server
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
            'DATABASE=QuanLyTonKho;'
            'UID=sa;'
            'PWD=182003;'
        )
        cursor = conn.cursor()

        # Kiểm tra ID nhân viên có trống không
        if self.username.get() == "":
            messagebox.showerror("Error", "Username must be entered by Employee.ID", parent=self.root)
            return

        # Truy vấn email và position của nhân viên từ cơ sở dữ liệu
        cursor.execute("SELECT Email, Position FROM Employee WHERE Emp_No=?", (self.username.get(),))
        result = cursor.fetchone()

        if result is None:
            messagebox.showerror('Error', "Invalid Employee ID, try again!", parent=self.root)
        else:
            email, position = result  # Lấy địa chỉ email và vị trí từ cơ sở dữ liệu

            # Kiểm tra nếu vị trí là 'Employee' thì không cho phép reset mật khẩu
            if position == 'Employee':
                messagebox.showerror("Error", "You have not permission to reset password!", parent=self.root)
                return

            # Gửi OTP qua email
            otp = self.send_otp_email(email)

            if otp is None:
                messagebox.showerror('Error', "Failed to send OTP. Please try again later.", parent=self.root)
                return

            self.var_otp = StringVar()
            self.var_new_password = StringVar()
            self.var_confirm_password = StringVar()
            self.generated_otp = otp  # Lưu OTP đã gửi để xác thực sau

            # Tạo cửa sổ Toplevel để nhập OTP và đặt lại mật khẩu
            self.forgot_wind = ctk.CTkToplevel(self.root)
            self.forgot_wind.title("Reset Password")
            self.forgot_wind.geometry('500x430+500+100')
            self.forgot_wind.configure(bg="white")  # Đặt nền của cửa sổ Toplevel là màu trắng
            self.forgot_wind.attributes('-topmost', True)
            self.forgot_wind.focus_force()

            # Tiêu đề cửa sổ
            title = Label(self.forgot_wind, text="Reset Password", font=("Goudy Old Style", 20, "bold"), bg="#3f51b5", fg="white")
            title.pack(side=TOP, fill=X)

            lbl_reset = ctk.CTkLabel(self.forgot_wind, text="Enter OTP Sent to Your Email", font=("Times New Roman", 18))
            lbl_reset.place(x=150, y=60)

            txt_reset = ctk.CTkEntry(self.forgot_wind, textvariable=self.var_otp, font=("Times new roman", 16), fg_color="light yellow", width=230, height=35)
            txt_reset.place(x=110, y=100)

            def submit_otp():
                if self.var_otp.get() == str(self.generated_otp):  # So sánh OTP nhập vào và OTP được gửi
                    messagebox.showinfo("Success", "OTP Verified. You can now reset your password.", parent=self.forgot_wind)
                    self.is_otp_verified = True  # Đặt trạng thái OTP đã xác thực
                else:
                    messagebox.showerror("Error", "Invalid OTP. Please try again.", parent=self.forgot_wind)
                    self.is_otp_verified = False  # Đặt trạng thái OTP chưa xác thực

            bnt_submit = ctk.CTkButton(self.forgot_wind, text="Submit", font=("goudy old style", 18, "bold"),
                                    fg_color="#4caf50", text_color="White", hover_color="#66CC00",
                                    corner_radius=8, width=110, height=40, command=submit_otp)
            bnt_submit.place(x=360, y=98)

            lbl_new_pass = ctk.CTkLabel(self.forgot_wind,  text="New Password", font=("Times New Roman", 18))
            lbl_new_pass.place(x=20, y=180)

            self.txt_new_pass = ctk.CTkEntry(self.forgot_wind, textvariable=self.var_new_password, font=("Times new roman", 16), fg_color="light yellow", show="*" , width=250, height=30)
            self.txt_new_pass.place(x=20, y=220)

            lbl_confirm_new_pass = ctk.CTkLabel(self.forgot_wind, text="Confirm New Password", font=("Times New Roman", 18))
            lbl_confirm_new_pass.place(x=20, y=280)

            self.txt_confirm_new_pass = ctk.CTkEntry(self.forgot_wind, textvariable=self.var_confirm_password, font=("Times new roman", 16), fg_color="light yellow", width=250, height=30)
            self.txt_confirm_new_pass.place(x=20, y=320)

            bnt_update_pass = ctk.CTkButton(self.forgot_wind, text="Update", command=self.update_password, font=("goudy old style", 18, "bold"),
                                fg_color="#2196f3", text_color="White", hover_color="#66CCFF",
                                corner_radius=8, width=100, height=40)

            bnt_update_pass.place(x=220, y=380) 

            # CTkCheckBox for "Show Password"
            self.chk_show_pass1 = IntVar()
            show_pass = ctk.CTkCheckBox(
                self.forgot_wind,
                text="Show New Password",
                variable=self.chk_show_pass1,
                onvalue=1,
                offvalue=0,
                command=self.toggle_show_new_pass,
                fg_color="#FF5722",
                hover_color="#FF7043",
                text_color="black",
                font=("goudy old style", 15, "italic"),
            )
            show_pass.place(x=290, y=223)

            self.chk_show_pass2 = IntVar()
            show_confirm_new_pass = ctk.CTkCheckBox(
                self.forgot_wind,
                text="Show Confirm New Password",
                variable=self.chk_show_pass2,
                onvalue=1,
                offvalue=0,
                command=self.toggle_show_confirm_new_pass,
                fg_color="#FF5722",
                hover_color="#FF7043",
                text_color="black",
                font=("goudy old style", 15, "italic"),
            )
            show_confirm_new_pass.place(x=290, y=323)

     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        if conn:
            conn.close()

#=======================def send_email====================
    def send_email_via_gmail(self, to_email, subject, body):
        # Cấu hình SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        email_user = "zquangvinh359@gmail.com"  # Địa chỉ email của bạn
        email_password = "trwa fmjj zlad vtdg"  # Mật khẩu ứng dụng (App Password) bạn đã tạo

        try:
            # Tạo kết nối đến máy chủ SMTP của Gmail
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Bật mã hóa kết nối

            # Đăng nhập vào tài khoản Gmail bằng mật khẩu ứng dụng
            server.login(email_user, email_password)

            # Tạo email
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = to_email
            msg['Subject'] = subject

            # Thêm nội dung email
            msg.attach(MIMEText(body, 'plain'))

            # Gửi email
            server.sendmail(email_user, to_email, msg.as_string())
            print("Email sent successfully!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            server.quit()  # Đóng kết nối đến server


    #=======================def send_otp_email====================
    def send_otp_email(self, to_email):
        # Tạo mã OTP ngẫu nhiên
        otp = random.randint(1000, 9999)

        # Cấu trúc nội dung email
        subject = "Your OTP Code"
        body = f"Your OTP code is: {otp}\n\n Your OTP code will expire after 1 minute"

        # Gửi email bằng hàm đã định nghĩa
        try:
            self.send_email_via_gmail(to_email, subject, body)  # Gọi hàm send_email_via_gmail
            print(f"OTP sent successfully to {to_email}: {otp}")
            return otp  # Trả về OTP đã gửi
        except Exception as e:
            print(f"An error occurred while sending OTP: {str(e)}")
            return None  # Trả về None nếu có lỗi


#=========================def update password======================
    def update_password(self):
        try:
            # Kiểm tra nếu mã OTP chưa được xác thực
            if not hasattr(self, "is_otp_verified") or not self.is_otp_verified:
                messagebox.showerror("Error", "You must verify the OTP before resetting the password.", parent=self.forgot_wind)
                return

            # Kiểm tra xem các trường bắt buộc đã được nhập chưa
            if self.var_new_password.get() == '' or self.var_confirm_password.get() == '':
                messagebox.showerror("Error", "All fields are required", parent=self.forgot_wind)
                return

            # Kiểm tra xác nhận mật khẩu
            if self.var_new_password.get() != self.var_confirm_password.get():
                messagebox.showerror("Error", "Confirm password does not match!", parent=self.forgot_wind)
                return

            # Mã hóa mật khẩu mới bằng SHA-256
            hashed_password = hashlib.sha256(self.var_new_password.get().encode()).hexdigest()

            # Kết nối với SQL Server
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
            cursor = conn.cursor()

            # Cập nhật mật khẩu mới vào cơ sở dữ liệu (reset mật khẩu)
            cursor.execute(
                "UPDATE Employee SET Password=? WHERE Emp_No=?",
                (
                    hashed_password,  # Mật khẩu đã được mã hóa
                    self.username.get()  # Sử dụng Emp_No từ username đã nhập
                )
            )
            conn.commit()

         
            # Thông báo thành công
            messagebox.showinfo("Success", "Password updated successfully", parent=self.forgot_wind)
            self.forgot_wind.destroy()  # Đóng cửa sổ quên mật khẩu

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.forgot_wind)
        finally:
            if conn:
                conn.close()



if __name__ == "__main__":
    root = ctk.CTk()
    obj = Login_System(root)
    root.mainloop()


       