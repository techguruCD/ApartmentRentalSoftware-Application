from typing import Optional
import PySide6.QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QSize,
    QDate
)
from PySide6.QtGui import (
    QIcon,
    QFont
)
from PySide6.QtWidgets import (
    QWidget,
    QScrollArea,
    QFrame,
    QLineEdit,
    QPlainTextEdit,
    QDateEdit,
    QTableView,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QLabel
)

from api import ApartmentApi, TenantApi, RentalApi
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog
from tablemodels.TenantTableModel import TenantTableModel
from tablemodels.ApartmentTableModel import ApartmentTableModel
import datetime

tr = QCoreApplication.translate
# Start date!, End date!, Rent price per month!, Are utilities included!, Property tax! [For the year], Tenant!, Apartment!, Note [text field]
class LeaseContractPage(CustomWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('LeaseContractPage - Title', 'Lease Contract'))
        
        self._next_page_tenant = None
        self._previous_page_tenant = None

        self._next_page_apartment = None
        self._previous_page_apartment = None

        self.__init_UI()

    def __init_UI(self):
        date = datetime.datetime.now()
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.button_back)
        back_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # self.label_title = QLabel(tr('TenantPage - Title', 'Tenant'), self)
        # self.label_title.setObjectName('TitleLabel')

        self.creation_date = QDateEdit(displayFormat='dd/MM/yyyy')
        self.creation_date.setObjectName('Input')
        self.creation_date.setDate(QDate(date.year, date.month, date.day))
        self.creation_date.setDisabled(True)

        self.end_date = QDateEdit(displayFormat='dd/MM/yyyy')
        self.end_date.setObjectName('Input')
        self.end_date.setDate(QDate(date.year, date.month, date.day))
        self.end_date.setDisabled(True)

        self.rent_price_per_month = QLineEdit(self)
        self.rent_price_per_month.setObjectName('Input')

        self.are_utilities_included = QLineEdit(self)
        self.are_utilities_included.setObjectName('Input')

        self.property_tax_year = QLineEdit(self)
        self.property_tax_year.setObjectName('Input')

        self.tenant = QLineEdit(self)
        self.tenant.setObjectName('Input')
        self.input_wrapper_tenant = InputWrapper(tr('Widgets - Tenant', 'Tenant'), self.tenant)
        self.input_wrapper_tenant.hide()

        self.apartment = QLineEdit(self)
        self.apartment.setObjectName('Input')
        self.input_wrapper_apartment = InputWrapper(tr('Widgets - Apartment', 'Apartment'), self.apartment)
        self.input_wrapper_apartment.hide()

        # tenant_frame start
        self.tenant_frame = QFrame(self)
        self.tenant_frame.setObjectName('Frame')
        layout_tenant = QGridLayout()
        layout_tenant.setSpacing(20)

        label = QLabel(tr('LeaseContractPage - Tenant label', 'Tenant'), font=QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.search_tenant = QLineEdit(self)
        self.search_tenant.setObjectName('Input')
        self.search_tenant.setPlaceholderText('🔍')

        self.table_model_tenant = TenantTableModel([])
        self.table_view_tenant = QTableView(self)
        self.table_view_tenant.setObjectName('Table')
        self.table_view_tenant.setModel(self.table_model_tenant)
        self.table_view_tenant.hideColumn(0)
        self.table_view_tenant.setMinimumHeight(100)

        button_next_tenant = QPushButton(icon=QIcon('data/arrow-long-right.svg'), parent=self)
        button_next_tenant.setObjectName('IconButton')
        button_next_tenant.setIconSize(QSize(24, 24))
        button_next_tenant.clicked.connect(self.next_page_tenant)
        button_next_tenant.setDisabled(True)

        button_previous_tenant = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        button_previous_tenant.setObjectName('IconButton')
        button_previous_tenant.setIconSize(QSize(24, 24))
        button_previous_tenant.clicked.connect(self.next_page_tenant)
        button_previous_tenant.setDisabled(True)

        layout_tenant.addWidget(label, 0, 0, 1, 3)
        layout_tenant.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search_tenant), 1, 0, 1, 3)
        layout_tenant.addWidget(self.table_view_tenant, 2, 0, 1, 3)
        layout_tenant.addWidget(button_previous_tenant, 3, 0, 1, 1)
        layout_tenant.addWidget(button_next_tenant, 3, 2, 1, 1)

        self.tenant_frame.setLayout(layout_tenant)
        # tenant_frame end

        # apartment_frame start
        self.apartment_frame = QFrame(self)
        self.apartment_frame.setObjectName('Frame')
        layout_apartment = QGridLayout()
        layout_apartment.setSpacing(20)

        label = QLabel(tr('LeaseContractPage - Apartment label', 'Apartment'), font=QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.search_apartment = QLineEdit(self)
        self.search_apartment.setObjectName('Input')
        self.search_apartment.setPlaceholderText('🔍')

        self.table_model_apartment = ApartmentTableModel([])
        self.table_view_apartment = QTableView(self)
        self.table_view_apartment.setObjectName('Table')
        self.table_view_apartment.setModel(self.table_model_apartment)
        self.table_view_apartment.hideColumn(0)
        self.table_view_apartment.setMinimumHeight(100)

        button_next_apartment = QPushButton(icon=QIcon('data/arrow-long-right.svg'), parent=self)
        button_next_apartment.setObjectName('IconButton')
        button_next_apartment.setIconSize(QSize(24, 24))
        button_next_apartment.clicked.connect(self.next_page_apartment)
        button_next_apartment.setDisabled(True)

        button_previous_apartment = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        button_previous_apartment.setObjectName('IconButton')
        button_previous_apartment.setIconSize(QSize(24, 24))
        button_previous_apartment.clicked.connect(self.next_page_apartment)
        button_previous_apartment.setDisabled(True)

        layout_apartment.addWidget(label, 0, 0, 1, 3)
        layout_apartment.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search_apartment), 1, 0, 1, 3)
        layout_apartment.addWidget(self.table_view_apartment, 2, 0, 1, 3)
        layout_apartment.addWidget(button_previous_apartment, 3, 0, 1, 1)
        layout_apartment.addWidget(button_next_apartment, 3, 2, 1, 1)

        self.apartment_frame.setLayout(layout_apartment)
        # apartment_frame end
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        self.button_save = QPushButton(tr('Buttons - Save', 'Save'), self)
        self.button_save.setObjectName('DialogButton')
        self.button_save.clicked.connect(self.save)
        self.button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'), self)
        self.button_cancel.setObjectName('DialogButton')
        self.button_cancel.clicked.connect(self.cancel)
        
        layout.addLayout(back_layout, 0, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('Widgets - Creation Date', 'Creation Date'), self.creation_date), 1, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - End Date', 'End Date'), self.end_date), 1, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Rent Price Per Month', 'Rent Price Per Month'), self.rent_price_per_month), 2, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Are Utilities Included', 'Are Utilities Included'), self.are_utilities_included), 2, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Property Tax For Year', 'Property Tax For Year'), self.property_tax_year), 3, 0, 1, 2)
        layout.addWidget(self.input_wrapper_tenant, 4, 0, 1, 1)
        layout.addWidget(self.input_wrapper_apartment, 4, 1, 1, 1)
        layout.addWidget(self.tenant_frame, 5, 0, 1, 2)
        layout.addWidget(self.apartment_frame, 6, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('Widgets - Note', 'Note'), self.note), 7, 0, 1, 2)

        layout.addWidget(self.button_save, 8, 0, 1, 1)
        layout.addWidget(self.button_cancel, 8, 1, 1, 1)
        
        scroll_widget = QWidget(self)
        scroll_widget.setObjectName('Window')
        scroll_widget.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(scroll)

        self.widget.setLayout(scroll_layout)

    def next_page_tenant(self):
        self.update_data(final_url=self._next_page_tenant)

    def previous_page_tenant(self):
        self.update_data(final_url=self._previous_page_tenant)

    def next_page_apartment(self):
        self.update_data(final_url=self._next_page_apartment)

    def previous_page_apartment(self):
        self.update_data(final_url=self._previous_page_apartment)

    def save(self):
        # data = {
        #     'first_name': self.first_name.text(),
        #     'last_name': self.last_name.text(),
        #     'phone': self.phone.text(),
        #     'mail': self.mail.text(),
        #     'parent_address': self.parent_address.text(),
        #     'parent_phone': self.parent_phone.text(),
        #     'note': self.note.toPlainText()
        # }
        if not RentalApi.rental_save(None):
            dialog = Dialog(tr('LeaseContractPage - Error title', 'Save error'),
                            tr('LeaseContractPage - Error text', 'An error occurred while updating data!'),
                            'error')
            if dialog.is_accepted:
                self.SignalClose.emit()
    def cancel(self):
        self.SignalClose.emit()