from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)

from widgets.elements import InputWrapper, CustomWindow, NamedHObjectLayout
from tools import get_utc_offset
from settings import email_subjects
from tablemodels.NamedDateTableModel import (
    NamedDateTableModel,
    DateEditDelegate,
    LineEditDelegate,
)
from api import (
    LeaseContractApi,

)
import datetime

tr = QtCore.QCoreApplication.translate

class ReminderPage(CustomWindow):
    def __init__(self, id: int = None):
        super().__init__()

        self.setWindowTitle(tr('ReminderPage - Title', 'Reminder'))

        self._id = None
        self._rental = None
        self._named_dates = []

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

        reminder_named_dates_layout.addWidget(label, 0, 0, 1, 4)
        reminder_named_dates_layout.addWidget(self.named_dates_button_add, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        reminder_named_dates_layout.addWidget(InputWrapper(tr('ReminderPage - Name', 'Name'), self.named_dates_name), 1, 1, 1, 2)
        reminder_named_dates_layout.addWidget(InputWrapper(tr('ReminderPage - Date', 'Date'), self.named_dates_date), 1, 3)
        reminder_named_dates_layout.addWidget(self.named_dates_table_view, 2, 0, 1, 4)

        reminder_rental_layout = QtWidgets.QGridLayout()
        reminder_rental_layout.setContentsMargins(10, 10, 10, 10)
        reminder_rental_layout.setSpacing(20)
        reminder_rental_frame = QtWidgets.QFrame()
        reminder_rental_frame.setObjectName('Frame')
        reminder_rental_frame.setLayout(reminder_rental_layout)

        label = QtWidgets.QLabel(tr('ReminderPage - Information rental label', 'Rental'), font=QtGui.QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.rental_search_widget = QtWidgets.QLineEdit()
        self.rental_search_widget.setObjectName('Input')
        self.rental_search_widget.textChanged.connect(self._rental_search)

        self.rental_search_layout = QtWidgets.QVBoxLayout()
        self.rental_search_layout.setContentsMargins(0, 0, 0, 0)
        self.rental_search_layout.setSpacing(10)
        self.rental_search_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setObjectName('Wrapper')
        scroll_widget.setLayout(self.rental_search_layout)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(150)

        reminder_rental_layout.addWidget(label, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        reminder_rental_layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.rental_search_widget), 1, 0)
        reminder_rental_layout.addWidget(scroll, 2, 0)

        layout.addWidget(reminder_information_frame, 0, 0, 1, 9)
        layout.addWidget(reminder_named_dates_frame, 1, 0, 1, 9)
        layout.addWidget(reminder_rental_frame, 2, 0, 1, 9)

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

    def _rental_search(self, search):
        rentals = []
        if search != '':
            success, data = LeaseContractApi.rentals_list(search, None)
            if success:
                rentals.extend(data['results'])
                while True:
                    if data['next'] is not None:
                        success, data = LeaseContractApi.rentals_list(None, data['next'])
                        if success:
                            rentals.extend(data['results'])
                    else:
                        break
        
        for i in range(self.rental_search_layout.count()):
            item = self.rental_search_layout.takeAt(0)
            item.widget().deleteLater()

        if self._rental is not None:
            self._add_rental(self._rental, False)

        for rental in rentals:
            frame = QtWidgets.QWidget()
            frame.setObjectName('Frame')
            button = QtWidgets.QPushButton(icon=QtGui.QIcon('data/plus-circle.svg'))
            button.setFixedSize(24, 24)
            button.setObjectName('IconButton')
            button.setIconSize(QtCore.QSize(24, 24))
            button.clicked.connect(lambda _=False, rental=rental: self._add_rental(rental, True))
            layout = NamedHObjectLayout(f'{rental["start_date"]} {rental["end_date"]} {rental["apartment"]["unique_identifier"]}', button, direction='left', text_align='right', font=QtGui.QFont('Open Sans', 16, 400))
            frame.setLayout(layout)

            self.rental_search_layout.addWidget(frame)

    def add_profile(self, profile, clear: bool, can_delete: bool = True):
        self._profile = profile

        if clear:
            for i in range(self.profiles.count()):
                item = self.profiles.takeAt(0)
                item.widget().deleteLater()

        frame = QtWidgets.QWidget()
        frame.setObjectName('Frame')
        button = QtWidgets.QPushButton(icon=QtGui.QIcon('data/minus-circle.svg'))
        button.setFixedSize(24, 24)
        button.setObjectName('IconButton')
        button.setIconSize(QtCore.QSize(24, 24))
        button.clicked.connect(lambda _=False: self.remove_profile())
        if not can_delete:
            button.setDisabled(True)
            self.profiles_search.setDisabled(True)
        layout = NamedHObjectLayout(f'{profile["first_name"]} {profile["last_name"]} {profile["id_card"]}', button, direction='left', text_align='right', font=QtGui.QFont('Open Sans', 16, 400))
        frame.setLayout(layout)

        self.profiles.addWidget(frame)

    def remove_profile(self): 
        self._profile = None

        for i in range(self.profiles.count()):
            item = self.profiles.takeAt(0)
            item.widget().deleteLater()