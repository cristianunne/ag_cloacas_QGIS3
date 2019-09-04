from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *

from .ClNodosTramosEntity import ClNodosTramosEntity



class ClNodosEntity():
    
    def __init__(self):
       
       self.cl_nodos_layer = None
       
    
    def initialize(self, cl_nodos_layer):
        
        self.cl_nodos_layer = cl_nodos_layer

    def addNodos(self, tramo_select, ztn_1, n_nod_1, n_rel_1, ty_z_1, ztn_2, cl_nodos_etiqueta_entity,
                 cl_nodos_tramos_layer):

        if ztn_1 == None or ztn_1 == "":
            ztn_1 = None

        if ztn_2 == None or ztn_2 == "":
            ztn_2 = None

        id_tramo = tramo_select['gid']

        # booro los que existen y los creo nuevamente

        array = []
        for feat in self.cl_nodos_layer.getFeatures():

            if feat["tramo_idtramo"] == id_tramo:
                array.append(feat.id())

        if len(array) > 0:
            self.cl_nodos_layer.startEditing()
            if self.cl_nodos_layer.deleteFeatures(array):

                self.cl_nodos_layer.commitChanges()
            else:
                self.cl_nodos_layer.rollback()

        # Ya borre los elementos procedo a agregarlos nuevamente

        vertices = tramo_select.geometry().asMultiPolyline()[0]

        features = []

        # creo el arreglo vacion con la dimension de los atributos
        attrs = [None] * len(self.cl_nodos_layer.fields())

        idx_idtramo = self.cl_nodos_layer.fieldNameIndex("tramo_idtramo")
        idx_ztn = self.cl_nodos_layer.fieldNameIndex("ztn")
        idx_n_nod = self.cl_nodos_layer.fieldNameIndex("n_nod")
        idx_n_rel = self.cl_nodos_layer.fieldNameIndex("n_rel")
        idx_ty_z = self.cl_nodos_layer.fieldNameIndex("ty_z")

        attrs[idx_idtramo] = id_tramo

        num_vert = len(vertices)
        i = 0
        create_feat = False

        cl_nodos_tramos_entity = ClNodosTramosEntity()
        cl_nodos_tramos_entity.initialize(cl_nodos_tramos_layer)

        for ver in vertices:
            feat = QgsFeature()

            # consulto si existe un nodo en la posicion del vertice
            feat_return = self.getExistNodo(ver)

            if feat_return != False:

                # Si me devuelve un punto lo consulto si es 0 y agrego del punto nuevo.... Tambien agrego la referencia a la tabla de claves
                # Consulto si estoy en el primer vertice para agregar el valor ztn_1 o si estoy en el ultimo agrego ztn2
                if i == 0:

                    # pROCESO PORQUE ESTOY EN EL PRIMER VERTICE ---- Accedo al valor del feat
                    if feat_return["ztn"] == None or feat_return["ztn"] == 0:
                        self.cl_nodos_layer.startEditing()

                        self.cl_nodos_layer.changeAttributeValue(feat_return.id(), idx_ztn, ztn_1, n_nod_1, n_rel_1,
                                                                 ty_z_1)
                        self.cl_nodos_layer.commitChanges()
                        # Cambio el valor de la etiqueta
                        cl_nodos_etiqueta_entity.setAttributeById(feat_return.id(), ztn_1, id_tramo)

                        # aGREGO LA REFERENCIA DEL NODO A LA TBALA DE CLAVES FORANEAS
                    else:

                        cl_nodos_etiqueta_entity.setAttributeById(feat_return.id(), feat_return["ztn"], id_tramo)


                elif i == (num_vert - 1):

                    if feat_return["ztn"] == None or feat_return["ztn"] == 0:
                        self.cl_nodos_layer.startEditing()
                        self.cl_nodos_layer.changeAttributeValue(feat_return.id(), idx_ztn, ztn_2)
                        self.cl_nodos_layer.commitChanges()
                        # Cambio el valor de la etiqueta
                        cl_nodos_etiqueta_entity.setAttributeById(feat_return.id(), ztn_2, id_tramo)

                        # aGREGO LA REFERENCIA DEL NODO A LA TBALA DE CLAVES FORANEAS

                    else:

                        # Cambio el valor de la etiqueta
                        cl_nodos_etiqueta_entity.setAttributeById(feat_return.id(), feat_return["ztn"], id_tramo)

            else:
                # Como no enncontre ningun punto agrego no mas
                if i == 0:
                    if ztn_1 == "":
                        ztn_1 = None
                    attrs[idx_ztn] = ztn_1


                elif i == (num_vert - 1):
                    if ztn_2 == "":
                        ztn_2 = None
                    attrs[idx_ztn] = ztn_2


                else:
                    attrs[idx_ztn] = None

                create_feat = True
                feat.setGeometry(QgsGeometry().fromPoint(ver))
                feat.setAttributes(attrs)

                features.append(feat)

            i = i + 1
        if create_feat == True:

            for feat_ in features:
                self.cl_nodos_layer.startEditing()

                res = self.cl_nodos_layer.addFeature(feat_)

                if res:

                    if self.cl_nodos_layer.commitChanges():

                        # Agrego tambien en la etiqueta
                        # Primero obtengo el ultimo punto agregado
                        last_feat_Add = self.getLastPointAdded()

                        cl_nodos_etiqueta_entity.addNodo(last_feat_Add.id(), id_tramo, last_feat_Add["ztn"],
                                                         last_feat_Add.geometry().asPoint())


                    else:
                        self.cl_nodos_layer.rollBack()
                        return False
                else:
                    return False
        else:

            return True

        return True

    def addNodosWithData(self, vertice, id_tramo, ztn_1, n_nod_1, n_rel_1, ty_z_1, cl_nodos_tramos_entity):

        attrs = [None] * len(self.cl_nodos_layer.fields())

        idx_idtramo = self.cl_nodos_layer.fieldNameIndex("tramo_idtramo")
        idx_ztn = self.cl_nodos_layer.fieldNameIndex("ztn")
        idx_n_nod = self.cl_nodos_layer.fieldNameIndex("n_nod")
        idx_n_rel = self.cl_nodos_layer.fieldNameIndex("n_rel")
        idx_ty_z = self.cl_nodos_layer.fieldNameIndex("ty_z")
        #cargo los atributos

        attrs[idx_idtramo] = id_tramo
        attrs[idx_ztn] = ztn_1
        attrs[idx_n_nod] = n_nod_1
        attrs[idx_n_rel] = n_rel_1
        attrs[idx_ty_z] = ty_z_1

        #consulto si existen nodos en la posicion de los vertices
        #si No existen los creo y si existen solo agrego la refeerencia a la tabla
        res_exist_nodo = False

        for nodo in self.cl_nodos_layer.getFeatures():
            if nodo == vertice:
                #agrego la referencia a la tabla
                if self.createNodo(nodo, cl_nodos_tramos_entity):
                    res_exist_nodo = True
                    return True

        if res_exist_nodo == False:
            #creo el cl_nodo
                pass

    def addNodosWithCompletedData(self, tramo_select, ztn_1, n_nod_1, n_rel_1, ty_z_1, ztn_2, n_nod_2, n_rel_2, ty_z_2,
                                  cl_nodos_tramos_entity):
        if ztn_1 == None or ztn_1 == "":
            ztn_1 = None

        if ztn_2 == None or ztn_2 == "":
            ztn_2 = None

        #Obtengo los vertices del Tramo
        vertices = tramo_select.geometry().asMultiPolyline()[0]

        features = []

        # creo el arreglo vacion con la dimension de los atributos
        attrs_inicio = [None] * len(self.cl_nodos_layer.fields())
        attrs_final = [None] * len(self.cl_nodos_layer.fields())
        attrs_otros = [None] * len(self.cl_nodos_layer.fields())

        #idx_idtramo = self.cl_nodos_layer.fieldNameIndex("tramo_idtramo")
        idx_ztn = self.cl_nodos_layer.fields().indexFromName("ztn")
        idx_n_nod = self.cl_nodos_layer.fields().indexFromName("n_nod")
        idx_n_rel = self.cl_nodos_layer.fields().indexFromName("n_rel")
        idx_ty_z = self.cl_nodos_layer.fields().indexFromName("ty_z")

        attrs_inicio[idx_ztn] = ztn_1
        attrs_inicio[idx_n_nod] = n_nod_1
        attrs_inicio[idx_n_rel] = n_rel_1
        attrs_inicio[idx_ty_z] = ty_z_1

        attrs_final[idx_ztn] = ztn_2
        attrs_final[idx_n_nod] = n_nod_2
        attrs_final[idx_n_rel] = n_rel_2
        attrs_final[idx_ty_z] = ty_z_2

        attrs_otros[idx_ztn] = None
        attrs_otros[idx_n_nod] = None
        attrs_otros[idx_n_rel] = None
        attrs_otros[idx_ty_z] = None

        num_vert = len(vertices)
        i = 0
        create_feat = False


        return_inicio = False
        return_final = False

        #Antes de Agregar, consulto si ya existe y ahi lo creo

        for ver in vertices:
            feat = QgsFeature()

            if i == 0:
                exists_ini = False
                features_cl_nodo_tramo = self.cl_nodos_layer.getFeatures()
                feat_cl_nodo_inicio = None

                for cl_nodo_tramo_feat in features_cl_nodo_tramo:

                    if ver == cl_nodo_tramo_feat.geometry().asPoint():
                        exists_ini = True
                        feat_cl_nodo_inicio = cl_nodo_tramo_feat
                        #Agrego solo a la tabla Foranea el DATO

                if exists_ini:
                    return_inicio = self.addReferenceToNodoTramo(cl_nodos_tramos_entity, feat_cl_nodo_inicio, tramo_select)
                else:
                    #cambio el metodo aca
                    feat.setGeometry(QgsGeometry().fromPointXY(ver))
                    feat.setAttributes(attrs_inicio)
                    features.append(feat)
                    return_inicio = self.createNodo(feat, cl_nodos_tramos_entity, tramo_select)

            elif i == (num_vert - 1):

                exists_ini_2 = False
                feat_cl_nodo_final = None

                for cl_nodo_tramo_feat in self.cl_nodos_layer.getFeatures():

                    if ver == cl_nodo_tramo_feat.geometry().asPoint():
                        exists_ini_2 = True
                        feat_cl_nodo_final = cl_nodo_tramo_feat

                if exists_ini_2:
                    return_final = self.addReferenceToNodoTramo(cl_nodos_tramos_entity, feat_cl_nodo_final, tramo_select)

                else:
                    feat.setGeometry(QgsGeometry().fromPointXY(ver))
                    feat.setAttributes(attrs_final)
                    features.append(feat)
                    return_final = self.createNodo(feat, cl_nodos_tramos_entity, tramo_select)

            else:
                #creo el nodo vacio sin atributos
                feat.setGeometry(QgsGeometry().fromPointXY(ver))
                feat.setAttributes(attrs_otros)
                features.append(feat)
                return_final = self.createNodo(feat, cl_nodos_tramos_entity, tramo_select)

            i = i + 1

        if return_inicio and return_final:
            return True
        else:
            return False

    def addReferenceToNodoTramo(self, cl_nodostramos_entity, feat, tramo_select):

        if cl_nodostramos_entity.addNodoTramo(tramo_select.id(), feat.id()):
            return True
        else:
            return False

    def createNodo(self, feat, cl_nodostramos_entity, tramo_select):

        self.cl_nodos_layer.startEditing()

        res = self.cl_nodos_layer.addFeature(feat)

        if res:

            if self.cl_nodos_layer.commitChanges():

                #Agregar el Nodo a la Tabla que mantiene la Relacion

                feat_last = self.getLastPointAdded()

                if cl_nodostramos_entity.addNodoTramo(tramo_select.id(), feat_last.id()):

                    return True
            else:
                self.cl_nodos_layer.rollBack()
                return False
        else:
            return False



    
    def getExistNodo(self, point):
        #recorro la capa de cl_nodos
        for feat in self.cl_nodos_layer.getFeatures():
        
            p = feat.geometry().asPoint()
            
            if p == point:
                return feat
           
        return False
        

    """
        Para Borrar debo considerar consultar la tabla que tiene las asociaciones y despues borrar
    """
    def deleteNodos(self, tramo_select, cl_nodos_tramos_layer):

        """recorro el layer_cl_nodos_tramos y me fijo si el tramo selct que quiero borrar solo esta 1 vez
            De lo contrario solo elimino las referencias en la tabla CL_NODOS_TRAMOs
        """
        cl_nodos_tramos_entity = ClNodosTramosEntity()
        cl_nodos_tramos_entity.initialize(cl_nodos_tramos_layer)
        
        devolver = True
        
        #obtengo el id del tramo
        id_tramo = tramo_select.id()
         
        
        #recorro el layer nodo y obtengo el id de los nodos que tiene el tramo seleccionado
        
        nodos_feat = self.cl_nodos_layer.getFeatures()
        
        arre_nodos = []
        nodos_tramos_current = []
        borrar = False
        
        
        #Reorro los nodos y obtengo los feat correspondiente al tramo en cuestion
        for feat in cl_nodos_tramos_layer.getFeatures():
            
            if feat['tramo_idtramo'] == tramo_select['gid']:
                
                nodos_tramos_current.append(feat)
        
        #Recorro solamente los obtenidos en el paso anterior
        for feat in nodos_tramos_current:
            cantidad = 0
            #Recorro la tabla nodos otra vez y verifico ese nodo cuantas veces esta
            for feat_nodos_layer in cl_nodos_tramos_layer.getFeatures():
                #consulto por su id
                if feat['cl_nodos_id_cl_nodos'] == feat_nodos_layer['cl_nodos_id_cl_nodos']:
                    cantidad = cantidad + 1
            
            #evaluo cantidad y proceso
            if cantidad == 1:
                #con los id recorro el layer y los borro
                self.cl_nodos_layer.startEditing()
                
                id_nodo = None
                #RECORRO LA CAPA NODOS Y OBTENGO EL CORRESPONDIENTE
                for feat_nodo in self.cl_nodos_layer.getFeatures():
                    if feat['cl_nodos_id_cl_nodos'] == feat_nodo['gid']:
                        id_nodo = feat_nodo.id()
                    
                
            
                res = self.cl_nodos_layer.deleteFeature(id_nodo)
         
            
                if res:
                
                    if self.cl_nodos_layer.commitChanges():
                        pass
                    
                    else:
                         self.cl_nodos_layer.rollBack()
                         devolver = False
                 
                
                
                
                 #debo borrar en la tabla Foranea
                for feat_nodos_layer in cl_nodos_tramos_layer.getFeatures():
                    #consulto por su id
                    if feat['cl_nodos_id_cl_nodos'] == feat_nodos_layer['cl_nodos_id_cl_nodos'] and feat['tramo_idtramo'] == feat_nodos_layer['tramo_idtramo']:
                        if cl_nodos_tramos_entity.deleteNodosTramos(feat_nodos_layer):
                            pass
                        else:
                            devolver = False
                
                        
                
            elif cantidad > 1:
                #debo borrar en la tabla Foranea
                for feat_nodos_layer in cl_nodos_tramos_layer.getFeatures():
                    #consulto por su id
                    if feat['cl_nodos_id_cl_nodos'] == feat_nodos_layer['cl_nodos_id_cl_nodos'] and feat['tramo_idtramo'] == feat_nodos_layer['tramo_idtramo']:
                        if cl_nodos_tramos_entity.deleteNodosTramos(feat_nodos_layer):
                            pass
                        else:
                            devolver = False
             
        return devolver

    def getLastPointAdded(self):
        
        features = self.cl_nodos_layer.getFeatures()
        last = None
        valor = -1
        
        for feat in features:
            if feat.id() > valor:
                valor = feat.id()
                last = feat
        return last

    def getInitialNodoByTramoTouches(self, tramo_select):

        #que sucederia si toca 2 cl_nodos que puede suceder.... Capturar el Punto Inicial y ahi buscar un NODO
        vertices = tramo_select.geometry().asMultiPolyline()[0]
        i = 0
        #recorro el vertice y busco coincidencia
        for ver in vertices:


            if i == 0:
                for feat in self.cl_nodos_layer.getFeatures():

                    if ver == feat.geometry().asPoint():
                        return feat
            i = i + 1

        return False

    def getFinalNodoByTramoTouches(self, tramo_select):
        # que sucederia si toca 2 cl_nodos que puede suceder.... Capturar el Punto Inicial y ahi buscar un NODO
        vertices = tramo_select.geometry().asMultiPolyline()[0]
        i = 0
        # recorro el vertice y busco coincidencia
        for ver in vertices:
            if i == (len(vertices) - 1):
                for feat in self.cl_nodos_layer.getFeatures():

                    if ver == feat.geometry().asPoint():
                        return feat
            i = i + 1

        return False

    def getVertices(self, tramo_select):
        vertices = tramo_select.geometry().asMultiPolyline()

