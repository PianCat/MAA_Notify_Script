# MAA Notify Script

[![Pyhthon Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/release/python-370/)
[![GPLv3 License](https://img.shields.io/github/license/hcy2206/FIRMS_Data_Visualization)](https://opensource.org/licenses/GPL-3.0)

本项目是 [MaaAssistantArknights](https://maa.plus) 的一款辅助脚本，用于解决用户在电脑上通过定时运行 MAA 的方式进行自动化刷图时，无法及时得知本次运行的结果的问题。

基于 [Server酱](https://sct.ftqq.com/) 提供的 API，实现了一个简单的通知脚本，通过对于 MAA 运行日志的分析，实现了当 MAA 一次运行结束之后，通过 Pushdeer 的方式 向用户推送此次运行的结果，包括是否出错、一些错误日志以及本次运行所掉落的物品。

下图是一些该项目原项目的通知的样例：

![Pic1](pics/Screenshot_20230921-112739.png)

![Pic2](pics/Screenshot_20230921-112756.png)

## 使用方法

1. [下载本项目](https://github.com/PianCat/MAA_Notify_Script/releases/download/v3.1.0-ServerChan/MAA_Notify_Script.zip) 解压后将得到的`MAA_Notify_Script`文件夹放置在 MAA 主文件夹`MAA-Arknights`下
2. 安装 python，并确保它可以在命令行中运行，即打开命令行，输入`python -v`，如果出现 python 的版本信息，则说明安装成功。 如果你明确知道你没有安装 python，又不知道应该如何安装，推荐从 Microsoft Store 中安装 [Python3.11](https://www.microsoft.com/store/productId/9NRWMJP3717K)，点击安装即可，无需额外配置即可运行
5. 将脚本 `MAA-Notification.bat` 的相对路径添加到 MAA 的`设置-连接设置-结束后脚本`中，即在该输入框中填入`MAA_Notify_Script\MAA-Notification.bat`
9. 在`main.py`中的`SERVERCHAN_KEY`填入你的key，简单来说需要从 Server酱 处获得 key，然后将其填入`SERVERCHAN_KEY`中。
10. Server酱 官方服务器 key 的获取：
    1. 使用`微信`扫码登录 [Server酱](https://sct.ftqq.com/sendkey) 。
    2. 在 `Key&API` 页面复制 `SendKey` ，将其填入`PUSHDEER_KEY`中。
    3. 注册成功后，点击下边栏的`Key`选项，即可看到你的 key，将其填入`SERVERCHAN_KEY`中。
    3. 推送渠道请参照 [通道配置](https://sct.ftqq.com/forward) 页面，同时兼容 [PushDeer](https://www.pushdeer.com/) 方式
10. Enjoy!
