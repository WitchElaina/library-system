from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from mainwindow_ui import Ui_MainWindow
from dialog_ui import Ui_Dialog

import library
import account

class LoginGUI(QDialog, Ui_Dialog):
    def __init__(self):
        super(LoginGUI, self).__init__(parent=None)
        self.setupUi(self)

    def return_value(self):
        ret = []
        ret.append(self.lineEdit_usrname)
        ret.append(self.lineEdit_pwd)
        ret.append(self.checkBox_is_reg)
        ret.append(self.checkBox_is_admin)

class ClientGUI(QMainWindow, Ui_MainWindow):
    library = None
    acc_ls = None
    def __init__(self):
        super(ClientGUI, self).__init__(parent=None)
        self.acc_dict = None
        self.setupUi(self)
        self.library = library.Library()
        self.library.load()
        self.acc_ls = account.AccountList()
        self.acc_ls.load()

    def init(self):
        login_window = LoginGUI()
        login_window.exec()
        args = login_window.return_value()
        if args[2]:
            self.register(args[0], args[1], args[3])
        else:
            self.login(args[0], args[1])
        pass

    def register(self, usr_name, user_pwd, is_admin):
        if self.acc_ls.register(usr_name, user_pwd, is_admin):
            self.login(usr_name, user_pwd)

    def login(self, usr_name, usr_pwd):
        self.acc_dict = self.acc_ls.login(usr_name, usr_pwd)
        self.flash_gui()

    def flash_gui(self):
        # flash book library
        self.textBrowser_main.clear()
        head = 'ID\tName\tAuthor\tPublishing\tClass\tRenter'
        for i in self.library.books:
            self.textBrowser_main.append(i.show())
        # todo: Flash GUI, Add sort, search, ...
