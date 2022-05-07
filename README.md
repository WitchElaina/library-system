[![wakatime](https://wakatime.com/badge/github/WitchElaina/library-system.svg)](https://wakatime.com/badge/github/WitchElaina/library-system) ![](https://img.shields.io/badge/Python-3.10.2-3776ab?logo=python&logoColor=white) ![](https://img.shields.io/badge/MacOS%2011.4-pass-green?logo=apple) ![](https://img.shields.io/badge/Windows11-no%20test-yellow?logo=windows)

USTB Python程序设计大作业

## 功能介绍

### 书籍管理

#### 基础信息

每个图书包含ID, 书名, 作者, 分类, 出版社等基础信息, 在录入时显示

#### 添加删除

管理员账户可以添加或删除书籍

#### 数据导入导出

可以导入其他数据, 或导出

### 书籍查询

用户可以根据ID精确查询书籍, 也可以通过关键词搜索书籍

### 借阅登记

普通用户可以借阅最多三本书籍, 每本书籍最多借阅21天



## 系统设计

### 书籍类

包含书籍的基本信息

### 图书馆类

拥有列表存放书籍

### 客户端类

包含图形界面已经对应文件io操作

