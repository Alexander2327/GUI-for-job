import time
from datetime import date
from pywinauto.application import Application
import psutil
import sys
from modal_win.mainwindow import *
from modal_win.firststage import *
from modal_win.secondstage import *
from modal_win.thirdstage import *
from modal_win.fourthstage import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWinExtras import QtWin
from AmplifierConfig import *

myappid = 'mycompany.myproduct.subproduct.version'
QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
style = "QPushButton {color: #b1b1b1; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, " \
        "stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646); " \
        "border-width: 1px; border-color: #1e1e1e; border-style: solid; border-radius: 6; padding: 3px; " \
        "font-size: 16px; padding-left: 10px; padding-right: 10px; min-width: 80px;}" \
        "QPushButton:pressed{background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d20," \
        " stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);}" \
        "QPushButton:hover{background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, " \
        "stop: 0 #2d2d20, stop: 0.1 #2b2b2b, stop: 0.3 #292929, stop: 0.6 #282828, stop: 1 #252525);}" \
        "QWidget{color: #b1b1b1; background-color: #323232}"
style1 = 'border: 2px solid red'
style2 = 'border: 2px solid #b1b1b1,QLineEdit:focus{border: 2px solid #ffaa00;}'


def check_process(process_name):
    pid = None
    for proc in psutil.process_iter():
        if process_name in proc.name():
            pid = proc.pid
    return pid


def zoc_min():
    zoc = Application(backend="win32").connect(process=check_process('zoc'), timeout=5)
    MainWindow = zoc.ZocMainWindow
    MainWindow.minimize()


def auto_log():
    zoc = Application(backend="win32").connect(process=check_process('zoc'), timeout=5)
    MainWindow = zoc.ZocMainWindow
    MainWindow.menu_item(u'Logging->Log to File').click()
    MainWindow.menu_item(u'Logging->Log to File').click()


def auto_upload(file, log='no'):
    """Функция автопосылки
            нужного файла через zoc"""
    zoc = Application(backend="win32").connect(process=check_process('zoc'), timeout=5)
    MainWindow = zoc.ZocMainWindow
    MainWindow.menu_item(u'Transfer->Send Binary File...').click()
    Upload_Window = zoc.SelectBinaryFileforUpload
    Upload_Window.type_keys(file, with_spaces=True)
    time.sleep(0.1)
    Upload_Window[u'Открыть'].click()
    time.sleep(2)
    if log == 'yes':
        MainWindow.menu_item(u'Logging->Log to File').click()
        MainWindow.menu_item(u'Logging->Log to File').click()
        MainWindow.minimize()


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.flag = True
        self.ui.radioButton.clicked.connect(self.get_text)
        self.ui.radioButton_2.clicked.connect(self.get_text)
        self.ui.radioButton_3.clicked.connect(self.get_text)
        self.ui.radioButton_4.clicked.connect(self.get_text)
        self.ui.radioButton_5.clicked.connect(self.get_text)
        self.ui.radioButton_6.clicked.connect(self.get_text)
        self.ui.pushButton_2.clicked.connect(self.exit_gui)
        self.ui.pushButton.clicked.connect(self.stage)
        self.ui.plainTextEdit_2.setPlaceholderText('Комментарий:\n\nНе выбраны модификация и параметры настройки ОУ.')
        self.ui.pushButton.setToolTip('Continue Setting')
        self.ui.label_5.setToolTip('Online Time')
        self.ui.label_4.setToolTip('Date')
        self.ui.label_6.setToolTip('Window Status')
        self.ui.pushButton_2.setToolTip('Program Exit')
        self.ui.label_4.setFont(QFont('Arial', 10, 57))
        self.ui.label_6.setFont(QFont('Arial', 8, 71))
        self.ui.label_5.setFont(QFont('Arial', 10, 57))
        self.ui.label_4.setText(QDate.currentDate().toString('dd/MM/yyyy'))
        self.ui.label_6.setText('Ready to work')
        self.ui.label_5.setStyleSheet("QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.ui.label_4.setStyleSheet("QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.ui.label_6.setStyleSheet(
            'QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}' + "QWidget{color: #b1b1b1; "
                                                                                      "background-color: #242424; "
                                                                                      "border:#242424}")
        self.ui.pushButton.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.ui.pushButton_2.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.curr_time = QtCore.QTime(00, 00, 00)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.app_timer)
        self.timer.start(1000)
        self.ui.label_5.setText(self.curr_time.toString())
        self.setWindowIcon(QIcon('pictures/iconmax.png'))
        self.ui.checkBox.setChecked(True)
        self.ui.checkBox.clicked.connect(self.log)
        self.ui.lineEdit_4.setReadOnly(True)
        self.ui.lineEdit_4.setEnabled(False)

    def log(self):
        if self.ui.checkBox.isChecked():
            self.ui.lineEdit_4.setReadOnly(True)
            self.ui.lineEdit_4.setEnabled(False)
        else:
            self.ui.lineEdit_4.setReadOnly(False)
            self.ui.lineEdit_4.setEnabled(True)

    def zoc_error(self):
        self.set_status(2)
        warning = QtWidgets.QMessageBox()
        warning.setIcon(QtWidgets.QMessageBox.Critical)
        warning.setFont(QFont('Arial', 10, 81))
        warning.setWindowTitle('Program Error')
        warning.setText('Ошибка. Программа "ZOC Terminal" не запущена.')
        warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
        warning.setStyleSheet(style)
        warning.exec_()
        self.set_status(1)

    def app_timer(self):
        self.curr_time = self.curr_time.addSecs(1)
        self.ui.label_5.setText(self.curr_time.toString())

    def stage(self):
        if self.checked_radiobutton():
            if (
                    self.ui.radioButton_5.isChecked() or self.ui.radioButton_6.isChecked()) and self.ui.radioButton_2.isChecked():
                self.stage_one()
            elif (
                    self.ui.radioButton_5.isChecked() or self.ui.radioButton_6.isChecked()) and self.ui.radioButton_4.isChecked():
                self.stage_two()
            elif (
                    self.ui.radioButton_5.isChecked() or self.ui.radioButton_6.isChecked()) and self.ui.radioButton_3.isChecked():
                self.stage_three()
            elif (
                    self.ui.radioButton_5.isChecked() or self.ui.radioButton_6.isChecked()) and self.ui.radioButton.isChecked():
                self.stage_four()
        elif self.checked_radiobutton() is False:
            self.ui.label_6.setText('Not active')
            warning = QtWidgets.QMessageBox()
            warning.setIcon(QtWidgets.QMessageBox.Warning)
            warning.setFont(QFont('Arial', 10, 81))
            warning.setWindowTitle('Program Warning')
            warning.setText('Не выбраны параметры настройки.')
            warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warning.setStyleSheet(style)
            warning.exec_()
            self.set_status(1)

    def set_status(self, status):
        if status == 1:
            self.ui.label_6.setText('Ready to work')
        elif status == 2:
            self.ui.label_6.setText('Not active')

    def stage_one(self):
        self.set_status(2)
        wind = FirstWindow(self)
        self.showMinimized()
        time.sleep(0.3)
        wind.show()
        wind.activateWindow()

    def stage_two(self):
        self.set_status(2)
        wind_2 = SecondWindow(self)
        self.showMinimized()
        time.sleep(0.3)
        wind_2.show()
        wind_2.activateWindow()

    def stage_three(self):
        self.set_status(2)
        wind_3 = ThirdWindow(self)
        self.showMinimized()
        time.sleep(0.3)
        wind_3.show()
        wind_3.activateWindow()

    def stage_four(self):
        self.set_status(2)
        wind_4 = FourthWindow(self)
        self.showMinimized()
        time.sleep(0.3)
        wind_4.show()
        wind_4.activateWindow()

    def exit_gui(self):
        self.set_status(2)
        question = QtWidgets.QMessageBox()
        question.setIcon(QtWidgets.QMessageBox.Question)
        question.setFont(QFont('Arial', 10, 81))
        question.setWindowTitle('Close Program')
        question.setText('Уверены, что хотите заакрыть программу?')
        question.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        question.setStyleSheet(style)
        res = question.exec_()
        if res == QtWidgets.QMessageBox.Yes:
            sys.exit()
        self.set_status(1)

    def closeEvent(self, value):
        self.set_status(2)
        question = QtWidgets.QMessageBox()
        question.setIcon(QtWidgets.QMessageBox.Question)
        question.setFont(QFont('Arial', 10, 81))
        question.setWindowTitle('Close Program')
        question.setText('Уверены, что хотите заакрыть программу?')
        question.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        question.setStyleSheet(style)
        res = question.exec_()
        if res == QtWidgets.QMessageBox.Yes:
            sys.exit()
        elif res == QtWidgets.QMessageBox.No:
            self.set_status(1)
            value.ignore()

    def checked_radiobutton(self):
        if (
                self.ui.radioButton.isChecked() or self.ui.radioButton_2.isChecked() or
                self.ui.radioButton_4.isChecked() or self.ui.radioButton_3.isChecked()) and (
                self.ui.radioButton_5.isChecked() or self.ui.radioButton_6.isChecked()):

            return True
        else:
            return False

    def get_text(self):
        comment1 = 'Подключите ПКУ к ПК через RS-232. Подключите питание к ПКУ (напряжение питания - 3,3 В). Для ' \
                   'продолжения настройки нажмите "Continue" '
        comment2 = 'Проверьте читсоту коннеторов. Подключите вход ОУ к выходу аттенюатора IQS-3150, выход ОУ - ко ' \
                   'входу измерителя мощности IQS-1700 (предварительно произведите калибровку входного сигнала). ' \
                   'Установоите входную мощность -6 дБм. Для проверки мощности нажмите лазера накачки, подключите ' \
                   'выходной коннектор лазера к измерителю ВЫСОКОЙ мощности IQS-1700. Для продолжения настройки ' \
                   'нажмите "Continue" '
        comment3 = 'Проверьте читсоту коннеторов. Подключите вход ОУ к выходу аттенюатора IQS-3150, выход ОУ - ко ' \
                   'входу измерителя мощности IQS-1700 (предварительно произведите калибровку входного сигнала). ' \
                   'Соедените плату лазера и ПКУ. Подключите питание к ПКУ (напряжение питания - 3,3 В). Установоите ' \
                   'входную мощность -6 дБм. Для продолжения настройки нажмите "Continue"'
        comment4 = 'Подключите питание к ОУ (напряжение питания - 3,3 В). Для продолжения настройки нажмите "Continue"'
        if self.checked_radiobutton() and self.ui.radioButton_5.isChecked():
            if self.ui.radioButton.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.insertPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_5.text()}\n\n{comment4}')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)
            elif self.ui.radioButton_2.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_5.text()}\n\n{comment1}')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)
            elif self.ui.radioButton_4.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_5.text()}\n\n{comment2}')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)
            elif self.ui.radioButton_3.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f"Комментарий:\n\nМодификация - {self.ui.radioButton_5.text()}\n\n{comment3[:-51]}10 дБм" \
                    + '. Для продолжения настройки нажмите "Continue"')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)

        elif self.checked_radiobutton() and self.ui.radioButton_6.isChecked():
            if self.ui.radioButton.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_6.text()}\n\n{comment4}')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)
            elif self.ui.radioButton_2.isChecked() and self.ui.radioButton_6.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_6.text()}\n\n{comment1}')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)
            elif self.ui.radioButton_4.isChecked() and self.ui.radioButton_6.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_6.text()}\n\n{comment2}')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)
            elif self.ui.radioButton_3.isChecked() and self.ui.radioButton_6.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_6.text()}\n\n{comment3}')
                self.ui.plainTextEdit_2.moveCursor(QtGui.QTextCursor.Start)
        elif self.checked_radiobutton() is False and (
                self.ui.radioButton_6.isChecked() or self.ui.radioButton_5.isChecked()):
            if self.ui.radioButton_6.isChecked():
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_6.text()}\n\nВыберите режим нстройки ОУ')
            else:
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(
                    f'Комментарий:\n\nМодификация - {self.ui.radioButton_5.text()}\n\nВыберите режим нстройки ОУ.')
        elif self.ui.radioButton_6.isChecked() is False and self.ui.radioButton_5.isChecked() is False:
            self.ui.plainTextEdit_2.clear()
            self.ui.plainTextEdit_2.appendPlainText(f'Комментарий:\n\nВыберите модификацию настраимого изделия.')


class FirstWindow(QtWidgets.QWidget):
    def __init__(self, parent=MyWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.modal = Ui_Form()
        self.flag = 0
        self.modal.setupUi(self)
        self.setWindowModality(2)
        if myapp.ui.radioButton_6.isChecked():
            self.modal.plainTextEdit_3.setPlainText('K25-M19')
        else:
            self.modal.plainTextEdit_3.setPlainText('K25-M12')
        self.modal.plainTextEdit_2.setPlaceholderText(
            'Комментарий:\n\nНажмите "Get Udrv" для активации процесса настройки.')
        self.modal.pushButton_2.setToolTip('Back to Master')
        self.modal.pushButton_8.setToolTip('Clear All')
        self.modal.pushButton_6.setToolTip('Voltage Correction')
        self.modal.pushButton.setToolTip('Start Configuration')
        self.modal.pushButton_5.setToolTip('Get Voltage')
        self.modal.pushButton_7.setToolTip('Upload DRV Setup')
        self.modal.label_6.setToolTip('Date')
        self.modal.label_7.setToolTip('Window Status')
        self.modal.pushButton_5.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_8.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_6.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_7.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_2.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_6.setStyleSheet("QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_10.setStyleSheet("QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_7.setStyleSheet(
            'QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}' + "QWidget{color: #b1b1b1; "
                                                                                      "background-color: #242424; "
                                                                                      "border:#242424}")
        self.modal.pushButton_2.clicked.connect(self.back_to_master)
        self.modal.plainTextEdit_3.setFont(QFont('Arial', 24, 81))
        self.modal.label_6.setFont(QFont('Arial', 10, 57))
        self.modal.label_7.setFont(QFont('Arial', 8, 71))
        self.modal.label_6.setText(QDate.currentDate().toString('dd/MM/yyyy'))
        self.modal.label_7.setText('Ready to work')
        self.modal.pushButton_6.setVisible(False)
        self.modal.pushButton_7.clicked.connect(self.upload)
        self.modal.pushButton_8.clicked.connect(self.clear)
        self.modal.pushButton.clicked.connect(self.config_1st)
        self.modal.pushButton_6.clicked.connect(self.correction)
        self.modal.pushButton_5.clicked.connect(self.get_u)
        self.modal.lineEdit_4.setFocus()
        self.modal.lineEdit_3.setReadOnly(True)
        self.modal.lineEdit_5.setReadOnly(True)
        self.modal.lineEdit_2.setReadOnly(True)
        self.modal.lineEdit.setReadOnly(True)
        self.config = None
        self.modal.label_10.setToolTip('Config File Status')
        self.modal.label_10.setFont(QFont('Arial', 8, 57))
        self.modal.label_10.setVisible(False)

    def file_status(self, txt, file):
        self.modal.label_10.setVisible(True)
        self.modal.label_10.setText(f'{file} {txt}')

    def clear(self):
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_3.clear()
        self.modal.lineEdit_5.clear()
        self.modal.lineEdit_2.clear()
        self.modal.lineEdit.clear()
        self.modal.lineEdit_4.clear()

    def get_u(self):
        self.modal.label_10.setVisible(False)
        if check_process('zoc') is not None:
            self.set_status(2)
            war = QtWidgets.QMessageBox()
            war.setIcon(QtWidgets.QMessageBox.Question)
            war.setFont(QFont('Arial', 10, 81))
            war.setWindowTitle('Start setting')
            war.setText('Начать настройку?')
            war.setStyleSheet(style)
            war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            res = war.exec_()
            if res == QtWidgets.QMessageBox.Yes:
                if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                    auto_upload('___Config DEFAULT 19.txt')
                    zoc_min()
                    self.complete_mes()
                else:
                    auto_upload('___Config DEFAULT 15.txt')
                    zoc_min()
                    self.complete_mes()
                self.modal.plainTextEdit_2.setPlainText(
                    f'Комментарий:\n\nИспользуя цифровой мультиметр, измерьтеизмерьте напряжение в контрольных точках '
                    f'драйвера температуры, предварительно установив режим вольтметра по постоянному току. Полученное '
                    f'значение напряжения запишите в графу "Udrv". В остальные графы введите соответствующие значения '
                    f'из паспорта к лазеру.')
                self.set_status(1)
                self.modal.lineEdit_3.setReadOnly(False)
                self.modal.lineEdit_2.setReadOnly(False)
                self.modal.lineEdit.setReadOnly(False)
            else:
                self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def lines_edit_check(self):
        data = [self.modal.lineEdit.text(), self.modal.lineEdit_2.text(), self.modal.lineEdit_3.text(),
                self.modal.lineEdit_4.text()]
        dt, k = [], 1
        for i in data:
            if i.startswith('-') and i == self.modal.lineEdit_4.text():
                if i[1:].replace('.', '', 1).isdigit():
                    dt.append(k)
                    k += 1
                else:
                    k += 1
            else:
                if i.replace('.', '', 1).isdigit():
                    dt.append(k)
                    k += 1
                else:
                    k += 1
        if '.' in self.modal.lineEdit.text() or self.modal.lineEdit.text().isdigit() is False:
            self.modal.lineEdit.setStyleSheet(style1)
            fl = False
        else:
            self.modal.lineEdit.setStyleSheet(style2)
            fl = True
        if len(dt) == 4 and fl is True:
            return True
        else:
            for i in range(2, 5):
                if i not in dt:
                    if i == 2:
                        self.modal.lineEdit_2.setStyleSheet(style1)
                    if i == 3:
                        self.modal.lineEdit_3.setStyleSheet(style1)
                    if i == 4:
                        self.modal.lineEdit_4.setStyleSheet(style1)
                else:
                    if i == 2:
                        self.modal.lineEdit_2.setStyleSheet(style2)
                    if i == 3:
                        self.modal.lineEdit_3.setStyleSheet(style2)
                    if i == 4:
                        self.modal.lineEdit_4.setStyleSheet(style2)
            return False

    def set_status(self, status):
        if status == 1:
            self.modal.label_7.setText('Ready to work')
        elif status == 2:
            self.modal.label_7.setText('Not active')

    def complete_mes(self, message=''):
        self.set_status(2)
        com = QtWidgets.QMessageBox()
        com.setIcon(QtWidgets.QMessageBox.Information)
        com.setFont(QFont('Arial', 10, 81))
        com.setWindowTitle('Configuration Completed')
        com.setText(f'Конфигурация прошла успешно.{message}')
        com.setStyleSheet(style)
        com.setStandardButtons(QtWidgets.QMessageBox.Ok)
        com.exec_()
        self.set_status(1)

    def config_1st(self):
        self.modal.label_10.setVisible(False)
        if self.modal.lineEdit.isReadOnly() is False:
            if self.lines_edit_check() is True:
                self.modal.lineEdit.setStyleSheet(style2)
                self.modal.lineEdit_2.setStyleSheet(style2)
                self.modal.lineEdit_3.setStyleSheet(style2)
                self.modal.lineEdit_4.setStyleSheet(style2)
                if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                    self.config = LineAmplifierConfig(int(self.modal.lineEdit.text()))
                else:
                    self.config = PreAmplifierConfig(int(self.modal.lineEdit.text()))
                self.config.u_drv = float(self.modal.lineEdit_4.text())
                self.config.i_eol = float(self.modal.lineEdit_3.text())
                self.config.i_op = float(self.modal.lineEdit_2.text())

                try:
                    self.config.write_config_file(self.config.new_config_dict(SN=int(self.modal.lineEdit.text()),
                                                                              CURRENT_CC_MAX=self.config.eol_calc(),
                                                                              CURRENT_PC_MAX=self.config.eol_calc(),
                                                                              CURRENT_GC_MAX=self.config.eol_calc(),
                                                                              DACSP=self.config.dacsp_calc(),
                                                                              SCC_HT=int(float(self.modal.lineEdit_3.
                                                                                               text()) + 0.5),
                                                                              EOL=int(float(self.modal.lineEdit_2.text()
                                                                                            ) + 0.5)))
                    self.file_status('saved successfully', f'File __Config_Write_{int(self.modal.lineEdit.text())}.txt')
                    auto_upload(f'__Config_Write_{int(self.modal.lineEdit.text())}.txt')
                    zoc_min()
                    self.complete_mes(message=' Не забдьте провести калибровку напряжения на драйвере.')
                    self.modal.plainTextEdit_2.setPlainText(
                        f'Комментарий:\n\nНажмите "DRV Setup", проведите измерение напрежения на драйвере и введите '
                        f'полученное значение для корректировки. Псоле нажмите "Correction".')
                    self.modal.lineEdit_5.setReadOnly(False)
                    self.modal.lineEdit_5.setFocus()
                    self.modal.pushButton_7.setVisible(True)
                except:
                    self.file_status('NOT saved', f'File __Config_Write_{int(self.modal.lineEdit.text())}.txt')

            else:
                self.set_status(2)
                war = QtWidgets.QMessageBox()
                war.setIcon(QtWidgets.QMessageBox.Warning)
                war.setFont(QFont('Arial', 10, 81))
                war.setWindowTitle('Program Warning')
                war.setText('Ошибка ввода данных. Проверьте корректность введенных значений.')
                war.setStyleSheet(style)
                war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                res = war.exec_()
                if res == QtWidgets.QMessageBox.Ok:
                    self.set_status(1)
        else:
            self.set_status(2)
            war = QtWidgets.QMessageBox()
            war.setIcon(QtWidgets.QMessageBox.Warning)
            war.setFont(QFont('Arial', 10, 81))
            war.setWindowTitle('Program Warning')
            war.setText('Для продолжения настройки необхожимо сначала измерить напряжение на драйвере.')
            war.setStyleSheet(style)
            war.setStandardButtons(QtWidgets.QMessageBox.Ok)
            res = war.exec_()
            if res == QtWidgets.QMessageBox.Ok:
                self.set_status(1)

    def check_corr(self):
        u_t = self.modal.lineEdit_5.text()
        if u_t.startswith('-'):
            u_t_m = u_t[1:]
        else:
            u_t_m = u_t
        if u_t_m.replace('.', '', 1).strip('0').isdigit() or u_t == '0':
            u = float(self.modal.lineEdit_5.text())
            if -0.4 <= u <= 0.4:
                self.complete_mes(message=' Коррекция не нужна.')
                self.modal.plainTextEdit_2.clear()
                return 1
            elif -2 <= u < -0.4 or 2 >= u > 0.4:
                self.modal.plainTextEdit_2.clear()
                return 2
            else:
                self.modal.lineEdit_5.setStyleSheet(style1)
                self.modal.plainTextEdit_2.clear()
                self.modal.plainTextEdit_2.appendPlainText(
                    'Комментарий:\n\nПовторите измерения. Введенные данные слишком большие.')
                return 3
        else:
            self.modal.plainTextEdit_2.clear()
            self.modal.plainTextEdit_2.appendPlainText('Комментарий:\n\nНеверный формат введенных данных.')
            self.modal.lineEdit_5.setStyleSheet(style1)

    def upload(self):
        self.modal.label_10.setVisible(False)
        if self.modal.lineEdit_5.isReadOnly() is False:
            auto_upload('___AMPDRVSETUP ON.txt')
            zoc_min()
            self.modal.pushButton_7.setVisible(False)
            self.modal.pushButton_6.setVisible(True)
            self.modal.lineEdit_5.setFocus()
        else:
            self.set_status(2)
            war = QtWidgets.QMessageBox()
            war.setIcon(QtWidgets.QMessageBox.Warning)
            war.setFont(QFont('Arial', 10, 81))
            war.setWindowTitle('Program Warning')
            war.setText('Корректировка недоступна.')
            war.setStyleSheet(style)
            war.setStandardButtons(QtWidgets.QMessageBox.Ok)
            res = war.exec_()
            if res == QtWidgets.QMessageBox.Ok:
                self.set_status(1)

    def correction(self):
        self.modal.label_10.setVisible(False)
        if self.check_corr() == 1:
            self.modal.lineEdit_5.setStyleSheet(style2)
            self.modal.pushButton_7.setVisible(True)
            self.modal.pushButton_6.setVisible(False)
        elif self.check_corr() == 2:
            self.modal.lineEdit_5.setStyleSheet(style2)
            try:
                self.config.dacsp_corr(float(self.modal.lineEdit_5.text()))
                self.file_status('saved successfully', f'File __Config_Write_{int(self.modal.lineEdit.text())}.txt')
                auto_upload(f'__Config_Write_{int(self.modal.lineEdit.text())}.txt')
                zoc_min()
                self.complete_mes()
                self.modal.pushButton_6.setVisible(False)
                self.modal.pushButton_7.setVisible(True)
                self.modal.plainTextEdit_2.clear()
            except:
                self.file_status('NOT saved', f'File __Config_Write_{int(self.modal.lineEdit.text())}.txt')
        else:
            pass

    def back_to_master(self):
        self.modal.label_10.setVisible(False)
        self.set_status(2)
        war = QtWidgets.QMessageBox()
        war.setIcon(QtWidgets.QMessageBox.Warning)
        war.setFont(QFont('Arial', 10, 81))
        war.setWindowTitle('Back to Master')
        war.setText('Уверены, что хотите вернуться на главное окно?')
        war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        war.setStyleSheet(style)
        res = war.exec_()
        if res == QtWidgets.QMessageBox.Yes:
            self.flag = 1
            self.close()
        self.set_status(1)

    def closeEvent(self, value):
        self.modal.label_10.setVisible(False)
        if self.flag == 1:
            self.close()
            myapp.setWindowState(Qt.WindowState.WindowNoState)
            myapp.set_status(1)
        else:
            self.set_status(2)
            war = QtWidgets.QMessageBox()
            war.setIcon(QtWidgets.QMessageBox.Warning)
            war.setFont(QFont('Arial', 10, 81))
            war.setWindowTitle('Back to Master')
            war.setText('Уверены, что хотите вернуться на главное окно?')
            war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            war.setStyleSheet(style)
            res = war.exec_()
            if res == QtWidgets.QMessageBox.Yes:
                myapp.setWindowState(Qt.WindowState.WindowNoState)
                myapp.set_status(1)
            elif res == QtWidgets.QMessageBox.No:
                value.ignore()
            self.flag = 0
            self.set_status(1)


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=MyWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.modal = Ui_Form_2()
        self.flag = 0
        self.modal.setupUi(self)
        self.setWindowModality(2)
        if myapp.ui.radioButton_6.isChecked():
            self.modal.plainTextEdit_3.setPlainText('K25-M19')
        else:
            self.modal.plainTextEdit_3.setPlainText('K25-M12')
        self.modal.plainTextEdit_2.setPlaceholderText(
            'Комментарий:\n\nВведите серийный номер изделия и выберите этап проверки качества сварки '
            'оптических компонентов.')
        self.modal.pushButton_2.setToolTip('Back to Master')
        self.modal.pushButton_5.setToolTip('Start Checking')
        self.modal.pushButton_6.setToolTip('Check Laser Temperature')
        self.modal.pushButton_8.setToolTip('Clear All')
        self.modal.pushButton_9.setToolTip('Upload Current')
        self.modal.pushButton_7.setToolTip('Upload Current')
        self.modal.label_6.setToolTip('Date')
        self.modal.label_7.setToolTip('Window Status')
        self.modal.pushButton_2.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_5.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_6.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_8.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_9.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_7.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_6.setStyleSheet("QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_7.setStyleSheet(
            'QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}' + "QWidget{color: #b1b1b1; "
                                                                                      "background-color: #242424; "
                                                                                      "border:#242424}")
        self.modal.plainTextEdit_3.setFont(QFont('Arial', 24, 81))
        self.modal.label_6.setFont(QFont('Arial', 10, 57))
        self.modal.label_7.setFont(QFont('Arial', 8, 71))
        self.modal.label_6.setText(QDate.currentDate().toString('dd/MM/yyyy'))
        self.modal.label_7.setText('Ready to work')
        self.modal.lineEdit_7.setFocus()
        self.modal.lineEdit_4.setReadOnly(True)
        self.modal.lineEdit_5.setReadOnly(True)
        self.modal.lineEdit_6.setReadOnly(True)
        self.modal.label_10.setToolTip('Config File Status')
        self.modal.label_10.setFont(QFont('Arial', 8, 57))
        self.modal.label_10.setVisible(False)
        self.modal.pushButton_8.clicked.connect(self.clear)
        self.modal.pushButton_2.clicked.connect(self.back_to_master)
        self.modal.radioButton_5.clicked.connect(self.get_text)
        self.modal.radioButton_6.clicked.connect(self.get_text)
        self.modal.pushButton_5.clicked.connect(self.check)
        self.modal.pushButton_9.clicked.connect(self.acc_op)
        self.modal.pushButton_7.clicked.connect(self.acc_eol)
        self.modal.pushButton_6.clicked.connect(self.report)
        self.config = None

    def report(self):
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_upload('__report.txt', 'yes')
            zoc_min()
            if read_temp():
                self.set_status(2)
                com = QtWidgets.QMessageBox()
                com.setIcon(QtWidgets.QMessageBox.Information)
                com.setFont(QFont('Arial', 10, 81))
                com.setWindowTitle('Temperature Test Completed')
                com.setText(f'Температура лазера соответствует 25 градусам.')
                com.setStyleSheet(style)
                com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                com.exec_()
                self.set_status(1)
            else:
                self.set_status(2)
                war = QtWidgets.QMessageBox()
                war.setIcon(QtWidgets.QMessageBox.Warning)
                war.setFont(QFont('Arial', 10, 81))
                war.setWindowTitle('Temperature Test Warning')
                war.setText('Температура лазера не соответствует 25 градусам.')
                war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                war.setStyleSheet(style)
                war.exec_()
                self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def acc_op(self):
        self.modal.lineEdit_6.clear()
        self.modal.lineEdit_6.setReadOnly(True)
        self.modal.lineEdit_5.setFocus()
        self.acc_i('op')

    def acc_eol(self):
        self.modal.lineEdit_5.clear()
        self.modal.lineEdit_5.setReadOnly(True)
        self.modal.lineEdit_6.setFocus()
        self.acc_i('eol')

    def acc_i(self, acc):
        self.modal.label_10.setVisible(False)
        if check_process('zoc') is not None:
            self.set_status(2)
            try:
                if acc == 'op':
                    if myapp.ui.radioButton_6.isChecked():
                        self.config = AmplifierConfig(19, int(self.modal.lineEdit_7.text()))
                    else:
                        self.config = AmplifierConfig(15, int(self.modal.lineEdit_7.text()))
                else:
                    if myapp.ui.radioButton_6.isChecked():
                        self.config = AmplifierConfig(19, int(self.modal.lineEdit_7.text()))
                    else:
                        self.config = AmplifierConfig(15, int(self.modal.lineEdit_7.text()))
                if self.config.found_error():
                    auto_log()
                    auto_upload('AM_CURRENT.txt')
                    if acc == 'op':
                        auto_upload(f'ACC 1 {self.config.get_config_value("EOL")}.txt')
                        zoc_min()
                        self.modal.lineEdit_5.setReadOnly(False)
                        self.set_status(1)
                    else:
                        auto_upload(f'ACC 1 {self.config.get_config_value("SCC_HT")}.txt')
                        zoc_min()
                        self.modal.lineEdit_6.setReadOnly(False)
                        self.set_status(1)
                else:
                    self.modal.label_10.setVisible(True)
                    self.modal.label_10.setText(f'File __Config_Write_{int(self.modal.lineEdit_7.text())} not found')
                    self.set_status(1)
            except:
                self.set_status(1)
                self.modal.label_10.setVisible(True)
                self.modal.label_10.setText('Input data error')
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def att_check(self):
        if self.modal.lineEdit_4.text() != '':
            if self.modal.lineEdit_4.text().startswith('-'):
                if self.modal.radioButton_6.isChecked():
                    if 1.5 < float(self.modal.lineEdit_4.text()[1:]) <= 2.25:
                        return True
                    else:
                        return False
                elif self.modal.radioButton_5.isChecked():
                    if 4.5 < float(self.modal.lineEdit_4.text()[1:]) <= 5.25:
                        return True
                    else:
                        return False
            else:
                if self.modal.radioButton_6.isChecked():
                    if 1.5 < float(self.modal.lineEdit_4.text()) <= 2.25:
                        return True
                    else:
                        return False
                elif self.modal.radioButton_5.isChecked():
                    if 4.5 < float(self.modal.lineEdit_4.text()) <= 5.25:
                        return True
                    else:
                        return False
        else:
            return True

    def complete_mes(self, message=''):
        self.set_status(2)
        com = QtWidgets.QMessageBox()
        com.setIcon(QtWidgets.QMessageBox.Information)
        com.setFont(QFont('Arial', 10, 81))
        com.setWindowTitle('Verification Completed')
        com.setText(f'Проверка завершена. Все значения соответствуют типовым.{message}')
        com.setStyleSheet(style)
        com.setStandardButtons(QtWidgets.QMessageBox.Ok)
        res = com.exec_()
        if res == QtWidgets.QMessageBox.Ok:
            self.get_text()
        self.set_status(1)

    def check_for_op(self):
        if int(self.modal.plainTextEdit_3.toPlainText()[5:]) == 19:
            if self.modal.radioButton_6.isChecked():
                if float(self.modal.lineEdit_5.text()) > 420:
                    if read_i_op():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            elif self.modal.radioButton_5.isChecked():
                if float(self.modal.lineEdit_5.text()) > 390:
                    if read_i_op():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            else:
                self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВыберите этап проверки.')
        elif int(self.modal.plainTextEdit_3.toPlainText()[5:]) == 12:
            if self.modal.radioButton_6.isChecked():
                if float(self.modal.lineEdit_5.text()) > 410:
                    if read_i_op():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            elif self.modal.radioButton_5.isChecked():
                if float(self.modal.lineEdit_5.text()) > 380:
                    if read_i_op():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            else:
                self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВыберите этап проверки.')

    def check_for_eol(self):
        if int(self.modal.plainTextEdit_3.toPlainText()[5:]) == 19:
            if self.modal.radioButton_6.isChecked():
                if float(self.modal.lineEdit_6.text()) > 420:
                    if read_i_eol():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            elif self.modal.radioButton_5.isChecked():
                if float(self.modal.lineEdit_6.text()) > 390:
                    if read_i_op():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            else:
                self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВыберите этап проверки.')
        elif int(self.modal.plainTextEdit_3.toPlainText()[5:]) == 12:
            if self.modal.radioButton_6.isChecked():
                if float(self.modal.lineEdit_6.text()) > 410:
                    if read_i_op():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            elif self.modal.radioButton_5.isChecked():
                if float(self.modal.lineEdit_6.text()) > 380:
                    if read_i_op():
                        if self.att_check():
                            self.complete_mes('')
                        else:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nВносимое затухание НЕ соответствует'
                                ' типовому значению. Проверьте качество сварки или исправность'
                                ' оптических компонентов.')
                    else:
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение тока полученное в ZOC'
                                                                ' НЕ соответствует значению указанному в'
                                                                ' конфигурации.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВысокие потери мощности лазера.'
                                                            ' Проверьте качество сварки.')
            else:
                self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВыберите этап проверки.')

    def check(self):
        self.modal.lineEdit_4.setStyleSheet(style2)
        self.modal.lineEdit_5.setStyleSheet(style2)
        self.modal.lineEdit_6.setStyleSheet(style2)
        if self.modal.lineEdit_4.text().replace('.', '', 1).isdigit() or (self.modal.lineEdit_4.text().startswith('-') and self.modal.lineEdit_4.text()[1:].replace('.', '', 1).isdigit()):
            if self.modal.lineEdit_5.text() == '' and self.modal.lineEdit_6.text() == '':
                if self.att_check():
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВносимое затухание соответствует'
                                                            ' типовому значению.')
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВносимое затухание НЕ соответствует'
                                                            'типовому значению. Проверьте качество сварки или '
                                                            'исправность оптических компонентов.')
            else:
                if self.modal.lineEdit_5.text() != '':
                    if self.p_op_cor():
                        self.check_for_op()
                    else:
                        self.modal.lineEdit_5.setStyleSheet(style1)
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНекорректное значение мощности.')
                elif self.modal.lineEdit_6.text() != '':
                    if self.p_eol_cor():
                        self.check_for_eol()
                    else:
                        self.modal.lineEdit_6.setStyleSheet(style1)
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНекорректное значение мощности.')
        elif self.modal.lineEdit_4.text() == '':
            if self.modal.lineEdit_5.text() != '':
                if self.p_op_cor():
                    self.check_for_op()
                else:
                    self.modal.lineEdit_5.setStyleSheet(style1)
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНекорректное значение мощности.')
            elif self.modal.lineEdit_6.text() != '':
                if self.p_eol_cor():
                    self.check_for_eol()
                else:
                    self.modal.lineEdit_6.setStyleSheet(style1)
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНекорректное значение мощности.')
        else:
            self.modal.lineEdit_4.setStyleSheet(style1)
            self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНекорректное значение затухания.')

    def p_op_cor(self):
        if self.modal.lineEdit_5.text().replace('.', '', 1).isdigit():
            return True
        else:
            return False

    def p_eol_cor(self):
        if self.modal.lineEdit_6.text().replace('.', '', 1).isdigit():
            return True
        else:
            return False

    def get_text(self):
        comment1 = 'Комментарий:\n\nПодключите выход аттенюатора IQS-3150 ко входу оптического усилителя, используя оптическю розетку,' \
                   'а выход ОУ подайте на калибровочный измеритель мощности IQS-1700 (предварительно необходимо' \
                   ' произвести чистку оптических коннекторов). Полученное значение с экрана монитора введите в ' \
                   'поле "A(dBm)...". Для проверки потерь мощности лазера подключите выходной коннектор лазера ' \
                   'к высокомощному измерителю мощности IQS-1700. Подайте питание на плату. Нажмите "ACC Iop" и' \
                   ' "ACC EOL". Полученные значения введите в соответствующие графы. Для проверки температры нажмите ' \
                   '"Check Temp", для проверки затхания и мощности нажмите "Check" '
        self.modal.plainTextEdit_2.setPlainText(comment1)
        self.modal.lineEdit_4.setReadOnly(False)

    def clear(self):
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_7.clear()
        self.modal.lineEdit_4.clear()
        self.modal.lineEdit_5.clear()
        self.modal.lineEdit_6.clear()
        self.modal.lineEdit_4.setStyleSheet(style2)
        self.modal.lineEdit_5.setStyleSheet(style2)
        self.modal.lineEdit_6.setStyleSheet(style2)
        self.modal.lineEdit_7.setFocus()
        self.modal.lineEdit_5.setReadOnly(True)
        self.modal.lineEdit_6.setReadOnly(True)
        self.modal.radioButton_6.setChecked(False)
        self.modal.plainTextEdit_2.clear()
        self.set_status(1)

    def set_status(self, status):
        if status == 1:
            self.modal.label_7.setText('Ready to work')
        elif status == 2:
            self.modal.label_7.setText('Not active')

    def back_to_master(self):
        self.modal.label_10.setVisible(False)
        self.set_status(2)
        war = QtWidgets.QMessageBox()
        war.setIcon(QtWidgets.QMessageBox.Warning)
        war.setFont(QFont('Arial', 10, 81))
        war.setWindowTitle('Back to Master')
        war.setText('Уверены, что хотите вернуться на главное окно?')
        war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        war.setStyleSheet(style)
        res = war.exec_()
        if res == QtWidgets.QMessageBox.Yes:
            self.flag = 1
            self.close()
        self.set_status(1)

    def closeEvent(self, value):
        self.modal.label_10.setVisible(False)
        if self.flag == 1:
            self.close()
            myapp.setWindowState(Qt.WindowState.WindowNoState)
            myapp.set_status(1)
        else:
            self.set_status(2)
            war = QtWidgets.QMessageBox()
            war.setIcon(QtWidgets.QMessageBox.Warning)
            war.setFont(QFont('Arial', 10, 81))
            war.setWindowTitle('Back to Master')
            war.setText('Уверены, что хотите вернуться на главное окно?')
            war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            war.setStyleSheet(style)
            res = war.exec_()
            if res == QtWidgets.QMessageBox.Yes:
                myapp.setWindowState(Qt.WindowState.WindowNoState)
                myapp.set_status(1)
            elif res == QtWidgets.QMessageBox.No:
                value.ignore()
            self.flag = 0
            self.set_status(1)


class ThirdWindow(QtWidgets.QWidget):
    def __init__(self, parent=MyWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.modal = Ui_Form_3()
        self.modal.setupUi(self)
        self.setWindowModality(2)
        self.flag = 0
        if myapp.ui.radioButton_6.isChecked():
            self.modal.plainTextEdit_3.setPlainText('K25-M19')
            self.get_text(6)
        else:
            self.modal.plainTextEdit_3.setPlainText('K25-M12')
            self.get_text(10)
        self.modal.pushButton_2.setToolTip('Back to Master')
        self.modal.pushButton_7.setToolTip('Check I/O Power')
        self.modal.pushButton_8.setToolTip('Start Correction')
        self.modal.pushButton_3.setToolTip('Start Uploading')
        self.modal.pushButton_9.setToolTip('Look Current and Input Power')
        self.modal.pushButton_4.setToolTip('Look Output Power')
        self.modal.pushButton_10.setToolTip('Check Output Power')
        self.modal.pushButton_11.setToolTip('Return Default Values')
        self.modal.pushButton_12.setToolTip('Clear All')
        self.modal.pushButton_6.setToolTip('Input Correction')
        self.modal.pushButton_5.setToolTip('Output Correction')
        self.modal.pushButton_13.setToolTip('Start Correction')
        self.modal.pushButton_14.setToolTip('Check Output Power')
        self.modal.label_6.setToolTip('Date')
        self.modal.label_7.setToolTip('Window Status')
        self.modal.pushButton_14.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_13.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_5.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_6.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_12.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_11.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_9.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_10.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_4.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_2.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_7.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_8.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_3.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_6.setStyleSheet("QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_7.setStyleSheet(
            'QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}' + "QWidget{color: #b1b1b1; "
                                                                                      "background-color: #242424; "
                                                                                      "border:#242424}")
        self.modal.plainTextEdit_3.setFont(QFont('Arial', 24, 81))
        self.modal.label_6.setFont(QFont('Arial', 10, 57))
        self.modal.label_7.setFont(QFont('Arial', 8, 71))
        self.modal.label_6.setText(QDate.currentDate().toString('dd/MM/yyyy'))
        self.modal.label_7.setText('Ready to work')
        self.modal.lineEdit_7.setFocus()
        self.modal.label_10.setToolTip('Config File Status')
        self.modal.label_10.setFont(QFont('Arial', 8, 57))
        self.modal.label_10.setVisible(False)
        self.modal.pushButton_2.clicked.connect(self.back_to_master)
        self.modal.pushButton_3.clicked.connect(self.start)
        self.modal.pushButton_8.clicked.connect(self.correct_1)
        self.modal.pushButton_7.clicked.connect(self.check_1)
        self.modal.pushButton_10.clicked.connect(self.check_2)
        self.modal.pushButton_9.clicked.connect(self.look_current)
        self.modal.pushButton_4.clicked.connect(self.look_power)
        self.modal.pushButton_12.clicked.connect(self.clear)
        self.modal.pushButton_11.clicked.connect(self.default)
        self.modal.pushButton_6.clicked.connect(self.input_correction)
        self.modal.pushButton_5.clicked.connect(self.am_power_apc)
        self.modal.pushButton_14.clicked.connect(self.check_3)
        self.modal.pushButton_13.clicked.connect(self.correct_3)
        self.modal.line_12.setStyleSheet('background-color: #ffaa00')
        self.modal.line_13.setStyleSheet('background-color: #ffaa00')
        self.modal.line_9.setStyleSheet('background-color: #ffaa00')
        self.modal.line_7.setStyleSheet('background-color: #ffaa00')
        self.modal.pushButton_8.setVisible(False)
        self.modal.pushButton_13.setVisible(False)
        self.modal.pushButton_4.setVisible(False)
        self.modal.pushButton_9.setVisible(True)
        self.modal.lineEdit_9.setReadOnly(True)
        self.modal.lineEdit_10.setReadOnly(True)
        self.modal.lineEdit_11.setReadOnly(True)
        self.config = None
        self.acc_eol = None
        self.acc_scc = None

    def start(self):
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            if myapp.ui.radioButton_6.isChecked():
                auto_upload('APC_19.txt')
            else:
                auto_upload('APC_15.txt')
            auto_upload('AM_Power.txt')
            auto_upload('_PH.txt')
            zoc_min()
            self.modal.lineEdit_8.setFocus()
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nВведите значение выходной мощности, полученное с экрана монитора. Для корректировки '
                'нажмите "Correct".')
            self.modal.pushButton_3.setVisible(False)
            self.modal.pushButton_8.setVisible(True)
            self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def file_status(self, txt, file):
        self.modal.label_10.setVisible(True)
        self.modal.label_10.setText(f'{file} {txt}')

    def correct_1(self):
        self.modal.lineEdit_8.setStyleSheet(style2)
        self.modal.lineEdit_7.setStyleSheet(style2)
        if self.modal.lineEdit_8.text().replace('.', '', 1).isdigit():
            if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                try:
                    if self.modal.lineEdit_7.text().isdigit():
                        self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                        self.config.tap_in_line = read_pdm1()
                        self.config.tap_out_line = float(self.modal.lineEdit_8.text())
                        self.config.write_config_file(
                            self.config.new_config_dict(TAP_IN_IL=self.config.tap_in_line_calc(),
                                                        TAP_OUT_IL=self.config.tap_out_line_calc()))
                        self.file_status('changed successfully',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНажмите "Check" для проверки входного '
                                                                'и выходного уровня мощности оптического усилителя.')
                    else:
                        self.modal.lineEdit_7.setStyleSheet(style1)
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНекорректное значение серийного номера.')
                except:
                    self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nОшибка при работе с файлом конфигурации.')
            else:
                try:
                    if self.modal.lineEdit_7.text().isdigit():
                        self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                        self.config.tap_in_pre = read_pdm1()
                        self.config.tap_out_pre = float(self.modal.lineEdit_8.text())
                        self.config.write_config_file(
                            self.config.new_config_dict(TAP_IN_IL=self.config.tap_in_pre_calc(),
                                                        TAP_OUT_IL=self.config.tap_out_pre_calc()))
                        self.file_status('changed successfully',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНажмите "Check" для проверки входного '
                                                                'и выходного уровня мощности оптического усилителя.')
                    else:
                        self.modal.lineEdit_7.setStyleSheet(style1)
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНекорректное значение серийного номера.')
                except:
                    self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nОшибка при работе с файлом конфигурации.')
        else:
            self.modal.lineEdit_8.setStyleSheet(style1)
            self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНекорректное значение мощности.')

    def check_1(self):
        self.modal.label_10.setVisible(False)
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            auto_upload(f'__Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
            if myapp.ui.radioButton_6.isChecked():
                auto_upload('APC_19.txt')
            else:
                auto_upload('APC_15.txt')
            auto_upload('AM_Power.txt')
            auto_upload('_PH.txt')
            zoc_min()
            if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                if -6.11 <= read_pdm1() <= -5.97:
                    self.set_status(2)
                    qst = QtWidgets.QMessageBox()
                    qst.setIcon(QtWidgets.QMessageBox.Question)
                    qst.setFont(QFont('Arial', 10, 81))
                    qst.setWindowTitle('Power Check')
                    qst.setText('Выходная мощность равна 19 дБм?')
                    qst.setStyleSheet(style)
                    qst.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    res = qst.exec_()
                    if res == QtWidgets.QMessageBox.Yes:
                        com = QtWidgets.QMessageBox()
                        com.setIcon(QtWidgets.QMessageBox.Information)
                        com.setFont(QFont('Arial', 10, 81))
                        com.setWindowTitle('Setup Completed')
                        com.setText('Настройка прошла успешно. Следуйте инструкциям для продолжения настройки.')
                        com.setStyleSheet(style)
                        com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        res = com.exec_()
                        if res == QtWidgets.QMessageBox.Ok:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nНажмите "PH/LC" для проодлжения настройки')
                            self.modal.line_12.setStyleSheet('background-color: #323232')
                            self.modal.line_13.setStyleSheet('background-color: #323232')
                            self.modal.line_9.setStyleSheet('background-color: #323232')
                            self.modal.line_7.setStyleSheet('background-color: #323232')
                            self.modal.line_10.setStyleSheet('background-color: #ffaa00')
                            self.modal.line_11.setStyleSheet('background-color: #ffaa00')
                            self.modal.line_14.setStyleSheet('background-color: #ffaa00')
                            self.modal.line_15.setStyleSheet('background-color: #ffaa00')
                            self.set_status(1)
                    else:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nСкорректируйте значение выходной мощности и заново проведите настройку.')
                        self.modal.lineEdit_8.setFocus()
                        self.set_status(1)
                else:
                    self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nЗначение входной мощности не равно -6 дБм')
                    self.set_status(1)
            else:
                if -10.11 <= read_pdm1() <= -9.97:
                    self.set_status(2)
                    qst = QtWidgets.QMessageBox()
                    qst.setIcon(QtWidgets.QMessageBox.Question)
                    qst.setFont(QFont('Arial', 10, 81))
                    qst.setWindowTitle('Power Check')
                    qst.setText('Выходная мощность равна 15 дБм?')
                    qst.setStyleSheet(style)
                    qst.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    res = qst.exec_()
                    if res == QtWidgets.QMessageBox.Yes:
                        com = QtWidgets.QMessageBox()
                        com.setIcon(QtWidgets.QMessageBox.Information)
                        com.setFont(QFont('Arial', 10, 81))
                        com.setWindowTitle('Setup Completed')
                        com.setText('Настройка прошла успешно. Следуйте инструкциям для продолжения настройки.')
                        com.setStyleSheet(style)
                        com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        res = com.exec_()
                        if res == QtWidgets.QMessageBox.Ok:
                            self.modal.plainTextEdit_2.setPlainText(
                                'Комментарий:\n\nНажмите "PH/LC" для проверки значения силы тока.')
                            self.modal.line_12.setStyleSheet('background-color: #323232')
                            self.modal.line_13.setStyleSheet('background-color: #323232')
                            self.modal.line_9.setStyleSheet('background-color: #323232')
                            self.modal.line_7.setStyleSheet('background-color: #323232')
                            self.modal.line_10.setStyleSheet('background-color: #ffaa00')
                            self.modal.line_11.setStyleSheet('background-color: #ffaa00')
                            self.modal.line_14.setStyleSheet('background-color: #ffaa00')
                            self.modal.line_15.setStyleSheet('background-color: #ffaa00')
                            self.set_status(1)
                    else:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nСкорректируйте значение выходной мощности и заново проведите настройку.')
                        self.modal.lineEdit_8.setFocus()
                        self.set_status(1)
                else:
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nЗначение входной мощности не равно -10 дБм.')
                    self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def look_current(self):
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            auto_upload('AM_Power.txt')
            auto_upload('_PHPHPH.txt')
            auto_upload('_LCLC_1.txt')
            zoc_min()
            if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                if 400 <= read_pdm1_2()[1] <= 550 and -6.11 <= read_pdm1_2()[0] <= -5.97:
                    com = QtWidgets.QMessageBox()
                    com.setIcon(QtWidgets.QMessageBox.Information)
                    com.setFont(QFont('Arial', 10, 81))
                    com.setWindowTitle('Successful Check')
                    com.setText('Проверка прошла успешно.')
                    com.setStyleSheet(style)
                    com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = com.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНажмите "AM Current" для продолжения настройки.')
                        self.modal.pushButton_9.setVisible(False)
                        self.modal.pushButton_4.setVisible(True)
                        self.set_status(1)
                else:
                    war = QtWidgets.QMessageBox()
                    war.setIcon(QtWidgets.QMessageBox.Warning)
                    war.setFont(QFont('Arial', 10, 81))
                    war.setWindowTitle('Warning')
                    war.setText('Сила тока и/или входная мощность не соответствуют типовым значениям.')
                    war.setStyleSheet(style)
                    war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = war.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nЗначение силы тока в режиме стабилизации мощности не соответствует '
                            'типовому значению и/или входная мощность нестабильна.')
                        self.set_status(1)
            else:
                if 180 <= read_pdm1_2()[1] <= 330 and -10.11 <= read_pdm1_2()[0] <= -9.97:
                    com = QtWidgets.QMessageBox()
                    com.setIcon(QtWidgets.QMessageBox.Information)
                    com.setFont(QFont('Arial', 10, 81))
                    com.setWindowTitle('Successful Check')
                    com.setText('Проверка прошла успешно.')
                    com.setStyleSheet(style)
                    com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = com.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНажмите "AM Current" для продолжения настройки.')
                        self.modal.pushButton_9.setVisible(False)
                        self.modal.pushButton_4.setVisible(True)
                        self.set_status(1)
                else:
                    war = QtWidgets.QMessageBox()
                    war.setIcon(QtWidgets.QMessageBox.Warning)
                    war.setFont(QFont('Arial', 10, 81))
                    war.setWindowTitle('Warning')
                    war.setText('Сила тока и/или входная мощность не соответствуют типовым значениям.')
                    war.setStyleSheet(style)
                    war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = war.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nЗначение силы тока в режиме стабилизации мощности не соответствует '
                            'типовому значению и/или входная мощность нестабильна.')
                        self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def look_power(self):
        self.modal.lineEdit_7.setStyleSheet(style2)
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            auto_upload('AM_CURRENT.txt')
            try:
                if self.modal.lineEdit_7.text().isdigit():
                    if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                        self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    else:
                        self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    if self.modal.lineEdit_10.isReadOnly():
                        self.acc_eol = self.config.get_config_value("EOL")
                        auto_upload(f'ACC 1 {self.acc_eol}.txt')
                        self.modal.lineEdit_9.setFocus()
                        self.modal.lineEdit_9.setReadOnly(False)
                        self.modal.lineEdit_10.setReadOnly(False)
                        self.set_status(1)
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nВведите значение выходной мощности при рабочем токе. Нажмите "AM '
                            'Current" для продолжения настройки.')
                        self.file_status('processed',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    else:
                        self.acc_scc = self.config.get_config_value("SCC_HT")
                        auto_upload(f'ACC 1 {self.acc_scc}.txt')
                        self.modal.lineEdit_10.setFocus()
                        self.set_status(1)
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nВведите значение выходной '
                                                                'мощности при максимальном токе. Нажмите "Check" '
                                                                'для проверки выходного уровня мощности '
                                                                'оптического усилителя.')
                        self.file_status('processed',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                else:
                    self.modal.lineEdit_7.setStyleSheet(style1)
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nНекорректное значение серийного номера.')
                    self.set_status(1)
            except:
                self.file_status('NOT processed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                self.set_status(1)

            auto_upload('_PH.txt')
            zoc_min()
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def check_2(self):
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_9.setStyleSheet(style2)
        self.modal.lineEdit_10.setStyleSheet(style2)
        if self.modal.lineEdit_9.text().replace('.', '', 1).isdigit() and self.modal.lineEdit_10.text().replace('.', '',
                                                                                                                1).isdigit():
            if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                if float(self.modal.lineEdit_9.text()) > 19 and float(self.modal.lineEdit_10.text()) > 19 and float(
                        self.acc_scc) > 19 and float(self.acc_eol) > 19:
                    self.set_status(2)
                    com = QtWidgets.QMessageBox()
                    com.setIcon(QtWidgets.QMessageBox.Information)
                    com.setFont(QFont('Arial', 10, 81))
                    com.setWindowTitle('Successful Check')
                    com.setText('Проверка прошла успешно.')
                    com.setStyleSheet(style)
                    com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = com.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nУстановите уровень входного сигнала равным -35 дБм. Нажмите "AM Gain" '
                            'для продолжения настройки.')
                        self.set_status(1)
                        self.modal.line_16.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_17.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_21.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_20.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_10.setStyleSheet('background-color: #323232')
                        self.modal.line_11.setStyleSheet('background-color: #323232')
                        self.modal.line_14.setStyleSheet('background-color: #323232')
                        self.modal.line_15.setStyleSheet('background-color: #323232')
                else:
                    self.set_status(2)
                    war = QtWidgets.QMessageBox()
                    war.setIcon(QtWidgets.QMessageBox.Warning)
                    war.setFont(QFont('Arial', 10, 81))
                    war.setWindowTitle('Warning')
                    war.setText('Низкая выходная мощность.')
                    war.setStyleSheet(style)
                    war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = war.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nЗначение уровня выходной мощности ниже требуемого.')
                        self.set_status(1)
            else:
                if float(self.modal.lineEdit_9.text()) > 15 and float(self.modal.lineEdit_10.text()) > 15 and float(
                        self.acc_scc) > 15 and float(self.acc_eol) > 15:
                    self.set_status(2)
                    com = QtWidgets.QMessageBox()
                    com.setIcon(QtWidgets.QMessageBox.Information)
                    com.setFont(QFont('Arial', 10, 81))
                    com.setWindowTitle('Successful Check')
                    com.setText('Проверка прошла успешно.')
                    com.setStyleSheet(style)
                    com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = com.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nУстановите уровень входного сигнала равным -35 дБм. Нажмите "AM Gain" '
                            'для продолжения настройки.')
                        self.set_status(1)
                        self.modal.line_16.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_17.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_21.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_20.setStyleSheet('background-color: #ffaa00')
                        self.modal.line_10.setStyleSheet('background-color: #323232')
                        self.modal.line_11.setStyleSheet('background-color: #323232')
                        self.modal.line_14.setStyleSheet('background-color: #323232')
                        self.modal.line_15.setStyleSheet('background-color: #323232')
                else:
                    self.set_status(2)
                    war = QtWidgets.QMessageBox()
                    war.setIcon(QtWidgets.QMessageBox.Warning)
                    war.setFont(QFont('Arial', 10, 81))
                    war.setWindowTitle('Warning')
                    war.setText('Низкая выходная мощность.')
                    war.setStyleSheet(style)
                    war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    res = war.exec_()
                    if res == QtWidgets.QMessageBox.Ok:
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nЗначение уровня выходной мощности ниже требуемого.')
                        self.set_status(1)
        elif self.modal.lineEdit_9.text().replace('.', '', 1).isdigit() is False:
            self.modal.lineEdit_9.setStyleSheet(style1)
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nНекорректное значение мощности.')
        elif self.modal.lineEdit_10.text().replace('.', '', 1).isdigit() is False:
            self.modal.lineEdit_10.setStyleSheet(style1)
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nНекорректное значение мощности.')

    def test_log(self):
        auto_log()

    def input_correction(self):
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            auto_upload('AM_GAIN.txt')
            auto_upload('_PHPHPH.txt')
            zoc_min()
            self.modal.lineEdit_7.setStyleSheet(style2)
            if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                self.get_text(35)
                try:
                    if self.modal.lineEdit_7.text().isdigit():
                        self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                        self.config.pd_in_line = read_pdm1_35()
                        self.config.write_config_file(
                            self.config.new_config_dict(
                                B_PD_IN=self.config.pd_in_line_calc(int(self.config.get_config_value('TAP_IN_IL')))))
                        self.file_status('changed successfully',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                        self.set_status(2)
                        self.test_log()
                        auto_upload('AM_GAIN.txt')
                        auto_upload('_PHPHPH.txt')
                        zoc_min()
                        if -35.20 <= read_pdm1_35_2() <= -34.9:
                            self.set_status(2)
                            com = QtWidgets.QMessageBox()
                            com.setIcon(QtWidgets.QMessageBox.Information)
                            com.setFont(QFont('Arial', 10, 81))
                            com.setWindowTitle('Successful Correction')
                            com.setText('Характеристика входного фотодиода скорректирована удачно.')
                            com.setStyleSheet(style)
                            com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            res = com.exec_()
                            if res == QtWidgets.QMessageBox.Ok:
                                self.modal.plainTextEdit_2.setPlainText(
                                    'Комментарий:\n\nУстановите уровень входного сигнала равным -35 дБм. Нажмите "AM '
                                    'Power" для продолжения настройки.')
                                self.set_status(1)
                                self.modal.line_18.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_19.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_22.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_23.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_16.setStyleSheet('background-color: #323232')
                                self.modal.line_17.setStyleSheet('background-color: #323232')
                                self.modal.line_21.setStyleSheet('background-color: #323232')
                                self.modal.line_20.setStyleSheet('background-color: #323232')
                        else:
                            self.set_status(2)
                            war = QtWidgets.QMessageBox()
                            war.setIcon(QtWidgets.QMessageBox.Warning)
                            war.setFont(QFont('Arial', 10, 81))
                            war.setWindowTitle('Warning')
                            war.setText('Характеристика входного фотодиода откалибрована неверно.')
                            war.setStyleSheet(style)
                            war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            res = war.exec_()
                            if res == QtWidgets.QMessageBox.Ok:
                                self.modal.plainTextEdit_2.setPlainText(
                                    'Комментарий:\n\nУровень входного сигнала не соответствует -35 дБм.')
                                self.set_status(1)
                    else:
                        self.modal.lineEdit_7.setStyleSheet(style1)
                        self.set_status(1)
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНекорректное значение серийного номера.')
                except:
                    self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nОшибка при работе с файлом конфигурации.')
                    self.set_status(1)
            else:
                self.get_text(35)
                try:
                    if self.modal.lineEdit_7.text().isdigit():
                        self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                        self.config.pd_in_pre = read_pdm1_35()
                        self.config.write_config_file(
                            self.config.new_config_dict(
                                B_PD_IN=self.config.pd_in_pre_calc(int(self.config.get_config_value('TAP_IN_IL')))))
                        self.set_status(1)
                        self.file_status('changed successfully',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                        self.set_status(2)
                        self.test_log()
                        auto_upload('AM_GAIN.txt')
                        auto_upload('_PHPHPH.txt')
                        zoc_min()
                        if -35.20 <= read_pdm1_35_2() <= -34.9:
                            self.set_status(2)
                            com = QtWidgets.QMessageBox()
                            com.setIcon(QtWidgets.QMessageBox.Information)
                            com.setFont(QFont('Arial', 10, 81))
                            com.setWindowTitle('Successful Correction')
                            com.setText('Характеристика входного фотодиода скорректирована удачно.')
                            com.setStyleSheet(style)
                            com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            res = com.exec_()
                            if res == QtWidgets.QMessageBox.Ok:
                                self.modal.plainTextEdit_2.setPlainText(
                                    'Комментарий:\n\nУстановите уровень входного сигнала равным -35 дБм. Нажмите "AM '
                                    'Power" для продолжения настройки.')
                                self.set_status(1)
                                self.modal.line_18.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_19.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_22.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_23.setStyleSheet('background-color: #ffaa00')
                                self.modal.line_16.setStyleSheet('background-color: #323232')
                                self.modal.line_17.setStyleSheet('background-color: #323232')
                                self.modal.line_21.setStyleSheet('background-color: #323232')
                                self.modal.line_20.setStyleSheet('background-color: #323232')
                        else:
                            self.set_status(2)
                            war = QtWidgets.QMessageBox()
                            war.setIcon(QtWidgets.QMessageBox.Warning)
                            war.setFont(QFont('Arial', 10, 81))
                            war.setWindowTitle('Warning')
                            war.setText('Характеристика входного фотодиода откалибрована неверно.')
                            war.setStyleSheet(style)
                            war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            res = war.exec_()
                            if res == QtWidgets.QMessageBox.Ok:
                                self.modal.plainTextEdit_2.setPlainText(
                                    'Комментарий:\n\nУровень входного сигнала не соответствует -35 дБм.')
                                self.set_status(1)
                    else:
                        self.modal.lineEdit_7.setStyleSheet(style1)
                        self.set_status(1)
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНекорректное значение серийного номера.')
                except:
                    self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nОшибка при работе с файлом конфигурации.')
                    self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def am_power_apc(self):
        self.modal.label_10.setVisible(False)
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            auto_upload('AM_Power.txt')
            auto_upload('APC_-2.txt')
            zoc_min()
            self.modal.lineEdit_11.setReadOnly(False)
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nВведите значение выходной мощности, полученное с экрана монитора. Для корректировки '
                'нажмите "Correct".')
            self.modal.pushButton_5.setVisible(False)
            self.modal.pushButton_13.setVisible(True)
            self.set_status(1)
            self.modal.lineEdit_11.setFocus()
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def correct_3(self):
        self.modal.lineEdit_11.setStyleSheet(style2)
        self.modal.lineEdit_7.setStyleSheet(style2)
        if self.modal.lineEdit_11.text()[1:].replace('.', '', 1).isdigit() and self.modal.lineEdit_11.text().startswith(
                '-'):
            if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                try:
                    if self.modal.lineEdit_7.text().isdigit():
                        self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                        self.config.pd_out_line = float(self.modal.lineEdit_11.text())
                        self.config.write_config_file(
                            self.config.new_config_dict(
                                B_PD_OUT=self.config.pd_out_line_calc(int(self.config.get_config_value('TAP_OUT_IL')))))
                        self.file_status('changed successfully',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНажмите "Check" для проверки '
                                                                'выходного уровня мощности оптического усилителя.')
                    else:
                        self.modal.lineEdit_7.setStyleSheet(style1)
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНекорректное значение серийного номера.')
                except:
                    self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nОшибка при работе с файлом конфигурации.')
            else:
                try:
                    if self.modal.lineEdit_7.text().isdigit():
                        self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                        self.config.pd_out_pre = float(self.modal.lineEdit_11.text())
                        self.config.write_config_file(
                            self.config.new_config_dict(
                                B_PD_OUT=self.config.pd_out_pre_calc(int(self.config.get_config_value('TAP_OUT_IL')))))
                        self.file_status('changed successfully',
                                         f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                        self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНажмите "Check" для проверки '
                                                                'выходного уровня мощности оптического усилителя.')
                    else:
                        self.modal.lineEdit_7.setStyleSheet(style1)
                        self.modal.plainTextEdit_2.setPlainText(
                            'Комментарий:\n\nНекорректное значение серийного номера.')
                except:
                    self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nОшибка при работе с файлом конфигурации.')
        else:
            self.modal.lineEdit_11.setStyleSheet(style1)
            self.modal.plainTextEdit_2.setPlainText('Комментарий:\n\nНекорректное значение мощности.')

    def check_3(self):
        self.modal.label_10.setVisible(False)
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            auto_upload('AM_Power.txt')
            auto_upload('APC_-2.txt')
            zoc_min()
            self.set_status(2)
            qst = QtWidgets.QMessageBox()
            qst.setIcon(QtWidgets.QMessageBox.Question)
            qst.setFont(QFont('Arial', 10, 81))
            qst.setWindowTitle('Power Check')
            qst.setText('Выходная мощность равна -2 дБм?')
            qst.setStyleSheet(style)
            qst.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            res = qst.exec_()
            if res == QtWidgets.QMessageBox.Yes:
                com = QtWidgets.QMessageBox()
                com.setIcon(QtWidgets.QMessageBox.Information)
                com.setFont(QFont('Arial', 10, 81))
                com.setWindowTitle('Setup Completed')
                com.setText('Настройка прошла успешно.')
                com.setStyleSheet(style)
                com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                res = com.exec_()
                if res == QtWidgets.QMessageBox.Ok:
                    self.clear()
                    self.set_status(1)
            else:
                self.modal.plainTextEdit_2.setPlainText(
                    'Комментарий:\n\nСкорректируйте значение выходной мощности и заново проведите настройку.')
                self.modal.lineEdit_11.setFocus()
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def get_text(self, mod):
        comment1 = 'Комментарий:\n\nПодключите выход аттенюатора IQS-3150 ко входу оптического усилителя, используя ' \
                   'оптическю розетку,' \
                   'а выход ОУ подайте на калибровочный измеритель мощности IQS-1700 (предварительно необходимо' \
                   ' произвести чистку оптических коннекторов). Подайте питание на плату. Установите входную мощность' \
                   f' равную -{mod} дБм. Введите серийный номер изделия. Для начала настройки нажмите кнопку "Start" ' \
                   f'выделенного блока пользовательского графического интерфейса.'

        self.modal.plainTextEdit_2.setPlainText(comment1)

    def set_status(self, status):
        if status == 1:
            self.modal.label_7.setText('Ready to work')
        elif status == 2:
            self.modal.label_7.setText('Not active')

    def default(self):
        self.modal.lineEdit_7.setStyleSheet(style2)
        if self.modal.lineEdit_7.text().isdigit():
            try:
                if self.modal.plainTextEdit_3.toPlainText() == 'K25-M19':
                    self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    self.config.write_config_file(
                        self.config.new_config_dict(TAP_IN_IL='71285303',
                                                    TAP_OUT_IL='121338885',
                                                    B_PD_IN='10729691',
                                                    B_PD_OUT='262413'))
                    self.file_status('changed successfully',
                                     f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.get_text(6)
                else:
                    self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    self.config.write_config_file(
                        self.config.new_config_dict(TAP_IN_IL='35727283',
                                                    TAP_OUT_IL='60813500',
                                                    B_PD_IN='10729691',
                                                    B_PD_OUT='262413'))
                    self.file_status('changed successfully',
                                     f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.get_text(10)
            except:
                self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
        else:
            self.modal.lineEdit_7.setStyleSheet(style1)
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nНекорректное значение серийного номера.')

    def clear(self):
        self.set_status(1)
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_7.clear()
        self.modal.lineEdit_7.setFocus()
        self.modal.lineEdit_8.clear()
        self.modal.lineEdit_9.clear()
        self.modal.lineEdit_10.clear()
        self.modal.lineEdit_11.clear()
        self.modal.lineEdit_9.setReadOnly(True)
        self.modal.lineEdit_10.setReadOnly(True)
        self.modal.lineEdit_11.setReadOnly(True)
        if myapp.ui.radioButton_6.isChecked():
            self.modal.plainTextEdit_3.setPlainText('K25-M19')
            self.get_text(6)
        else:
            self.modal.plainTextEdit_3.setPlainText('K25-M12')
            self.get_text(10)
        lines_list = [self.modal.line_10, self.modal.line_11, self.modal.line_12, self.modal.line_13,
                      self.modal.line_14, self.modal.line_15, self.modal.line_16, self.modal.line_17,
                      self.modal.line_18, self.modal.line_19, self.modal.line_20, self.modal.line_21,
                      self.modal.line_22, self.modal.line_23, self.modal.line_7, self.modal.line_9]
        for n in lines_list:
            n.setStyleSheet('background-color: #323232')
        self.modal.line_12.setStyleSheet('background-color: #ffaa00')
        self.modal.line_13.setStyleSheet('background-color: #ffaa00')
        self.modal.line_9.setStyleSheet('background-color: #ffaa00')
        self.modal.line_7.setStyleSheet('background-color: #ffaa00')
        self.modal.pushButton_8.setVisible(False)
        self.modal.pushButton_4.setVisible(False)
        self.modal.pushButton_13.setVisible(False)
        self.modal.pushButton_9.setVisible(True)
        self.modal.pushButton_3.setVisible(True)
        self.modal.pushButton_5.setVisible(True)

    def back_to_master(self):
        self.modal.label_10.setVisible(False)
        self.set_status(2)
        war = QtWidgets.QMessageBox()
        war.setIcon(QtWidgets.QMessageBox.Warning)
        war.setFont(QFont('Arial', 10, 81))
        war.setWindowTitle('Back to Master')
        war.setText('Уверены, что хотите вернуться на главное окно?')
        war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        war.setStyleSheet(style)
        res = war.exec_()
        if res == QtWidgets.QMessageBox.Yes:
            self.flag = 1
            self.close()
        self.set_status(1)

    def closeEvent(self, value):
        self.modal.label_10.setVisible(False)
        if self.flag == 1:
            self.close()
            myapp.setWindowState(Qt.WindowState.WindowNoState)
            myapp.set_status(1)
        else:
            self.set_status(2)
            war = QtWidgets.QMessageBox()
            war.setIcon(QtWidgets.QMessageBox.Warning)
            war.setFont(QFont('Arial', 10, 81))
            war.setWindowTitle('Back to Master')
            war.setText('Уверены, что хотите вернуться на главное окно?')
            war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            war.setStyleSheet(style)
            res = war.exec_()
            if res == QtWidgets.QMessageBox.Yes:
                myapp.setWindowState(Qt.WindowState.WindowNoState)
                myapp.set_status(1)
            elif res == QtWidgets.QMessageBox.No:
                value.ignore()
            self.flag = 0
            self.set_status(1)


class FourthWindow(QtWidgets.QWidget):
    def __init__(self, parent=MyWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.modal = Ui_Form_4()
        self.modal.setupUi(self)
        self.setWindowModality(2)
        self.flag = 0
        if myapp.ui.radioButton_6.isChecked():
            self.modal.plainTextEdit_3.setPlainText('K25-M19')
        else:
            self.modal.plainTextEdit_3.setPlainText('K25-M12')
        self.modal.plainTextEdit_2.setPlaceholderText('Комментарий:\n\nВведите серийный номер изделия. Нажмите '
                                                      '"Configure" для начала конфигурирования.\n\nВнимание: Дата '
                                                      'изготовления изделия автоматически сохраняется '
                                                      'текущая. Вы можете вручную изменить или получить любой '
                                                      'параметр файла конфигурации.')
        self.modal.pushButton_2.setToolTip('Back to Master')
        self.modal.pushButton_5.setToolTip('Check AMP Status')
        self.modal.pushButton_4.setToolTip('Start Configuration')
        self.modal.pushButton_3.setToolTip('Upload Defaults')
        self.modal.pushButton_6.setToolTip('Get Config Value')
        self.modal.pushButton_7.setToolTip('Change Config Value')
        self.modal.pushButton_8.setToolTip('Clear All')
        self.modal.label_6.setToolTip('Date')
        self.modal.label_7.setToolTip('Window Status')
        self.modal.pushButton_8.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_2.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_5.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_4.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_3.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_6.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.pushButton_7.setStyleSheet(
            style[:-50] + "QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_6.setStyleSheet("QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}")
        self.modal.label_7.setStyleSheet(
            'QToolTip {color: #b1b1b1; background-color: #323232; border: #1e1e1e}' + "QWidget{color: #b1b1b1; "
                                                                                      "background-color: #242424; "
                                                                                      "border:#242424}")
        self.modal.plainTextEdit_3.setFont(QFont('Arial', 24, 81))
        self.modal.label_6.setFont(QFont('Arial', 10, 57))
        self.modal.label_7.setFont(QFont('Arial', 8, 71))
        self.modal.label_6.setText(QDate.currentDate().toString('dd/MM/yyyy'))
        self.modal.label_7.setText('Ready to work')
        self.modal.label_10.setToolTip('Config File Status')
        self.modal.label_10.setFont(QFont('Arial', 8, 57))
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_7.setFocus()
        self.modal.pushButton_2.clicked.connect(self.back_to_master)
        self.modal.pushButton_4.clicked.connect(self.config_dt)
        self.modal.pushButton_3.clicked.connect(self.set_defaults)
        self.modal.pushButton_5.clicked.connect(self.check_defaults)
        self.modal.pushButton_6.clicked.connect(self.get_value)
        self.modal.pushButton_7.clicked.connect(self.change_value)
        self.modal.pushButton_8.clicked.connect(self.clear)
        self.config = None

    def change(self, t):
        if t == 'DT':
            self.config.write_config_file(self.config.new_config_dict(DT=self.modal.lineEdit_9.text()))
        elif t == 'NF':
            self.config.write_config_file(self.config.new_config_dict(NF=self.modal.lineEdit_9.text()))

    def change_value(self):
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_7.setStyleSheet(style2)
        try:
            if self.modal.lineEdit_7.text().isdigit():
                if myapp.ui.radioButton_6.isChecked():
                    self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    text = str(self.modal.comboBox_2.currentText())
                    self.change(text)
                    self.modal.plainTextEdit_2.setPlainText(
                        f'Комментарий:\n\nЗнчение параметра {self.modal.comboBox_2.currentText()} успешно изменено.')
                    self.file_status('changed successfully',
                                     f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                else:
                    self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    text = str(self.modal.comboBox_2.currentText())
                    self.change(text)
                    self.modal.plainTextEdit_2.setPlainText(
                        f'Комментарий:\n\nЗнчение параметра {self.modal.comboBox_2.currentText()} успешно изменено.')
                    self.file_status('changed successfully',
                                     f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
            else:
                self.modal.lineEdit_7.setStyleSheet(style1)
                self.modal.plainTextEdit_2.setPlainText(
                    'Комментарий:\n\nНекорректное значение серийного номера.')
        except:
            self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nОшибка при работе с файлом конфигурации.')

    def get_value(self):
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_7.setStyleSheet(style2)
        try:
            if self.modal.lineEdit_7.text().isdigit():
                if myapp.ui.radioButton_6.isChecked():
                    self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    text = str(self.modal.comboBox.currentText())
                    self.modal.lineEdit_8.setText(str(self.config.get_config_value(text)))
                    self.modal.plainTextEdit_2.setPlainText(
                        f'Комментарий:\n\nЗнчение параметра {self.modal.comboBox.currentText()} успешно получено.')
                else:
                    self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    text = str(self.modal.comboBox.currentText())
                    self.modal.lineEdit_8.setText(str(self.config.get_config_value(text)))
                    self.modal.plainTextEdit_2.setPlainText(
                        f'Комментарий:\n\nЗнчение параметра {self.modal.comboBox.currentText()} успешно получено.')
            else:
                self.modal.lineEdit_7.setStyleSheet(style1)
                self.modal.plainTextEdit_2.setPlainText(
                    'Комментарий:\n\nНекорректное значение серийного номера.')
        except:
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nОшибка при работе с файлом конфигурации.')

    def check_defaults(self):
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_log()
            auto_upload('__AMP status.txt')
            auto_upload('_PHPHPH.txt')
            zoc_min()
            if amp_status():
                com = QtWidgets.QMessageBox()
                com.setIcon(QtWidgets.QMessageBox.Information)
                com.setFont(QFont('Arial', 10, 81))
                com.setWindowTitle('Successful Check')
                com.setText('Проверка прошла успешно.')
                com.setStyleSheet(style)
                com.setStandardButtons(QtWidgets.QMessageBox.Ok)
                res = com.exec_()
                if res == QtWidgets.QMessageBox.Ok:
                    self.modal.plainTextEdit_2.clear()
                self.set_status(1)
            else:
                war = QtWidgets.QMessageBox()
                war.setIcon(QtWidgets.QMessageBox.Warning)
                war.setFont(QFont('Arial', 10, 81))
                war.setWindowTitle('Warning')
                war.setText('Неверные дата или значения "Defaults".')
                war.setStyleSheet(style)
                war.setStandardButtons(QtWidgets.QMessageBox.Ok)
                res = war.exec_()
                if res == QtWidgets.QMessageBox.Ok:
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nПроверьте значения "Defaults" или дату изготовления изделия. При '
                        'необходимости измените значения вручную.')
                    self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def set_defaults(self):
        self.modal.label_10.setVisible(False)
        if check_process('zoc') is not None:
            self.set_status(2)
            auto_upload('DEFAULTS.txt')
            zoc_min()
            com = QtWidgets.QMessageBox()
            com.setIcon(QtWidgets.QMessageBox.Information)
            com.setFont(QFont('Arial', 10, 81))
            com.setWindowTitle('Power Supply Reset')
            com.setText('Необходимо перезагрузить источник питания.')
            com.setStyleSheet(style)
            com.setStandardButtons(QtWidgets.QMessageBox.Ok)
            res = com.exec_()
            if res == QtWidgets.QMessageBox.Ok:
                self.modal.plainTextEdit_2.setPlainText(
                    'Комментарий:\n\nНажмите "Check" для проверки данных файла конфигурации.')
            self.set_status(1)
        elif check_process('zoc') is None:
            self.set_status(2)
            myapp.zoc_error()
            self.set_status(1)

    def config_dt(self):
        self.modal.lineEdit_7.setStyleSheet(style2)
        try:
            if self.modal.lineEdit_7.text().isdigit():
                if myapp.ui.radioButton_6.isChecked():
                    self.config = LineAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    self.config.write_config_file(
                        self.config.new_config_dict(
                            DT=f'{date.today().day}.{f"{date.today().month:02d}"}.{str(date.today().year)[2:]}'))
                    self.file_status('changed successfully',
                                     f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nНажмите "Defaults" для продолжения настройки.')
                else:
                    self.config = PreAmplifierConfig(int(self.modal.lineEdit_7.text()))
                    self.config.write_config_file(
                        self.config.new_config_dict(
                            DT=f'{date.today().day}.{f"{date.today().month:02d}"}.{str(date.today().year)[2:]}'))
                    self.file_status('changed successfully',
                                     f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
                    self.modal.plainTextEdit_2.setPlainText(
                        'Комментарий:\n\nНажмите "Defaults" для продолжения настройки.')
            else:
                self.modal.lineEdit_7.setStyleSheet(style1)
                self.modal.plainTextEdit_2.setPlainText(
                    'Комментарий:\n\nНекорректное значение серийного номера.')
        except:
            self.file_status('NOT changed', f'File __Config_Write_{int(self.modal.lineEdit_7.text())}.txt')
            self.modal.plainTextEdit_2.setPlainText(
                'Комментарий:\n\nОшибка при работе с файлом конфигурации.')

    def file_status(self, txt, file):
        self.modal.label_10.setVisible(True)
        self.modal.label_10.setText(f'{file} {txt}')

    def set_status(self, status):
        if status == 1:
            self.modal.label_7.setText('Ready to work')
        elif status == 2:
            self.modal.label_7.setText('Not active')

    def clear(self):
        self.modal.plainTextEdit_2.clear()
        self.modal.label_10.setVisible(False)
        self.modal.lineEdit_7.setFocus()
        self.modal.lineEdit_7.clear()
        self.modal.lineEdit_8.clear()
        self.modal.lineEdit_9.clear()
        self.set_status(1)

    def back_to_master(self):
        self.modal.label_10.setVisible(False)
        self.set_status(2)
        war = QtWidgets.QMessageBox()
        war.setIcon(QtWidgets.QMessageBox.Warning)
        war.setFont(QFont('Arial', 10, 81))
        war.setWindowTitle('Back to Master')
        war.setText('Уверены, что хотите вернуться на главное окно?')
        war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        war.setStyleSheet(style)
        res = war.exec_()
        if res == QtWidgets.QMessageBox.Yes:
            self.flag = 1
            self.close()
        self.set_status(1)

    def closeEvent(self, value):
        self.modal.label_10.setVisible(False)
        if self.flag == 1:
            self.close()
            myapp.setWindowState(Qt.WindowState.WindowNoState)
            myapp.set_status(1)
        else:
            self.set_status(2)
            war = QtWidgets.QMessageBox()
            war.setIcon(QtWidgets.QMessageBox.Warning)
            war.setFont(QFont('Arial', 10, 81))
            war.setWindowTitle('Back to Master')
            war.setText('Уверены, что хотите вернуться на главное окно?')
            war.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            war.setStyleSheet(style)
            res = war.exec_()
            if res == QtWidgets.QMessageBox.Yes:
                myapp.setWindowState(Qt.WindowState.WindowNoState)
                myapp.set_status(1)
            elif res == QtWidgets.QMessageBox.No:
                value.ignore()
            self.flag = 0
            self.set_status(1)


logging_file = 'logfile1.txt'  # из главного экрана взять потом


def read_logfile():
    """Функция считывает содержимое
                логфайла в список"""
    log_list = []
    with open(fr'C:\Users\danil\OneDrive\Документы\ZOC7 Files\Log\логфайл\{logging_file}') as logFile:
        for row in logFile:
            log_list.append(row.split(' '))
        return log_list


def read_temp():
    """Функция считывает температуру лазера,
        True - температура впорядке, False - средняя температура ниже/выше
            нормы или имеется скачок температуры"""
    temp_list = []
    for sublist in read_logfile():
        if 'LASER1:' in sublist and 'C\n' in sublist:
            temp_list.append(sublist[1])
    if 24.8 <= sum(map(lambda x: float(x), temp_list)) / len(temp_list) <= 25.2 and len(
            list(filter(lambda x: 24.7 <= x <= 25.3, map(lambda x: float(x), temp_list)))) == len(temp_list):
        return True
    else:
        return False


def read_i_op():
    """Функция считывает рабочий ток лазера,
        True - впорядке, False - ток ниже/выше
            нормы или имеется скачок тока"""
    iop_list, acc = [], 0
    for sublist in read_logfile():
        if 'ACC' in sublist:
            acc = float(sublist[2])
        if 'LASER1:' in sublist and 'mA\n' in sublist:
            iop_list.append(sublist[1])
    if acc - 3 <= sum(map(lambda x: float(x), iop_list)) / len(iop_list) <= acc + 3 and len(
            list(filter(lambda x: acc - 3 <= x <= acc + 3, map(lambda x: float(x), iop_list)))) == len(iop_list):
        return True
    else:
        return False


def read_i_eol():
    """Функция считывает EOL ток лазера,
        True - впорядке, False - ток ниже/выше
            нормы или имеется скачок тока"""
    i_eol_list, acc = [], 0
    for sublist in read_logfile():
        if 'ACC' in sublist:
            acc = float(sublist[2])
        if 'LASER1:' in sublist and 'mA\n' in sublist:
            i_eol_list.append(sublist[1])
    if acc - 10 <= sum(map(lambda x: float(x), i_eol_list)) / len(i_eol_list) <= acc and len(
            list(filter(lambda x: acc - 10 <= x <= acc + 5, map(lambda x: float(x), i_eol_list)))) == len(i_eol_list):
        return True
    else:
        return False


def read_pdm1():
    """Функция возвращает вх ФД для калибровки"""
    pdm = -50
    for sublist in read_logfile():
        if 'PDM1:' in sublist and 'dBm\n' in sublist:
            pdm = float(sublist[1])
    return round(pdm, 2)


def read_pdm1_2():
    """Функция возвращает кортеж откалиброванный вх ФД для проверки и ток"""
    i_list, pdm_list, pdm, i = [], [], -50, 0
    for sublist in read_logfile():
        if 'PDM1:' in sublist and 'dBm\n' in sublist:
            pdm_list.append(sublist[1])
        elif 'LASER1:' in sublist and 'mA\n' in sublist:
            i_list.append(sublist[1])
    pdm = sum(map(lambda x: float(x), pdm_list)) / len(pdm_list)
    i = sum(map(lambda x: float(x), i_list)) / len(i_list)
    return round(pdm, 2), round(i, 2)


def amc_pdm2():
    """Функция возвращает вых ФД при токе рабочем/макс"""
    pdm2 = -50
    for sublist in read_logfile():
        if 'PDM2:' in sublist and 'dBm\n' in sublist:
            pdm2 = float(sublist[1])
    return round(pdm2, 2)


def read_pdm1_35():
    """Функция возвращает мин. значение при калибр вх -35"""
    pdm_list = []
    for sublist in read_logfile():
        if 'PDM1:' in sublist and 'dBm\n' in sublist:
            pdm_list.append(sublist[1])
    return min(map(lambda x: float(x), pdm_list))


def read_pdm1_35_2():
    """Функция возвращает откалибр. ФД вх -35 для проверки"""
    pdm_list, pdm = [], -50
    for sublist in read_logfile():
        if 'PDM1:' in sublist and 'dBm\n' in sublist:
            pdm_list.append(sublist[1])
    pdm = sum(map(lambda x: float(x), pdm_list)) / len(pdm_list)
    return round(pdm, 2)


def amp_status():
    """Функция проверки даты и режима работы и отсутствия сигнала,
    True - все впорядке, False - что-то не сходится"""
    am, date_amp, pdm_list1, pdm_list2 = None, None, [], []
    for sublist in read_logfile():
        if 'AM:' in sublist:
            am = sublist[1].strip()
        elif 'Date:' in sublist:
            date_amp = sublist[1].strip()
        elif 'PDM1:' in sublist and 'dBm\n' in sublist:
            pdm_list1.append(sublist[1])
        elif 'PDM2:' in sublist and 'dBm\n' in sublist:
            pdm_list2.append(sublist[1])
    if am == 'G' and date_amp == f'{date.today().day}.{f"{date.today().month:02d}"}.{str(date.today().year)[2:]}' and -50 <= sum(
            map(lambda x: float(x), pdm_list1)) / len(pdm_list1) <= -47 and -50 <= sum(
        map(lambda x: float(x), pdm_list2)) / len(pdm_list2) <= -47:
        return True
    else:
        return False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('pictures/iconmax.png'))
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
