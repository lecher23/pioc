## 介绍
pioc工具旨在提供一个统一的对象注入服务, 通过控制反转的方式实现对系统的解藕.

## 使用方式

### 服务注册

pioc 使用装饰器的方式进行服务注册,在需要托管的服务器前使用装饰器:

```@PIOC.service("new_service_name", "requried_service")```

这样就可以声明一个服务名称为new_service_name的服务

### 服务使用

假设已经注册了一个test_service的服务, 在要使用到该服务的地方使用装饰器进行注入:

```@PIOC.require("test_service")```

### 注入方式:

pioc 使用键值对的方式对服务进行注入, 因此被注入的方法应该声明一个跟服务名称一致的默认参数, 默认值建议设置成None
