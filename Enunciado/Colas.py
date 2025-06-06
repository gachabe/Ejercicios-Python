import copy


class Vacia(Exception):
    """ error accediendo a un elemento de un contenedor vacio"""
    pass

class Cola():
    """ implementación de colas utilizando listas circulares """
    
    DEFAULT_CAPACITY = 3
    
    def __init__(self):
        """ crea una cola vacía """
        self._data = [None] * Cola.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0
        
    def inserta(self, x):
        "Añade un elemento al final de la cola"
        if self._size == len(self._data):
            self._resize(2*len(self._data))
        pos = (self._front + self._size) % len(self._data)
        self._data[pos] = x
        self._size += 1
        return self
    
    def _resize(self, new_capacity):
        old_data = self._data
        pos = self._front
        self._data = [None]*new_capacity
        for k in range(self._size):
            self._data[k] = old_data[pos]
            pos = (1 + pos) % len(old_data)
        self._front = 0
    
    def esVacia(self):
        """ verifica si la cola no contiene ningún elemento """
        return self._size == 0
        
    def primero(self):
        """ devuelve el primer elemento de la cola. No altera la cola """
        if self.esVacia():
            raise Vacia
        return self._data[self._front]
    
    def resto(self):
        """ devuelve la cola sin el primero """
        if self.esVacia():
            raise Vacia
        self._data[self._front] = None                      # ponemos a None la posicion del primer elemento
        self._front = (self._front + 1) % len(self._data)   # el nuevo primer elemento esta una posicion mas adelante
        self._size -= 1                                     # hay un elemento menos
        return self
    
    def _toList(self):
        result = []
        for k in range(self._size):
            pos = (self._front + k) % len(self._data)
            val = self._data[pos]  
            if val is not None:
                result.append(val)
        return result
        
    def __eq__(self, c2):
        return self._toList() == c2._toList()
    
    def __repr__(self):
        return f"C {self._toList()}"
