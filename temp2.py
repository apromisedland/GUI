import time
from your_module import SerialCommunication, DisconnectException

def continuously_update_images(serial_comm):
    try:
        while serial_comm.is_connected():
            try:
                serial_comm.request_jpeg_image()
                print("Image requested successfully.")
            except DisconnectException as e:
                print(f"Failed to request image: {e}")
                break  # 如果请求图像失败，可能是设备断开连接，退出循环

            time.sleep(1)  # 每秒请求一次，可根据需要调整时间间隔
    except KeyboardInterrupt:
        print("Stopped by user.")

def main():
    # 假定已有连接的serial_comm实例
    port = "COM3"  # 示例端口，实际应由用户选择
    port_num = 3   # 端口编号，对应实际硬件连接
    serial_comm = SerialCommunication(port=port, port_num=port_num)

    if serial_comm.is_connected():
        print("Starting to update images continuously...")
        continuously_update_images(serial_comm)
    else:
        print("Device not connected.")

if __name__ == "__main__":
    main()

# 代码解释：
# 函数continuously_update_images：这个函数通过一个无限循环来持续请求图像。如果设备断开连接或发生其他异常，循环将中断。
# 异常处理：通过捕获DisconnectException来处理在图像请求过程中可能发生的断开连接情况。
# 主函数main：假设serial_comm已经根据用户选择的端口创建。主函数检查设备是否已连接，如果连接，则开始持续更新图像；如果未连接，则显示未连接的状态。
# 此代码段应整合到整体应用程序架构中，确保serial_comm实例在适当的上下文中被正确初始化和使用。
# 此外，图像请求的频率（这里是每秒一次）可以根据实际的设备响应速度和应用需求进行调整。
