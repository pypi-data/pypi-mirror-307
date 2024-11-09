"""
UV VIS Spectrometer for Xeuss3 data viewer
author : Emeline COURNEDE  (adapted by OT)
(C) CEA 2024
"""
from PyQt5 import QtCore, QtGui, QtWidgets,uic
import pandas as pd
import numpy as np
import os
import pySAXS
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class UV_Vis_Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        #super(UV_Vis_Ui_Dialog, self).__init__()
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + "UV-vis_interface_EM.ui", self)  #

        # icon & title bar
        self.icon = QtGui.QIcon(pySAXS.ICON_PATH +"Logo_UV-vis-Em.png")
        self.setWindowIcon(self.icon)
        self.selected_files = []
        pixmap = QtGui.QPixmap(pySAXS.ICON_PATH + "Logo_UV-vis-Em.PNG")
        scaled_pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.ui.logolabel.setPixmap(scaled_pixmap)

        #table widget
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Name'])
        # Stretch the column to fill the available space
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Connect button clicks to their functions
        self.ui.pushButton.clicked.connect(self.select_input_directory)
        self.ui.pushButton_2.clicked.connect(self.select_dark_file)
        self.ui.pushButton_3.clicked.connect(self.select_blank_file)
        self.ui.tableWidget.itemSelectionChanged.connect(self.display_graph)
        # matplotlib widget
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ui.verticalLayout.addWidget(self.toolbar)
        self.ui.verticalLayout.addWidget(self.canvas)

        self.setGeometry(100, 100, 600, 900)


    def setupUi(self):
        MainWindow=self
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        #MainWindow.setFixedSize(660, 960)
        MainWindow.setWindowTitle("Xeuss3 UV-Vis data treatment")

        # Set the window icon

        icon = QtGui.QIcon(pySAXS.ICON_PATH +"Logo_UV-vis-Em.png")
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Create a horizontal layout for the title
        self.topLayout = QtWidgets.QHBoxLayout()

        # Add the title
        '''
        self.titleLabel = QtWidgets.QLabel("UV-vis_Xeuss3.0_LIONS", self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.topLayout.addWidget(self.titleLabel)
        '''
        # Add logo with title\n",
        self.logoLabel = QtWidgets.QLabel(self.centralwidget)
        pixmap = QtGui.QPixmap(pySAXS.ICON_PATH +"Logo_UV-vis-Em.PNG")
        scaled_pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.logoLabel.setPixmap(scaled_pixmap)
        self.logo_and_title_layout = QtWidgets.QHBoxLayout()
        self.logo_and_title_layout.addWidget(self.logoLabel)
        # Config police text\n",
        self.titleLabel = QtWidgets.QLabel("Xeuss3 UV-Vis data treatment", self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.titleLabel.setFont(font)
        # logo and text alignment\n",
        self.logo_and_title_layout.addWidget(self.titleLabel, alignment=QtCore.Qt.AlignVCenter)
        self.logo_and_title_layout.addStretch()
        self.logo_and_title_widget = QtWidgets.QWidget(self.centralwidget)
        self.logo_and_title_widget.setLayout(self.logo_and_title_layout)
        self.verticalLayout.addWidget(self.logo_and_title_widget)


        self.verticalLayout.addLayout(self.topLayout)

        self.inputLayout = QtWidgets.QHBoxLayout()
        self.inputDirectoryEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.pushButton = QtWidgets.QPushButton("Directory", self.centralwidget)
        self.inputLayout.addWidget(self.inputDirectoryEdit)
        self.inputLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.inputLayout)

        self.darkLayout = QtWidgets.QHBoxLayout()
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.pushButton_2 = QtWidgets.QPushButton("Select Dark File", self.centralwidget)
        self.darkLayout.addWidget(self.lineEdit_2)
        self.darkLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.darkLayout)

        self.blankLayout = QtWidgets.QHBoxLayout()
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.pushButton_4 = QtWidgets.QPushButton("Select Blank File", self.centralwidget)
        self.blankLayout.addWidget(self.lineEdit_3)
        self.blankLayout.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.blankLayout)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['Name'])
        self.verticalLayout.addWidget(self.tableWidget)

        self.axisLayout = QtWidgets.QGridLayout()
        self.label_x_min = QtWidgets.QLabel("X Min:", self.centralwidget)
        self.lineEdit_x_min = QtWidgets.QLineEdit(self.centralwidget)
        self.label_x_max = QtWidgets.QLabel("X Max:", self.centralwidget)
        self.lineEdit_x_max = QtWidgets.QLineEdit(self.centralwidget)
        self.label_y_min = QtWidgets.QLabel("Y Min:", self.centralwidget)
        self.lineEdit_y_min = QtWidgets.QLineEdit(self.centralwidget)
        self.label_y_max = QtWidgets.QLabel("Y Max:", self.centralwidget)
        self.lineEdit_y_max = QtWidgets.QLineEdit(self.centralwidget)

        self.axisLayout.addWidget(self.label_x_min, 0, 0)
        self.axisLayout.addWidget(self.lineEdit_x_min, 0, 1)
        self.axisLayout.addWidget(self.label_x_max, 0, 2)
        self.axisLayout.addWidget(self.lineEdit_x_max, 0, 3)
        self.axisLayout.addWidget(self.label_y_min, 1, 0)
        self.axisLayout.addWidget(self.lineEdit_y_min, 1, 1)
        self.axisLayout.addWidget(self.label_y_max, 1, 2)
        self.axisLayout.addWidget(self.lineEdit_y_max, 1, 3)

        self.verticalLayout.addLayout(self.axisLayout)

        #self.figure = Figure()
        #self.canvas = FigureCanvas(self.figure)
        #self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #self.canvas.updateGeometry()
        #self.ui.navi_toolbarEDF = NavigationToolbar(self.ui.matplotlibwidgetEDF, self)
        #self.toolbar = NavigationToolbar(self.canvas, self.centralwidget)


        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)


        #MainWindow.setCentralWidget(self.centralwidget)
        '''
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        '''
        # Add this attribute in the Ui_MainWindow class to keep track of selected files
        self.selected_files = []

        # Connect button clicks to their functions
        self.pushButton.clicked.connect(self.select_input_directory)
        self.pushButton_2.clicked.connect(self.select_dark_file)
        self.pushButton_4.clicked.connect(self.select_blank_file)
        self.tableWidget.itemSelectionChanged.connect(self.display_graph)
        self.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UV-vis_Xeuss3.0_LIONS"))

    def select_input_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        if directory:
            self.ui.inputDirectoryEdit.setText(directory)
            self.load_csv_files(directory)

    def load_csv_files(self, directory):
        self.ui.tableWidget.setRowCount(0)
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv') and f not in ['dark.csv', 'blank.csv']]
        for file in csv_files:
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)
            self.ui.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(file))

    def select_dark_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Dark File", "", "CSV Files (*.csv)")
        if file:
            self.ui.lineEdit_2.setText(file)

    def select_blank_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Blank File", "", "CSV Files (*.csv)")
        if file:
            self.ui.lineEdit_3.setText(file)

    def display_graph(self):
        input_directory = self.inputDirectoryEdit.text()
        dark_file = self.ui.lineEdit_2.text()
        blank_file = self.ui.lineEdit_3.text()

        if not input_directory or not dark_file or not blank_file:
            QtWidgets.QMessageBox.warning(None, "Error", "Please select input directory, dark file, and blank file.")
            return

        selected_items = self.ui.tableWidget.selectedItems()
        self.selected_files = [item.text() for item in selected_items]

        if not self.selected_files:
            return

        dark_df = pd.read_csv(dark_file, header=None)
        dark_intensity = dark_df.iloc[:, 1]

        blank_df = pd.read_csv(blank_file, header=None)
        blank_intensity = blank_df.iloc[:, 1]

        self.figure.clear()  # Clear the figure to avoid overlapping of old plots

        for selected_csv in self.selected_files:
            csv_path = os.path.join(input_directory, selected_csv)

            df = pd.read_csv(csv_path, header=None)
            df = df.rename(columns={df.columns[0]: 'Wavelength'})
            df = df.rename(columns={df.columns[1]: 'Intensity'})

            df['Dark'] = dark_intensity
            df['Blank'] = blank_intensity

            numerator = df['Blank'] - df['Dark']
            denominator = df['Intensity'] - df['Dark']
            valid_mask = (numerator > 0) & (denominator > 0)
            absorbance = np.full(df.shape[0], np.nan)
            absorbance[valid_mask] = np.log10(numerator[valid_mask] / (denominator[valid_mask]))
            df['Absorbance'] = absorbance

            self.plot_graph(df['Wavelength'], df['Absorbance'], selected_csv)

    def plot_graph(self, x, y, title):
        ax = self.figure.gca()  # Get the current axis
        ax.plot(x, y, label=title)
        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylabel("Absorbance (u.a.)")

        # Set limits if specified
        try:
            x_min = float(self.lineEdit_x_min.text())
            x_max = float(self.lineEdit_x_max.text())
            ax.set_xlim(x_min, x_max)
        except ValueError:
            pass

        try:
            y_min = float(self.lineEdit_y_min.text())
            y_max = float(self.lineEdit_y_max.text())
            ax.set_ylim(y_min, y_max)
        except ValueError:
            pass

        ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = UV_Vis_Ui_Dialog()
    dialog.show()
    sys.exit(app.exec_())