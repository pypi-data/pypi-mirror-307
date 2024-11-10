<!--
 * @Author: 余洋 yuyangit.0515@qq.com
 * @Date: 2024-10-18 13:02:23
 * @LastEditors: 余洋 yuyangit.0515@qq.com
 * @LastEditTime: 2024-10-23 20:51:38
 * @FilePath: /xy_web_work/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# xy_web_work

- [简体中文](./README.md)
- [繁體中文](readme/README.zh-hant.md)
- [English](readme/README.en.md)

## 说明

xy-web-service服务设置模块.

## 源码仓库

- <a href="https://github.com/xy-web-service/xy_web_work.git" target="_blank">Github地址</a>  
- <a href="https://gitee.com/xy-opensource/xy_web_work.git" target="_blank">Gitee地址</a>  
- <a href="https://gitcode.com/xy-opensource/xy_web_work.git" target="_blank">GitCode地址</a>  

## 安装

```bash
# bash
pip install xy_web_work
```

## 使用

###### 1. 通用

```bash
# 创建项目
xy_web_server -c project -n xy_web_demo
cd xy_web_demo
xy_web_server
# >>>>>>>>>>>> xy_web_demo - v0.0.1 <<<<<<<<<<<<<
# 
# xy_web_work Hello World!!!

```
###### 2. 扩展或者定制
```python
# main.py
from xy_web_work.WebWork import WebWork as xyWebWork
from xy_web_work.Settings.Settings import Settings


class WebServerWork(xyWebWork):
    settings: Settings | None = Settings()

    def __init__(self):
        self.prog = "xy_test_demo"
        self.description = f""">>>>>>>>>>>> xy_test_demo - v1.0.0 <<<<<<<<<<<<<"""


if __name__ == "__main__":
    web_server_work = WebServerWork()
    web_server_work.main()
```

```bash
# bash
python main.py -c project -n xy_web_work_demo
# 创建项目 [ xy_web_work_demo ] 成功!!!
# 项目路径 ==>>> /mnt/bs-media/Workspace/project/opensource/xy-web-service/xy_web_work/test/xy_web_work_demo

cp main.py xy_web_work_demo
cd xy_web_work_demo
python main.py -c runner
# >>>>>>>>>>>> xy_web_work_demo - v1.0.1 <<<<<<<<<<<<<
# xy_web_work Hello World!!!

```

## 许可证
xy_web_work 根据 <木兰宽松许可证, 第2版> 获得许可。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 捐赠
如果小伙伴们觉得这些工具还不错的话，能否请咱喝一杯咖啡呢?  

![Pay-Total](./readme/Pay-Total.png)


## 联系方式

```
微信: yuyangiit
邮箱: yuyangit.0515@qq.com
```