import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global

IMAGE_GOAL_WIDTH_INT = 240
IMAGE_GOAL_HEIGHT_INT = IMAGE_GOAL_WIDTH_INT
CLOSED_RESULT_INT = -1
CLOSED_WITH_BREATHING_RESULT_INT = -2


class RestComposite(QtWidgets.QWidget):
    result_signal = QtCore.pyqtSignal(int)
    # -used both for wait and for closing

    def __init__(self):
        super().__init__()
        self.show()

        self.updating_gui_bool = False
        self.rest_actions_qbg = QtWidgets.QButtonGroup()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        vbox_l2.addStretch(1)

        # Main area
        self.main_area_qgb = QtWidgets.QGroupBox("Rest")
        vbox_l2.addWidget(self.main_area_qgb)

        vbox_l3 = QtWidgets.QVBoxLayout()
        self.main_area_qgb.setLayout(vbox_l3)

        self.title_qll = QtWidgets.QLabel()
        vbox_l3.addWidget(self.title_qll)
        self.image_qll = QtWidgets.QLabel()
        vbox_l3.addWidget(self.image_qll)
        self.image_qll.setScaledContents(True)
        self.image_qll.setMinimumWidth(IMAGE_GOAL_WIDTH_INT)
        self.image_qll.setMinimumHeight(IMAGE_GOAL_HEIGHT_INT)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        self.wait_qpb = QtWidgets.QPushButton("Wait")
        hbox_l4.addWidget(self.wait_qpb)
        self.wait_qpb.clicked.connect(self.on_wait_clicked)
        self.wait_qpb.setFont(mc_global.get_font_xlarge())
        hbox_l4.addWidget(QtWidgets.QLabel("for"))
        self.wait_qsb = QtWidgets.QSpinBox()
        self.wait_qsb.setMinimum(1)
        self.wait_qsb.setFont(mc_global.get_font_xlarge())
        hbox_l4.addWidget(self.wait_qsb)
        hbox_l4.addWidget(QtWidgets.QLabel("minutes"))
        hbox_l4.addStretch(1)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        self.close_qpb = QtWidgets.QPushButton("Close")
        hbox_l4.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_button_clicked)
        self.close_qpb.setFont(mc_global.get_font_xlarge())
        hbox_l4.addWidget(QtWidgets.QLabel("and disable reminders"))
        hbox_l4.addStretch(1)

        vbox_l2.addStretch(1)

        # Breathe
        vbox_l2.addWidget(QtWidgets.QLabel("After taking a break:"))
        # TODO: select a new breathing phrase? From a combobox?
        self.close_and_breathe_qpb = QtWidgets.QPushButton("Breathe")
        vbox_l2.addWidget(self.close_and_breathe_qpb)
        self.close_and_breathe_qpb.clicked.connect(self.on_close_and_breathe_button_clicked)
        self.close_and_breathe_qpb.setFont(mc_global.get_font_xlarge(i_bold=False))

    def on_wait_clicked(self):
        # minutes_int = self.wait_qsb.value()
        # self.dialog_outcome_int = minutes_int
        # self.accept()
        self.result_signal.emit(self.wait_qsb.value())

    def on_close_and_breathe_button_clicked(self):
        self.result_signal.emit(CLOSED_WITH_BREATHING_RESULT_INT)

    def on_close_button_clicked(self):
        self.result_signal.emit(CLOSED_RESULT_INT)

    def resize_image(self):
        if self.image_qll.pixmap() is None:
            return
        old_width_int = self.image_qll.pixmap().width()
        old_height_int = self.image_qll.pixmap().height()
        if old_width_int == 0:
            return
        width_relation_float = old_width_int / IMAGE_GOAL_WIDTH_INT
        height_relation_float = old_height_int / IMAGE_GOAL_HEIGHT_INT

        if width_relation_float > height_relation_float:
            scaled_width_int = IMAGE_GOAL_WIDTH_INT
            scaled_height_int = (scaled_width_int / old_width_int) * old_height_int
        else:
            scaled_height_int = IMAGE_GOAL_HEIGHT_INT
            scaled_width_int = (scaled_height_int / old_height_int) * old_width_int

        self.image_qll.setFixedWidth(scaled_width_int)
        self.image_qll.setFixedHeight(scaled_height_int)

    def update_gui(self):
        self.updating_gui_bool = True
        if mc_global.active_rest_action_id_it == mc_global.NO_REST_ACTION_SELECTED_INT:
            pass
        else:
            rest_action = model.RestActionsM.get(mc_global.active_rest_action_id_it)
            if rest_action.image_path_str and os.path.isfile(rest_action.image_path_str):
                self.image_qll.show()
                self.image_qll.setPixmap(
                    QtGui.QPixmap(
                        rest_action.image_path_str
                    )
                )
                self.resize_image()
            else:
                self.image_qll.hide()
                self.image_qll.clear()

            self.title_qll.setText(rest_action.title_str)
            self.title_qll.setFont(mc_global.get_font_xlarge())
            self.title_qll.setWordWrap(True)

            self.updating_gui_bool = False

