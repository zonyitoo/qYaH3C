# qYaH3C
带GUI界面的[YaH3C](https://github.com/humiaozuzu/YaH3C)实现，使用PyQt4编写

**版本: 0.6.1** 更新YaH3C内核

注：此版本更新了用户信息保存地址，默认保存在`/etc/yah3c.conf`(旧版保存在用户的Home目录下的`.yah3c/users.conf`)

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

## 安装

首先确保已安装好依赖包

``` bash
## Ubuntu/Debian
sudo apt-get install python python-netifaces python-qt4 python-notify gksu dhcpcd
```

* Ubuntu下安装DEB包
从[此处](https://github.com/zonyitoo/qYaH3C/downloads)下载最新版本的DEB包，在Ubuntu下可**双击安装**，或执行以下命令：

``` bash
sudo dpkg -i qyah3c_[VERSION]_all.deb
```

在Gnome或Unity启动菜单中打开**qYaH3C**，或在终端执行`sudo qyah3c`即可使用

* Archlinux[安装包](https://github.com/zonyitoo/qYaH3C/downloads)

* 下载源码包

可以从[这里](https://github.com/zonyitoo/qYaH3C/downloads)下载`qyah3c-[VERSION]-all.tar.gz`包

* 直接从github下载最新版

首先确保已安装好依赖包及git（见上），解开压缩包后进入目录执行

``` bash
chmod +x install.sh
sudo ./install.sh
sudo qyah3c
```

卸载：进入目录执行

``` bash
chmod +x uninstall.sh
sudo ./uninstall.sh
```

注：将自动使用GTK主题(在Gnome运行正常)，其它桌面环境请自行修改或删掉`src/qyah3c.py`中

``` python
app.setStyle(QStyleFactory.create("gtk"))
```

安装后可在`/usr/share/qYaH3C/qyah3c.py`中修改

## Q & A
* Q: Unity(Ubuntu)中不能显示系统托盘图标

这是因为在Unity中默认是不显示托盘图标的，要显示出来需要先安装`dconf-tools`

``` bash
sudo apt-get install dconf-tools
```

然后打开`dconf-editor`，然后找到desktop > unity > panel，在systray-whitelist的值加入`'qyah3c'`即可

* Q: 怎么才算是已经成功登录？

如果软件的“登录”按钮变成了“下线”，那就代表已经登录成功了。同时，在详情里面会显示“Got EAP Succeed”

* Q: 为什么登录了之后还是上不了网？

登录成功之后需要手动刷新IP地址，如果你用的是图形界面，那么可以使用图形界面中的网络管理器(NetworkManager)来刷新IP地址。
如Ubuntu里面，点开右上角的连接图标，单击“有线连接(Wired Connection)”然后它就会自动重新获取IP地址，等获取成功之后就能上网了。

如果使用的是终端登录，那么可以安装`dhcpcd`工具来获取IP地址。

* Q: 为什么认证成功之后详情里一直在重复显示“Got EAP Request for identity”之类的信息？

这是因为认证协议中要求在认证成功之后，客户端要和服务器要保持联系。

## 打包DEB

下载源码后直接进入目录运行`mkpkg.sh`即可生成，依赖：dpkg

## ScreenShots
程序主界面

![主界面](https://github.com/downloads/zonyitoo/qYaH3C/screenshot.png)

## 已知BUG
* 认证登录后系统报错，但程序运行正常

## TODO
* 开机启动连网
* 界面优化

## Thanks
* [houqp](https://github.com/houqp) - Refered to houqp's [pyh3c](https://github.com/houqp/pyh3c).
* [tigersoldier](https://github.com/tigersoldier) -  Write EAP-Md5 for YaH3C.
* [humiaozuzu](https://github.com/humiaozuzu) - The Author of YaH3C
