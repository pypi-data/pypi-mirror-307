# -*- coding=utf-8 -*-

from tinymoss import TinyMoss
import time



if __name__ == '__main__':
  
  moss = TinyMoss()
  try:
    moss.startup(restart_on_error=True)
  except KeyboardInterrupt:
    moss.shutdown()
  