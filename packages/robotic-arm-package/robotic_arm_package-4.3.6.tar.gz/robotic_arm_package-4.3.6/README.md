# robotic_arm_package

睿尔曼机械臂Python版本二次开发包  

## 一、引言

本开发包旨在为睿尔曼机械臂的二次开发提供便捷的Python接口。通过本开发包，用户能够实现对机械臂的控制、路径规划、状态监控等一系列功能，从而加速机械臂相关应用的开发过程。

## 二、支持的操作系统与软件版本

### 操作系统

- **Windows（64位和32位）**：支持Windows操作系统下的64位和32位版本，方便Windows用户进行机械臂开发。
- **Linux（x86和arm）**：支持Linux操作系统的x86架构和arm架构，满足不同硬件环境的需求。

### 软件版本

- **Python 3.9以上**：本开发包基于Python 3.9及以上版本进行开发，确保与最新Python版本的兼容性。

## 三、安装与使用

### 安装

用户可以通过pip命令进行安装：
```bash  
pip install robotic_arm_package
```

### 使用

安装完成后，用户可以在Python脚本中导入开发包并使用相关API接口进行机械臂的开发工作。以下是一个简单的使用机械臂Python开发包连接机械臂并查询机械臂版本的示例代码：

```python
import time
from robotic_arm_package.robotic_arm import *

robot = Arm(RM75, "192.168.1.18")

software_info = robot.Get_Arm_Software_Info()
if software_info[0] == 0:
    print("\n================== Arm Software Information ==================")
    print("Arm Model: ", software_info[1].product_version)
    print("Algorithm Library Version: ", software_info[1].algorithm_info.version)
    print("Control Layer Software Version: ", software_info[1].ctrl_info.version)
    print("Dynamics Version: ", software_info[1].dynamic_info.model_version)
    print("Planning Layer Software Version: ", software_info[1].plan_info.version)
    print("==============================================================\n")
else:
    print("\nFailed to get arm software information, Error code: ", software_info[0], "\n")
```