# 该程序使用tkinter库创建一个图形用户界面（GUI）来控制机械臂。
# 主要功能包括：配置机械臂在XYZ轴每步移动的毫米长度。录制和执行操作序列。显示操作进度。提供急停功能。

import tkinter as tk
from tkinter import ttk
from your_module import SerialCommunication
import time
import threading

class ControlPanel:
    def __init__(self, master):
        self.master = master
        self.master.title("Mechanical Arm Control and Operation")

        self.serial_comm = SerialCommunication(port="COM3", port_num=3)  # 示例端口和编号
        self.operation_sequence = []  # 用于存储操作序列
        self.step_size = {'X': 1.0, 'Y': 1.0, 'Z': 1.0}  # 默认步长，单位毫米

        self.create_controls()
        self.create_configuration()
        self.create_operation_controls()
    # self.master 是主窗口。
    # self.serial_comm 创建串口通信实例。
    # self.operation_sequence 用于存储操作序列。
    # self.step_size 用于配置每步移动的毫米长度，默认值为1.0。
    # self.create_controls() 创建控制按钮。
    # self.create_configuration() 创建配置输入框。
    # self.create_operation_controls() 创建操作控制界面。
    def create_controls(self):
        movements = {'X+': (1, 10), 'X-': (1, -10), 'Y+': (2, 10), 'Y-': (2, -10), 'Z+': (3, 10), 'Z-': (3, -10)}
        for idx, (label, (motor_id, steps)) in enumerate(movements.items()):
            button = tk.Button(self.master, text=label, command=lambda m_id=motor_id, s=steps: self.record_and_move(m_id, s))
            button.grid(row=0, column=idx)

        stop_button = tk.Button(self.master, text="Emergency Stop", command=self.emergency_stop, bg='red', fg='white')
        stop_button.grid(row=0, column=len(movements))
    # movements 字典定义了每个方向的移动命令。
    # for 循环创建移动按钮并将它们放置在网格布局中。
    # button 绑定了record_and_move方法，将电机ID和步数传递给该方法。
    # stop_button 创建了急停按钮，绑定了emergency_stop方法。
    def create_configuration(self):
        label_frame = tk.LabelFrame(self.master, text="Configuration", padx=10, pady=10)
        label_frame.grid(row=1, columnspan=7, sticky='w')

        for idx, axis in enumerate(['X', 'Y', 'Z']):
            label = tk.Label(label_frame, text=f"{axis} step size (mm):")
            label.grid(row=1, column=2*idx)
            entry = tk.Entry(label_frame, width=5)
            entry.insert(0, self.step_size[axis])
            entry.grid(row=1, column=2*idx+1)
            entry.bind('<Return>', lambda event, a=axis, e=entry: self.update_step_size(a, e))
    # label_frame 创建一个标签框，用于放置配置输入框。
    # for 循环创建了三个输入框，分别用于配置X、Y、Z轴的步长。
    # entry.bind('&lt;Return&gt;', ...) 绑定了&lt;Return&gt;（回车键）事件，当用户按下回车键时，调用update_step_size方法更新步长。
    def create_operation_controls(self):
        self.progress = ttk.Progressbar(self.master, length=200, mode='determinate')
        self.progress.grid(row=3, columnspan=6)

        start_button = tk.Button(self.master, text="Start", command=self.start_operations)
        start_button.grid(row=2, column=3)
    # self.progress 创建进度条，用于显示操作进度。
    # start_button 创建了开始按钮，绑定了start_operations方法。
    def update_step_size(self, axis, entry):
        try:
            self.step_size[axis] = float(entry.get())
            print(f"Updated {axis} step size to {self.step_size[axis]} mm")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    # 从输入框中读取新的步长值，并更新self.step_size。
    # 使用try...except块捕获无效输入，确保程序不会崩溃。
    def record_and_move(self, motor_id, steps):
        effective_steps = steps * self.step_size['XYZ'[motor_id-1]]  # 调整步长
        self.operation_sequence.append((motor_id, effective_steps))
        self.serial_comm.send_command((motor_id, effective_steps))
        print(f"Recorded and moved motor {motor_id} by {effective_steps} mm.")
        print("Current operation sequence:", self.operation_sequence)
    # 根据配置的步长调整移动的步数。
    # 将操作记录到self.operation_sequence中。
    # 使用send_command方法发送移动命令到机械臂。
    # 打印当前的操作序列。
    def start_operations(self):
        def run_operations():
            total_steps = len(self.operation_sequence)
            self.progress['maximum'] = total_steps
            for idx, (motor_id, steps) in enumerate(self.operation_sequence):
                try:
                    self.serial_comm.send_command((motor_id, steps))
                    self.progress['value'] = idx + 1
                    self.master.update_idletasks()
                    time.sleep(1)  # Simulate the time taken for each operation
                except Exception as e:
                    print(f"Error during operation {idx + 1}: {e}")
                    break
            print("Operation sequence completed.")
            self.progress['value'] = 0

        operation_thread = threading.Thread(target=run_operations)
        operation_thread.start()
    # run_operations函数在新线程中执行操作序列，防止GUI冻结。
    # total_steps获取操作序列的总步数，并设置进度条的最大值。
    # for循环逐步执行操作序列，更新进度条。
    # 使用try...except块捕获异常，确保程序在出错时不会崩溃。
    # operation_thread启动一个新线程，执行run_operations函数。
    def emergency_stop(self):
        self.serial_comm.send_command((0, 0))
        self.operation_sequence.clear()
        self.progress['value'] = 0
        print("Emergency stop activated and operation sequence cleared.")
    # 发送急停命令。清空操作序列。重置进度条。打印急停信息。
def main():
    root = tk.Tk()
    app = ControlPanel(root)
    root.mainloop()
    # 创建主窗口root。创建ControlPanel实例。进入tkinter主循环，等待用户交互。
if __name__ == "__main__":
    main()



