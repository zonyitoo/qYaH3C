# qYaH3C
带GUI界面的[YaH3C](https://github.com/humiaozuzu/YaH3C)实现，使用PyQt4编写

![截图](https://github.com/downloads/zonyitoo/qYaH3C/screenshot.png)

**版本: 0.4**

##测试环境：

* 中山大学东校区
* Ubuntu Linux 12.04 x64
* Python版本2.7.3


## 依赖
* python2.7
* python-netifaces
* python-qt4
* python-notify
* gksu
* dhcpcd

## 安装
* 安装DEB

首先确保已安装好依赖包

	sudo apt-get install python python-netifaces python-qt4 python-notify gksu dhcpcd

从[此处](https://github.com/zonyitoo/qYaH3C/downloads)下载最新版本的DEB包，在Ubuntu下可双击安装，或执行以下命令：

	sudo dpkg -i qyah3c_[VERSION]_all.deb

在Gnome或Unity启动菜单中打开**qYaH3C**即可使用

* 直接下载源码

首先确保已安装好依赖包及git（见上），解开压缩包后进入`application`目录执行

	sudo ./qYaH3C.py

注：在Gnome环境中将自动使用GTK主题，其它桌面环境请自行修改`application/qYaH3C.py`中`app.setStyle(QStyleFactory.create("gtk"))`或者直接删掉这句。DEB版安装后可在`/usr/share/qYaH3C/qYaH3C.py`中修改

## 已知BUG
* 无故程序崩溃

## TODO
* 断线自动重连
* 开机启动连网
