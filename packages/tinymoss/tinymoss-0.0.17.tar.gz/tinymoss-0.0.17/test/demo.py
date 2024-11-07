# coding: utf-8

from json import loads, dumps
import sys


from tinymoss.connections import MqttConnection

if __name__ =='__main__':
  
  mqttc = MqttConnection('mqtt.eclipseprojects.io', 1883)
      
  def _on_connected (client, userdata, connect_flags, reason_code, properties):
    print('_on_connected')
    # mqttc.publish('/fino/sensors/123456/pull', dumps({}))
    mqttc.subscribe('/fino/sensors/+/push')
    
    
  def _on_messaged(client, userdata, topic, payload): 
    print(topic, payload)
    
  mqttc.on_connected = _on_connected
  mqttc.on_messaged = _on_messaged
  mqttc.connect()
  
  
  try:
    mqttc.loop()
  except KeyboardInterrupt:
    sys.exit(0)
  