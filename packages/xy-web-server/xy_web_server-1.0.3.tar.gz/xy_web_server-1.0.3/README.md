<!--
 * @Author: 余洋 yuyangit.0515@qq.com
 * @Date: 2024-10-18 13:02:23
 * @LastEditors: 余洋 yuyangit.0515@qq.com
 * @LastEditTime: 2024-10-23 20:51:38
 * @FilePath: /xy_web_server/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# xy_web_server

- [简体中文](./README.md)
- [繁體中文](readme/README.zh-hant.md)
- [English](readme/README.en.md)

## 说明

xy-web-service服务模块.

## 源码仓库

- <a href="https://github.com/xy-web-service/xy_web_server.git" target="_blank">Github地址</a>  
- <a href="https://gitee.com/xy-opensource/xy_web_server.git" target="_blank">Gitee地址</a>  
- <a href="https://gitcode.com/xy-opensource/xy_web_server.git" target="_blank">GitCode地址</a>  

## 安装

```bash
# bash
pip install xy_web_server
```

## 使用

```bash
# bash
xy_web_server -c project -n xy_web_server_demo
# 创建项目 [ xy_web_server_demo ] 成功!!!
# 项目路径 ==>>> /mnt/bs-media/Workspace/project/opensource/xy-web-service/xy_web_server/test/xy_web_server_demo

cd xy_web_server_demo
xy_web_server
# >>>>>>>>>>>> xy_web_server_demo - v1.0.1 <<<<<<<<<<<<<
#
# xy_web_server_demo Hello World!!!
```

> <b>提示: </b> 运行Tornado与Django web服务请参考 [案例](./samples/xy_web_server_demo)

## Web服务开发

### 1. 创建项目
```bash
# bash
xy_web_server -c project -n xy_web_server_demo
# 创建项目 [ xy_web_server_demo ] 成功!!!
# 项目路径 ==>>> /mnt/bs-media/Workspace/project/opensource/xy-web-service/xy_web_server/test/xy_web_server_demo

cd xy_web_server_demo
xy_web_server
# >>>>>>>>>>>> xy_web_server_demo - v1.0.1 <<<<<<<<<<<<<
#
# xy_web_server_demo Hello World!!!
```
### 2. 接入Django服务和Django-ORM, Tornado

> 具体请参考 [Runner.py](./samples/xy_web_server_demo/source/Runner/Runner.py)

#### 1. 加载Django设置

> <b>注意: </b> 加载Django要在引入Tornado的RequestHandler早, 这样才能够在Tornado的RequestHandler中调用Django的模型
```python
# Runner.py
admin_path = Path.cwd().joinpath("source/Runner/Admin/").resolve().as_posix()
sys.path.insert(0, admin_path)
# 若需要使用Django-orm调用该函数
Django().load("xy_web_server_demo.settings")
```

#### 2. 接入manage.py管理

[Runner.py](./samples/xy_web_server_demo/source/Runner/Runner.py) 文件中的django_manage方法等同于
```bash
# bash
# ./samples/xy_web_server_demo/source/Runner/Admin/manage.py
python manage.py 后续参数...
```

例如: 
```bash
# bash
xy_web_server -w django shell
#相当于

cd xy_web_server_demo/source/Runner/Admin

python manage.py shell

#############################################################################
# 同步数据表, 在每次启动服务之前需要同步数据表
xy_web_server -w django makemigrations
xy_web_server -w django migrate

```

#### 3. 启动Django服务

> <b>注意: </b> 后台用户名: root  密码: 1

[Runner.py](./samples/xy_web_server_demo/source/Runner/Runner.py) 文件中的 django_start 方法等同于
```bash
# bash
# ./samples/xy_web_server_demo/source/Runner/Admin/manage.py
python manage.py runserver 127.0.0.1:8401
```
例如: 
```bash
# bash
xy_web_server -w django start
#相当于

cd xy_web_server_demo/source/Runner/Admin

python manage.py runserver 127.0.0.1:8401
```

#### 4. 启动Tornado服务

[Runner.py](./samples/xy_web_server_demo/source/Runner/Runner.py) 文件中的 tornado_start 方法
```bash
# bash
xy_web_server -w tornado start
```

## 许可证
xy_web_server 根据 <木兰宽松许可证, 第2版> 获得许可。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 捐赠
如果小伙伴们觉得这些工具还不错的话，能否请咱喝一杯咖啡呢?  

![Pay-Total](./readme/Pay-Total.png)


## 联系方式

```
微信: yuyangiit
邮箱: yuyangit.0515@qq.com
```