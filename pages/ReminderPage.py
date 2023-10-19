from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from widgets.elements import InputWrapper, CustomWindow
from tablemodels.NamedDateTableModel import NamedDateTableModel, DateEditDelegate, LineEditDelegate
import datetime

tr = QtCore.QCoreApplication.translate

class ReminderPage(CustomWindow):
    def __init__(self, id: int = None):
        super().__init__()

        self._id = None

        self.__init_UI()

        self.show()

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
        reminder_information_frame.setObjectName('Frame')
        reminder_information_frame.setLayout(reminder_information_layout)

        label = QtWidgets.QLabel(tr('ReminderPage - Information frame label', 'Reminder Information'), font=QtGui.QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.creation_date = QtWidgets.QDateEdit(displayFormat='dd/MM/yyyy')
        self.creation_date.setObjectName('Input')
        self.creation_date.setDate(QtCore.QDate(date.year, date.month, date.day))
        self.creation_date.setDisabled(True)

        self.reminder_text = QtWidgets.QLineEdit()
        self.reminder_text.setObjectName('Input')

        self.notify_owner = QtWidgets.QCheckBox()
        self.notify_owner.setText(tr('ReminderPage - Notify owner', 'Notify owner'))
        self.notify_owner.setObjectName('Checkbox')

        reminder_information_layout.addWidget(label, 0, 0, 1, 4)
        reminder_information_layout.addWidget(self.notify_owner, 1, 0)
        reminder_information_layout.addWidget(InputWrapper(tr('ReminderPage - Text', 'Text'), self.reminder_text), 1, 1, 1, 2)
        reminder_information_layout.addWidget(InputWrapper(tr('ReminderPage - Creation date', 'Creation date'), self.creation_date), 1, 3)

        self.table_model = NamedDateTableModel([{'name': '1', 'date': '2023-10-19T10:12:00Z'}, {'name': '2', 'date': '2023-10-19T15:17:00Z'}])
        self.table_view = QtWidgets.QTableView()
        self.table_view.setObjectName('Table')
        line_edit_delegate = LineEditDelegate()
        date_edit_delegate = DateEditDelegate()
        
        self.table_view.setModel(self.table_model)
        self.table_view.setItemDelegateForColumn(1, line_edit_delegate)
        self.table_view.setItemDelegateForColumn(2, date_edit_delegate)
        

        # self.table_view.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        # self.table_view.setSelectionMode(QtWidgets.QTableView.SelectionMode.NoSelection)


        layout.addWidget(reminder_information_frame, 0, 0, 1, 9)
        layout.addWidget(self.table_view, 1, 0, 1, 9)

