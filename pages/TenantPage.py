from typing import Optional
import PySide6.QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QSize
)
from PySide6.QtGui import (
    QIcon
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLineEdit,
    QPlainTextEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QLabel
)

from widgets.elements import (
    InputWrapper
)

tr = QCoreApplication.translate
# Name!, Last Name!, Phone!, Mail!, Parents' Address, Parents' Phone, Note [text field]
class TenantPage(QFrame):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        self.setWindowTitle(tr('TenantPage - Title', 'Tenant'))
        self.__init_UI()
    def __init_UI(self):
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.button_back)
        back_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label_title = QLabel(tr('TenantPage - Title', 'Tenant'), self)
        self.label_title.setObjectName('TitleLabel')

        self.first_name = QLineEdit(self)
        self.first_name.setObjectName('Input')
        self.last_name = QLineEdit(self)
        self.last_name.setObjectName('Input')
        
        self.phone = QLineEdit(self)
        self.phone.setObjectName('Input')
        self.mail = QLineEdit(self)
        self.mail.setObjectName('Input')
        
        self.parent_address = QLineEdit(self)
        self.parent_address.setObjectName('Input')
        self.parent_phone = QLineEdit(self)
        self.parent_phone.setObjectName('Input')
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        self.button_save = QPushButton(tr('Buttons - Save', 'Save'), self)
        self.button_save.setObjectName('DialogButton')
        self.button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'), self)
        self.button_cancel.setObjectName('DialogButton')
        
        layout.addLayout(back_layout, 0, 0, 1, 2)
        layout.addWidget(self.label_title, 1, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('Widgets - First Name', 'First Name'), self.first_name), 2, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Last Name', 'Last Name'), self.last_name), 2, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Phone', 'Phone'), self.phone), 3, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Mail', 'Mail'), self.mail), 3, 1, 1, 1)

        layout.addWidget(InputWrapper(tr("Widgets - Parents' address", "Parents' address"), self.parent_address), 4, 0, 1, 1)
        layout.addWidget(InputWrapper(tr("Widgets - Parents' phone", "Parents' phone"), self.parent_phone), 4, 1, 1, 1)

        layout.addWidget(InputWrapper(tr('Widgets - Note', 'Note'), self.note), 5, 0, 1, 2)
        layout.addWidget(self.button_save, 6, 0, 1, 1)
        layout.addWidget(self.button_cancel, 6, 1, 1, 1)

        # layout.setRowStretch(0, 0)
        # layout.setRowStretch(1, 0)
        # layout.setRowStretch(2, 0)
        # layout.setRowStretch(3, 0)
        # layout.setRowStretch(4, 0)
        # layout.setRowStretch(5, 1)
        # layout.setRowStretch(6, 9)

        self.setLayout(layout)