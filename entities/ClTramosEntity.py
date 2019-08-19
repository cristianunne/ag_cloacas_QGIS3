from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *




class ClTramosEntity():
    
    def __init__(self):
        
        
        self.cl_tramo = None


    
    def initialize(self, cl_tramo):
        
        self.cl_tramo = cl_tramo
    

    def addAttributes(self, feat_linea, tipo, longitud, diametro, material, conforme):


        #obtengo el id del tramo
        id_tramo = feat_linea["gid"]
        
        if diametro == "":
            diametro = None
        
        #obtengo los indices de los atributos
        idx_tipo =  self.cl_tramo.fieldNameIndex("tipo")
        idx_longitud =  self.cl_tramo.fieldNameIndex("longitud")
        idx_diametro =  self.cl_tramo.fieldNameIndex("diametro")
        idx_material=  self.cl_tramo.fieldNameIndex("material")
        idx_conforme =  self.cl_tramo.fieldNameIndex("conforme")
        idx_sentido = self.cl_tramo.fieldNameIndex("sentido")

        sentido = "ft"
        
        attrs = {idx_tipo :  tipo, idx_longitud : longitud, idx_diametro : diametro, idx_material : material, idx_conforme : conforme, idx_sentido: sentido}

        #Inicio la edicion y la termino
        self.cl_tramo.startEditing()

        if  self.cl_tramo.changeAttributeValues(layer_select_tramo.id(), attrs ):
            self.cl_tramo.commitChanges()
            return True
        else:

            self.cl_tramo.rollBack()
            return False

    def addVertexToLine(self, tramo):
        #distancia ocupada para interpolar el punto
        distance = 10
        
        geom_line = tramo.geometry()
        
        #inicio la edicion del layer
        self.cl_tramo.startEditing()
        
        #Obtengo el punto de la interpolacion
        point = geom_line.interpolate(distance)
        
        #inseto el vertice
        res = geom_line.insertVertex(point.asPoint().x(), point.asPoint().y(), 1)
        
        if res:
            self.cl_tramo.changeGeometry(tramo.id(), geom_line)
            self.cl_tramo.commitChanges()
            return True
        
        self.cl_tramo.rollBack()
        return False

    def assignSymbolToInicio(self, feat_point_symbol, tramo_select):
        
        #obtengo el id del punto_symbol
        gid_point_sym = feat_point_symbol['gid']
        id_tramo = tramo_select["gid"]
        
        #obtengo los indices de las columnas
        idx_gid_sym_inicio = self.cl_tramo.fieldNameIndex("id_nodo_symbol_inicio")
        
        attrs = {idx_gid_sym_inicio :  gid_point_sym}

        # Inicio la edicion y la termino
        self.cl_tramo.startEditing()
        
        if self.cl_tramo.changeAttributeValues(id_tramo, attrs):
            self.cl_tramo.commitChanges()
            return True
        else:
            self.cl_tramo.rollBack()
            return False
    
    def assignSymbolToFinal(self, feat_point_symbol, tramo_select):
        
        #obtengo el id del punto_symbol
        gid_point_sym = feat_point_symbol['gid']
        id_tramo = tramo_select["gid"]
        
        #obtengo los indices de las columnas
        idx_gid_sym_inicio = self.cl_tramo.fieldNameIndex("id_nodo_symbol_final")
        
        attrs = {idx_gid_sym_inicio :  gid_point_sym}

        # Inicio la edicion y la termino
        self.cl_tramo.startEditing()

        if self.cl_tramo.changeAttributeValues(id_tramo, attrs):
            self.cl_tramo.commitChanges()
            return True
        else:
            self.cl_tramo.rollBack()
            return False

    def addFkToInicio(self, last_tr_inicio_add, tramo_select):
        
        #obtengo el id del punto_symbol
        gid_point = last_tr_inicio_add['gid']
        id_tramo = tramo_select["gid"]
        
        #obtengo los indices de las columnas
        idx_gid_sym_inicio = self.cl_tramo.fieldNameIndex("id_nodo_tr_inicio")
        
        attrs = {idx_gid_sym_inicio :  gid_point}

        # Inicio la edicion y la termino
        self.cl_tramo.startEditing()

        if self.cl_tramo.changeAttributeValues(id_tramo, attrs):
            self.cl_tramo.commitChanges()
            return True
        else:
            self.cl_tramo.rollBack()
            return False
    
    def addFkToFinal(self, last_tr_final_add, tramo_select):
        
         #obtengo el id del punto_symbol
        gid_point = last_tr_final_add['gid']
        id_tramo = tramo_select["gid"]
        
        #obtengo los indices de las columnas
        idx_gid_sym_final = self.cl_tramo.fieldNameIndex("id_nodo_tr_final")
        
        attrs = {idx_gid_sym_final :  gid_point}

        # Inicio la edicion y la termino
        self.cl_tramo.startEditing()
        
        if self.cl_tramo.changeAttributeValues(id_tramo, attrs):
            self.cl_tramo.commitChanges()
            return True
        else:
            self.cl_tramo.rollBack()
            return False

    def changeDirectionTramo(self, dir_select):

        sentido = None
        #reorro los tramos y selecciono segun el id
        for tramo in self.cl_tramo.getFeatures():

            if tramo.id() == dir_select['tramo_idtramo']:

                if tramo['sentido'] == 'ft':

                    sentido = 'tf'
                else:
                    sentido = 'ft'

        # obtengo los indices de las columnas
        idx_sentido = self.cl_tramo.fields().indexFromName("sentido")

        attrs = {idx_sentido: sentido}

        self.cl_tramo.startEditing()

        if self.cl_tramo.changeAttributeValues(dir_select['tramo_idtramo'], attrs):

            self.cl_tramo.commitChanges()
            return True
        else:
            self.cl_tramo.rollBack()
            return False

    def deleteTramo(self, tramo_feat):

        self.cl_tramo.startEditing()

        res = self.cl_tramo.deleteFeature(tramo_feat.id())
        if res:
            if self.cl_tramo.commitChanges():
                return True
            else:
                self.cl_tramo.rollBack()
                return False
        return False
    
    def deleteVertex(self, tramo):

        self.cl_tramo.startEditing()
        self.cl_tramo.deleteVertex(tramo.id(), 1)

        if self.cl_tramo.commitChanges():

            return True

        else:
            self.cl_tramo.rollBack()
            return False
    
    def getIdTramo(self, tramo):

        return tramo.id()

    def getLongitudTramo(self, tramo):

        long = tramo.geometry().length()

        return long

    def getVertexTramoAsPoint(self, tramo):

        #Arreglo de puntos a devolver
        points = []
        geom = tramo.geometry()
        n = 0
        #ingresa por el primer vertice
        ver = geom.vertexAt(0)
        #count vertex and extract nodes
        while(ver != QgsPoint(0,0)):

            n +=1
            points.append(ver)
            ver=geom.vertexAt(n)

        return points

    def getNumVertex(self, tramo):
        geom = tramo.geometry()
        n = 0
        #ingresa por el primer vertice
        ver = geom.vertexAt(0)
        #count vertex and extract nodes
        while(ver != QgsPoint(0,0)):
            n +=1
            ver = geom.vertexAt(n)

        return n

    def setNullData(self, tramo):

        num_attr = 8
        #modificar los atributos del 1 al 7
        self.cl_tramo.startEditing()

        for i in range(num_attr):

            if i >= 1 and i <= 7:
                self.cl_tramo.changeAttributeValue(tramo.id(), i, None)

        if self.cl_tramo.commitChanges():

            return True

        else:
            self.cl_tramo.rollBack()
            return False

    def verifiedTramo(self, tramo_select):

        id_nodo_symbol_inicio = tramo_select["id_nodo_symbol_inicio"]
        id_nodo_symbol_final = tramo_select["id_nodo_symbol_final"]

        res = False

        if id_nodo_symbol_inicio != None:
            res = True

        if id_nodo_symbol_final != None:
            res = True

        return res