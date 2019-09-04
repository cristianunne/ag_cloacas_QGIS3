from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *

from ..entities.ClDirectionEntity import ClDirectionEntity

import os

try:
    from qgis.PyQt.QtWidgets import *
except:
    pass

from ..Path import PathClass


class DirectionChange():

    def __init__(self, iface, toolbar):
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()

        dir = PathClass()
        filename = os.path.join(dir.getPath(), 'icons\dir_change.png')

        # Create actions
        self.direction_change = QAction(QIcon(filename),
                                        QCoreApplication.translate("AG_Cloacas", "Cambiar Sentido"),
                                        self.iface.mainWindow())

        self.direction_change.setCheckable(True)

        # Connect to signals for button behaviour
        self.direction_change.triggered.connect(self.direction_change_action)

        # Add actions to the toolbar
        self.toolbar.addAction(self.direction_change)


    def direction_change_action(self):
        if self.direction_change.isChecked():
            res_dialog = self.showdialog()


            if (res_dialog == 1):

                try:

                    layer_cl_direction = QgsProject.instance().mapLayersByName('cl_direction')[0]

                    # instanciio las clases e inicializo
                    cl_direction_entity = ClDirectionEntity()
                    cl_direction_entity.initialize(layer_cl_direction)

                    try:
                        layer_dir_selected = layer_cl_direction.selectedFeatures()

                        if (len(layer_dir_selected) >= 1):

                            dir_selected = layer_cl_direction.selectedFeatures()[0]

                            if cl_direction_entity.changeDirection(dir_selected):
                                pass


                        else:
                            self.iface.messageBar().pushMessage("Error", "Seleccione una Direccion",
                                                                Qgis.Warning)


                    except(IndexError):
                        self.iface.messageBar().pushMessage("Error", "Seleccione una Direccion",
                                                            Qgis.Warning)

                except (IndexError):
                    self.iface.messageBar().pushMessage("Error", "Debe cargar la capa 'cl_direction'", Qgis.Critical)
                    self.direction_change.setChecked(False)
            self.direction_change.setChecked(False)




    def showdialog(self):

        retval = QMessageBox.question(self.iface.mainWindow(),
                                      "??", "Cambiar Direccion?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        val = None

        if retval == QMessageBox.Yes:

            val = 1
        else:
            val = 0

        return val
