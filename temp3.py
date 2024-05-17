import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
from pcb import PCB


def load_pcb_image():
    filepath = filedialog.askopenfilename(title="Select a PCB file", filetypes=[("PCB files", "*.pcb")])
    if not filepath:
        return  # 用户取消选择文件

    pcb = PCB(filepath)
    image = pcb.get_image()
    image_photo = ImageTk.PhotoImage(image)

    # 更新界面上的图像和文件路径
    label_image.config(image=image_photo)
    label_image.image = image_photo  # 保持引用，防止被垃圾回收
    label_file_path.config(text=f"File Path: {filepath}")


def main():
    root = tk.Tk()
    root.title("PCB Viewer")

    # 设置UI元素
    global label_image, label_file_path
    label_image = Label(root)
    label_image.pack()

    label_file_path = Label(root, text="File Path: None")
    label_file_path.pack()

    btn_load_pcb = tk.Button(root, text="Load PCB", command=load_pcb_image)
    btn_load_pcb.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

# 代码解释：
# 初始化UI：使用tkinter创建一个基本的窗口（root）。设置按钮（btn_load_pcb）来触发PCB文件的加载。设置两个标签（label_image和label_file_path），一个用于显示PCB图像，一个用于显示文件路径。
# 文件选择和加载：当用户点击“Load PCB”按钮时，通过filedialog.askopenfilename函数弹出文件选择窗口。
# 选择文件后，使用PCB类的构造函数加载文件，并调用get_image方法获取PCB图像。将获取的图像转换为tkinter兼容的格式，并在UI上显示。
# 显示文件路径：在标签label_file_path上更新文件路径。这个程序提供了一个基本框架，用于在图形用户界面中加载和显示PCB文件。确保在实际部署中对PCB类进行适当的实现，包括处理图像和文件路径。
