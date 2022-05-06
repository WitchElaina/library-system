import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from mainwindow_ui import Ui_MainWindow
from dialog_ui import Ui_Dialog
from add_dialog_ui import Ui_Add_Dialog

import library
import account
import book


class LoginGUI(QDialog, Ui_Dialog):
    def __init__(self):
        super(LoginGUI, self).__init__(parent=None)
        self.setupUi(self)

    def return_value(self):
        ret = []
        ret.append(self.lineEdit_usrname.text())
        ret.append(self.lineEdit_pwd.text())
        ret.append(self.checkBox_is_reg.checkState())
        ret.append(self.checkBox_is_admin.checkState())
        return ret


class AddGUI(QDialog, Ui_Add_Dialog):
    def __init__(self):
        super(AddGUI, self).__init__(parent=None)
        self.setupUi(self)

    def return_value(self):
        ret = []
        ret.append(self.lineEdit_name.text())
        ret.append(self.lineEdit_author.text())
        ret.append(self.lineEdit_pub.text())
        ret.append(self.comboBox_class.currentIndex())
        return ret


def show_msg(content, title='Message'):
    msg = QMessageBox()
    msg.setText(content)
    msg.setWindowTitle(title)
    msg.exec()


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
        self.show_id = []
        for i in book.classify_dict:
            self.comboBox_filter_mode.addItem(book.classify_dict[i])
        # self.all_id = []
        # for i in self.library.books:
        #     self.all_id.append(i.id)

        # bind event listener
        self.checkBox_enable_filter.stateChanged.connect(self.set_filter_enabled)
        self.lineEdit_serach_input.textEdited.connect(self.search)
        self.pushButton_add.clicked.connect(self.add_book)
        self.comboBox_filter_mode.currentIndexChanged.connect(self.filter)

        # init app
        self.init()

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
        stats = self.acc_ls.register(usr_name, user_pwd, is_admin)
        if stats:
            self.login(usr_name, user_pwd)
        else:
            show_msg('Register Error')
            return self.init()

    def login(self, usr_name, usr_pwd):
        self.acc_dict = self.acc_ls.login(usr_name, usr_pwd)
        if not self.acc_dict:
            show_msg('Login Error')
            return self.init()
        else:
            self.flash_gui()
            show_msg('Success')

    def search(self):
        if self.comboBox_search_mode.currentIndex() == 0:
            self.show_id = self.library.id_search(self.lineEdit_serach_input.text())
        else:
            search_mode = self.comboBox_search_mode.currentIndex()
            self.show_id = self.library.keyword_search(self.lineEdit_serach_input.text(), search_mode)
        self.show_books()

    def filter(self):
        if self.checkBox_enable_filter.checkState():
            self.show_id = self.library.filter(self.comboBox_filter_mode.currentIndex())
            self.show_books()
        else:
            self.show_all()

    def add_book(self):
        add_window = AddGUI()
        add_window.setWindowTitle('Add Book')
        add_window.exec()
        args = add_window.return_value()
        self.library.add_book(args[0], args[1], args[3], args[2])
        self.flash_gui()
        show_msg('Success')

    def set_filter_enabled(self):
        self.comboBox_filter_mode.setEnabled(self.checkBox_enable_filter.checkState())
        self.filter()

    def button_enable_set(self):
        # Admin
        self.pushButton_add.setEnabled(self.acc_dict['is_admin'])
        self.pushButton_del.setEnabled(self.acc_dict['is_admin'])
        self.comboBox_all_book.setEnabled(self.acc_dict['is_admin'])
        self.pushButton_load.setEnabled(self.acc_dict['is_admin'])
        self.pushButton_save.setEnabled(self.acc_dict['is_admin'])

        # Borrow
        if len(self.acc_dict['books']) == 3:
            self.pushButton_borrow.setEnabled(False)
            self.comboBox_borrow.setEnabled(False)

        # Return
        if not self.acc_dict['books']:
            self.pushButton_return.setEnabled(False)
            self.comboBox_return.setEnabled(False)

        # filter
        self.set_filter_enabled()

    def show_all(self):
        self.textBrowser_main.clear()
        self.textBrowser_main_my.clear()
        self.comboBox_all_book.clear()
        head = 'ID\tName\tAuthor\tPublishing\tClass\tRenter'
        self.textBrowser_main.append(head)
        self.textBrowser_main_my.append(head)
        for i in self.library.books:
            self.textBrowser_main.append(i.show())
            self.textBrowser_main_my.append(i.show())
            self.comboBox_all_book.addItem(i.ID + ' ' + i.name)


    def show_books(self):
        self.textBrowser_main.clear()
        self.textBrowser_main_my.clear()
        self.comboBox_all_book.clear()
        head = 'ID\tName\tAuthor\tPublishing\tClass\tRenter'
        self.textBrowser_main.append(head)
        self.textBrowser_main_my.append(head)
        if self.lineEdit_serach_input.text() != '' or self.checkBox_enable_filter.checkState():
            for i in self.library.books:
                if i.ID in self.show_id:
                    self.textBrowser_main.append(i.show())
                    self.textBrowser_main_my.append(i.show())
                    self.comboBox_all_book.addItem(i.ID + ' ' + i.name)
        else:
            for i in self.library.books:
                self.textBrowser_main.append(i.show())
                self.textBrowser_main_my.append(i.show())
                self.comboBox_all_book.addItem(i.ID + ' ' + i.name)

    def flash_gui(self):
        # set buttons
        self.button_enable_set()

        # set personal info
        self.lineEdit_usr.setText(self.acc_dict['username'])
        self.lineEdit_status.setText(str(self.acc_dict['is_admin']))
        self.lineEdit_brd.setText(str(len(self.acc_dict['books'])))
        self.lineEdit_brd_max.setText('3')

        # flash book library
        self.show_books()
        # todo: Flash GUI, Add filter, search, ...


if __name__ == '__main__':
    app = QApplication([])
    window = ClientGUI()
    window.show()
    sys.exit(app.exec_())
