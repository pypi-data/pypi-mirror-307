## TinyMoss

[![Supported Versions](https://img.shields.io/badge/python-&nbsp;&nbsp;3.10&nbsp;|&nbsp;3.11&nbsp;|&nbsp;3.12&nbsp;-blue)](https://pypi.org/project/tinymoss/)
![PyPI - License](https://img.shields.io/pypi/l/tinymoss)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tinymoss)


基于RabbitMQ的轻量级分布式消息开发框架。



### 快速使用

#### 安装 RabbitMQ

#### 安装库
```bash
pip install tinymoss
```

#### 项目结构

```bash
project --- 项目目录
  |--- app.py  主入口程序
  |--- moss.nodes.json 节点配置文件
  |--- nodes   自定义节点目录
         |--- node1 noed1节点
                 |--- __init__.py  初始化文件
                 |--- node1.py   node1节点的具体实现
         |--- node2 noed2节点
                 |--- __init__.py  初始化文件
                 |--- node2.py   node2节点的具体实现
```

#### 定义节点

```python
# node1.py

class HelloNode(MossNode):
  
  _should_shutup = False

  def on_running(self):
    print('Hello Node is running')
  
    while not self._should_shutup:
      time.sleep(5)
      self.pub_to_service('<Other Node Service Id>', 'Hi!')

    
  def on_messaged(self, route, body):
    data = str (body, 'utf-8')
    print(f'[Rx] {route}, {data}')
    if route == 'urn:node:id:5cf3ed19-571d-4631-9bb0-e62de70bedea:service:shutup':
      self._should_shutup = True
```

#### 配置节点 

```json
{
  "amqp": "amqp://guest:guest@localhost:5672/%2F",
  "nodes": [
    {
      "id": "urn:node:id:5cf3ed19-571d-4631-9bb0-e62de70bedea",
      "pacakge": "nodes/node1",
      "name": "HelloNode",
      "nodeData": {},
      "services":[
        "urn:node:id:5cf3ed19-571d-4631-9bb0-e62de70bedea:service:shutup"
      ],
      "config": {}
    }
  ]
}
```


#### 调起 TinyMoss
```python
from tinymoss import TinyMoss

moss = TinyMoss()
try:
    moss.startup()
except KeyboardInterrupt:
    moss.shutdown()
```

### TinyMoss

核心组件， 负责加载节点，并提供节点间通信的支持

```python
moss = TinyMoss()
# or
moss = TinyMoss('<your node config file path>')
```

#### 方法
| 名称 | 返回 | 说明|
|----|----|----|
| TinyMoss | TinyMoss实例 | TinyMoss的构造函数，默认使用 ```moss.nodes.json``` 作为节点配置 |
| all_nodes | list[dict] | 返回已加载节点的配置列表 |
| find_node | MossNode | 查找指定ID的节点实例 |
| startup | void | 启动Moss |
| shutdown | void | 关闭Moss |
| reboot | void | 重启Moss，注意重启会在延迟5秒后执行 |


### 节点 MossNode

节点是TinyMoss中的核心组件，通常由一个派生自MossNode的类表示， 通过Moss与其他节点通信。与ROS中的概念相似，节点可以发布或订阅话题，也可以提供或使用服务。

**例如，咱们有一个机器人，和一个遥控器，那么这个机器人和遥控器开始工作后，就是两个节点。遥控器起到了下达指令的作用；机器人负责监听遥控器下达的指令，完成相应动作。从这里我们可以看出，节点是一个能执行特定工作任务的工作单元，并且能够相互通信，从而实现一个机器人系统整体的功能。在这里我们把遥控器和机器人简单定义为两个节点，实际上在机器人中根据控制器、传感器、执行机构等不同组成模块，还可以将其进一步细分为更多的节点，这个是根据用户编写的程序来定义的。）**

—— ROS2

#### 属性

| 名称 | 类型 | 说明|
|----|----|----|
| nodeId | str | 节点ID |
| services | list | 节点支持的服务ID |
| config | dict | 节点自定义配置 |
| nodeData | dict | 节点自定义数据 |

#### 方法

| 名称 | 返回 | 说明|
|----|----|----|
| pub_to_node | void | 直接与指定的节点通信 |
| pub_to_service | void | 与其他节点的服务通信 |

### 节点服务 Service

每个节点可以定义多个服务， 服务是一个全局唯一的字符串ID，通常我们使用 ``` <节点Id>:service:<服务名称> ``` 的格式来定义。 每个派生自MossNode的节点会自动订阅配置文件中给定的ID， 并通过 ```on_messaged``` 回调推送消息。

### 节点自定义配置 Config

通过节点配置项，设置每个节点独有的选项， Moss会将这些选项透传给节点。

### 节点自定义数据 NodeData

与节点配置相似，Moss会将这些数据透传给节点。


## 组件

### MqttConnection
TinyMoss提供了一个MqttConnection用于广播通信。示例如下：

```python

# coding: utf-8

from json import loads, dumps
import sys


from tinymoss.connections import MqttConnection

if __name__ =='__main__':
  
  mqttc = MqttConnection('mqtt.eclipseprojects.io', 1883)
      
  def _on_connected (client, userdata, connect_flags, reason_code, properties):
    print('_on_connected')

    # mqttc.publish('/sensors/123456/pull', dumps({}))
    mqttc.subscribe('/sensors/+/push')
    
    
  def _on_messaged(client, userdata, topic, payload): 
    print(topic, payload)
    
  mqttc.on_connected = _on_connected
  mqttc.on_messaged = _on_messaged
  mqttc.connect()
  
  
  try:
    mqttc.loop()
  except KeyboardInterrupt:
    sys.exit(0)
  

```