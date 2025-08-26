from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import pyodbc
from datetime import datetime
from pathlib import Path
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import time
import random
import os
import datetime

class ImportClass:
    def __init__(self, root, emp_no, emp_name):
        self.root = root
        self.root.geometry("1250x810+220+30")
        self.root.title("Import Management")
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


        self.var_empNo= StringVar(value=emp_no)
        self.var_empName= StringVar(value=emp_name)
        self.var_CategoryName= StringVar()
        self.var_Description= StringVar()

         # Store Frame
        SupplierFrame = Frame(self.root, bd=4, relief=RIDGE, bg='#FFFFFF')
        SupplierFrame.place(x=80, y=50, width=800, height=207)

          # Title
        title_supplier = Label(SupplierFrame, text="Supplier Details", font=("goudy old style", 22), bg="light gray").pack(side=TOP, fill=X)

        self.fetch_supplier_data(SupplierFrame)


        self.ImportFrame= Frame(self.root, relief=RIDGE, bg="white")
        self.ImportFrame.place(x=40, y=300, width=820, height=680)

        lbl_empNo= Label(self.ImportFrame, text="Emp.No", font=("goudy old style",18), bg="white").place(x=80, y=10)
        txt_empid= ctk.CTkEntry(self.ImportFrame, textvariable= self.var_empNo, font=("Times new roman",18), fg_color="lightyellow", state="readonly", width=180, height=30).place(x=160, y=8)

        lbl_empName= Label(self.ImportFrame, text="Emp Name", font=("goudy old style",18), bg="white").place(x=80, y=100)

        txt_empid= ctk.CTkEntry(self.ImportFrame, textvariable= self.var_empName, font=("Times new roman",18), fg_color="lightyellow", state="readonly", width=180, height=30).place(x=180, y=80)
        
        lbl_CategoryName= Label(self.ImportFrame, text="Category Name", font=("goudy old style",18), bg="white").place(x=80, y=230)

        txt_CategoryName = ctk.CTkEntry(self.ImportFrame, textvariable=self.var_CategoryName, font=("Times new roman", 18), fg_color="lightyellow", width=230, height=30).place(x=220, y=183)

        lbl_description= Label(self.ImportFrame, text="Description", font=("goudy old style",18), bg="white").place(x=80, y=380)

        
        self.txt_description = ctk.CTkTextbox(self.ImportFrame, font=("Times new roman", 18), fg_color="lightyellow",
                                  border_color="gray",  # Màu viền
                                  border_width=2, width=400, height=160)
        
        self.txt_description.place(x=210, y=260)

           # Store Frame
        Bill_Imported_Frame = Frame(self.root, bd=8, relief=RIDGE, bg='#FFFFFF')
        Bill_Imported_Frame.place(x=880, y=50, width=610, height=800)

        # Title
        title = Label(Bill_Imported_Frame, text="Bill Imported Area", font=("goudy old style", 25, "bold"), bg="#FF3333", fg="white", padx=23, pady=9)
        title.pack(side=TOP, fill=X)

        # Thanh cuộn dọc
        self.scrooly_y = Scrollbar(Bill_Imported_Frame, orient=VERTICAL)
        # Thanh cuộn ngang
        self.scrooly_x = Scrollbar(Bill_Imported_Frame, orient=HORIZONTAL)

             # Text widget (với padding, căn sát bên trái, wrap=NONE để cho phép cuộn ngang)
        self.txt_bill_area = ctk.CTkTextbox(Bill_Imported_Frame, yscrollcommand=self.scrooly_y.set, xscrollcommand=self.scrooly_x.set, 
                                wrap=NONE, padx=10, pady=10, font=("Courier New", 10), width=50, height=20, fg_color="white")
        self.txt_bill_area.pack(fill=BOTH, expand=1)


               # Cấu hình thanh cuộn dọc
        self.scrooly_y.config(command=self.txt_bill_area.yview)
        self.scrooly_y.pack(side=RIGHT, fill=Y)

        # Cấu hình thanh cuộn ngang
        self.scrooly_x.config(command=self.txt_bill_area.xview)
        self.scrooly_x.pack(side=BOTTOM, fill=X)


                
                # Kiểm tra và ẩn thanh cuộn nếu không cần thiết
        self.txt_bill_area.bind("<Configure>", self.check_scrollbars)

         #Billing button
        btn_BillFrame= Frame(self.root, relief=RIDGE, bg='#FFFFFF')
        btn_BillFrame.place(x=880, y=860, width=610, height=140)


        self.btn_print =ctk.CTkButton(btn_BillFrame, text="Print", command=self.print_bill,
                           font=("Goudy Old Style", 18, "bold"), 
                           fg_color="#33CC00", text_color="white", 
                           hover_color="#339900",  # Màu khi hover
                           corner_radius=8,  # Bo góc cho nút
                           cursor="hand2", width=120, height=60)
        self.btn_print.place(x=20, y=30)


        self.btn_ClearAll = ctk.CTkButton(btn_BillFrame, text="Clear All", command=self.clear_all,
                                    font=("Goudy Old Style", 18, "bold"), 
                                    fg_color="gray", text_color="white", 
                                    hover_color="#B3B3B3",  # Màu khi hover
                                    corner_radius=8,  # Bo góc cho nút
                                    cursor="hand2", width=120, height=60)
        self.btn_ClearAll.place(x=175, y=30)


        self.btn_Generate= ctk.CTkButton(btn_BillFrame, text="Generate/Save Bill", font=("goudy old style", 18, "bold"), command=self.generate_bill,
                                    fg_color="#009688",
                                    text_color="white", 
                                    hover_color='#00695C',
                                    corner_radius=8,
                                    cursor="hand2" , width=130, height=60)
        self.btn_Generate.place(x=330, y=30) 



        self.btn_Add= ctk.CTkButton(self.ImportFrame, text="Add to Bill", font=("goudy old style", 18, "bold"), command=self.add_to_bill,
                                    fg_color="#3366FF",
                                    text_color="white", 
                                    hover_color='#00CCFF',
                                    corner_radius=8,
                                    cursor="hand2" , width=130, height=60)
        self.btn_Add.place(x=280, y=475) 


        self.btn_Clear= ctk.CTkButton(self.ImportFrame, text="Clear", font=("goudy old style", 18, "bold"), command=self.clear,
                                    fg_color="#FF9900",
                                    text_color="white", 
                                    hover_color='#FFCC33',
                                    corner_radius=8,
                                    cursor="hand2" , width=130, height=60)
        self.btn_Clear.place(x=430, y=475) 


#====================def fetch_store_data======================
    def fetch_supplier_data(self, SupplierFrame):
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
            cursor.execute("SELECT Sup_ID, Sup_Name, Address, Contact FROM Supplier")
            rows = cursor.fetchall()

            # Khung chứa Listbox và thanh cuộn
            listbox_frame = Frame(SupplierFrame)
            listbox_frame.place(x=0, y=40, width=793, height=160)

            # Tạo thanh cuộn dọc và ngang
            scrollbar_y = Scrollbar(listbox_frame, orient=VERTICAL)
            scrollbar_x = Scrollbar(listbox_frame, orient=HORIZONTAL)

            # Tạo Listbox với thanh cuộn
            self.listbox = Listbox(
                listbox_frame, font=("Times new roman", 16), bg="white", selectmode=SINGLE,
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

#====================def check_scrollbars===================
    def check_scrollbars(self, event=None):
        """
        Kiểm tra xem nội dung có vượt qua kích thước của Text widget hay không, 
        nếu không thì ẩn thanh cuộn tương ứng.
        """
        # Kiểm tra cuộn dọc
        if self.txt_bill_area.yview() == (0.0, 1.0):  # Nội dung không cần cuộn dọc
            self.scrooly_y.pack_forget()  # Ẩn thanh cuộn dọc
        else:
            self.scrooly_y.pack(side=RIGHT, fill=Y)  # Hiển thị lại nếu cần

        # Kiểm tra cuộn ngang
        if self.txt_bill_area.xview() == (0.0, 1.0):  # Nội dung không cần cuộn ngang
            self.scrooly_x.pack_forget()  # Ẩn thanh cuộn ngang
        else:
            self.scrooly_x.pack(side=BOTTOM, fill=X)  # Hiển thị lại nếu cần



#===========================def add_to_bill=============================
    def add_to_bill(self):
     try:
        # Lấy dữ liệu từ StringVar
        emp_no = self.var_empNo.get().strip()
        emp_name = self.var_empName.get().strip()
        category_name = self.var_CategoryName.get().strip()

        # Lấy dữ liệu từ Textbox (self.txt_description)
        description = self.txt_description.get("1.0", END).strip()  # Lấy nội dung từ dòng đầu đến cuối và loại bỏ khoảng trắng

        # Kiểm tra xem các trường bắt buộc có được nhập hay không
        if not emp_no or not emp_name or not category_name or not description:
            messagebox.showerror("Error", "Please fill in all required fields (Emp.No, Emp.Name, Category Name, and Description).", parent=self.root)
            return

        # Kiểm tra nội dung hiện tại trong txt_bill_area
        current_bill_content = self.txt_bill_area.get("1.0", END).strip()

        if "Invoice.No:" not in current_bill_content:
            # Tạo Invoice_No ngẫu nhiên (6 chữ số)
            invoice_no = f"{random.randint(100000, 999999)}"

            # Kiểm tra xem có chọn dữ liệu từ Listbox không (chỉ cần kiểm tra lần đầu)
            selected_supplier = self.listbox.curselection()
            if not selected_supplier:
                messagebox.showwarning("Warning", "Please select a supplier from the list.", parent= self.root)
                return

            # Lấy dữ liệu từ Listbox
            supplier_info = self.listbox.get(selected_supplier[0])  # Dữ liệu dạng "Sup_ID - Sup_Name - Address - Contact"
            supplier_details = supplier_info.split(" - ")  # Tách chuỗi theo dấu " - "
            supplier_details_formatted = f"""Supplier.ID: {supplier_details[0]}
Supplier Name: {supplier_details[1]}
Address: {supplier_details[2]}
Contact: {supplier_details[3]}"""

            # Định dạng thông tin đầy đủ (khi chưa có gì trong hóa đơn)
            full_bill_content = f"""Invoice.No: {invoice_no}
Emp.No: {emp_no}
Employee Name: {emp_name}
Date: {time.strftime("%d/%m/%Y")}
Time: {time.strftime("%H:%M:%S")}
{"="*76}
{supplier_details_formatted}
{"="*76}
Category Information:
Category Name: {category_name}
Description: 
\n{description}

"""
            # Thêm nội dung đầy đủ vào Text Widget
            self.txt_bill_area.insert(END, full_bill_content)
        else:
            # Khi hóa đơn đã có thông tin cơ bản, chỉ thêm Category Name và Description mới
            additional_content = f"""
{"="*76}
Category Information:
Category Name: {category_name}
Description: 
\n{description}


"""
            # Thêm nội dung mới vào Text Widget
            self.txt_bill_area.insert(END, additional_content)

     except Exception as e:
        messagebox.showerror("Error", f"Error adding to bill: {str(e)}")


#============================def generate_bill============================

    def generate_bill(self):
     try:
        # Hiển thị hộp thoại xác nhận
        confirm = messagebox.askyesno("Confirm", "Are you sure to generate the bill?", parent=self.root)
        if not confirm:
            return  # Nếu người dùng chọn "No", thoát hàm
        
        # Lấy nội dung từ Text widget
        bill_content = self.txt_bill_area.get("1.0", "end").strip()
        if not bill_content:
            messagebox.showerror("Error", "The bill is empty. Cannot save an empty bill.", parent=self.root)
            return
        
        # Tìm Invoice No, Employee No, và Supplier ID trong bill
        invoice_no = None
        emp_no = None
        sup_id = None
        for line in bill_content.split("\n"):
            if line.startswith("Invoice.No:"):
                invoice_no = line.split(":")[1].strip()
            elif line.startswith("Emp.No:"):
                emp_no = line.split(":")[1].strip()
            elif line.startswith("Supplier.ID:"):
                sup_id = line.split(":")[1].strip()
        
        # Kiểm tra thông tin bắt buộc
        if not invoice_no:
            messagebox.showerror(
                "Error",
                "Invoice number not found in the bill.\nPlease add at least one category to the bill before saving.", parent=self.root
            )
            return
        if not emp_no or not sup_id:
            messagebox.showerror(
                "Error",
                "Missing Employee No or Supplier ID in the bill.\nPlease ensure all required fields are filled.", parent=self.root
            )
            return
        
        # Lấy ngày giờ hiện tại
        date_imported = datetime.datetime.now().strftime('%Y-%m-%d')  # Ngày hiện tại
        time_imported = datetime.datetime.now().strftime('%H:%M:%S')  # Thời gian hiện tại
       # Kết nối tới SQL Server
        conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=LAPTOP-NGQUJ9MT\\QUANGVINH;'
                'DATABASE=QuanLyTonKho;'
                'UID=sa;'
                'PWD=182003;'
            )
        cursor = conn.cursor()

        # Thêm bản ghi vào bảng Import_Bill
        try:
            invoice_sql= f"Invoice.No.{invoice_no}"
            cursor.execute(
                """
                INSERT INTO Import_Bill (Invoice_No, Date_Imported, Time_Imported, Emp_no, Sup_ID)
                VALUES (?, ?, ?, ?, ?)
                """,
                (invoice_sql, date_imported, time_imported, emp_no, sup_id)
            )
            conn.commit()
        except Exception as db_error:
            conn.rollback()
            messagebox.showerror("Database Error", f"An error occurred while saving to the database: {str(db_error)}", parent=self.root)
            return
        finally:
            cursor.close()
            conn.close()
        
        # Đường dẫn lưu hóa đơn dạng file
        save_dir = "C:/Đồ án Python/bill_imported"  # Thay đổi nếu cần
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)  # Tạo thư mục nếu chưa tồn tại
        
        # Tạo tên file hóa đơn
        file_name = f"Invoice.No.{invoice_no}.txt"
        file_path = os.path.join(save_dir, file_name)
        
        # Lưu nội dung hóa đơn vào file
        with open(file_path, "w", encoding="utf-8") as bill_file:
            bill_file.write(bill_content)
        
        # Hiển thị thông báo thành công
        messagebox.showinfo(
            "Success",
            f"Bill saved successfully!\nLocation: {file_path}\nAlso saved to the database.", parent=self.root
        )
    
     except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)


#==========================def clear========================
    def clear(self):
        # Kiểm tra nếu các trường đều trống
        if not self.var_CategoryName.get().strip() and not self.txt_description.get("1.0", END).strip():
            messagebox.showerror("Error", "Both Category Name and Description are already empty!", parent=self.root)
            return  # Thoát khỏi hàm nếu các trường đã trống
        
        # Nếu có dữ liệu, xóa các trường
        self.var_CategoryName.set('')
        self.txt_description.delete("1.0", END)


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
                initialdir="C:/Đồ án Python/bill_imported",  # Đường dẫn đến thư mục hóa đơn
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
#========================def clear_all=======================

    def clear_all(self):
        # Kiểm tra nếu Text Widget txt_bill_area trống
        if not self.txt_bill_area.get('1.0', 'end-1c').strip():  # Kiểm tra nội dung trong Text Widget
            messagebox.showerror("Error", "No bill data to clear!", parent=self.root)
            return
         # Xóa dữ liệu trong Text Widget hóa đơn
        self.txt_bill_area.delete('1.0', END)  # Xóa toàn bộ nội dung từ đầu đến cuối

        # Xóa chọn trong Listbox (nếu Listbox tồn tại)
        if hasattr(self, "listbox"):  # Kiểm tra nếu self.listbox đã được tạo
            self.listbox.selection_clear(0, END)  # Xóa toàn bộ lựa chọn trong Listbox
        
        self.var_CategoryName.set('')
        self.txt_description.delete("1.0", END)

        
        
    
if __name__ == "__main__":
    root = ctk.CTk()
    obj = ImportClass(root)
    root.mainloop()
