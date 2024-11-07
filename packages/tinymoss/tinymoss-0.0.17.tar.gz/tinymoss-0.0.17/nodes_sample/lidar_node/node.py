#coding: utf-8

from tinymoss.nodes import MossNode
import time


class LidarNode(MossNode):
  
  def on_running(self):
    print('Lidar Node is running')
    while not self._amqp.was_consuming:
      time.sleep(.1)
    
    while self._amqp.was_consuming:
      time.sleep(5)
      self.pub_to_node('urn:device:id:6a56ddde-0c63-4a7f-88f3-56243eed611d', 'WARNING!')

    
  def on_messaged(self, route, body):
    data = str (body, 'utf-8')
    print(f'{route}, {data}')
    
    
  def on_node_messaged(self, body):
    data = str (body, 'utf-8')
    print(f'收到来自其他节点的信息, {data}')