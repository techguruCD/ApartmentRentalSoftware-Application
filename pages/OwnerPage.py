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
    QLabel,
    QPlainTextEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

import api.OwnerApi as api
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog

tr = QCoreApplication.translate
# First name!, Last name!, Phone!, Email!, Note[Text field]
class OwnerPage(CustomWindow):
    def __init__(self, id: int = None):
        super().__init__()
        self.__id = id

        self.setWindowTitle(tr('OwnerPage - Title', 'Apartment Owner'))
        
        self.__init_UI()

        if self.__id is not None:
            self.__load_owner()

    def __init_UI(self):
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        self.button_back.clicked.connect(self.cancel)
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.button_back)
        back_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # self.label_title = QLabel(tr('OwnerPage - Title', 'Apartment Owner'), self)
        # self.label_title.setObjectName('TitleLabel')

        self.first_name = QLineEdit(self)
        self.first_name.setObjectName('Input')
        self.last_name = QLineEdit(self)
        self.last_name.setObjectName('Input')
        
        self.phone = QLineEdit(self)
        self.phone.setObjectName('Input')
        self.email = QLineEdit(self)
        self.email.setObjectName('Input')
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        button_save = QPushButton(tr('Buttons - Save', 'Save'), self)
        button_save.setObjectName('DialogButton')
        button_save.clicked.connect(self.save)
        button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'), self)
        button_cancel.setObjectName('DialogButton')
        button_cancel.clicked.connect(self.cancel)
        
        layout.addLayout(back_layout, 0, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('Widgets - First Name', 'First Name'), self.first_name), 1, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Last Name', 'Last Name'), self.last_name), 1, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Phone', 'Phone'), self.phone), 2, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Email', 'Email'), self.email), 2, 1, 1, 1)

        layout.addWidget(InputWrapper(tr('Widgets - Note', 'Note'), self.note), 3, 0, 1, 2)
        layout.addWidget(button_save, 4, 0, 1, 1)
        layout.addWidget(button_cancel, 4, 1, 1, 1)

        layout.setRowStretch(3, 1)

        self.widget.setLayout(layout)
    
    def save(self):
        data = {
            'first_name': self.first_name.text(),
            'last_name': self.last_name.text(),
            'phone': self.phone.text(),
            'email': self.email.text(),
            'note': self.note.toPlainText()
        }

        success, owner = api.update_owner(data) if self.__id != None else api.create_owner(data)
        if not success:
            dialog = Dialog(tr('Dialog - Error title', 'Update error'),
                            tr('Dialog - Error text', 'An error occurred while updating data!'),
                            'error')
        else:
            dialog = Dialog(tr('OwnerPage - Success title', 'Save success'),
                            tr('OwnerPage - Success text', 'Save success'),
                            'success')
            self.cancel()

    def cancel(self):
        self.Signal.emit({'window': 'back'})

    def __load_owner(self):
        success, owner = api.get_owner(self.__id)
        if success:
            print(owner)
            self.first_name.setText(owner['first_name'])
            self.last_name.setText(owner['last_name'])
            self.phone.setText(owner['phone'])
            self.email.setText(owner['email'])
            self.note.setPlainText(owner['note'])
        else:
            Dialog(tr('Dialog - Error title', 'Update error'),
                tr('Dialog - Error text', 'An error occurred while load data!'),
                'error')
