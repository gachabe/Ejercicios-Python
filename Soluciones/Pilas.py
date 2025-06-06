class Vacia(Exception):
    """ error accediendo a un elemento de un contenedor vacio"""
    pass

class Pila():
    """ implementación de pilas utilizando listas """
    
    def __init__(self):
        """ crea una pila vacía """
        self._data = []
        
    def esVacia(self):
        """ verifica si la pila no contiene ningún elemento """
        return self._data == []
        
    def apila(self, x):
        """ añade un elemento en la parte superior de la pila """
        self._data.append(x)
        return self
    
    def cima(self):
        """ devuelve el elemento en la parte superior de la pila.
            No altera la pila """
        if self.esVacia():
            raise Vacia('La pila está vacia')
        else:
            return self._data[-1]
    
    def desapila(self):
        """ devuelve la pila sin la cima"""
        if self.esVacia():
            raise Vacia('La pila está vacia')
        else:
            # self._data.pop()
            self._data = self._data[:-1]
            return self
        
    def __eq__(self, p):
        return self._data == p._data

    def __repr__(self):
        return "|".join(map(str,self._data[::-1])) + ' -'