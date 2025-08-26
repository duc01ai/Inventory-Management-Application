import customtkinter as ctk

class FullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Full Screen Application")
        
        # Đặt kích thước cửa sổ để phù hợp với kích thước màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Đặt cửa sổ ở kích thước toàn màn hình và che thanh taskbar
        self.root.overrideredirect(True)  # Loại bỏ các thanh tiêu đề và viền cửa sổ
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Thêm nút để thoát chế độ toàn màn hình
        self.exit_button = ctk.CTkButton(root, text="Exit Full Screen", command=self.exit_fullscreen, fg_color="red", text_color="white")
        self.exit_button.pack(pady=20)

    def exit_fullscreen(self):
        # Đặt lại cửa sổ về chế độ có thể điều khiển được
        self.root.overrideredirect(False)
        # Đóng ứng dụng
        self.root.quit()

if __name__ == "__main__":
    root = ctk.CTk()
    app = FullScreenApp(root)
    root.mainloop()
