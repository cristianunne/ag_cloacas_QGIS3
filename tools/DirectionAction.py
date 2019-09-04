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


class DirectionAction():
    
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()

        dir = PathClass()
        filename = os.path.join(dir.getPath(), 'icons\direction.png')
        
          # Create actions 
        self.direction = QAction(QIcon(filename),  QCoreApplication.translate("AG_Cloacas", "Agregar Direccion al Tramo"),  self.iface.mainWindow())
            
        self.direction.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.direction.triggered.connect(self.direction_action)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.direction)
        
        
        
    def direction_action(self):
        #primero utilizo el box para consultar si agregar
        #Accedo si el tool ha sido activado
        if self.direction.isChecked():
            
            res_dialog = self.showdialog()
            if(res_dialog == 1):
            
                try:
                    
                    layer_cl_tramos = QgsProject.instance().mapLayersByName('cl_tramos')[0]
                    layer_cl_direction = QgsProject.instance().mapLayersByName('cl_direction')[0]
                    
                    #instanciio las clases e inicializo
                    cl_direction_entity = ClDirectionEntity()
                    cl_direction_entity.initialize(layer_cl_direction)

                    try:
                        layer_select_tramo = layer_cl_tramos.selectedFeatures()
                        
                        if(len(layer_select_tramo) >= 1):
                            select_tramo = layer_cl_tramos.selectedFeatures()[0]
                            if cl_direction_entity.addDirection(select_tramo):
                                self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", Qgis.Info)
                                self.direction.setChecked(False)
                        else:
                            self.iface.messageBar().pushMessage("Error", "Seleccione un Tramo", Qgis.Warning)
                            
                    except(IndexError):
                        self.iface.messageBar().pushMessage("Error", "Seleccione un Tramo", Qgis.Warning)

                except (IndexError):
                    self.iface.messageBar().pushMessage("Error", "Debe cargar la capa 'cl_tramos', 'cl_direction'", Qgis.Critical)
                    self.direction.setChecked(False)
                    
            self.direction.setChecked(False)
        
        

    def showdialog(self):

        retval = QMessageBox.question(self.iface.mainWindow(),
                "??", "Agregar Direccion?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        val = None
        
        if retval == QMessageBox.Yes:
            
            val = 1
        else:
            val = 0
        
        
        return val        
        
    
    