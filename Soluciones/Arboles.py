class AG():
    
    def __init__(self,dato):
        self.dato=dato
        self.padre=None
        self.hijos=[]
        
    def añade_hijo(self,nodo):
        self.hijos.append(nodo)
        nodo.padre=self
        
    def es_hoja(self):
        return self.hijos==[]
    
    def __repr__(self):
        return self._imprime_arbol()

    def _imprime_arbol(self, prof = 0):  # A es un (sub)árbol y prof la profundidad del mismo 

        def tabula(prof):
            return ("" if prof == 0 else "|     " * (prof - 1) + "|-----")

        def espacios(prof):
            return "|     " * prof + "|"

        ret = ""
        if self.hijos != []:
            ret += tabula(prof) + str(self.dato) + "\n"
            for H in self.hijos:
                ret += espacios(prof) + "\n"
                ret += H._imprime_arbol(prof + 1)
            return ret
        else:
            return tabula(prof) + str(self.dato) + "\n" 

    @classmethod
    def crea_arbol_desde_lista(cls,x):
        if isinstance(x,tuple):
            dato, hijos = x
            A = cls(dato)
            for hl in hijos:
                H = AG.crea_arbol_desde_lista(hl)
                A.añade_hijo(H)
            return A
        else:
            return cls(x)
    
from Pilas import Pila

class ABB:
    # Clase interna
    class __Nodo:
        
        def __init__(self, clave, izq = None, der = None):
            self.clave = clave
            self.izq = izq
            self.der = der
            
        def __repr__(self):
            return str(self.clave)
    
    def __init__(self):
        self.__raiz = None
        
    def __repr__(self):
        return ABB.__print2DTree(self.__raiz)
    
    def esVacio(self):       
        return self.__raiz is None

    def raiz(self):          
        if self.esVacio():      
            raise Exception("Un árbol vacío no tiene nodo raiz")
        return self.__raiz.clave
    
    # Inserta un valor en el árbol 
    # Devuelve False si el valor ya está en el árbol, 
    # En caso contrario, lo inserta y devuelve True
    def inserta(self, v):
        actual = self.__raiz
        if actual == None:
            self.__raiz = self.__Nodo(v)
            
        while actual != None:
            if v == actual.clave:
                return False
            elif v < actual.clave:
                padre = actual
                actual = actual.izq
                if actual == None:
                    padre.izq = self.__Nodo(v)
            else:
                padre = actual
                actual = actual.der
                if actual == None:
                    padre.der = self.__Nodo(v)
        return True
        
    def borra(self, v):
        actual = self.__raiz
        if actual == None:
            return False
        
        padre = None
        last_dir = None
        while actual != None:
            if v == actual.clave:
                if actual.izq == None and actual.der == None:
                    self.__actualiza_padre(padre, last_dir, None)
                elif actual.izq == None:
                    self.__actualiza_padre(padre, last_dir, actual.der)
                elif actual.der == None:
                    self.__actualiza_padre(padre, last_dir, actual.izq)
                else:
                    maximo_por_la_izquierda = ABB.__busca_max(actual.izq)
                    self.borra(maximo_por_la_izquierda)
                    actual.clave = maximo_por_la_izquierda
                return True
            elif v < actual.clave:
                padre = actual
                actual = actual.izq
                last_dir = "IZQ"
            else:
                padre = actual
                actual = actual.der
                last_dir = "DER"

        return False
    
    @staticmethod
    def __busca_max(nodo):
        actual = nodo
        while actual.der != None:
            actual = actual.der
        
        return actual.clave
    
    def __actualiza_padre(self, padre, last_dir, nuevo_hijo):
        if padre == None:
            self.__raiz = nuevo_hijo
        else:
            if last_dir == "IZQ":
                padre.izq = nuevo_hijo
            else:
                padre.der = nuevo_hijo
                
    
    def recorrido(self):                          
        pila = Pila().apila(self.__raiz)          
        while not pila.esVacia():                 
            item = pila.cima() 
            pila.desapila()
            if isinstance(item,self.__Nodo):
                pila.apila(item.der)         
                pila.apila(item.clave)       
                pila.apila(item.izq)         
            elif item:                            
                yield item 

    # Busca un valor en el árbol 
    # Devuelve True si el valor ya está en el árbol, 
    # En caso contrario, devuelve True
    def en_arbol(self, v):
        actual = self.__raiz
            
        while actual != None:
            if v == actual.clave:
                return True
            elif v < actual.clave:
                actual = actual.izq
            else:
                actual = actual.der
        
        return False
    
    @staticmethod    
    def __print2DTree(root, space = 0, LEVEL_SPACE = 5):
        if root == None: 
            return ""
        space += LEVEL_SPACE
        ret = ""
        ret += ABB.__print2DTree(root.der, space) + "\n"
        for i in range(LEVEL_SPACE, space): 
            ret += " "
        ret += "|" + str(root.clave) + "|<"
        ret += ABB.__print2DTree(root.izq, space)
        
        return ret