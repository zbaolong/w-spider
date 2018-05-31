# w-spider

## 1. 项目介绍

一个通过八爪鱼采集数据作为数据源，整理和解析的基于Flask的爬虫应用

### 项目结构说明

```
├─requirement  // 依赖
├─spider // 爬虫相关文件
│  └─util
└─web // Flask应用相关文件
    ├─app  
    │  ├─controller // 视图函数
    │  │  ├─parse
    │  │  └─upload
    │  ├─models  // 模型
    │  │  └─history
    ├─util  // 工具类
    │  └─parse
```


## 2. 启动项目

### 1. 修改配置文件

在`config.py`文件中修改数据连接配置：

```python
DATEBASE_USERNAME = 'your user'
DATEBASE_PASSWORD = 'your password'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '3306'
DATABASE_NAME = 'wspider'
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8" .format(DATEBASE_USERNAME,
                               DATEBASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
```


### 2. 创建数据库

```
$ cd web
$ python manage.py database reload
```

如果无法执行则使用创建迁移文件的方法：

```
$ cd web
$ python manage.py database create
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```


## 3. 使用步骤

打开八爪鱼，选择自定义采集：

[![000.png](https://i.loli.net/2018/05/31/5b0fadd2ddc8d.png)](https://i.loli.net/2018/05/31/5b0fadd2ddc8d.png)

选择第二个采集方式

[![6677.png](https://i.loli.net/2018/05/31/5b0fadd2ecd81.png)](https://i.loli.net/2018/05/31/5b0fadd2ecd81.png)

启动本地采集

[![7766.png](https://i.loli.net/2018/05/31/5b0fadd2eefcf.png)](https://i.loli.net/2018/05/31/5b0fadd2eefcf.png)

输入采集的地址，如`https://landing.toutiao.com/articles_news_baby/`，点击下一步

[![9999.png](https://i.loli.net/2018/05/31/5b0fadd3051b7.png)](https://i.loli.net/2018/05/31/5b0fadd3051b7.png)

以此点击第一和第二个标题链接：

[![88877.png](https://i.loli.net/2018/05/31/5b0fadd379914.png)](https://i.loli.net/2018/05/31/5b0fadd379914.png)

并选择分页，拉至页面底部点击下一页的按钮

![44444.png](https://i.loli.net/2018/05/31/5b0faf149b21b.png)

然后开始选择字段（页面网址的字段的选择在添加特殊字段里），并严格按照页面网址、标题、作者、时间、摘要、源代码、正文、标签、分类顺序进行点击

![](tutorial.gif)

爬取之后的CSV文件示例如下；

![TIM截图20180531162419.png](https://i.loli.net/2018/05/31/5b0fb14ced2d7.png)

实例文件在[data.csv](https://gitee.com/giteePushy/w-spider/blob/dev/data/data.csv)