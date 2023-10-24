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
import uuid

tr = QtCore.QCoreApplication.translate

class TaskPage(CustomWindow):
    def __init__(self, id: int = None):
        super().__init__()

        self.setWindowTitle(tr('TaskPage - Title', 'Task'))

        self.__id = id
        self._lease_contract = None
        self._dates = []
        self._actions = {}
        self._cell_actions = []

        self.__init_UI()

        if self.__id is not None:
            self.__load_task()

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
        
        task_information_layout = QtWidgets.QGridLayout()
        task_information_layout.setSpacing(20)
        task_information_frame = QtWidgets.QFrame()
        task_information_frame.setLayout(task_information_layout)

        self.rental_label = QtWidgets.QLabel(font=QtGui.QFont('Open Sans', 16, 400))
        self.rental_label.setHidden(True)

        self.creation_date = QtWidgets.QDateEdit(displayFormat='dd/MM/yyyy')
        self.creation_date.setObjectName('Input')
        self.creation_date.setDate(QtCore.QDate(date.year, date.month, date.day))
        self.creation_date.setDisabled(True)

        self.email_subject = QtWidgets.QComboBox()
        self.email_subject.setObjectName('Input')
        self.email_subject.addItems(email_subjects)

        self.task_text = QtWidgets.QLineEdit()
        self.task_text.setObjectName('Input')

        self.task_note = QtWidgets.QTextEdit()
        self.task_note.setObjectName('Input')

        self.notify_owner = QtWidgets.QCheckBox()
        self.notify_owner.setText(tr('TaskPage - Notify owner', 'Notify owner'))
        self.notify_owner.setObjectName('Checkbox')

        task_information_layout.addWidget(self.rental_label, 0, 0, 1, 4)
        task_information_layout.addWidget(self.notify_owner, 1, 0)
        task_information_layout.addWidget(InputWrapper(tr('TaskPage - Email subject', 'Email subject'), self.email_subject), 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        task_information_layout.addWidget(InputWrapper(tr('TaskPage - Text', 'Text'), self.task_text), 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        task_information_layout.addWidget(InputWrapper(tr('TaskPage - Creation date', 'Creation date'), self.creation_date), 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        task_information_layout.addWidget(InputWrapper(tr('TaskPage - Note', 'Note'), self.task_note), 2, 0, 1, 4)

        task_dates_layout = QtWidgets.QGridLayout()
        task_dates_layout.setSpacing(20)
        task_dates_frame = QtWidgets.QFrame()
        task_dates_frame.setObjectName('Frame')
        task_dates_frame.setLayout(task_dates_layout)

        label = QtWidgets.QLabel(tr('TaskPage - Information dates label', 'Dates'), font=QtGui.QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.dates_table_model = NamedDateTableModel([])
        
        self.dates_table_view = QtWidgets.QTableView()
        self.dates_table_view.doubleClicked.connect(self._delete_named_date)
        self.dates_table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.dates_table_view.setObjectName('Table')
        self.dates_table_view.setModel(self.dates_table_model)
        self.dates_table_view.setItemDelegate(LineEditDelegate())
        self.dates_table_view.setItemDelegateForColumn(2, DateEditDelegate())
        self.dates_table_view.setMinimumHeight(150)

        self.dates_date = QtWidgets.QDateTimeEdit(displayFormat='dd/MM/yyyy hh:mm')
        self.dates_date.setDate(QtCore.QDate(date.year, date.month, date.day))
        self.dates_date.setObjectName('Input')
        self.dates_name = QtWidgets.QLineEdit()
        self.dates_name.setObjectName('Input')

        self.dates_button_add = QtWidgets.QPushButton(icon=QtGui.QIcon('data/plus-circle.svg'))
        self.dates_button_add.clicked.connect(self._add_named_date)
        self.dates_button_add.setObjectName('IconButton')
        self.dates_button_add.setFixedSize(24, 24)
        self.dates_button_add.setObjectName('IconButton')
        self.dates_button_add.setIconSize(QtCore.QSize(24, 24))

        task_dates_layout.addWidget(label, 0, 0, 1, 4, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        task_dates_layout.addWidget(self.dates_button_add, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        task_dates_layout.addWidget(InputWrapper(tr('TaskPage - Name', 'Name'), self.dates_name), 1, 1, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        task_dates_layout.addWidget(InputWrapper(tr('TaskPage - Date', 'Date'), self.dates_date), 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        task_dates_layout.addWidget(self.dates_table_view, 2, 0, 1, 4)
        
        task_actions_layout = QtWidgets.QGridLayout()
        task_actions_layout.setSpacing(20)
        task_actions_frame = QtWidgets.QFrame()
        task_actions_frame.setObjectName('Frame')
        task_actions_frame.setLayout(task_actions_layout)

        label = QtWidgets.QLabel(tr('TaskPage - Information actions label', 'Actions'), font=QtGui.QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.actions_action = QtWidgets.QLineEdit()
        self.actions_action.setObjectName('Input')

        self.actions_button_add = QtWidgets.QPushButton(icon=QtGui.QIcon('data/plus-circle.svg'))
        self.actions_button_add.clicked.connect(lambda _=False: self._add_action())
        self.actions_button_add.setObjectName('IconButton')
        self.actions_button_add.setFixedSize(24, 24)
        self.actions_button_add.setObjectName('IconButton')
        self.actions_button_add.setIconSize(QtCore.QSize(24, 24))

        self.actions_layout = QtWidgets.QVBoxLayout()
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(10)

        task_actions_layout.addWidget(label, 0, 2, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        task_actions_layout.addWidget(self.actions_button_add, 1, 0)
        task_actions_layout.addWidget(InputWrapper(tr('TaskPage - Action', 'Action'), self.actions_action), 1, 1, 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        task_actions_layout.addLayout(self.actions_layout, 2, 0, 4, 4)

        task_lease_contract_layout = QtWidgets.QGridLayout()
        task_lease_contract_layout.setContentsMargins(10, 10, 10, 10)
        task_lease_contract_layout.setSpacing(20)
        task_lease_contract_frame = QtWidgets.QFrame()
        task_lease_contract_frame.setObjectName('Frame')
        task_lease_contract_frame.setLayout(task_lease_contract_layout)

        label = QtWidgets.QLabel(tr('TaskPage - Information lease contract label', 'Lease Contract'), font=QtGui.QFont('Open Sans', 24, 600))
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

        task_lease_contract_layout.addWidget(label, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        task_lease_contract_layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.lease_contract_search_widget), 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        task_lease_contract_layout.addWidget(scroll, 2, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

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

        layout.addWidget(task_information_frame, 1, 0, 1, 9)
        layout.addWidget(task_dates_frame, 2, 0, 1, 9)
        layout.addWidget(task_actions_frame, 3, 0, 1, 9)
        layout.addWidget(task_lease_contract_frame, 4, 0, 1, 9)

        layout.addWidget(button_back, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_save, 5, 0, 1, 2)
        layout.addWidget(button_cancel, 5, 2, 1, 2)

    def _add_named_date(self):
        date = self.dates_date.dateTime().toString('yyyy-MM-ddThh:mm:00') + get_utc_offset()
        name = self.dates_name.text()

        self.dates_name.setText('')

        self._dates.append({'name': name, 'date': date})

        self.dates_table_model = NamedDateTableModel(self._dates)
        self.dates_table_view.setModel(self.dates_table_model)
    
    def _delete_named_date(self, index: QtCore.QModelIndex):
        if index.column() == 0:
            self._dates.pop(index.row())
            
            self.dates_table_model = NamedDateTableModel(self._dates)
            self.dates_table_view.setModel(self.dates_table_model)

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


    def _add_action(self, action: dict = None):
        if action is None:
            action = {
            'action': self.actions_action.text(),
            'done': False
            }

            self.actions_action.setText('')

        key = uuid.uuid4().__str__()
        frame = QtWidgets.QWidget()
        frame.setObjectName('Frame')
        button = QtWidgets.QPushButton(icon=QtGui.QIcon('data/minus-circle.svg'))
        button.setFixedSize(24, 24)
        button.setObjectName('IconButton')
        button.setIconSize(QtCore.QSize(24, 24))
        button.clicked.connect(lambda _=False, frame=frame, key=key: self.remove_action(key, frame))

        checkbox = QtWidgets.QCheckBox()
        checkbox.setObjectName('Checkbox')
        checkbox.setText(tr('TaskPage - Action done', 'Done'))
        checkbox.setChecked(True if action['done'] else False)
        checkbox.clicked.connect(lambda _=False, checkbox=checkbox, key=key: self.update_action(key, checkbox))
        checkbox.setFixedWidth(100)

        label = QtWidgets.QLabel(action['action'], font=QtGui.QFont('Open Sans', 16, 400))
        label.setObjectName('Label')

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(label)
        layout.addWidget(checkbox)
        frame.setLayout(layout)

        self.actions_layout.addWidget(frame)

        self._actions[key] = action

    def remove_action(self, key, widget):
        self.actions_layout.removeWidget(widget)
        widget.deleteLater()

        self._actions.pop(key)
    
    def update_action(self, key, widget):
        self._actions[key]['done'] = widget.isChecked()

    def save(self):
        data = {
            'id': self.__id,
            'date': self.creation_date.date().toString('yyyy-MM-dd'),
            'notify_owner': True if self.notify_owner.isChecked() else False,
            'text': self.task_text.text(),
            'note': self.task_note.toPlainText(),
            'email_subject': self.email_subject.currentText(),
            'lease_contract': self._lease_contract,
            'dates': self._dates,
            'actions': self._actions.values()
        }

        if self.__id is None:
            success, _ = NotificationsApi.create_task(data)
            if not success:
                dialog = Dialog(tr('Dialog - Error title', 'Save error'),
                                tr('Dialog - Error text', 'An error occurred while saving data!'),
                                'error') 
                if dialog.is_accepted:
                    self.close()
                return

        else:
            success, _ = NotificationsApi.update_task(data)
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

    def __load_task(self):
        success, task = NotificationsApi.get_task(self.__id)
        if success:
            creation_date = datetime.date.fromisoformat(task['date'])
            self.creation_date.setDate(QtCore.QDate(creation_date.year, creation_date.month, creation_date.day))
            self.task_text.setText(task['text'])
            self.task_note.setText(task['note'])
            self.email_subject.setCurrentIndex(email_subjects.index(task['email_subject']))

            self._add_lease_contract(task['lease_contract'], False, False)

            self._dates = task['dates']
            self.dates_table_model = NamedDateTableModel(self._dates)
            self.dates_table_view.setModel(self.dates_table_model)

            for action in task['actions']:
                self._add_action(action)

        else:
            Dialog(tr('Dialog - Error title', 'Load error'),
                   tr('Dialog - Error text', 'An error occurred while load data!'),
                   'error')