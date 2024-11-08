# shici
![Python Versions](https://img.shields.io/pypi/pyversions/shici)
[![LatestVersionInPypi](https://img.shields.io/pypi/v/shici.svg?style=flat)](https://pypi.python.org/pypi/shici)
![Mypy coverage](https://img.shields.io/badge/mypy-100%25-green.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

#### 介绍
生活既要有眼前的专注于极致，也要有跳出圈子，领略不同风光的诗和远方

#### 软件概要
采用python自带的random库，从favorite.txt中任意选一行作为返回值


#### 安装

```
pip install git+https://gitee.com/waketzheng/shici.git
```

#### 使用说明

1. 常规使用
```
import shici

shici.random()
```

2. 修改可选值

```
shici.show()  # 展示已有可选项
shici.join('床前明月光，梦里鬓如霜')  # 增加一个
shici.remove('床前明月光，梦里鬓如霜')  # 删除一个
```
