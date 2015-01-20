from __future__ import print_function
import sys
from PyQt4 import QtGui, QtCore, Qt
# from PyQt import QtWidgets
import pyqtgraph as pg
import numpy as np
from astropy.io import fits
from ifupy.core import Cube
from ifupy.core import read_data


class Main(QtGui.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.init_ui()
        self.data = {}

    def init_ui(self):
        # Set up menu bars and tool bars
        self.init_menubar()
        self.init_toolbar()

        # Set app layout
        # grid = QtWidgets.QGridLayout()
        # self.setLayout(grid)

        # --------------------
        # Set the MDI area as the central widget
        # --------------------
        self.mdiarea = QtGui.QMdiArea()
        # self.mdiarea.setTabPosition(QtGui.QTabWidget.North)
        # self.mdiarea.setTabShape(QtGui.QTabWidget.Rounded)
        self.mdiarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiarea.setActivationOrder(QtGui.QMdiArea.CreationOrder)
        # self.mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
        # self.mdiarea.setTabsClosable(True)
        # self.mdiarea.setTabsMovable(True)
        self.mdiarea.show()
        self.setCentralWidget(self.mdiarea)

        self.mdiarea.cascadeSubWindows()

        # --------------------
        # Set up dock areas around central widget
        # --------------------
        data_dock = QtGui.QDockWidget("Data Sets", self)
        data_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, data_dock)

        tool_dock = QtGui.QDockWidget("Tools", self)
        tool_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, tool_dock)

        # --------------------
        # Set up data tree widget
        # --------------------
        self.tree_view = QtGui.QTreeWidget()
        self.tree_view.setColumnCount(2)
        self.tree_view.setHeaderLabels(QtCore.QStringList(["Name", "Shape"]))
        data_dock.setWidget(self.tree_view)

        # --------------------
        # Set up tool area widget
        # --------------------
        tool_box = QtGui.QToolBox(tool_dock)

        basic_tools = QtGui.QWidget()
        basic_tools.setLayout(QtGui.QGridLayout())

        image_tools = QtGui.QWidget()
        image_tools.setLayout(QtGui.QGridLayout())

        spec_tools = QtGui.QWidget()
        spec_tools.setLayout(QtGui.QGridLayout())

        select_tool = QtGui.QPushButton('Select', basic_tools)
        select_tool.setCheckable(True)
        select_tool.clicked[bool].connect(self.add_plot)

        tool_box.addItem(basic_tools, "Basic")
        tool_box.addItem(image_tools, "Imaging")
        tool_box.addItem(spec_tools, "Spectroscopy")

        tool_dock.setWidget(tool_box)

        # --------------------
        # Status bar
        # --------------------
        self.statusBar().showMessage('Ready')

        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('IFUpy')
        self.show()

    def init_menubar(self):
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def init_toolbar(self):
        open_file = QtGui.QAction(QtGui.QIcon('img/open127.png'), 'Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open new File')
        open_file.triggered.connect(self._file_dialog)

        toolbar = self.addToolBar('Open')
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addAction(open_file)

    def _file_dialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                  '/Users/nearl/Downloads/ForRaymond')
        name, data_list = read_data(fname)
        self.data[name] = data_list
        self.update_tree_data()

    def add_plot(self):
        current_limb = self.tree_view.currentItem()
        plot_data = current_limb.data(2, QtCore.Qt.UserRole).toPyObject()()
        plot_title = current_limb.data(0, QtCore.Qt.UserRole)

        win = pg.ImageView()
        win.setImage(plot_data)

        sub_win = self.mdiarea.addSubWindow(win)
        sub_win.setWindowTitle(plot_title)
        # p1 = win.plot(y=np.random.normal(size=100))
        win.show()

    def update_tree_data(self):
        self.tree_view.clear()

        for key, val in self.data.items():
            new_item = QtGui.QTreeWidgetItem(self.tree_view)
            new_item.setText(0, key)

            for v in val:
                new_data = QtGui.QTreeWidgetItem(new_item)
                new_data.setText(0, v.name)
                new_data.setText(1, str(v.shape()))
                new_data.setData(2, QtCore.Qt.UserRole, v)



def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()