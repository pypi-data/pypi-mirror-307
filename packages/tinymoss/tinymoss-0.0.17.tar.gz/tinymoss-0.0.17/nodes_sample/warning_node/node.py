#coding: utf-8

from tinymoss.nodes import MossNode


    
class WarningNode(MossNode):
  
  def on_running(self):
    print('Warning Node is running')
  
  
  def on_messaged(self, route, body):
    return super().on_messaged(route, body)
  
  
  def on_node_messaged(self, payload):
    content = str(payload, 'utf-8')
    print(f'Recv from node: {content}')