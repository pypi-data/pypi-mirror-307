# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-16 15:46
# @Author : 毛鹏
class WidgetTool:

    @classmethod
    def remove_layout(cls, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                cls.remove_layout(item.layout())
                item.layout().deleteLater()
