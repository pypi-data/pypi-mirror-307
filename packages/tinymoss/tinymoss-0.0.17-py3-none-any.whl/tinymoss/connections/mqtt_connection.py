# -*- coding=utf-8 -*-

"""
@comments   MqttConnection 基于paho-mqtt封装的操作类
@auth       xuwh
@date       2024-8-28
"""

import re
from paho.mqtt.client import Client, CallbackAPIVersion, MQTTMessage
from uuid import uuid4
import logging
import time

LOGGER = logging.getLogger(__name__)

class MqttConnection():
  """MQTT协议连接对象，提供MQTT相关的一系列方法"""
  
  on_connected = None
  """当成功连接到网关后执行的回调内容
  
  ```on_connected(client, userdata, connect_flags, reason_code, properties)```
  """
  on_messaged = None
  """当收到消息时执行的回调内容，  如果设置了on_messaged_source,则本回调将不触发
  
    ```on_messaged(client, userdata, topic, payload)```
  """
  on_messaged_source = None
  """当收到消息时执行的回调内容，该回调将透传MQTTMessage对象
  
    ```on_messaged(client, userdata, message:MQTTMessage)```
  """
  on_lost_connection = None
  """当断开连接时执行的回调内容
  
  ```on_lost_connection(client, userdata, disconnect_flags, reason_code, properties)```
  """
  
  on_connect_fail = None
  """当连接失败时触发的回调

  Returns:
      ```on_connect_fail(client, userdata)```
  """
  
  on_publish = None
  
  on_subscribe = None
  
  def __init__(self, host:str, port:int=1883, username:str=None, password:str=None, auto_connect:bool=False, message_expired:int = 0):
    """基于```CallbackAPIVersion.VERSION2@paho-mqtt ```初始化的客户端实例

    Args:
        host (str): 连接网关的主机
        port (int, optional): 连接网关的端口. Defaults to 1883.
        username (str, optional): 连接网关的用户名. Defaults to None.
        password (str, optional): 连接网关的密码. Defaults to None.
        auto_connect (bool, optional): 是否自动连接. Defaults to False. True表示初始化结束后立刻进行连接
        message_expired (int, optional): 消息的过期时间，单位是秒，当消息延迟到达达到该设置后，将直接丢弃消息. Defaults to 0 = 永不过期.
    """
    self._client = Client(CallbackAPIVersion.VERSION2)
    
    self._host = host
    self._port = port
    self._username = username
    self._password = password
    self._message_expired = message_expired
    
    if self._username is not None and len(self._username) > 0:
      self._client.username_pw_set(self._username, self._password)
    if auto_connect:
      self._client.connect(self._host, self._port)
  
  
  
  
  def connect(self):
    """连接到网关
    """
    self._client.on_connect = self._on_connect
    self._client.on_disconnect = self._on_disconnect
    self._client.on_message = self._on_message
    self._client.on_connect_fail = self._on_connect_fail
    self._client.on_publish = self._on_publish
    self._client.on_subscribe = self._on_subscribe
    
    return self._client.connect(self._host, self._port)
  
  
  def disconnect(self):
    """从网关断开连接"""
    if self._client and self._client.is_connected():
      return self._client.disconnect('666')
    return 0
  
  
  def subscribe(self, 
                topic: str | tuple[str] | list[tuple[str]] | list[tuple[str, int]],
                qos: int = 0):
    """订阅指定的消息或消息列表"""
    
    if self._client and self._client.is_connected():
      return self._client.subscribe(topic, qos)
    return None
  
  def publish(self, 
              topic:str, 
              payload:str|bytes, 
              qos: int = 0,
              retain: bool = False,):
    """发布主题和内容"""
    
    if self._client and self._client.is_connected():
      return self._client.publish(topic, payload, qos, retain)
    
    return None
  
  
  def loop(self):
    """阻塞当前进程， 持续等待订阅的主题内容。"""
    
    self._client.loop_forever()
  
  
  def _on_connect(self,  client, userdata, connect_flags, reason_code, properties) :
    LOGGER.debug('_on_connect')
    if self.on_connected:
      self.on_connected(self, userdata, connect_flags, reason_code, properties)
    
  
  def _on_disconnect(self,  client, userdata, disconnect_flags, reason_code, properties) :
    LOGGER.debug('_on_disconnect')
    if self.on_lost_connection:
      self.on_lost_connection(self, userdata, disconnect_flags, reason_code, properties)
  
  def _on_message(self,  client, userdata, message:MQTTMessage) :
    
    if self._message_expired > 0 and int(time.time() - message.timestamp) > self._message_expired:
      return
    
    if self.on_messaged_source:
      self.on_messaged_source(self, userdata, message)
      return
    
    topic = message.topic
    payload = str(message.payload, 'utf8')
    if self.on_messaged:
      self.on_messaged(self, userdata, topic, payload)
  
  
  def _on_connect_fail(self,  client, userdata) :
    if self.on_connect_fail:
      self.on_connect_fail(self, userdata)
  
  def _on_publish(self,  client, userdata, mid, reason_code, properties) :
    if self.on_publish:
      self.on_publish(self, userdata, mid, reason_code, properties)
  
  def _on_subscribe(self,  client, userdata, mid, reason_code_list, properties) :
    if self.on_subscribe:
      self.on_subscribe(self, userdata, mid, reason_code_list, properties)
    
  
  