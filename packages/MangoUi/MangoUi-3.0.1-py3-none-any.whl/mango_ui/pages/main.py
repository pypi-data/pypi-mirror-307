# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-31 9:51
# @Author : 毛鹏
from PySide6.QtWidgets import QApplication

from mango_ui import MangoMainWindow
from mango_ui.pages import *
from mango_ui.settings.settings import STYLE, MENUS


def main():
    page_dict = {
        'home': HomePage,
        'component': ComponentPage,
        'feedback': FeedbackPage,
        'container': ContainerPage,
        'charts': ChartsPage,
        'display': DisplayPage,
        'graphics': GraphicsPage,
        'input': InputPage,
        'layout': LayoutPage,
        'menu': MenuPage,
        'miscellaneous': MiscellaneousPage,
        'window': WindowPage,
    }

    app = QApplication([])
    login_window = MangoMainWindow(STYLE, MENUS, page_dict)
    login_window.show()
    app.exec()


main()
