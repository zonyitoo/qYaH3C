# qYaH3C
带GUI界面的[YaH3C](https://github.com/humiaozuzu/YaH3C)实现，使用PyQt4编写

![截图](https://github.com/downloads/zonyitoo/qYaH3C/screenshot.png)

**版本: 0.5.3**
待机自动重连BUG解决

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

* Archlinux[安装包](https://github.com/zonyitoo/qYaH3C/downloads)

* 直接下载源码

可以从[这里](https://github.com/zonyitoo/qYaH3C/downloads)下载`qyah3c-[VERSION]-all.tar.gz`包

GIT：首先确保已安装好依赖包及git（见上），解开压缩包后进入目录执行

	chmod +x install.sh
	sudo ./install.sh
	sudo qyah3c

卸载：进入目录执行

	chmod +x uninstall.sh
	sudo ./uninstall.sh

注：将自动使用GTK主题，其它桌面环境请自行修改`src/qyah3c.py`中

	app.setStyle(QStyleFactory.create("gtk"))

或者直接删掉这句。

DEB版安装后可在`/usr/share/qYaH3C/qyah3c.py`中修改

* Unity中不能显示系统托盘图标

这是因为在Unity中默认是不显示托盘图标的，要显示出来需要先安装`dconf-tools`
	
	sudo apt-get install dconf-tools
	
然后打开`dconf-editor`，然后找到desktop > unity > panel，在systray-whitelist的值加入`'qyah3c'`即可

* 打包

下载源码后直接进入目录运行`mkpkg.sh`即可生成，依赖：dpkg

## 已知BUG
* 无故程序崩溃

## TODO
* 断线自动重连
* 开机启动连网
