# coding: utf-8

import unittest
import time
import os
import importlib.util
from json import loads
from tinymoss.nodes import MossNode
import sys
import logging

LOGGER = logging.getLogger(__name__)


class MossNodeConfig(object):

    def __init__(self,
                 id: str, pacakge: str, name: str, nodeData: dict = {}, config: dict = {}, services: list = []):

        self.id = id
        self.package = pacakge
        self.name = name
        self.nodeData = nodeData
        self.config = config
        self.services = services

    def __repr__(self) -> str:
        return f'<MossNodeConfig ({self.id}, {self.name}, {self.package})>'


class TinyMoss():
    """TinyMoss, 轻量级分布式消息组件
    """

    def __init__(self, nodes_conf_path: str = 'moss.nodes'):
        """初始化 TinyMoss """
        self._nodes_conf_path = nodes_conf_path if nodes_conf_path.endswith(
            '.json') else f'{nodes_conf_path}.json'
        self._nodes: list[MossNode] = []
        self._nodes_conf = []

    def _load_nodes_conf(self) -> bool:
        """加载节点配置文件

        Raises:
            Exception: when the node configuration file is missing or not configured

        Returns:
            bool: 配置文件是否正确
        """
        if self._nodes_conf_path is None:
            raise Exception(
                'The node configuration file is missing or not configured!!')

        with open(self._nodes_conf_path, 'r') as conf:
            self._nodes_conf = loads(conf.read())

        return self._nodes_conf is not None and 'nodes' in self._nodes_conf

    def _load_nodes(self):
        """加载节点实例

        Raises:
            Exception: when not contain any nodes
        """
        nodes = self._nodes_conf['nodes']
        amqp = self._nodes_conf['amqp']
        if len(nodes) == 0:
            raise Exception(
                'Moss cannot be started because it does not contain any nodes')

        if amqp is None:
            raise Exception(
                'Moss cannot be started because it does not contain amqp')

        nodes = list(map(lambda x: MossNodeConfig(**x), nodes))

        for node in nodes:
            for filename in os.listdir(node.package):
                if filename.endswith('.py') and filename != '__init__.py':
                    module_name = filename[:-3]  # 去掉 .py 后缀
                    module_path = os.path.join(node.package, filename)

                    # 动态导入模块
                    spec = importlib.util.spec_from_file_location(
                        module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # 查找派生类
                    for attr in dir(module):
                        n = getattr(module, attr)
                        if isinstance(n, type) and issubclass(n, MossNode) and n is not MossNode:
                            self._nodes.append(
                                n(amqp=amqp, node_id=node.id, services=node.services, config=node.config, node_data=node.nodeData))

    def _safe_exit(self):
        try:
            sys.exit(0)
        except:
            pass
        finally:
            pass

    def all_nodes(self):
        return self._nodes_conf

    def find_node(self, id: str):
        matches = list(filter(lambda x: id == x.nodeId, self._nodes))
        return matches[0] if len(matches) > 0 else None

    def startup(self, restart_on_error: bool = False):
        """启动Moss，并以阻塞方式运行直到主动停止

        Args:
            restart_on_error (bool, optional): 发生错误时，是否自动重新启动. Defaults to False.

        Raises:
            Exception: _description_
        """

        self.startup_async()
        
        try:
            while True:
                time.sleep(.01)
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            LOGGER.error(str(ex))
            LOGGER.error(ex.with_traceback())
            if restart_on_error:
                self.reboot()


    def startup_async(self):
      """启动Moss，并以异步方式运行

      Raises:
          Exception: _description_
      """
      if not self._load_nodes_conf():
          raise Exception(
              f'Node configuration file is incorrect at {self._nodes_conf_path} !!')

      self._load_nodes()

      list(map(lambda n: n.start(), self._nodes))


    def shutdown(self):
        """关闭 Moss"""
        self._safe_exit()

    def reboot(self):
        """重启 Moss"""

        downcount = 5
        LOGGER.debug(f'\nMoss will restart after {downcount} sec')

        while downcount > 0:
            time.sleep(1)
            downcount -= 1
            LOGGER.debug(f'Moss will restart after {downcount} sec')

        python = sys.executable  # 获取当前 Python 解释器的路径
        os.execl(python, python, *sys.argv)  # 使用 os.execl 替换当前进程


if __name__ == '__main__':

    print('*' * 80)
    print('TMoss 测试程序')
    print('*' * 80)

    moss = TinyMoss()
    moss.startup()

    downcount = 3
    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        moss.shutdown()
