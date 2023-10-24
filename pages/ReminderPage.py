from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from tablemodels.NamedDateTableModel import (
    NamedDateTableModel,
    DateEditDelegate,
    LineEditDelegate,
)
from widgets.elements import (
    InputWrapper,
    CustomWindow,
    NamedHObjectLayout
)
from api import (
    LeaseContractApi,
    NotificationsApi,
)
from settings import email_subjects
from widgets.dialogs import Dialog
from tools import get_utc_offset
import datetime

tr = QtCore.QCoreApplication.translate

class ReminderPage(CustomWindow):
    def __init__(self, id: int = None):
        super().__init__()

        self.setWindowTitle(tr('ReminderPage - Title', 'Reminder'))

        self.__id = id
        self._lease_contract = None
        self._named_dates = []

        self.__init_UI()

        if self.__id is not None:
            self.__load_reminder()

    def __init_UI(self):
        date = datetime.datetime.now()

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setObjectName('Window')
        scroll_widget.setLayout(layout)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        scroll_layout = QtWidgets.QVBoxLayout()
        scroll_layout.addWidget(scroll)
        self.widget.setLayout(scroll_layout)
        
        reminder_information_layout = QtWidgets.QGridLayout()
        reminder_information_layout.setSpacing(20)
        reminder_information_frame = QtWidgets.QFrame()
        reminder_information_frame.setLayout(reminder_information_layout)

        self.rental_label = QtWidgets.QLabel(font=QtGui.QFont('Open Sans', 16, 400))
        self.rental_label.setHidden(True)

        self.creation_date = QtWidgets.QDateEdit(displayFormat='dd/MM/yyyy')
        self.creation_date.setObjectName('Input')
        self.creation_date.setDate(QtCore.QDate(date.year, date.month, date.day))
        self.creation_date.setDisabled(True)

        self.email_subject = QtWidgets.QComboBox()
        self.email_subject.setObjectName('Input')
        self.email_subject.addItems(email_subjects)

        self.reminder_text = QtWidgets.QLineEdit()
        self.reminder_text.setObjectName('Input')

        self.notify_owner = QtWidgets.QCheckBox()
        self.notify_owner.setText(tr('ReminderPage - Notify owner', 'Notify owner'))
        self.notify_owner.setObjectName('Checkbox')

        reminder_information_layout.addWidget(self.rental_label, 0, 0, 1, 4)
        reminder_information_layout.addWidget(self.notify_owner, 1, 0)
        reminder_information_layout.addWidget(InputWrapper(tr('ReminderPage - Email subject', 'Email subject'), self.email_subject), 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_information_layout.addWidget(InputWrapper(tr('ReminderPage - Text', 'Text'), self.reminder_text), 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_information_layout.addWidget(InputWrapper(tr('ReminderPage - Creation date', 'Creation date'), self.creation_date), 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        reminder_named_dates_layout = QtWidgets.QGridLayout()
        reminder_named_dates_layout.setSpacing(20)
        reminder_named_dates_frame = QtWidgets.QFrame()
        reminder_named_dates_frame.setObjectName('Frame')
        reminder_named_dates_frame.setLayout(reminder_named_dates_layout)

        label = QtWidgets.QLabel(tr('ReminderPage - Information dates label', 'Dates'), font=QtGui.QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.named_dates_table_model = NamedDateTableModel([])
        
        self.named_dates_table_view = QtWidgets.QTableView()
        self.named_dates_table_view.doubleClicked.connect(self._delete_named_date)
        self.named_dates_table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.named_dates_table_view.setObjectName('Table')
        self.named_dates_table_view.setModel(self.named_dates_table_model)
        self.named_dates_table_view.setItemDelegate(LineEditDelegate())
        self.named_dates_table_view.setItemDelegateForColumn(2, DateEditDelegate())

        self.named_dates_date = QtWidgets.QDateTimeEdit(displayFormat='dd/MM/yyyy hh:mm')
        self.named_dates_date.setDate(QtCore.QDate(date.year, date.month, date.day))
        self.named_dates_date.setObjectName('Input')
        self.named_dates_name = QtWidgets.QLineEdit()
        self.named_dates_name.setObjectName('Input')

        self.named_dates_button_add = QtWidgets.QPushButton(icon=QtGui.QIcon('data/plus-circle.svg'))
        self.named_dates_button_add.clicked.connect(self._add_named_date)
        self.named_dates_button_add.setObjectName('IconButton')
        self.named_dates_button_add.setFixedSize(24, 24)
        self.named_dates_button_add.setObjectName('IconButton')
        self.named_dates_button_add.setIconSize(QtCore.QSize(24, 24))

        reminder_named_dates_layout.addWidget(label, 0, 0, 1, 4, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_named_dates_layout.addWidget(self.named_dates_button_add, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        reminder_named_dates_layout.addWidget(InputWrapper(tr('ReminderPage - Name', 'Name'), self.named_dates_name), 1, 1, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_named_dates_layout.addWidget(InputWrapper(tr('ReminderPage - Date', 'Date'), self.named_dates_date), 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_named_dates_layout.addWidget(self.named_dates_table_view, 2, 0, 1, 4)

        reminder_lease_contract_layout = QtWidgets.QGridLayout()
        reminder_lease_contract_layout.setContentsMargins(10, 10, 10, 10)
        reminder_lease_contract_layout.setSpacing(20)
        reminder_lease_contract_frame = QtWidgets.QFrame()
        reminder_lease_contract_frame.setObjectName('Frame')
        reminder_lease_contract_frame.setLayout(reminder_lease_contract_layout)

        label = QtWidgets.QLabel(tr('ReminderPage - Information lease contract label', 'Lease Contract'), font=QtGui.QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.lease_contract_search_widget = QtWidgets.QLineEdit()
        self.lease_contract_search_widget.setObjectName('Input')
        self.lease_contract_search_widget.textChanged.connect(self._lease_contract_search)

        self.lease_contract_search_layout = QtWidgets.QVBoxLayout()
        self.lease_contract_search_layout.setContentsMargins(0, 0, 0, 0)
        self.lease_contract_search_layout.setSpacing(10)
        self.lease_contract_search_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setObjectName('Wrapper')
        scroll_widget.setLayout(self.lease_contract_search_layout)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(150)

        reminder_lease_contract_layout.addWidget(label, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_lease_contract_layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.lease_contract_search_widget), 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_lease_contract_layout.addWidget(scroll, 2, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        button_save = QtWidgets.QPushButton(tr('Buttons - Save', 'Save'))
        button_save.setObjectName('DialogButton')
        button_save.clicked.connect(self.save)

        button_cancel = QtWidgets.QPushButton(tr('Buttons - Cancel', 'Cancel'))
        button_cancel.setObjectName('DialogButton')
        button_cancel.clicked.connect(self.cancel)

        button_back = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-left.svg'))
        button_back.setObjectName('IconButton')
        button_back.setIconSize(QtCore.QSize(24, 24))
        button_back.clicked.connect(self.cancel)

        layout.addWidget(reminder_information_frame, 1, 0, 1, 9)
        layout.addWidget(reminder_named_dates_frame, 2, 0, 1, 9)
        layout.addWidget(reminder_lease_contract_frame, 3, 0, 1, 9)

        layout.addWidget(button_back, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_save, 4, 0, 1, 2)
        layout.addWidget(button_cancel, 4, 2, 1, 2)

    def _add_named_date(self):
        date = self.named_dates_date.dateTime().toString('yyyy-MM-ddThh:mm:00') + get_utc_offset()
        name = self.named_dates_name.text()

        self.named_dates_name.setText('')

        self._named_dates.append({'name': name, 'date': date})

        self.named_dates_table_model = NamedDateTableModel(self._named_dates)
        self.named_dates_table_view.setModel(self.named_dates_table_model)
    
    def _delete_named_date(self, index: QtCore.QModelIndex):
        if index.column() == 0:
            self._named_dates.pop(index.row())
            
            self.named_dates_table_model = NamedDateTableModel(self._named_dates)
            self.named_dates_table_view.setModel(self.named_dates_table_model)

    def _lease_contract_search(self, search):
        lease_contracts = []
        if search != '':
            success, data = LeaseContractApi.lease_contract_list(search, None)
            if success:
                lease_contracts.extend(data['results'])
                while True:
                    if data['next'] is not None:
                        success, data = LeaseContractApi.rentals_list(None, data['next'])
                        if success:
                            lease_contracts.extend(data['results'])
                    else:
                        break
        
        for i in range(self.lease_contract_search_layout.count()):
            item = self.lease_contract_search_layout.takeAt(0)
            item.widget().deleteLater()

        if self._lease_contract is not None:
            self._add_lease_contract(self._lease_contract, False)

        for lease_contract in lease_contracts:
            frame = QtWidgets.QWidget()
            frame.setObjectName('Frame')
            button = QtWidgets.QPushButton(icon=QtGui.QIcon('data/plus-circle.svg'))
            button.setFixedSize(24, 24)
            button.setObjectName('IconButton')
            button.setIconSize(QtCore.QSize(24, 24))
            button.clicked.connect(lambda _=False, lease_contract=lease_contract: self._add_lease_contract(lease_contract, True))
            layout = NamedHObjectLayout(f'{lease_contract["start_date"]} {lease_contract["end_date"]} {lease_contract["tenant"]["first_name"]} {lease_contract["tenant"]["last_name"]} {lease_contract["apartment"]["name"]} {lease_contract["apartment"]["unique_identifier"]}', button, direction='left', text_align='right', font=QtGui.QFont('Open Sans', 16, 400))
            frame.setLayout(layout)

            self.lease_contract_search_layout.addWidget(frame)

    def _add_lease_contract(self, lease_contract, clear: bool, can_delete: bool = True):
        self._lease_contract = lease_contract

        if clear:
            for i in range(self.lease_contract_search_layout.count()):
                item = self.lease_contract_search_layout.takeAt(0)
                item.widget().deleteLater()

        frame = QtWidgets.QWidget()
        frame.setObjectName('Frame')
        button = QtWidgets.QPushButton(icon=QtGui.QIcon('data/minus-circle.svg'))
        button.setFixedSize(24, 24)
        button.setObjectName('IconButton')
        button.setIconSize(QtCore.QSize(24, 24))
        button.clicked.connect(lambda _=False: self._remove_lease_contract())
        if not can_delete:
            button.setDisabled(True)
            self.lease_contract_search_widget.setDisabled(True)
        layout = NamedHObjectLayout(f'{lease_contract["start_date"]} {lease_contract["end_date"]} {lease_contract["tenant"]["first_name"]} {lease_contract["tenant"]["last_name"]} {lease_contract["apartment"]["name"]} {lease_contract["apartment"]["unique_identifier"]}', button, direction='left', text_align='right', font=QtGui.QFont('Open Sans', 16, 400))
        frame.setLayout(layout)

        self.lease_contract_search_layout.addWidget(frame)

    def _remove_lease_contract(self):
        self._lease_contract = None

        for i in range(self.lease_contract_search_layout.count()):
            item = self.lease_contract_search_layout.takeAt(0)
            item.widget().deleteLater()

    def save(self):
        data = {
            'id': self.__id,
            'date': self.creation_date.date().toString('yyyy-MM-dd'),
            'notify_owner': True if self.notify_owner.isChecked() else False,
            'text': self.reminder_text.text(),
            'email_subject': self.email_subject.currentText(),
            'lease_contract': self._lease_contract,
            'dates': self._named_dates,
        }

        if self.__id is None:
            success, _ = NotificationsApi.create_reminder(data)
            if not success:
                dialog = Dialog(tr('Dialog - Error title', 'Save error'),
                                tr('Dialog - Error text', 'An error occurred while saving data!'),
                                'error') 
                if dialog.is_accepted:
                    self.close()
                return

        else:
            success, reminder = NotificationsApi.update_reminder(data)
            if not success:
                dialog = Dialog(tr('Dialog - Error title', 'Update error'),
                                tr('Dialog - Error text', 'An error occurred while updating data!'),
                                'error') 
                if dialog.is_accepted:
                    self.close()
                return

        self.close()

    def cancel(self):
        self.Signal.emit({'window': 'back'})

    def __load_reminder(self):
        success, reminder = NotificationsApi.get_reminder(self.__id)
        if success:
            creation_date = datetime.date.fromisoformat(reminder['date'])
            self.creation_date.setDate(QtCore.QDate(creation_date.year, creation_date.month, creation_date.day))
            self.reminder_text.setText(reminder['text'])
            self.email_subject.setCurrentIndex(email_subjects.index(reminder['email_subject']))

            self._add_lease_contract(reminder['lease_contract'], False, False)

            self._named_dates = reminder['dates']
            self.named_dates_table_model = NamedDateTableModel(self._named_dates)
            self.named_dates_table_view.setModel(self.named_dates_table_model)

        else:
            Dialog(tr('Dialog - Error title', 'Load error'),
                   tr('Dialog - Error text', 'An error occurred while load data!'),
                   'error')