# coding : utf-8

import threading
import functools
import logging
import time
import pika
from tinymoss.connections import AMQPConnection
from tinymoss.connections import MqttConnection
from pika.exchange_type import ExchangeType
from abc import ABC, abstractmethod
import uuid

LOGGER = logging.getLogger(__name__)

class MossNode(threading.Thread, ABC):
  """TinyMoss节点， 提供节点之间的通信。 MossNode是线程安全的
  """
  
  def __init__(self, **kwargs):
    """初始化TinyMoss节点。 MossNode是线程安全的
    
      args:
        kwargs: amqp ,node_id, services, config, node_data
    """
    super(MossNode, self).__init__()
    self._reconnect_delay = 0
    self._amqp_url = self._get_config(kwargs, 'amqp', 'amqp://guest:guest@localhost:5672/%2F')
    self._amqp = AMQPConnection(self._amqp_url)
    
    #_host, _port, _username, _password = self._read_mqtt_config(kwargs)
    #self._mqtt = MqttConnection(_host, _port, _username, _password)
    self.daemon =  True
    
    self.nodeId = self._get_config(kwargs, 'node_id', str(uuid.uuid4()))
    self.services = self._get_config(kwargs, 'services', [])
    self.config = self._get_config(kwargs, 'config', {})
    self.nodeData = self._get_config(kwargs, 'node_data', {})
    
    self._sub_queue()
    self._amqp.add_on_message_callback(cb=self._on_messaged)


  def __repr__(self) -> str:
     return f'<MossNode ({self.nodeId})>'
  
  # def _read_mqtt_config(self, cnf:dict):
  #   if 'mqtt' not in cnf:
  #     return
    
  #   _ = cnf['mqtt']
  #   _host = _['host'] if 'host' in _  else 'localhost'
  #   _port = _['port'] if 'port' in _  else 1883
  #   _username = _['userName'] if 'username' in _  else None
  #   _password = _['password'] if 'password' in _  else None
    
  #   return (_host, _port, _username, _password)
  
  
  def _sub_queue(self):
    self._amqp.sub_queue(self.nodeId, auto_delete=True)
    list(map(lambda service: self._amqp.sub_queue(service, auto_delete=True), self.services))
  
  
  def _on_running(self):
    
    #self._mqtt.connect()
    
    while not self._amqp.was_consuming:
      time.sleep(.1)
    self.on_running()
  
  
  def _get_config(self, source:dict, key:str, default:any = None):
    return source[key] if key in source else default
  
  @abstractmethod
  def on_running(self):
    raise NotImplementedError()
  
  
  @abstractmethod
  def on_messaged(self, route, payload):
    pass
  
  
  def _on_messaged(self, route, payload):
    
    self.on_messaged(route, payload)
  
  
  def pub_to_node(self, node_id:str, payload:str | bytes):
    
    if self._amqp.check_queue(node_id):
      self._amqp.pub_queue(node_id, payload)
    else:
      LOGGER.debug('Trying to send a message to a queue that doesn\'t exist')
  
  
  def pub_to_service(self, service:str, payload:str|bytes):
    
    if self._amqp.check_queue(service):
      self._amqp.pub_queue(service, payload)
  
  
  def run(self):
      
      threading.Thread(target=self._on_running, daemon=True).start()
      while True:
          try:
              self._amqp.run()
          except KeyboardInterrupt:
              self._amqp.stop()
              break
          self._maybe_reconnect()

  def _maybe_reconnect(self):
      if self._amqp.should_reconnect:
          self._amqp.stop()
          reconnect_delay = self._get_reconnect_delay()
          LOGGER.info('Reconnecting after %d seconds', reconnect_delay)
          time.sleep(reconnect_delay)
          self._amqp = AMQPConnection(self._amqp_url)
          self._sub_queue()
          self._amqp.add_on_message_callback(cb=self._on_messaged)
          

  def _get_reconnect_delay(self):
      if self._amqp.was_consuming:
          self._reconnect_delay = 0
      else:
          self._reconnect_delay += 1
      if self._reconnect_delay > 30:
          self._reconnect_delay = 30
      return self._reconnect_delay

  
  