#-*- coding: UTF-8 -*-
__author__ = '余洋'
'''
  * @File    :   PairDelegate.py
  * @Time    :   2023/04/23 14:09:10
  * @Author  :   余洋 
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
'''

from abc import ABCMeta, abstractmethod

class PairDelegate(ABCMeta):
    
    @abstractmethod
    def should_set_value(self, name: str | None, value=None, exist_ok: bool = True, ok: bool = False) -> bool:
        return ok
    
    @abstractmethod
    def should_delete(self, name, ok: bool = False) -> bool:
        return ok
    
    @abstractmethod
    def should_update(self, value, ok: bool = False) -> bool:
        return ok