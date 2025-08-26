import customtkinter as ctk
from tkinter import ttk

# Tạo ứng dụng chính
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CTk with Treeview Example")
        self.geometry("600x400")

        # Label sử dụng CTkLabel
        lbl_title = ctk.CTkLabel(self, text="Product List", font=("Arial", 16))
        lbl_title.pack(pady=10)

        # Frame để chứa Treeview
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview trong frame
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price"), show="headings", height=10)
        self.tree.pack(fill="both", expand=True)

        # Định nghĩa cột
        self.tree.heading("ID", text="Product ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Price", text="Price")

        # Căn chỉnh cột
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Price", width=100, anchor="e")

        # Thêm dữ liệu mẫu
        data = [
            (1, "Apple", "$1"),
            (2, "Banana", "$0.5"),
            (3, "Cherry", "$2"),
        ]
        for item in data:
            self.tree.insert("", "end", values=item)

        # Nút thoát sử dụng CTkButton
        btn_quit = ctk.CTkButton(self, text="Quit", command=self.quit)
        btn_quit.pack(pady=10)

# Khởi chạy ứng dụng
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Giao diện Dark
    ctk.set_default_color_theme("blue")  # Chủ đề màu xanh
    app = App()
    app.mainloop()
