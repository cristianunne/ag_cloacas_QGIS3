from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

from TramosAction_dialog import TramosActionDialog
from Symbol_inicio_tramos_dialog import Symbol_inicioTramosDialog
from Nodo_Final_Tramo import NodoFinalTramosDialog
from Symbol_final_tramos_dialog import Symbol_finalTramosDialog
from Resumen_Final_Tramo_Dialog import ResumenFinalTramosDialog


#Importo las entidades
from ClTramosEntity import ClTramosEntity
from ClNodoTrSymbolEntity import ClNodoTrSymbolEntity
from ClVentilacionEntity import ClVentilacionEntity
from ClCotasEntity import ClCotasEntity
from ClNodosEntity import ClNodosEntity
from ClDirectionEntity import ClDirectionEntity
from ClNodosEtiqueta import ClNodosEtiquetaEntity
from ClNodosEtiqueta2Entity import ClNodosEtiqueta2Entity
from ClNodosTramos import ClNodosTramosEntity

class TramosAction():
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        
        #Llamo a las clases de los Formularios
        self.dlg_tramos = TramosActionDialog()
        self.dlg_symbol_inicio = Symbol_inicioTramosDialog()
        self.dlg_nodo_final = NodoFinalTramosDialog()
        self.dlg_symbol_final = Symbol_finalTramosDialog()
        self.dlg_resumen_final = ResumenFinalTramosDialog()
        
        
         #CREO LAS VARIABLES QUE GUARDAN LOS DATOS
        self.n_nodo_inicial = None
        self.tipo_z_inicial = None
        self.ztn_inicial = None
        self.tipo_simbol_inicio = None
        
        self.n_nodo_final = None
        self.tipo_z_final = None
        self.ztn_final = None
        self.tipo_simbol_final = None
        self.longitud_linea = None
        
        self.tipo_material = None
        self.nro_conforme = None
        self.cota_cano_inicio = None
        self.cota_cano_final = None
        self.diametro = None
        self.cb_tipo_tramo = None
        
        
        #Creo las entidades vacias
        self.cl_tramos_entity = None
        
        
         # Create actions 
        self.tramos = QAction(QIcon(":/plugins/AGCloacas/polilinea.png"),  QCoreApplication.translate("AG_Cloacas", "Agregar Propieades al Tramo"),  self.iface.mainWindow())
            
        self.tramos.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.tramos.triggered.connect(self.action_tramos)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.tramos)
        
        #Set Eavbled a los vbotomnes d los formnularios
        
        self.dlg_symbol_inicio.rb_inicio_pld.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_des.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_cal.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_brv.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_brs.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_ese.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_brh.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_til.clicked.connect(self.setEnabledOkButtonInicio)
        self.dlg_symbol_inicio.rb_inicio_nada.clicked.connect(self.setEnabledOkButtonInicio)
        
        self.dlg_symbol_final.rb_final_pld.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_des.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_cal.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_brv.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_brs.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_ese.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_brh.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_til.clicked.connect(self.setEnabledOkButtonFinal)
        self.dlg_symbol_final.rb_final_nada.clicked.connect(self.setEnabledOkButtonFinal)
    
    
    def action_tramos(self):
       
        
        #RESETEO LOS FORMS A ESTADO VACIO
        self.resetAllForms()
        
        #Accedo si el tool ha sido activado
        if self.tramos.isChecked():
            try:
                layer_cl_tramos = QgsMapLayerRegistry.instance().mapLayersByName('cl_tramos')[0]
                cl_nodo_tr_symbol = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodo_tr_symbol')[0]
                cl_ventilacion = QgsMapLayerRegistry.instance().mapLayersByName('cl_ventilacion')[0]
                layer_cl_cotas = QgsMapLayerRegistry.instance().mapLayersByName('cl_cotas')[0]
                layer_cl_nodos = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodos')[0]
                layer_cl_nodos_etiquetas = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodos_etiqueta')[0]
                layer_cl_nodos_etiqueta_2 = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodos_etiqueta_2')[0]
                layer_cl_direction = QgsMapLayerRegistry.instance().mapLayersByName('cl_direction')[0]
                self.layer_cl_nodos_tramos = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodos_tramos')[0]
                
                #Instancio las entidades y le paso las capas correspondietes
                self.cl_tramos_entity = ClTramosEntity()
                self.cl_tramos_entity.initialize(layer_cl_tramos)
                
                self.cl_nodo_symbol_entity = ClNodoTrSymbolEntity()
                self.cl_nodo_symbol_entity.initialize(cl_nodo_tr_symbol)
                
                self.cl_ventilacion_entity = ClVentilacionEntity()
                self.cl_ventilacion_entity.initialize(cl_ventilacion)
                
                self.cl_nodosetiqueta2_entity = ClNodosEtiqueta2Entity()
                self.cl_nodosetiqueta2_entity.initialize(layer_cl_nodos_etiqueta_2)
                
                self.cl_cotas_entity = ClCotasEntity()
                self.cl_cotas_entity.initialize(layer_cl_cotas)
                
                self.cl_nodos_entity = ClNodosEntity()
                self.cl_nodos_entity.initialize(layer_cl_nodos)
                
                self.cl_direction = ClDirectionEntity()
                self.cl_direction.initialize(layer_cl_direction)
                
                
                self.cl_nodos_etiqueta_entity = ClNodosEtiquetaEntity()
                self.cl_nodos_etiqueta_entity.initialize(layer_cl_nodos_etiquetas)
                
                self.cl_nodos_tramos_entity = ClNodosTramosEntity()
                self.cl_nodos_tramos_entity.initialize(self.layer_cl_nodos_tramos)
                
                #verifico que haya al menos un elemento seleccionado
                layer_select_tramo = layer_cl_tramos.selectedFeatures()
                
                if(len(layer_select_tramo) >= 1):
                    #guardo solo el elemento 1 de la seleccion
                    tramo_select = layer_select_tramo[0]
                    
                    #PRIMERO VERIFICO QUE NO HAYA NINGUN TIPO DE DATOS CARGADOS EN EL TRAMO
                    if self.cl_tramos_entity.verifiedTramo(tramo_select) == False:

                        #evaluo si hay un simbolo al inicio y al Final y proceso segun ello
                        res_exists_symbol_inicio = self.cl_nodo_symbol_entity.getExistSymbolInicio(tramo_select)
                        res_exists_symbol_final = self.cl_nodo_symbol_entity.getExistSymbolFinal(tramo_select)


                        if res_exists_symbol_inicio == False and res_exists_symbol_final == False:

                            self.resetDialogs()
                            self.showBoxsCompleted(tramo_select)
                            self.tramos.setChecked(False)

                        elif res_exists_symbol_inicio != False and res_exists_symbol_final == False:

                            self.resetDialogs()
                            self.showBoxWithInitialData(tramo_select)
                            self.tramos.setChecked(False)

                        elif res_exists_symbol_inicio == False and res_exists_symbol_final != False:
                            self.resetDialogs()
                            self.showBoxWithFinalData(tramo_select)
                            self.tramos.setChecked(False)

                        elif res_exists_symbol_inicio != False and res_exists_symbol_final != False:

                            self.resetDialogs()
                            self.showBoxWithInitialAndFinalData(tramo_select)
                            self.tramos.setChecked(False)
                    else:
                        self.iface.messageBar().pushMessage("Error", "Ya existen Propiedades Agregadas. Borrelos e intente nuevamente!", level=QgsMessageBar.CRITICAL)

                else:
                    self.iface.messageBar().pushMessage("Error", "Seleccione un Tramo", level=QgsMessageBar.WARNING)
                
                self.tramos.setChecked(False)
                
            except (IndexError):
                self.iface.messageBar().pushMessage("Error", "Debe cargar la capa Todas las capas", level=QgsMessageBar.CRITICAL)
                self.tramos.setChecked(False)
                
        
    #Muestra los cuadros de dialogos vacios sin datos.
    #Empleado cuando no hay datos en los tramos conectados
    def showBoxsCompleted(self, tramo_select):

        res = self.dlg_tramos.exec_()

        if res == 1:
            # Guardo las Variables del nodo inicial
            self.n_nodo_inicial = self.dlg_tramos.n_nodo_inicial.text()
            self.tipo_z_inicial = self.dlg_tramos.tipo_z_inicial.currentText()
            self.ztn_inicial = self.dlg_tramos.ztn_inicial.text()

            res_2 = self.dlg_symbol_inicio.exec_()

            if res_2 == 1:
                # Obtengo el tipo de grafico para el inicio
                self.tipo_simbol_inicio = self.optioninicioChecked()

                # simbolo al final
                res_3 = self.dlg_nodo_final.exec_()

                if res_3 == 1:
                    # guardo las variables del nodo final
                    self.n_nodo_final = self.dlg_nodo_final.n_nodo_final.text()
                    self.tipo_z_final = self.dlg_nodo_final.tipo_z_final.currentText()
                    self.ztn_final = self.dlg_nodo_final.ztn_final.text()

                    res_4 = self.dlg_symbol_final.exec_()

                    if res_4 == 1:
                        # Guardo el tipo de simbologia al final
                        self.tipo_simbol_final = self.optionFinalChecked()

                        # seteo los textos que ya tengo en el dlg.resumen
                        id_tr = str(self.cl_tramos_entity.getIdTramo(tramo_select))
                        self.longitud_linea = self.cl_tramos_entity.getLongitudTramo(tramo_select)

                        # Cargo lo datos al form resumen
                        self.setInfoResumenFinal(id_tr, self.n_nodo_inicial, self.n_nodo_final,
                                                 self.tipo_simbol_inicio, self.tipo_simbol_final,
                                                 self.longitud_linea)

                        res_5 = self.dlg_resumen_final.exec_()

                        if (res_5 == 1):
                            # Obtengo los parametros del form Resumen
                            self.tipo_material = self.optionResumenChecked()
                            self.nro_conforme = self.dlg_resumen_final.nro_conforme.text()
                            self.cota_cano_inicio = self.dlg_resumen_final.cota_cano_inicio.text()
                            self.cota_cano_final = self.dlg_resumen_final.cota_cano_final.text()
                            self.diametro = self.dlg_resumen_final.diametro.text()
                            self.cb_tipo_tramo = self.dlg_resumen_final.cb_tipo_tramo.currentText()

                            #proceso el tramo
                            self.tramosActionProcess(tramo_select)

    def showBoxWithInitialData(self, tramo_select):
        res_exists_symbol_inicio = self.cl_nodo_symbol_entity.getExistSymbolInicio(tramo_select)
        #if res_exists_symbol_inicio != False:
            #cargo los box con los datos del cl_nodos
        feat = self.cl_nodos_entity.getInitialNodoByTramoTouches(tramo_select)
        if feat != False:
            #ya tengo el CL_NODO
            n_nod = feat['n_nod']
            ztn_inicio = feat['ztn']
            tipo_z = feat['ty_z']


            self.dlg_tramos.n_nodo_inicial.setText(str(n_nod))
            self.dlg_tramos.n_nodo_inicial.setEnabled(False)

            self.dlg_tramos.ztn_inicial.setText(str(ztn_inicio))
            self.dlg_tramos.ztn_inicial.setEnabled(False)

            self.dlg_tramos.tipo_z_inicial.setCurrentIndex(self.dlg_tramos.tipo_z_inicial.findText(str(tipo_z)))
            self.dlg_tramos.tipo_z_inicial.setEnabled(False)

            #muestro las ventanas
            res = self.dlg_tramos.exec_()

            #debo seleccionar el tipo de simbolo asignado
            if res == 1:
                # elijo  el simbolo segun el simbolo que viene ya cargado
                # Guardo las Variables del nodo inicial
                self.n_nodo_inicial = self.dlg_tramos.n_nodo_inicial.text()
                self.tipo_z_inicial = self.dlg_tramos.tipo_z_inicial.currentText()
                self.ztn_inicial = self.dlg_tramos.ztn_inicial.text()

                if res_exists_symbol_inicio != False:
                    self.evalButtonSymbolInicio(res_exists_symbol_inicio['ty_sym'])

                    #guardo el tipo de simbolo al inicio
                    res_2 = self.dlg_symbol_inicio.exec_()

                    if res_2 == 1:

                        self.tipo_simbol_inicio = self.optioninicioChecked()

                        #simbolo al final
                        res_3 = self.dlg_nodo_final.exec_()

                        if res_3 == 1:
                            # guardo las variables del nodo final
                            self.n_nodo_final = self.dlg_nodo_final.n_nodo_final.text()
                            self.tipo_z_final = self.dlg_nodo_final.tipo_z_final.currentText()
                            self.ztn_final = self.dlg_nodo_final.ztn_final.text()

                            res_4 = self.dlg_symbol_final.exec_()

                            if res_4 == 1:
                                # Guardo el tipo de simbologia al final
                                self.tipo_simbol_final = self.optionFinalChecked()

                                # seteo los textos que ya tengo en el dlg.resumen
                                id_tr = str(self.cl_tramos_entity.getIdTramo(tramo_select))
                                self.longitud_linea = self.cl_tramos_entity.getLongitudTramo(tramo_select)

                                # Cargo lo datos al form resumen
                                self.setInfoResumenFinal(id_tr, self.n_nodo_inicial, self.n_nodo_final,
                                                         self.tipo_simbol_inicio, self.tipo_simbol_final,
                                                         self.longitud_linea)

                                res_5 = self.dlg_resumen_final.exec_()

                                if (res_5 == 1):
                                    # Obtengo los parametros del form Resumen
                                    self.tipo_material = self.optionResumenChecked()
                                    self.nro_conforme = self.dlg_resumen_final.nro_conforme.text()
                                    self.cota_cano_inicio = self.dlg_resumen_final.cota_cano_inicio.text()
                                    self.cota_cano_final = self.dlg_resumen_final.cota_cano_final.text()
                                    self.diametro = self.dlg_resumen_final.diametro.text()
                                    self.cb_tipo_tramo = self.dlg_resumen_final.cb_tipo_tramo.currentText()

                                    # proceso el tramo
                                    self.tramosActionProcess(tramo_select)


    def showBoxWithFinalData(self, tramo_select):

        res_exists_symbol_final = self.cl_nodo_symbol_entity.getExistSymbolFinal(tramo_select)

        if res_exists_symbol_final != False:
            print(res_exists_symbol_final['ty_sym'])
        # if res_exists_symbol_inicio != False:
        # cargo los box con los datos del cl_nodos
        feat = self.cl_nodos_entity.getFinalNodoByTramoTouches(tramo_select)
        if feat != False:
            # ya tengo el CL_NODO
            n_nod_final = feat['n_nod']
            ztn_final = feat['ztn']
            tipo_z_final = feat['ty_z']

            # muestro las ventanas
            res = self.dlg_tramos.exec_()

            # debo seleccionar el tipo de simbolo asignado
            if res == 1:
                # Guardo las Variables del nodo inicial
                self.n_nodo_inicial = self.dlg_tramos.n_nodo_inicial.text()
                self.tipo_z_inicial = self.dlg_tramos.tipo_z_inicial.currentText()
                self.ztn_inicial = self.dlg_tramos.ztn_inicial.text()

                #guardo el tipo de simbolo al inicio
                res_2 = self.dlg_symbol_inicio.exec_()

                if res_2 == 1:

                    self.tipo_simbol_inicio = self.optioninicioChecked()

                    # guardo las variables del nodo final recuperando los datos desde el FEAT
                    self.dlg_nodo_final.n_nodo_final.setText(str(n_nod_final))
                    self.dlg_nodo_final.ztn_final.setText(str(ztn_final))
                    self.dlg_nodo_final.tipo_z_final.setCurrentIndex(self.dlg_nodo_final.tipo_z_final.findText(str(tipo_z_final)))

                    self.dlg_nodo_final.n_nodo_final.setEnabled(False)
                    self.dlg_nodo_final.tipo_z_final.setEnabled(False)
                    self.dlg_nodo_final.ztn_final.setEnabled(False)

                    #simbolo al final
                    res_3 = self.dlg_nodo_final.exec_()

                    if res_3 == 1:

                        self.n_nodo_final = self.dlg_nodo_final.n_nodo_final.text()
                        self.tipo_z_final = self.dlg_nodo_final.tipo_z_final.currentText()
                        self.ztn_final = self.dlg_nodo_final.ztn_final.text()

                        self.evalButtonSymbolFinal(res_exists_symbol_final['ty_sym'])

                        res_4 = self.dlg_symbol_final.exec_()

                        if res_4 == 1:
                                # Guardo el tipo de simbologia al final
                                self.tipo_simbol_final = self.optionFinalChecked()

                                # seteo los textos que ya tengo en el dlg.resumen
                                id_tr = str(self.cl_tramos_entity.getIdTramo(tramo_select))
                                self.longitud_linea = self.cl_tramos_entity.getLongitudTramo(tramo_select)

                                # Cargo lo datos al form resumen
                                self.setInfoResumenFinal(id_tr, self.n_nodo_inicial, self.n_nodo_final,
                                                         self.tipo_simbol_inicio, self.tipo_simbol_final,
                                                         self.longitud_linea)

                                res_5 = self.dlg_resumen_final.exec_()

                                if (res_5 == 1):
                                    # Obtengo los parametros del form Resumen
                                    self.tipo_material = self.optionResumenChecked()
                                    self.nro_conforme = self.dlg_resumen_final.nro_conforme.text()
                                    self.cota_cano_inicio = self.dlg_resumen_final.cota_cano_inicio.text()
                                    self.cota_cano_final = self.dlg_resumen_final.cota_cano_final.text()
                                    self.diametro = self.dlg_resumen_final.diametro.text()
                                    self.cb_tipo_tramo = self.dlg_resumen_final.cb_tipo_tramo.currentText()

                                    # proceso el tramo
                                    self.tramosActionProcess(tramo_select)


    def showBoxWithInitialAndFinalData(self, tramo_select):
        res_exists_symbol_inicio = self.cl_nodo_symbol_entity.getExistSymbolInicio(tramo_select)
        if res_exists_symbol_inicio != False:
            feat = self.cl_nodos_entity.getFinalNodoByTramoTouches(tramo_select)

            if feat != False:
                #ya tengo el CL_NODO
                n_nod = feat['n_nod']
                ztn_inicio = feat['ztn']
                tipo_z = feat['ty_z']
                self.dlg_tramos.n_nodo_inicial.setText(str(n_nod))
                self.dlg_tramos.n_nodo_inicial.setEnabled(False)

                self.dlg_tramos.ztn_inicial.setText(str(ztn_inicio))
                self.dlg_tramos.ztn_inicial.setEnabled(False)

                self.dlg_tramos.tipo_z_inicial.setCurrentIndex(self.dlg_tramos.tipo_z_inicial.findText(str(tipo_z)))
                self.dlg_tramos.tipo_z_inicial.setEnabled(False)

                # muestro las ventanas
                res = self.dlg_tramos.exec_()

                # debo seleccionar el tipo de simbolo asignado
                if res == 1:
                    # elijo  el simbolo segun el simbolo que viene ya cargado

                    if res_exists_symbol_inicio != False:
                        self.evalButtonSymbolInicio(res_exists_symbol_inicio['ty_sym'])

                        #guardo el tipo de simbolo al inicio
                        res_2 = self.dlg_symbol_inicio.exec_()
                        if res_2 == 1:

                            self.tipo_simbol_inicio = self.optioninicioChecked()
                            #obtengo los datos del Nodo Final

                            res_exists_symbol_final = self.cl_nodo_symbol_entity.getExistSymbolFinal(tramo_select)

                            feat_final = self.cl_nodos_entity.getFinalNodoByTramoTouches(tramo_select)
                            if feat_final != False:
                                n_nod_final = feat_final['n_nod']
                                ztn_final = feat_final['ztn']
                                tipo_z_final = feat_final['ty_z']

                                # guardo las variables del nodo final recuperando los datos desde el FEAT
                                self.dlg_nodo_final.n_nodo_final.setText(str(n_nod_final))
                                self.dlg_nodo_final.ztn_final.setText(str(ztn_final))
                                self.dlg_nodo_final.tipo_z_final.setCurrentIndex(
                                    self.dlg_nodo_final.tipo_z_final.findText(str(tipo_z_final)))

                                self.dlg_nodo_final.n_nodo_final.setEnabled(False)
                                self.dlg_nodo_final.tipo_z_final.setEnabled(False)
                                self.dlg_nodo_final.ztn_final.setEnabled(False)

                                # simbolo al final
                                res_3 = self.dlg_nodo_final.exec_()

                                if res_3 == 1:
                                    self.n_nodo_final = self.dlg_nodo_final.n_nodo_final.text()
                                    self.tipo_z_final = self.dlg_nodo_final.tipo_z_final.currentText()
                                    self.ztn_final = self.dlg_nodo_final.ztn_final.text()

                                    self.evalButtonSymbolFinal(res_exists_symbol_final['ty_sym'])

                                    res_4 = self.dlg_symbol_final.exec_()

                                    if res_4 == 1:
                                        # Guardo el tipo de simbologia al final
                                        self.tipo_simbol_final = self.optionFinalChecked()

                                        # seteo los textos que ya tengo en el dlg.resumen
                                        id_tr = str(self.cl_tramos_entity.getIdTramo(tramo_select))
                                        self.longitud_linea = self.cl_tramos_entity.getLongitudTramo(tramo_select)

                                        # Cargo lo datos al form resumen
                                        self.setInfoResumenFinal(id_tr, self.n_nodo_inicial, self.n_nodo_final,
                                                                 self.tipo_simbol_inicio, self.tipo_simbol_final,
                                                                 self.longitud_linea)

                                        res_5 = self.dlg_resumen_final.exec_()

                                        if (res_5 == 1):
                                            # Obtengo los parametros del form Resumen
                                            self.tipo_material = self.optionResumenChecked()
                                            self.nro_conforme = self.dlg_resumen_final.nro_conforme.text()
                                            self.cota_cano_inicio = self.dlg_resumen_final.cota_cano_inicio.text()
                                            self.cota_cano_final = self.dlg_resumen_final.cota_cano_final.text()
                                            self.diametro = self.dlg_resumen_final.diametro.text()
                                            self.cb_tipo_tramo = self.dlg_resumen_final.cb_tipo_tramo.currentText()

                                            # proceso el tramo
                                            self.tramosActionProcess(tramo_select)


    def evalButtonSymbolInicio(self, symbol):

        self.dlg_symbol_inicio.rb_inicio_brs.setEnabled(False)

        if symbol == "PLD":
            self.dlg_symbol_inicio.rb_inicio_pld.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(False)

        elif symbol == "DES":
            self.dlg_symbol_inicio.rb_inicio_des.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(False)

        elif symbol == "CAL":
            self.dlg_symbol_inicio.rb_inicio_cal.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(False)

        elif symbol == "BRV":
            self.dlg_symbol_inicio.rb_inicio_brv.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(True)
            self.dlg_symbol_inicio.rb_inicio_brs.setEnabled(True)

        elif symbol == "BRS":
            self.dlg_symbol_inicio.rb_inicio_brs.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(True)
            self.dlg_symbol_inicio.rb_inicio_brs.setEnabled(True)

        elif symbol == "ESE":
            self.dlg_symbol_inicio.rb_inicio_ese.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(False)

        elif symbol == "BRH":
            self.dlg_symbol_inicio.rb_inicio_brh.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(False)

        elif symbol == "TIL":
            self.dlg_symbol_inicio.rb_inicio_til.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(False)

        elif symbol == "Nada":
            self.dlg_symbol_inicio.rb_inicio_nada.setChecked(True)
            self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(False)

        #desbloqueo el boton de aceptar
        self.dlg_symbol_inicio.ok.setEnabled(True)

        #Bloquear todos los botones
        self.dlg_symbol_inicio.rb_inicio_pld.setEnabled(False)
        self.dlg_symbol_inicio.rb_inicio_des.setEnabled(False)
        self.dlg_symbol_inicio.rb_inicio_cal.setEnabled(False)

        self.dlg_symbol_inicio.rb_inicio_ese.setEnabled(False)
        self.dlg_symbol_inicio.rb_inicio_brh.setEnabled(False)
        self.dlg_symbol_inicio.rb_inicio_til.setEnabled(False)
        self.dlg_symbol_inicio.rb_inicio_nada.setEnabled(False)

    def evalButtonSymbolFinal(self, symbol):
        if symbol == "PLD":
            self.dlg_symbol_final.rb_final_pld.setChecked(True)

        elif symbol == "DES":
            self.dlg_symbol_final.rb_final_des.setChecked(True)

        elif symbol == "CAL":
            self.dlg_symbol_final.rb_final_cal.setChecked(True)

        elif symbol == "BRV":
            self.dlg_symbol_final.rb_final_brv.setChecked(True)

        elif symbol == "BRS":
            self.dlg_symbol_final.rb_final_brs.setChecked(True)

        elif symbol == "ESE":
            self.dlg_symbol_final.rb_final_ese.setChecked(True)

        elif symbol == "BRH":
            self.dlg_symbol_final.rb_final_brh.setChecked(True)

        elif symbol == "TIL":
            self.dlg_symbol_final.rb_final_til.setChecked(True)

        elif symbol == "Nada":
            self.dlg_symbol_final.rb_final_nada.setChecked(True)

        #desbloqueo el boton de aceptar
        self.dlg_symbol_final.ok.setEnabled(True)

        self.dlg_symbol_final.rb_final_pld.setEnabled(False)
        self.dlg_symbol_final.rb_final_des.setEnabled(False)
        self.dlg_symbol_final.rb_final_cal.setEnabled(False)
        self.dlg_symbol_final.rb_final_brv.setEnabled(False)
        self.dlg_symbol_final.rb_final_brs.setEnabled(False)
        self.dlg_symbol_final.rb_final_ese.setEnabled(False)
        self.dlg_symbol_final.rb_final_brh.setEnabled(False)
        self.dlg_symbol_final.rb_final_til.setEnabled(False)
        self.dlg_symbol_final.rb_final_nada.setEnabled(False)

    def resetDialogs(self):

        self.dlg_tramos.n_nodo_inicial.setEnabled(True)
        self.dlg_tramos.ztn_inicial.setEnabled(True)
        self.dlg_tramos.tipo_z_inicial.setEnabled(True)

        self.dlg_symbol_inicio.rb_inicio_pld.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_des.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_cal.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_brv.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_brs.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_ese.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_brh.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_til.setEnabled(True)
        self.dlg_symbol_inicio.rb_inicio_nada.setEnabled(True)

        self.dlg_symbol_inicio.rb_inicio_pld.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_des.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_cal.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_brv.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_brs.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_ese.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_brh.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_til.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_nada.setChecked(True)

        self.n_nodo_final = self.dlg_nodo_final.n_nodo_final.setEnabled(True)
        self.tipo_z_final = self.dlg_nodo_final.tipo_z_final.setEnabled(True)
        self.ztn_final = self.dlg_nodo_final.ztn_final.setEnabled(True)

        self.dlg_symbol_final.rb_final_pld.setEnabled(True)
        self.dlg_symbol_final.rb_final_des.setEnabled(True)
        self.dlg_symbol_final.rb_final_cal.setEnabled(True)
        self.dlg_symbol_final.rb_final_brv.setEnabled(True)
        self.dlg_symbol_final.rb_final_brs.setEnabled(True)
        self.dlg_symbol_final.rb_final_ese.setEnabled(True)
        self.dlg_symbol_final.rb_final_brh.setEnabled(True)
        self.dlg_symbol_final.rb_final_til.setEnabled(True)
        self.dlg_symbol_final.rb_final_nada.setEnabled(True)

        self.dlg_symbol_final.rb_final_pld.setChecked(False)
        self.dlg_symbol_final.rb_final_des.setChecked(False)
        self.dlg_symbol_final.rb_final_cal.setChecked(False)
        self.dlg_symbol_final.rb_final_brv.setChecked(False)
        self.dlg_symbol_final.rb_final_brs.setChecked(False)
        self.dlg_symbol_final.rb_final_ese.setChecked(False)
        self.dlg_symbol_final.rb_final_brh.setChecked(False)
        self.dlg_symbol_final.rb_final_til.setChecked(False)
        self.dlg_symbol_final.rb_final_nada.setChecked(True)

    def tramosActionProcess(self, tramo_select):

        # evaluo si hay un simbolo al inicio del tramo
        res_exists_symbol_inicio = self.cl_nodo_symbol_entity.getExistSymbolInicio(tramo_select)
        res_exists_symbol_final = self.cl_nodo_symbol_entity.getExistSymbolFinal(tramo_select)
        res_inicio = False

        # Evaluo el tipo de simbolo al inicio
        if self.tipo_simbol_inicio == "BRV":

            # Proceso el inicio segun la respuesta devuelta (devuelve el FEAT si encontro un punto al inicio)
            if res_exists_symbol_inicio != False:
                # me devolvio un feature

                if res_exists_symbol_inicio['ty_sym'] == "Nada":
                    res_add_point = self.cl_nodo_symbol_entity.addNodoSymbol(tramo_select, "BRV", True)
                    last_point_sym_add = self.cl_nodo_symbol_entity.getLastPointAdded()
                    res_inicio = self.cl_tramos_entity.assignSymbolToInicio(last_point_sym_add, tramo_select)

                else:

                    res_inicio = self.cl_tramos_entity.assignSymbolToInicio(res_exists_symbol_inicio, tramo_select)

                # Agrego la ventilacion
                res_vent = self.cl_ventilacion_entity.addVentilacion(tramo_select)

                if res_vent != False:
                    self.actionsPropertiesTramoBrv(tramo_select)
            else:

                res_add_point = self.cl_nodo_symbol_entity.addNodoSymbol(tramo_select, "BRV", True)

                if res_add_point:
                    # si es True asigno el id al tramo
                    last_point_sym_add = self.cl_nodo_symbol_entity.getLastPointAdded()

                    res_inicio = self.cl_tramos_entity.assignSymbolToInicio(last_point_sym_add, tramo_select)

                    # Agrego la ventilacion
                    res_vent = self.cl_ventilacion_entity.addVentilacion(tramo_select)

                    if res_vent != False:
                        self.actionsPropertiesTramoBrv(tramo_select)

            #proceso el punto final si res_inicio es True
            if res_inicio:

                if res_exists_symbol_final != False:
                    res_final = self.cl_tramos_entity.assignSymbolToFinal(res_exists_symbol_final, tramo_select)
                else:
                    res_add_point = self.cl_nodo_symbol_entity.addNodoSymbol(tramo_select, self.tipo_simbol_final,
                                                                             False)
                    if res_add_point:
                        last_point_sym = self.cl_nodo_symbol_entity.getLastPointAdded()
                        res_final = self.cl_tramos_entity.assignSymbolToFinal(last_point_sym, tramo_select)

            #proceso la direccion
            if res_final:
                if self.cl_direction.addDirection(tramo_select):
                    self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", level=QgsMessageBar.INFO)
        elif self.tipo_simbol_inicio == "BRS" or self.tipo_simbol_inicio == "CAL" or self.tipo_simbol_inicio == "ESE" or self.tipo_simbol_inicio == "BRH":

            if res_exists_symbol_inicio != False:
                res_inicio = self.cl_tramos_entity.assignSymbolToInicio(res_exists_symbol_inicio, tramo_select)
                if res_inicio:
                    self.actionsPropertiesTramoOtros(tramo_select)

            else:
                res_add_point = self.cl_nodo_symbol_entity.addNodoSymbol(tramo_select, self.tipo_simbol_inicio, True)
                if res_add_point:
                    last_point_sym_add = self.cl_nodo_symbol_entity.getLastPointAdded()
                    res_inicio = self.cl_tramos_entity.assignSymbolToInicio(last_point_sym_add, tramo_select)

                    if res_inicio:
                        self.actionsPropertiesTramoOtros(tramo_select)

            #ahora proceso el vertice final si el inicio fue exitoso en todo el proceso
            if res_inicio == True:
                if res_exists_symbol_final != False:
                    res_final = self.cl_tramos_entity.assignSymbolToFinal(res_exists_symbol_final, tramo_select)

                else:
                    res_add_point = self.cl_nodo_symbol_entity.addNodoSymbol(tramo_select, self.tipo_simbol_final,
                                                                             False)
                    if res_add_point:
                        last_point_sym = self.cl_nodo_symbol_entity.getLastPointAdded()
                        res_final = self.cl_tramos_entity.assignSymbolToFinal(last_point_sym, tramo_select)
            if res_final:
                if self.cl_direction.addDirection(tramo_select):
                    self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", level=QgsMessageBar.INFO)

        elif self.tipo_simbol_inicio == "Nada":
            res_add_point = self.cl_nodo_symbol_entity.addNodoSymbol(tramo_select, self.tipo_simbol_inicio, True)
            if res_add_point:
                # si es True asigno el id al tramo
                last_point_sym_add = self.cl_nodo_symbol_entity.getLastPointAdded()
                res_inicio = self.cl_tramos_entity.assignSymbolToInicio(last_point_sym_add, tramo_select)
                if res_inicio:
                    self.actionsPropertiesTramoOtros(tramo_select)

            if res_inicio == True:
                if res_exists_symbol_final != False:
                    res_final = self.cl_tramos_entity.assignSymbolToFinal(res_exists_symbol_final, tramo_select)

                else:
                    res_add_point = self.cl_nodo_symbol_entity.addNodoSymbol(tramo_select, self.tipo_simbol_final,
                                                                             False)
                    if res_add_point:
                        last_point_sym = self.cl_nodo_symbol_entity.getLastPointAdded()
                        res_final = self.cl_tramos_entity.assignSymbolToFinal(last_point_sym, tramo_select)
            if res_final:
                if self.cl_direction.addDirection(tramo_select):
                    self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", level=QgsMessageBar.INFO)

    """
        -------- METODO QUE PROCESA EL TRAMO
        Recibe FALSE si ya hay un cl_nodo y solo necesito actualizar los datos contenidos en el, sino me lo duplica
    """

    def actionsPropertiesTramoBrv(self, tramo_select):

        # Agrego el vertice al tramo
        if self.cl_tramos_entity.addVertexToLine(tramo_select):

            #cargo las propiedades al tramo
            if self.cl_tramos_entity.addAttributes(tramo_select, self.cb_tipo_tramo, self.longitud_linea, self.diametro,
                                                   self.tipo_material, self.nro_conforme):
                #EVALUO SI HAY UN FEAT, ASI ACTUALIZO O AGREGO

                res_cl_nodos = self.cl_nodos_entity.addNodosWithCompletedData(tramo_select, self.ztn_inicial, self.n_nodo_inicial, self.n_nodo_inicial, self.tipo_z_inicial,
                                                               self.ztn_final, self.n_nodo_final, self.n_nodo_final, self.tipo_z_final, self.cl_nodos_etiqueta_entity,
                                                               self.layer_cl_nodos_tramos, self.cl_nodos_tramos_entity)
                if res_cl_nodos:
                    if self.cl_nodos_etiqueta_entity.addNodoEtiquetaToInicio(tramo_select, self.cl_nodos_entity):
                        if self.cl_nodos_etiqueta_entity.addNodoEtiquetaToFinal(tramo_select, self.cl_nodos_entity):
                            if self.cl_nodosetiqueta2_entity.addNodoEtiqueta2ToInicio(tramo_select, self.cl_nodos_entity):
                                if self.cl_nodosetiqueta2_entity.addNodoEtiqueta2ToFinal(tramo_select, self.cl_nodos_entity):
                                    #agrego la cota de inicio
                                    if self.cl_cotas_entity.addCotaInicio(tramo_select, self.cota_cano_inicio, self.cl_nodos_entity):
                                        self.cl_cotas_entity.addCotaFinal(tramo_select, self.cota_cano_final, self.cl_nodos_entity)

    def actionsPropertiesTramoOtros(self, tramo_select):
        res_cl_nodos = self.cl_nodos_entity.addNodosWithCompletedData(tramo_select, self.ztn_inicial,
                                                                      self.n_nodo_inicial, self.n_nodo_inicial,
                                                                      self.tipo_z_inicial,
                                                                      self.ztn_final, self.n_nodo_final,
                                                                      self.n_nodo_final, self.tipo_z_final,
                                                                      self.cl_nodos_etiqueta_entity,
                                                                      self.layer_cl_nodos_tramos,
                                                                      self.cl_nodos_tramos_entity)

        if res_cl_nodos:
            if self.cl_nodos_etiqueta_entity.addNodoEtiquetaToInicio(tramo_select, self.cl_nodos_entity):
                if self.cl_nodos_etiqueta_entity.addNodoEtiquetaToFinal(tramo_select, self.cl_nodos_entity):
                    if self.cl_nodosetiqueta2_entity.addNodoEtiqueta2ToInicio(tramo_select, self.cl_nodos_entity):
                        if self.cl_nodosetiqueta2_entity.addNodoEtiqueta2ToFinal(tramo_select, self.cl_nodos_entity):
                            # agrego la cota de inicio
                            if self.cl_cotas_entity.addCotaInicio(tramo_select, self.cota_cano_inicio,
                                                                  self.cl_nodos_entity):
                                if self.cl_cotas_entity.addCotaFinal(tramo_select, self.cota_cano_final,
                                                                  self.cl_nodos_entity):
                                    self.cl_tramos_entity.addAttributes(tramo_select, self.cb_tipo_tramo,
                                                                        self.longitud_linea, self.diametro,
                                                                        self.tipo_material, self.nro_conforme)
    


    """
        ------METODOS QUE AFECTAMN A LOS FORMS
    """
    
    def optioninicioChecked(self):
        
        if self.dlg_symbol_inicio.rb_inicio_brv.isChecked():
            
            self.dlg_symbol_final.rb_final_pld.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_cal.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_brv.setEnabled(False)
            self.dlg_symbol_final.rb_final_ese.setEnabled(False)
            self.dlg_symbol_final.rb_final_brh.setEnabled(False)
            
            return self.dlg_symbol_inicio.rb_inicio_brv.text()
        
        elif self.dlg_symbol_inicio.rb_inicio_brs.isChecked():
          
            self.dlg_symbol_final.rb_final_brv.setEnabled(False)
            self.dlg_symbol_final.rb_final_pld.setEnabled(True)
            self.dlg_symbol_final.rb_final_des.setEnabled(True)
            self.dlg_symbol_final.rb_final_cal.setEnabled(True)
            self.dlg_symbol_final.rb_final_des.setEnabled(True)
            self.dlg_symbol_final.rb_final_ese.setEnabled(True)
            self.dlg_symbol_final.rb_final_brh.setEnabled(True)

            return self.dlg_symbol_inicio.rb_inicio_brs.text()
        
        elif self.dlg_symbol_inicio.rb_inicio_nada.isChecked():
       
            return self.dlg_symbol_inicio.rb_inicio_nada.text()
        
        elif self.dlg_symbol_inicio.rb_inicio_cal.isChecked():
            
            self.dlg_symbol_final.rb_final_pld.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_cal.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_brv.setEnabled(False)
            self.dlg_symbol_final.rb_final_ese.setEnabled(False)
            self.dlg_symbol_final.rb_final_brh.setEnabled(False)
       
            return self.dlg_symbol_inicio.rb_inicio_cal.text()
        
        elif self.dlg_symbol_inicio.rb_inicio_ese.isChecked():
            
            self.dlg_symbol_final.rb_final_pld.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_cal.setEnabled(False)
            self.dlg_symbol_final.rb_final_brv.setEnabled(False)
            self.dlg_symbol_final.rb_final_ese.setEnabled(False)
            self.dlg_symbol_final.rb_final_brh.setEnabled(True)
       
            return self.dlg_symbol_inicio.rb_inicio_ese.text()

        elif self.dlg_symbol_inicio.rb_inicio_brh.isChecked():
            self.dlg_symbol_final.rb_final_pld.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(True)
            self.dlg_symbol_final.rb_final_cal.setEnabled(False)
            self.dlg_symbol_final.rb_final_brv.setEnabled(False)
            self.dlg_symbol_final.rb_final_ese.setEnabled(False)
            self.dlg_symbol_final.rb_final_brh.setEnabled(False)

            return self.dlg_symbol_inicio.rb_inicio_brh.text()

    def optionFinalChecked(self):
        if self.dlg_symbol_final.rb_final_brs.isChecked():
            return self.dlg_symbol_final.rb_final_brs.text()
        
        elif self.dlg_symbol_final.rb_final_nada.isChecked():
            return self.dlg_symbol_final.rb_final_nada.text()
        
        elif self.dlg_symbol_final.rb_final_ese.isChecked():
            return self.dlg_symbol_final.rb_final_ese.text()
        
        elif self.dlg_symbol_final.rb_final_brh.isChecked():
            return self.dlg_symbol_final.rb_final_brh.text()
        
        elif self.dlg_symbol_final.rb_final_des.isChecked():
            return self.dlg_symbol_final.rb_final_des.text()
    
    def optionResumenChecked(self):
        if self.dlg_resumen_final.br_sd.isChecked():
            return self.dlg_resumen_final.br_sd.text()
        elif self.dlg_resumen_final.br_pvc.isChecked():
            return self.dlg_resumen_final.br_pvc.text()
        elif self.dlg_resumen_final.br_ff.isChecked():
            return self.dlg_resumen_final.br_ff.text()
        elif self.dlg_resumen_final.br_fg.isChecked():
            return self.dlg_resumen_final.br_fg.text()
        elif self.dlg_resumen_final.br_fd.isChecked():
            return self.dlg_resumen_final.br_fd.text()
        elif self.dlg_resumen_final.br_ha.isChecked():
            return self.dlg_resumen_final.br_ha.text()
        elif self.dlg_resumen_final.br_hc.isChecked():
            return self.dlg_resumen_final.br_hc.text()
        elif self.dlg_resumen_final.br_hs.isChecked():
            return self.dlg_resumen_final.br_hs.text()
        elif self.dlg_resumen_final.br_a.isChecked():
            return self.dlg_resumen_final.br_a.text()
        elif self.dlg_resumen_final.br_ac.isChecked():
            return self.dlg_resumen_final.br_ac.text()
        elif self.dlg_resumen_final.br_vi.isChecked():
            return self.dlg_resumen_final.br_vi.text()
        elif self.dlg_resumen_final.br_pe.isChecked():
            return self.dlg_resumen_final.br_pe.text()
        elif self.dlg_resumen_final.br_pead.isChecked():
            return self.dlg_resumen_final.br_pead.text()
        elif self.dlg_resumen_final.br_pp.isChecked():
            return self.dlg_resumen_final.br_pp.text()
        elif self.dlg_resumen_final.br_mam.isChecked():
            return self.dlg_resumen_final.br_mam.text()

    def resetAllForms(self):
        
        self.dlg_tramos.n_nodo_inicial.clear() 
        self.dlg_tramos.ztn_inicial.clear()
        
        self.dlg_tramos.tipo_z_inicial.setCurrentIndex(0)
        self.dlg_nodo_final.n_nodo_final.clear()
        self.dlg_nodo_final.ztn_final.clear()
        self.dlg_nodo_final.tipo_z_final.setCurrentIndex(0)
        
        self.dlg_resumen_final.nro_conforme.clear()
        self.dlg_resumen_final.cota_cano_inicio.clear()
        self.dlg_resumen_final.cota_cano_final.clear()
        self.dlg_resumen_final.diametro.clear()
        
        self.dlg_symbol_inicio.ok.setEnabled(False)
        self.dlg_symbol_final.ok.setEnabled(False)

    def setEnabledOkButtonInicio(self):
        self.dlg_symbol_inicio.ok.setEnabled(True)
    
    def setEnabledOkButtonFinal(self):
        self.dlg_symbol_final.ok.setEnabled(True)
        
    def setInfoResumenFinal(self, id_tramo, nro_rel_inicio, nro_rel_final, tipo_sim_inicio, tipo_sim_final, longitud_linea):
        
        self.dlg_resumen_final.id_tramo_text.setText(id_tramo)
        self.dlg_resumen_final.nro_rel_inicio.setText(nro_rel_inicio)
        self.dlg_resumen_final.nro_rel_final.setText(nro_rel_final)
        self.dlg_resumen_final.tipo_sim_inicio.setText(tipo_sim_inicio)
        self.dlg_resumen_final.tipo_sim_final.setText(tipo_sim_final)
        self.dlg_resumen_final.longitud_linea.setText(str(longitud_linea))