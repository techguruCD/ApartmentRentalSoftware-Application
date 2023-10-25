from typing import Optional
import PySide6.QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QSize,
    QDate,
    QModelIndex
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
    QComboBox,
    QDoubleSpinBox,
    QCheckBox,
    QTableView,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QLabel
)

from api import ApartmentApi, TenantApi, LeaseContractApi
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog
from tablemodels.TenantTableModel import TenantTableModel
from tablemodels.ApartmentTableModel import ApartmentTableModel
import datetime

tr = QCoreApplication.translate
# Start date!, End date!, Rent price per month!, Are utilities included!, Property tax! [For the year], Tenant!, Apartment!, Note [text field]


class LeaseContractPage(CustomWindow):
    def __init__(self, id: int = 1):
        super().__init__()
        self.__id = id
        self.__tenant = None
        self.__apartment = None

        self.setWindowTitle(tr('LeaseContractPage - Title', 'Lease Contract'))

        self._next_page_tenant = None
        self._previous_page_tenant = None

        self._next_page_apartment = None
        self._previous_page_apartment = None

        self.__init_UI()

        self.update_data_apartment()
        self.update_data_tenant()

        self.table_view_tenant.resizeColumnsToContents()
        self.table_view_apartment.resizeColumnsToContents()

        if self.__id is not None:
            self.__load_leaseContract()

            self.tenant.setText(self.__tenant['first_name'] + ' ' + self.__tenant['last_name'])
            self.input_wrapper_tenant.show()
            self.tenant_frame.hide()

            self.apartment.setText(self.__apartment['address'])
            self.input_wrapper_apartment.show()
            self.apartment_frame.hide()

    def __init_UI(self):
        date = datetime.datetime.now()
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon(
            'data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.button_back)
        back_layout.addSpacerItem(QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.start_date = QDateEdit(displayFormat='dd/MM/yyyy')
        self.start_date.setObjectName('Input')
        self.start_date.setDate(QDate(date.year, date.month, date.day))
        self.start_date.setDisabled(True)

        self.end_date = QDateEdit(displayFormat='dd/MM/yyyy')
        self.end_date.setObjectName('Input')
        self.end_date.setDate(QDate(date.year, date.month, date.day))
        self.end_date.setDisabled(True)

        self.rent_price_per_month = QDoubleSpinBox(self)
        self.rent_price_per_month.setObjectName('Input')

        self.are_utilities_included = QCheckBox(self)
        self.are_utilities_included.setText(
            tr('Widgets - Are Utilities Included', 'Are Utilities Included'))
        self.are_utilities_included.setObjectName('Checkbox')

        self.property_tax_year = QDoubleSpinBox(self)
        self.property_tax_year.setObjectName('Input')

        self.tenant = QPushButton(self)
        self.tenant.setObjectName('Input')
        self.input_wrapper_tenant = InputWrapper(
            tr('Widgets - Tenant', 'Tenant'), self.tenant)
        self.input_wrapper_tenant.hide()

        self.apartment = QPushButton(self)
        self.apartment.setObjectName('Input')
        self.input_wrapper_apartment = InputWrapper(
            tr('Widgets - Apartment', 'Apartment'), self.apartment)
        self.input_wrapper_apartment.hide()

        # tenant_frame start
        self.tenant_frame = QFrame(self)
        self.tenant_frame.setObjectName('Frame')
        layout_tenant = QGridLayout()
        layout_tenant.setSpacing(20)

        label = QLabel(tr('LeaseContractPage - Tenant label',
                       'Tenant'), font=QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.search_tenant = QLineEdit(self)
        self.search_tenant.setObjectName('Input')
        self.search_tenant.setPlaceholderText('🔍')
        self.search_tenant.textChanged.connect(lambda _: self.update_data_tenant())
        self.combo_status_tenant = QComboBox(self)
        self.combo_status_tenant.setObjectName('Input')
        self.combo_status_tenant.addItem(tr('TenantStatus - All', 'All'))
        self.combo_status_tenant.addItem(tr('TenantStatus - Active', 'Active'))
        self.combo_status_tenant.addItem(tr('TenantStatus - Inactive', 'Inactive'))
        self.combo_status_tenant.currentIndexChanged.connect(lambda _: self.update_data_tenant())

        layout_search = QHBoxLayout()
        layout_search.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search_tenant))
        layout_search.addWidget(InputWrapper(tr('Widgets - Status', 'Status'), self.combo_status_tenant))
        layout_search.setStretch(0, 2)
        layout_search.setStretch(1, 1)

        self.table_model_tenant = TenantTableModel([])
        self.table_view_tenant = QTableView(self)
        self.table_view_tenant.setObjectName('Table')
        self.table_view_tenant.setModel(self.table_model_tenant)
        self.table_view_tenant.hideColumn(0)
        self.table_view_tenant.horizontalHeader().setStretchLastSection(True)
        self.table_view_tenant.doubleClicked.connect(self.table_click_tenant)
        self.table_view_tenant.setMinimumHeight(100)

        self.button_next_tenant = QPushButton(icon=QIcon(
            'data/arrow-long-right.svg'), parent=self)
        self.button_next_tenant.setObjectName('IconButton')
        self.button_next_tenant.setIconSize(QSize(24, 24))
        self.button_next_tenant.clicked.connect(self.next_page_tenant)
        self.button_next_tenant.setDisabled(True)

        self.button_previous_tenant = QPushButton(
            icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_previous_tenant.setObjectName('IconButton')
        self.button_previous_tenant.setIconSize(QSize(24, 24))
        self.button_previous_tenant.clicked.connect(self.next_page_tenant)
        self.button_previous_tenant.setDisabled(True)

        layout_tenant.addWidget(label, 0, 0, 1, 3)
        layout_tenant.addLayout(layout_search, 1, 0, 1, 3)
        layout_tenant.addWidget(self.table_view_tenant, 2, 0, 1, 3)
        layout_tenant.addWidget(self.button_previous_tenant, 3, 0, 1, 1)
        layout_tenant.addWidget(self.button_next_tenant, 3, 2, 1, 1)

        self.tenant_frame.setLayout(layout_tenant)
        # tenant_frame end

        self.tenant.clicked.connect(self.input_wrapper_tenant.hide)
        self.tenant.clicked.connect(self.tenant_frame.show)

        # apartment_frame start
        self.apartment_frame = QFrame(self)
        self.apartment_frame.setObjectName('Frame')
        layout_apartment = QGridLayout()
        layout_apartment.setSpacing(20)

        label = QLabel(tr('LeaseContractPage - Apartment label',
                       'Apartment'), font=QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.search_apartment = QLineEdit(self)
        self.search_apartment.setObjectName('Input')
        self.search_apartment.setPlaceholderText('🔍')
        self.search_apartment.textChanged.connect(lambda _: self.update_data_apartment())

        self.table_model_apartment = ApartmentTableModel([])
        self.table_view_apartment = QTableView(self)
        self.table_view_apartment.setObjectName('Table')
        self.table_view_apartment.setModel(self.table_model_apartment)
        self.table_view_apartment.hideColumn(0)
        self.table_view_apartment.horizontalHeader().setStretchLastSection(True)
        self.table_view_apartment.doubleClicked.connect(self.table_click_apartment)
        self.table_view_apartment.setMinimumHeight(100)

        self.button_next_apartment = QPushButton(
            icon=QIcon('data/arrow-long-right.svg'), parent=self)
        self.button_next_apartment.setObjectName('IconButton')
        self.button_next_apartment.setIconSize(QSize(24, 24))
        self.button_next_apartment.clicked.connect(self.next_page_apartment)
        self.button_next_apartment.setDisabled(True)

        self.button_previous_apartment = QPushButton(
            icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_previous_apartment.setObjectName('IconButton')
        self.button_previous_apartment.setIconSize(QSize(24, 24))
        self.button_previous_apartment.clicked.connect(self.next_page_apartment)
        self.button_previous_apartment.setDisabled(True)

        layout_apartment.addWidget(label, 0, 0, 1, 3)
        layout_apartment.addWidget(InputWrapper(
            tr('Widgets - Search', 'Search'), self.search_apartment), 1, 0, 1, 3)
        layout_apartment.addWidget(self.table_view_apartment, 2, 0, 1, 3)
        layout_apartment.addWidget(self.button_previous_apartment, 3, 0, 1, 1)
        layout_apartment.addWidget(self.button_next_apartment, 3, 2, 1, 1)

        self.apartment_frame.setLayout(layout_apartment)
        # apartment_frame end

        self.apartment.clicked.connect(self.input_wrapper_apartment.hide)
        self.apartment.clicked.connect(self.apartment_frame.show)

        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        self.button_save = QPushButton(tr('Buttons - Save', 'Save'), self)
        self.button_save.setObjectName('DialogButton')
        self.button_save.clicked.connect(self.save)
        self.button_cancel = QPushButton(
            tr('Buttons - Cancel', 'Cancel'), self)
        self.button_cancel.setObjectName('DialogButton')
        self.button_cancel.clicked.connect(self.cancel)

        layout.addLayout(back_layout, 0, 0, 1, 2)
        layout.addWidget(InputWrapper(
            tr('Widgets - Creation Date', 'Creation Date'), self.start_date), 1, 0, 1, 1)
        layout.addWidget(InputWrapper(
            tr('Widgets - End Date', 'End Date'), self.end_date), 1, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Rent Price Per Month',
                         'Rent Price Per Month'), self.rent_price_per_month), 2, 0, 1, 1)
        layout.addWidget(self.are_utilities_included, 2, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Property Tax For Year',
                         'Property Tax For Year'), self.property_tax_year), 3, 0, 1, 2)
        layout.addWidget(self.input_wrapper_tenant, 4, 0, 1, 1)
        layout.addWidget(self.input_wrapper_apartment, 4, 1, 1, 1)
        layout.addWidget(self.tenant_frame, 5, 0, 1, 2)
        layout.addWidget(self.apartment_frame, 6, 0, 1, 2)
        layout.addWidget(InputWrapper(
            tr('Widgets - Note', 'Note'), self.note), 7, 0, 1, 2)

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

    def table_click_tenant(self, index: QModelIndex):
        self.tenant_frame.hide()
        self.input_wrapper_tenant.show()
        self.__tenant = self.table_model_tenant._data[index.row()]
        self.tenant.setText(self.__tenant['first_name'] + ' ' + self.__tenant['last_name'])

    def table_click_apartment(self, index: QModelIndex):
        self.apartment_frame.hide()
        self.input_wrapper_apartment.show()
        self.__apartment = self.table_model_apartment._data[index.row()]
        self.apartment.setText(self.__apartment['address'])

    def update_data_tenant(self, final_url: str = None):
        search = self.search_tenant.text()
        status = None

        if search == "":
            search = None
        match self.combo_status_tenant.currentIndex():
            case 1:
                status = 'active'
            case 2:
                status = 'inactive'

        success, data = TenantApi.tenant_list(search, status, final_url)
        if success:
            self.table_model_tenant = TenantTableModel(data['results'])
            self.table_view_tenant.setModel(self.table_model_tenant)

            if (data['previous']) is None:
                self.button_previous_tenant.setDisabled(True)
            else:
                self.button_previous_tenant.setDisabled(False)
                self._previous_page_tenant = data['previous']
            
            if data['next'] is None:
                self.button_next_tenant.setDisabled(True)
            else:
                self.button_next_tenant.setDisabled(False)
                self._next_page_transaction = data['next']

    def update_data_apartment(self, final_url: str = None):
        search = self.search_apartment.text()
        if search == "":
            search = None

        success, data = ApartmentApi.apartment_list(search, final_url)
        if success:
            self.table_model_apartment = ApartmentTableModel(data['results'])
            self.table_view_apartment.setModel(self.table_model_apartment)

            if (data['previous']) is None:
                self.button_previous_apartment.setDisabled(True)
            else:
                self.button_previous_apartment.setDisabled(False)
                self._previous_page_apartment = data['previous']
            
            if data['next'] is None:
                self.button_next_apartment.setDisabled(True)
            else:
                self.button_next_apartment.setDisabled(False)
                self._next_page_apartment = data['next']

    def next_page_tenant(self):
        self.update_data_tenant(final_url=self._next_page_tenant)

    def previous_page_tenant(self):
        self.update_data_tenant(final_url=self._previous_page_tenant)

    def next_page_apartment(self):
        self.update_data_apartment(final_url=self._next_page_apartment)

    def previous_page_apartment(self):
        self.update_data_apartment(final_url=self._previous_page_apartment)

    def save(self):
        data = {
            'start_date': self.start_date.text(),
            'end_date': self.end_date.text(),
            'rent_price': self.rent_price_per_month.value(),
            'utilities_included': self.are_utilities_included.isChecked(),
            'tax': self.property_tax_year.value(),
            'note': self.note.toPlainText(),
            'tenant': self.__tenant,
            'apartment': self.__apartment
        }
        if self.__id != None:
            data['id'] = self.__id
        success, leaseContract = LeaseContractApi.update_lease_contract(
            data) if self.__id != None else LeaseContractApi.create_lease_contract(data)
        if not success:
            dialog = Dialog(tr('Dialog - Error title', 'Update error'),
                            tr('Dialog - Error text',
                               'An error occurred while updating data!'),
                            'error')
        else:
            Dialog(tr('TenantPage - Success title', 'Save success'),
                   tr('TenantPage - Success text', 'Tenant Created'),
                   'success')
            self.cancel()

    def cancel(self):
        self.SignalClose.emit()

    def __load_leaseContract(self):
        success, leaseContract = LeaseContractApi.get_lease_contract(self.__id)
        if success:
            self.start_date.setDate(QDate.fromString(leaseContract['start_date'], 'dd/mm/yyyy'))
            self.end_date.setDate(QDate.fromString(leaseContract['end_date'], 'dd/mm/yyyy'))
            self.rent_price_per_month.setValue(leaseContract['rent_price'])
            self.are_utilities_included.setChecked(leaseContract['utilities_included'])
            self.property_tax_year.setValue(leaseContract['tax'])
            self.note.setPlainText(leaseContract['note'])
            self.__tenant = leaseContract['tenant']
            self.__apartment = leaseContract['apartment']
        else:
            Dialog(tr('Dialog - Error title', 'Update error'),
                   tr('Dialog - Error text', 'An error occurred while load data!'),
                   'error')
