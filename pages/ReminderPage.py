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

        self.setWindowTitle(tr('ReminderPage - Title', 'Reminder'))

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
        # reminder_information_frame.setObjectName('Frame')
        reminder_information_frame.setLayout(reminder_information_layout)

        # label = QtWidgets.QLabel(tr('ReminderPage - Information frame label', 'Reminder Information'), font=QtGui.QFont('Open Sans', 24, 600))
        # label.setObjectName('Label')

        self.creation_date = QtWidgets.QDateEdit(displayFormat='dd/MM/yyyy')
        self.creation_date.setObjectName('Input')
        self.creation_date.setDate(QtCore.QDate(date.year, date.month, date.day))
        self.creation_date.setDisabled(True)

        self.reminder_text = QtWidgets.QLineEdit()
        self.reminder_text.setObjectName('Input')

        self.notify_owner = QtWidgets.QCheckBox()
        self.notify_owner.setText(tr('ReminderPage - Notify owner', 'Notify owner'))
        self.notify_owner.setObjectName('Checkbox')

        # reminder_information_layout.addWidget(label, 0, 0, 1, 4)
        reminder_information_layout.addWidget(self.notify_owner, 1, 0)
        reminder_information_layout.addWidget(InputWrapper(tr('ReminderPage - Text', 'Text'), self.reminder_text), 1, 1, 1, 2)
        reminder_information_layout.addWidget(InputWrapper(tr('ReminderPage - Creation date', 'Creation date'), self.creation_date), 1, 3)


        reminder_named_dates_layout = QtWidgets.QGridLayout()
        reminder_named_dates_layout.setSpacing(20)
        reminder_named_dates_frame = QtWidgets.QFrame()
        reminder_named_dates_frame.setObjectName('Frame')
        reminder_named_dates_frame.setLayout(reminder_named_dates_layout)

        label = QtWidgets.QLabel(tr('ReminderPage - Information dates label', 'Dates'), font=QtGui.QFont('Open Sans', 24, 600))
        label.setObjectName('Label')


        self.named_dates_table_model = NamedDateTableModel([{'name': '1', 'date': '2023-10-19T10:12:00Z'}, {'name': '2', 'date': '2023-10-19T15:17:00Z'}])
        
        self.named_dates_table_view = QtWidgets.QTableView()
        self.named_dates_table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.named_dates_table_view.setObjectName('Table')
        self.named_dates_table_view.setModel(self.named_dates_table_model)
        self.named_dates_table_view.setItemDelegate(LineEditDelegate())
        self.named_dates_table_view.setItemDelegateForColumn(2, DateEditDelegate())

        self.named_dates_date = QtWidgets.QDateTimeEdit(displayFormat='dd/MM/yyyy hh:mm')
        self.named_dates_date.setObjectName('Input')
        self.named_dates_name = QtWidgets.QLineEdit()
        self.named_dates_name.setObjectName('Input')

        self.named_dates_button_add = QtWidgets.QPushButton(icon=QtGui.QIcon('data/plus-circle.svg'))
        self.named_dates_button_add.setObjectName('IconButton')
        self.named_dates_button_add.setFixedSize(24, 24)
        self.named_dates_button_add.setObjectName('IconButton')
        self.named_dates_button_add.setIconSize(QtCore.QSize(24, 24))

        reminder_named_dates_layout.addWidget(label, 0, 0, 1, 4)
        reminder_named_dates_layout.addWidget(self.named_dates_button_add, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        reminder_named_dates_layout.addWidget(InputWrapper(tr('ReminderPage - Name', 'Name'), self.named_dates_name), 1, 1, 1, 2)
        reminder_named_dates_layout.addWidget(InputWrapper(tr('ReminderPage - Date', 'Date'), self.named_dates_date), 1, 3)
        reminder_named_dates_layout.addWidget(self.named_dates_table_view, 2, 0, 1, 4)


        layout.addWidget(reminder_information_frame, 0, 0, 1, 9)
        layout.addWidget(reminder_named_dates_frame, 1, 0, 1, 9)
