from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors

def coloredIcon(color: QtGui.QColor, icon_path: str,
                size: QtCore.QSize, scale: int = 2):
    icon = QtGui.QPixmap(size.width() * scale, size.height() * scale)
    pixmap_icon = QtGui.QPixmap(icon_path)

    icon.fill(QtCore.Qt.GlobalColor.transparent)
    icon.fill(color)
    painter = QtGui.QPainter(icon)
    painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                           QtGui.QPainter.RenderHint.SmoothPixmapTransform)
    painter.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, size.width() * scale, size.height() * scale,
                       pixmap_icon)

    painter.end()

    return icon

class InputWrapper(QtWidgets.QFrame):
    def __init__(self, text: str, widget: QtWidgets.QWidget):
        super().__init__()

        self.setObjectName('InputWrapper')
        self.border = QtWidgets.QFrame(self)
        self.border.setObjectName('InputWrapperBorder')
        self.border.move(0,10)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(0)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        label = QtWidgets.QLabel(text, font=QtGui.QFont('Open Sans', 16, 400))

        layout.addWidget(label, 0, 0, 1, 3)
        layout.addWidget(widget, 1, 0, 1, 3)

        self.border.stackUnder(label)

        self.setLayout(layout)
        label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            # QtWidgets.QSizePolicy.Policy.Fixed
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    
    def resizeEvent(self, event) -> None:
        self.border.resize(self.width(), self.height() - 10)

class CustomWindow(QtWidgets.QWidget):
    SignalShowMinimized = QtCore.Signal()
    SignalShowNormal = QtCore.Signal()
    SignalShowMaximized = QtCore.Signal()
    SignalShowFullScreen = QtCore.Signal()
    SignalClose = QtCore.Signal()

    Signal = QtCore.Signal(dict)

    def __init__(self):
        self.start = None
        self.end = None
        self.movement = None
        self.pressing = False
        super().__init__()

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.__init_inner_UI()

    def setWindowTitle(self, title: str):
        self.title.setText(title)

    def connect_control_signals(self, parent: QtWidgets.QWidget):
        self.SignalClose.connect(lambda: parent.close())
        self.SignalShowMinimized.connect(lambda: parent.showMinimized())
        self.SignalShowMaximized.connect(lambda: parent.showMaximized())
        self.SignalShowNormal.connect(lambda: parent.showNormal())
        self.SignalShowFullScreen.connect(lambda: parent.showFullScreen())
        self.Signal.connect(parent.onSignal)

    def __init_inner_UI(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                           QtWidgets.QSizePolicy.Policy.Expanding)

        screenScale = QtWidgets.QApplication.primaryScreen().devicePixelRatio()
        self.btn_showMinimized = QtWidgets.QPushButton()
        self.btn_showMinimized.setObjectName('btn_showMinimized')
        self.btn_showMinimized.clicked.connect(self.__click_showMinimized)
        self.btn_showMinimized.setFixedSize(14, 14)
        self.btn_showMinimized.setIconSize(QtCore.QSize(12, 12))
        self.btn_showMinimized.setIcon(coloredIcon(
                QtGui.QColor(169, 114, 41),
                'data/showMinimized.svg',
                QtCore.QSize(48, 48),
                screenScale
        ))

        self.btn_showFullScreen = QtWidgets.QPushButton()
        self.btn_showFullScreen.setObjectName('btn_showFullScreen')
        self.btn_showFullScreen.clicked.connect(self.__click_showFullScreen)
        self.btn_showFullScreen.setFixedSize(14, 14)
        self.btn_showFullScreen.setIconSize(QtCore.QSize(12, 12))
        self.btn_showFullScreen.setIcon(coloredIcon(
                QtGui.QColor(41, 96, 24),
                'data/showFullScreen.svg',
                QtCore.QSize(48, 48),
                screenScale
        ))

        self.btn_close = QtWidgets.QPushButton()
        self.btn_close.setObjectName('btn_close')
        self.btn_close.clicked.connect(self.__click_close)
        self.btn_close.setFixedSize(14, 14)
        self.btn_close.setIconSize(QtCore.QSize(10, 10))
        self.btn_close.setIcon(coloredIcon(
                QtGui.QColor(143, 28, 19),
                'data/close.svg',
                QtCore.QSize(48, 48),
                screenScale
        ))

        self.title = QtWidgets.QLabel('', font=QtGui.QFont('Open Sans', 24, 700))
        self.title.setStyleSheet(f'color: {colors["primary_dark"]}')
        self.title.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.title.mouseDoubleClickEvent = self.__click_showMaximized
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setMinimumHeight(40)

        control_buttons_layout = QtWidgets.QHBoxLayout()
        control_buttons_layout.setContentsMargins(10, 10, 0, 0)
        control_buttons_layout.setSpacing(5)
        control_buttons_layout.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignTop |
                QtCore.Qt.AlignmentFlag.AlignRight)

        control_buttons_layout.addWidget(self.btn_close)
        control_buttons_layout.addWidget(self.btn_showFullScreen)
        control_buttons_layout.addWidget(self.btn_showMinimized)

        self.sub_control_buttons_frame = QtWidgets.QFrame()
        self.sub_control_buttons_frame.setFixedSize(62, 24)
        self.sub_control_buttons_frame.setLayout(control_buttons_layout)
        self.sub_control_buttons_frame.adjustSize()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.widget = QtWidgets.QFrame()
        self.widget.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding
        )

        layout.addWidget(self.title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.widget)

        self.wrapper = QtWidgets.QWidget()
        self.wrapper.setObjectName('Wrapper')
        self.wrapper.setLayout(layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.wrapper)

        self.setLayout(main_layout)
        self.sub_control_buttons_frame.setParent(self)

        self.setMinimumWidth(self.sub_control_buttons_frame.width())

    def __click_close(self):
        self.SignalClose.emit()
        self.close()

    def __click_showFullScreen(self):
        if self.isFullScreen():
            self.SignalShowNormal.emit()
            self.showNormal()
        else:
            self.SignalShowFullScreen.emit()
            self.showFullScreen()

    def __click_showMaximized(self, event: QtGui.QMouseEvent):
        event.ignore()
        if self.isMaximized():
            self.SignalShowNormal.emit()
            self.showNormal()
        else:
            self.SignalShowMaximized.emit()
            self.showMaximized()

    def __click_showMinimized(self):
        self.SignalShowMinimized.emit()
        self.showMinimized()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.title.adjustSize()
        self.setMinimumWidth(self.sub_control_buttons_frame.width() * 2 + self.title.width() + 20)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.position().y() < 40:
            self.start = self.mapToGlobal(event.position())
            self.pressing = True

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        movable_widget = self
        if self.parent() is not None:
            movable_widget = self.parent()
        if self.pressing:
            self.end = self.mapToGlobal(event.position())
            self.movement = self.end - self.start
            movable_widget.setGeometry(self.mapToGlobal(self.movement).x(),
                             self.mapToGlobal(self.movement).y(),
                             self.width(),
                             self.height())
            self.start = self.end

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.pressing = False

class NamedHObjectLayout(QtWidgets.QHBoxLayout):
    def __init__(self,
                 name: str,
                 object,
                 direction: str ='right',
                 font: QtGui.QFont = None,
                 text_align: str = 'left',
                 spacing: int = 10,
                 ):
        QtWidgets.QHBoxLayout.__init__(self)
        self.layout().setSpacing(spacing)
        label = QtWidgets.QLabel(name)
        label.setObjectName('Label')
        if font is not None:
            label.setFont(font)

        if text_align == 'left':
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        elif text_align == 'center':
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        elif text_align == 'Hcenter':
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        elif text_align == 'Vcenter':
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        elif text_align == 'right':
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        if direction == 'right':
            self.layout().addWidget(label)
            self.layout().addWidget(object)
        elif direction == 'left':
            self.layout().addWidget(object)
            self.layout().addWidget(label)
     