from typing import Optional
import PySide6.QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QSize,
    QModelIndex
)
from PySide6.QtGui import (
    QIcon
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLineEdit,
    QPlainTextEdit,
    QTableView,
    QLabel,
    QComboBox,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

import api.ApartmentApi as api
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog
from tablemodels.ApartmentTableModel import ApartmentTableModel

tr = QCoreApplication.translate
# Name!, Last Name!, Phone!, Mail!, Parents' Address, Parents' Phone, Note [text field]
class HomePage(CustomWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('HomePage - Title', 'Home'))
        self._next_page = None
        self._previous_page = None
        self._current_page = None

        self.__init_UI()

        self.update_data()
        self.table_view.resizeColumnsToContents()

        self.SignalUpdate.connect(self._update_data_signal_handler)


    def __init_UI(self):
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        layout_back = QHBoxLayout()
        layout_back.addWidget(self.button_back)
        layout_back.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.search = QLineEdit(self)
        self.search.setObjectName('Input')
        self.search.setPlaceholderText('🔍')
        self.search.textChanged.connect(lambda _: self.update_data())

        self.table_model = ApartmentTableModel([])
        self.table_view = QTableView(self)
        self.table_view.setObjectName('Table')
        self.table_view.setModel(self.table_model)

        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.doubleClicked.connect(self.table_click)
        self.table_view.hideColumn(0)

        self.button_next = QPushButton(icon=QIcon('data/arrow-long-right.svg'))
        self.button_next.setObjectName('IconButton')
        self.button_next.setIconSize(QSize(24, 24))
        self.button_next.clicked.connect(self.next_page)
        self.button_next.setDisabled(True)
        self.button_previous = QPushButton(icon=QIcon('data/arrow-long-left.svg'))
        self.button_previous.setObjectName('IconButton')
        self.button_previous.setIconSize(QSize(24, 24))
        self.button_previous.clicked.connect(self.previous_page)
        self.button_previous.setDisabled(True)

        self.button_rental_fee_table = QPushButton(tr('Buttons - Rental Fee Table', 'Rental Fee Table'), self)
        self.button_rental_fee_table.setObjectName('LightBlueButton')
        self.button_utility_fee_table = QPushButton(tr('Buttons - Utility Fee Table', 'Utility Fee Table'), self)
        self.button_utility_fee_table.setObjectName('LightBlueButton')
        self.button_add_appartment = QPushButton(tr('Buttons - Add Apartment', 'Add Apartment'), self)
        self.button_add_appartment.setObjectName('LightBlueButton')
        self.button_add_appartment.clicked.connect(self.button_add_appartment_click)
        self.button_seal = QPushButton(tr('Buttons - Seal', 'Seal'), self)
        self.button_seal.setObjectName('GreenButton')
        self.button_export = QPushButton(tr('Buttons - Export', 'Export'), self)
        self.button_export.setObjectName('GreenButton')
        self.button_smart_form = QPushButton(tr('Buttons - Smart Form', 'Smart Form'), self)
        self.button_smart_form.setObjectName('BlueButton')

        button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'), self)
        button_cancel.setObjectName('DialogButton')
        button_cancel.clicked.connect(self.cancel)

        layout_control = QVBoxLayout()
        layout_control.addWidget(self.button_rental_fee_table)
        layout_control.addWidget(self.button_utility_fee_table)
        layout_control.addWidget(self.button_add_appartment)
        layout_control.addWidget(self.button_seal)
        layout_control.addWidget(self.button_export)
        layout_control.addWidget(self.button_smart_form)
        layout_control.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addLayout(layout_back, 0, 0, 1, 4)
        layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search), 1, 0, 1, 3)
        layout.addWidget(self.table_view, 2, 0, 1, 3)
        layout.addWidget(self.button_previous, 3, 0)
        layout.addWidget(self.button_next, 3, 2)
        layout.addLayout(layout_control, 1, 3, 3, 1)
        layout.addWidget(button_cancel, 4, 0, 1, 4)

        layout.setRowStretch(2, 1)

        self.widget.setLayout(layout)

    def table_click(self, index: QModelIndex):
        self.Signal.emit({'window': 'apartment', 'id': self.table_model._data[index.row()]['id']})

    def button_add_appartment_click(self):
        self.Signal.emit({'window': 'apartment'})

    def _update_data_signal_handler(self):
        self.update_data(self._current_page)

    def update_data(self, final_url: str = None):
        search = self.search.text()
        success, data = api.apartment_list(search, final_url)
        if success:
            self.table_model = ApartmentTableModel(data['results'])
            self.table_view.setModel(self.table_model)

            if (data['previous']) is None:
                self.button_previous.setDisabled(True)
            else:
                self.button_previous.setDisabled(False)
                self._previous_page = data['previous']
            
            if data['next'] is None:
                self.button_next.setDisabled(True)
            else:
                self.button_next.setDisabled(False)
                self._next_page = data['next']

            self._current_page = data['current']
    
    def next_page(self):
        self.update_data(final_url=self._previous_page)
    
    def previous_page(self):
        self.update_data(final_url=self._previous_page)

    def cancel(self):
        self.SignalClose.emit()