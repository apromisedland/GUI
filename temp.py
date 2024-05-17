import serial.tools.list_ports
from your_module import SerialCommunication, get_port_list

def main():
    # 获取可用的COM端口列表
    available_ports = get_port_list()
    print("Available COM Ports:")
    for i, port in enumerate(available_ports):
        print(f"{i + 1}. {port}")

    # 让用户选择一个COM口
    choice = int(input("Please select a COM port (number): ")) - 1
    if choice < 0 or choice >= len(available_ports):
        print("Invalid choice. Exiting.")
        return

    selected_port = available_ports[choice]
    port_num = choice if choice < len(available_ports) - 2 else None  # 计算真实端口的编号，排除测试端口

    # 创建串口通信实例
    serial_comm = SerialCommunication(port=selected_port, port_num=port_num)

    # 显示连接状态
    connection_status = "Connected" if serial_comm.is_connected() else "Disconnected"
    print(f"Status: {connection_status}")

if __name__ == "__main__":
    main()

# 代码解释：
# 获取端口列表：使用get_port_list函数列出所有可用的串口和测试端口。
# 用户选择COM口：用户通过输入选择一个端口，程序通过输入的数字定位到相应的端口。
# 实例化通信类：使用用户选择的端口初始化SerialCommunication类。如果选择的是测试端口，端口编号（port_num）将被设定为None。
# 显示连接状态：通过调用is_connected方法获取并显示当前的连接状态。这段代码实现了上位机程序设计步骤中的第一步，即选择COM口并显示设备的连接状态。
