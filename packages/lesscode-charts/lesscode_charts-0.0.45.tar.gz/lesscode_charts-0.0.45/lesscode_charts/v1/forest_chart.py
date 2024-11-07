import copy
from typing import List

from lesscode_charts.utils.common_utils import find_child

"""
森林或者树图
"""


class ForestChart:
    @staticmethod
    def forest(data: List[dict], key: str = "", parent_key="", title="", **kwargs):
        """
        :param title: 图题
        :param data: 数据，示例：[{ "id":"1101","name": '节点名称1', "depth": 0, "value": 10, "unit": '单位',"parent_id":"11"}]
        :param key: id
        :param parent_key:parent_id
        :return:
        """
        data = copy.copy(data)
        result = {
            "title": title,
            "chart_type": "forest",
            "series": find_child(data=data, key=key, parent_key=parent_key)
        }
        if kwargs:
            result["pool"] = kwargs
        return result
