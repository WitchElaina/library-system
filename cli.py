import sys
import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QLineEdit
from mainwindow_ui import Ui_MainWindow
from dialog_ui import Ui_Dialog
from add_dialog_ui import Ui_Add_Dialog

import library
import account
import book


def show_msg(content, title='Message'):
    msg = QMessageBox()
    msg.setText(content)
    msg.setWindowTitle(title)
    msg.exec()


def file_judge():
    if not os.path.exists('account.json'):
        with open('account.json', 'w') as json_f:
            json_f.write('{}')
    if not os.path.exists('library.json'):
        with open('account.json', 'w') as json_f:
            json_f.write('{}')


class LoginGUI(QDialog, Ui_Dialog):
    def __init__(self):
        super(LoginGUI, self).__init__(parent=None)
        self.setupUi(self)
        self.flash()
        self.checkBox_is_reg.stateChanged.connect(self.flash)
        self.buttonBox.rejected.connect(exit)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        show_msg('Exited')
        exit(0)

    def set_pwd_echo_mode(self):
        if self.checkBox_is_reg.checkState():
            self.lineEdit_pwd.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_pwd.setEchoMode(QLineEdit.EchoMode.Password)

    def flash(self):
        self.set_pwd_echo_mode()
        self.checkBox_is_admin.setEnabled(self.checkBox_is_reg.checkState())

    def return_value(self):
        ret = []
        ret.append(self.lineEdit_usrname.text())
        ret.append(self.lineEdit_pwd.text())
        ret.append(bool(self.checkBox_is_reg.checkState()))
        ret.append(bool(self.checkBox_is_admin.checkState()))
        print(ret)
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
        self.pushButton_borrow.clicked.connect(self.borrow_book)
        self.pushButton_return.clicked.connect(self.return_book)
        self.comboBox_search_mode.currentIndexChanged.connect(self.search)
        self.pushButton_del.clicked.connect(self.del_book)

        # init app
        self.init()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        show_msg('Exited')
        exit(0)

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
            self.reload_return_list()
            self.button_enable_set()
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
        try:
            self.library.add_book(args[0], args[1], args[3], args[2])
        except Exception as err:
            show_msg(str(err))
        else:
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

        # Borrow
        if len(self.acc_dict['books']) >= 3:
            self.pushButton_borrow.setEnabled(False)
            self.comboBox_borrow.setEnabled(False)
        else:
            self.pushButton_borrow.setEnabled(True)
            self.comboBox_borrow.setEnabled(True)

        # Return
        if not self.acc_dict['books']:
            self.pushButton_return.setEnabled(False)
            self.comboBox_return.setEnabled(False)
        else:
            self.pushButton_return.setEnabled(True)
            self.comboBox_return.setEnabled(True)

        # filter
        self.set_filter_enabled()

        # delete
        if self.comboBox_all_book.count() == 0:
            self.pushButton_del.setEnabled(False)
        else:
            self.pushButton_del.setEnabled(True)

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
        self.copy_combox()

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
        self.copy_combox()

    def copy_combox(self):
        self.comboBox_borrow.clear()
        for i in range(self.comboBox_all_book.count()):
            cur_str = self.comboBox_all_book.itemText(i)
            cur_str.split()
            if self.library.borrow_require(cur_str[0]):
                self.comboBox_borrow.addItem(self.comboBox_all_book.itemText(i))

    def borrow_book(self):
        book_id = self.comboBox_borrow.currentText().split()[0]
        owner_id = self.lineEdit_usr.text()
        self.library.borrow_book(owner_id, book_id)
        self.acc_ls.borrow_book(owner_id, book_id)
        self.reload_return_list()

    def return_book(self):
        book_id = self.comboBox_return.currentText().split()[0]
        owner_id = self.lineEdit_usr.text()
        self.library.return_book(book_id)
        self.acc_ls.return_book(owner_id, book_id)
        self.reload_return_list()

    def reload_return_list(self):
        self.comboBox_return.clear()
        self.acc_dict = self.acc_ls.reload(self.lineEdit_usr.text())
        for i in self.library.books:
            if i.ID in self.acc_dict['books']:
                self.comboBox_return.addItem(i.ID + ' ' + i.name)
        self.flash_gui()

    def del_book(self):
        del_id = self.comboBox_all_book.currentText().split()[0]
        self.library.del_book(del_id)
        self.reload_return_list()

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
    file_judge()
    app = QApplication([])
    window = ClientGUI()
    window.show()
    sys.exit(app.exec_())
