from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
tr = QtCore.QCoreApplication.translate

from pages import (
    TenantPage,
    TenantListPage,
    UtilityBillsPaymentsPage,
    RentPaymentsPage,
    ReminderPage,
    ReminderListPage,
    TaskPage,
    TaskListPage,
    ApartmentPage,
    OwnerPage,
    LeaseContractPage
)

import widgets.dialogs as dialogs
from models import create_tables

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        create_tables()
        super().__init__()

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.windows_queue = []

        self.set_window('apartment')

        self.show()


    def _signal_handler(self, params):
        window_name = params.pop('window', None)
        if window_name is not None:
            self.set_window(window_name, **params)

    def set_window(self, window_name: str, **kwargs):
        if window_name != 'back':
            self.windows_queue.append((self.takeCentralWidget(), self.minimumSize()))

        match window_name:
            case 'rent_paymets': # This is a separate window and we must show it separately
                window = RentPaymentsPage()
                window.setMinimumSize(600, 400)
                return

            case 'utility_bills_payments': # This is a separate window and we must show it separately
                window = UtilityBillsPaymentsPage()
                window.setMinimumSize(600, 400)
                return

            case 'reminder':
                self.setCentralWidget(ReminderPage(**kwargs))
                self.setMinimumSize(900, 800)
            
            case 'reminder_list':
                self.setCentralWidget(ReminderListPage(**kwargs))
                self.setMinimumSize(600, 400)

            case 'task':
                self.setCentralWidget(TaskPage(**kwargs))
                self.setMinimumSize(900, 800)

            case 'task_list':
                self.setCentralWidget(TaskListPage(**kwargs))
                self.setMinimumSize(600, 400)

            case 'tenant':
                self.setCentralWidget(TenantPage(**kwargs))
                self.setMinimumSize(900, 800)

            case 'tenant_list':
                self.setCentralWidget(TenantListPage(**kwargs))
                self.setMinimumSize(900, 800)

            case 'owner':
                self.setCentralWidget(OwnerPage(**kwargs))
                self.setMinimumSize(900, 800)

            case 'apartment':
                self.setCentralWidget(ApartmentPage(**kwargs))
                self.setMinimumSize(900, 800)

            case 'lease_contract':
                self.setCentralWidget(LeaseContractPage(**kwargs))
                self.setMinimumSize(900, 800)

            case 'back':
                window, min_size = self.windows_queue.pop(-1)
                window.SignalUpdate.emit()
                self.setCentralWidget(window)
                self.setMinimumSize(min_size)
                return

        self.centralWidget().connect_control_signals(self)


def addFont(file_name):
    with open(file_name, 'rb') as file:
        font = file.read()
        QtGui.QFontDatabase.addApplicationFontFromData(font)

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    addFont('data/Open_Sans/OpenSans-ExtraBold.ttf')
    addFont('data/Open_Sans/OpenSans-Bold.ttf')
    addFont('data/Open_Sans/OpenSans-SemiBold.ttf')
    addFont('data/Open_Sans/OpenSans-Medium.ttf')
    addFont('data/Open_Sans/OpenSans-Regular.ttf')
    addFont('data/Open_Sans/OpenSans-Light.ttf')

    styles = open("data/styles.qss", 'r').read()
    app.setStyleSheet(styles)
    app.setStyle('Fusion')

    window = MainWindow()
    app.exec()

