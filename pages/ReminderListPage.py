from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from widgets.elements import (
    InputWrapper,
    CustomWindow,
)
from api import (
    NotificationsApi
)
from tablemodels.ReminderTableModel import ReminderTableModel

tr = QtCore.QCoreApplication.translate

class ReminderListPage(CustomWindow):
    Signal = QtCore.Signal(dict)
    def __init__(self) -> None:
        super().__init__()

        self.__init_UI()
        
        self.update_data()
        self.table_view.resizeColumnsToContents()

    def __init_UI(self):
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        button_add_reminder = QtWidgets.QPushButton(tr('ReminderListPage - Add reminder', 'Add reminder'))
        button_add_reminder.setObjectName('BlueButton')
        button_add_reminder.clicked.connect(lambda: self.Signal.emit({'window': 'reminder'}))

        self.filter_by_active = QtWidgets.QCheckBox()
        self.filter_by_active.setText(tr('ReminderListPage - Show only active', 'Show only active'))
        self.filter_by_active.setObjectName('Checkbox')
        self.filter_by_active.clicked.connect(lambda: self.update_data())

        self.table_model = ReminderTableModel([])
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SelectionMode.NoSelection)
        self.table_view.doubleClicked.connect(self.__table_click)
        self.table_view.hideColumn(0)
        self.table_view.setObjectName('Table')

        self.button_next = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-right.svg'))
        self.button_next.setObjectName('IconButton')
        self.button_next.setIconSize(QtCore.QSize(24, 24))
        self.button_next.clicked.connect(self.next_page)
        self.button_next.setDisabled(True)
        self.button_previous = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-left.svg'))
        self.button_previous.setObjectName('IconButton')
        self.button_previous.setIconSize(QtCore.QSize(24, 24))
        self.button_previous.clicked.connect(self.previous_page)
        self.button_previous.setDisabled(True)

        self.search = QtWidgets.QLineEdit()
        self.search.setObjectName('Input')
        self.search.setPlaceholderText('🔍')
        self.search.textChanged.connect(lambda _: self.update_data())

        button_back = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-left.svg'))
        button_back.setObjectName('IconButton')
        button_back.setIconSize(QtCore.QSize(24, 24))
        button_back.clicked.connect(self.cancel)

        layout.addWidget(button_back, 0, 0)
        layout.addWidget(button_add_reminder, 0, 1)
        layout.addWidget(self.filter_by_active, 0, 6, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search), 0, 7, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.table_view, 1, 0, 9, 8)
        layout.addWidget(self.button_previous, 10, 0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.button_next, 10, 7, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.widget.setLayout(layout)

    def update_data(self, final_url: str = None):
        active = self.filter_by_active.isChecked()

        search = self.search.text()
        if search == '':
            search = None
        
        success, data = NotificationsApi.reminder_list(search, active, final_url)
        if success:
            self.table_model = ReminderTableModel(data['results'])
            self.table_view.setModel(self.table_model)

            if data['previous'] is None:
                self.button_previous.setDisabled(True)
            else:
                self.button_previous.setDisabled(False)
                self._previous_page = data['previous']

            if data['next'] is None:
                self.button_next.setDisabled(True)
            else:
                self.button_next.setDisabled(False)
                self._next_page = data['next']

    def next_page(self):
        self.update_data(final_url=self._next_page)

    def previous_page(self):
        self.update_data(final_url=self._previous_page)

    def __table_click(self, index: QtCore.QModelIndex):
        self.Signal.emit({'window': 'reminder', 'id': self.table_model._data[index.row()]['id']})

    def cancel(self):
        self.Signal.emit({'window': 'back'})
