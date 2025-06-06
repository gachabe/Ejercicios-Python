from Pilas import Pila
from Colas import Cola
from Arboles import AG

# Clase para representar los vértices de un grafo
# El atributo nombre es la etiqueta del nodo, en realidad 
# identificaremos a cada nodo de un grafo por un índice
class Vertice:       
    def __init__(self, nombre):
        self.nombre = nombre      

    def __str__(self):       
        return '<Vértice {}>'.format(self.nombre)
    
# Clase para representar grafos no dirigidos    
class Grafo:     
    
    def __init__(self):     
        self._vertices = []  
        self._mat_ady = {}    

    def n_vertices(self):   
        return len(self._vertices) 

    def n_aristas(self):       
        return len(self._mat_ady) // 2
    
    def __str__(self):      
        nV = self.n_vertices()
        nA = self.n_aristas()
        return f"<Grafo de {nV} vertices y {nA} aristas>"
   
    def añade_vertice(self, v): 
        self._vertices.append(v) 

    def indice_valido(self, i): 
        if i < 0 or self.n_vertices() <= i: 
            raise IndexError   
        return True          
   
    def obten_vertice(self, i):  
        if self.indice_valido(i): 
            return self._vertices[i]

    def añade_arista(self, i, j): 
        self.indice_valido(i)   
        self.indice_valido(j)    
        if i == j:            
            raise ValueError   
        self._mat_ady[i, j] = 1 
        self._mat_ady[j, i] = 1 

    def hay_arista(self, i, j): 
        self.indice_valido(i)    
        self.indice_valido(j)    
        return (i,j) in self._mat_ady     

    # Generador de los vértices
    def vertices(self):      
        return range(self.n_vertices())

   
    # Generador de los vértices adyacentes a uno dado   
    def vertices_adyacentes(self, n):   
        self.indice_valido(n)    
        for j in self.vertices(): 
            if j != n and self.hay_arista(n, j): 
                yield j         
    
    # Función de impresión del grafo (informa de sus vértices y aristas) 
    def imprime(self,prefix=''):    
        print(f'{prefix}{self}')                                   
        for v in self.vertices():                                  
            print(f'{prefix}{v}:',self.obten_vertice(v))        
            for k in range(v+ 1, self.n_vertices()):           
                if self.hay_arista(v, k):  
                    print(prefix,self._vertices[v].nombre,'<->',self._vertices[k].nombre)
    
    
# Función que genera los nodos adyacentes en el grafo a un vértice  dado
# La lista de vivitados es una lista de booleanos, cada posición indica 
#  si el correspondiente nodo ha sido visitado. La función actualiza visitados
def vertices_adyacentes_no_visitados(grafo,n,visitados):
    for j in grafo.vertices_adyacentes(n):
        if not visitados[j]:
            visitados[j]=True
            yield j

# Función para transformar los cáminos con índices en caminos 
# con las correspondientes etiquetas            

def vertices_camino(grafo,c):
    return [grafo.obten_vertice(v).nombre for v in c]            
            
            
# Recorrido en profundidad de un grafo, a partir de un vértice n
def recorrido_profundidad(grafo,n):
    grafo.indice_valido(n)
    visitados = [False] * grafo.n_vertices() 
    pila=Pila().apila(n)
    visitados[n]=True
    yield n
    while not pila.esVacia(): 
        actual = pila.cima()
        try:
            vecino=next(vertices_adyacentes_no_visitados(grafo,actual,visitados))
            pila.apila(vecino)
            yield vecino
        except StopIteration:
            pila.desapila()
            

# Recorrido en anchura de un grafo, a partir de un vértice n
def recorrido_anchura(grafo,n):
    grafo.indice_valido(n)
    visitados = [False] * grafo.n_vertices() 
    cola=Cola().inserta(n)
    visitados[n]=True
    while not cola.esVacia():     # Aplica Regla 1 siempre que pueda
        actual = cola.primero()
        cola.resto()
        yield actual
        for j in vertices_adyacentes_no_visitados(grafo,actual,visitados):
            cola.inserta(j)

            
# Caminos desde un vértice dado a todos los vértices del grafo, recorridos en profundidad            
def recorrido_profundidad_caminos(grafo,n):
    grafo.indice_valido(n)
    visitados = [False] * grafo.n_vertices()
    pila=Pila().apila(n)
    visitados[n]=True
    camino_actual=[n]
    yield camino_actual
    while not pila.esVacia(): 
        actual = pila.cima()
        try:
            vecino=next(vertices_adyacentes_no_visitados(grafo,actual,visitados))
            pila.apila(vecino)
            camino_actual.append(vecino)
            yield camino_actual
        except StopIteration:
            pila.desapila()
            camino_actual.pop(-1)
            
# Lista de vértices a partir de la lista de sus índices            
def vertices_camino(grafo,c):
    return [grafo.obten_vertice(v).nombre for v in c]


# Caminos desde un vértice dado a todos los vértices del grafo, recorridos en anchura            
def recorrido_anchura_caminos(grafo,n):
    grafo.indice_valido(n)
    visitados = [False] * grafo.n_vertices() 
    cola=Cola().inserta([n])
    visitados[n]=True
    while not cola.esVacia(): 
        actual = cola.primero()
        cola.resto()
        yield actual
        for j in vertices_adyacentes_no_visitados(grafo,actual[-1],visitados):
            cola.inserta(actual+[j])

            
# Arbol de expansión de un grafo, con raíz en un vértice n, y obtenido mediante un recorrido en profundidad            
def arbol_expansion_grafo_profundidad(grafo,n):
    grafo.indice_valido(n)
    arbol=AG(n)
    pila=Pila().apila(arbol)
    visitados = [False] * grafo.n_vertices() 
    visitados[n]=True
    while not pila.esVacia(): 
        actual = pila.cima()
        try:
            vecino=next(vertices_adyacentes_no_visitados(grafo,actual.dato,visitados))
            subarbol_vecino=AG(vecino)
            actual.añade_hijo(subarbol_vecino)
            pila.apila(subarbol_vecino)
        except StopIteration:
            pila.desapila()
    return arbol


# Clase para representar grafos dirigidos
class Grafod(Grafo):        

    def n_aristas(self):       
        return len(self._mat_ady) 
    
    def añade_arista(self, i, j): 
        self.indice_valido(i)   
        self.indice_valido(j)    
        if i == j:            
            raise ValueError   
        self._mat_ady[i, j] = 1 
 
    def vertices_sucesores(self, n):   # en realidad es vertices_adyacentes
        self.indice_valido(n)    
        for j in self.vertices(): 
            if j != n and self.hay_arista(n, j): 
                yield j         
 
    def vertices_predecesores(self, n):   
        self.indice_valido(n)    
        for j in self.vertices(): 
            if j != n and self.hay_arista(j,n): 
                yield j         
               
    def imprime(self,prefix=''):    
        print(f'{prefix}{self}')                                   
        for v in self.vertices():                                  
            print(f'{prefix}{v}:',self.obten_vertice(v))           
            for k in self.vertices(): 
                if self.hay_arista(v, k):  
                    print(prefix,self._vertices[v].nombre,'-->',self._vertices[k].nombre)
    

    
# Ordenación topológica de los vértices de un grafo dirigido    
def ordena_vertices_topologicamente(grafo):
    orden = []
    n_vertices = grafo.n_vertices() 
    visitados = [False] * n_vertices 
    while len(orden) < n_vertices: # hasta que estén todos ordenados    
        siguiente=None
        for v in grafo.vertices(): 
            if (not visitados[v] and  
                 all(visitados[j] for j in grafo.vertices_predecesores(v))): 
                siguiente=v        # si todos los predecesores de v están ordenados,
                                   # ese vértice puede ser el siguiente a ordenar
                break
        if siguiente is None:      # si no hay ninguno que pueda ser el siguiente, es que hay 
                                   # un ciclo entre los que quedan por ordenar
            print('Grafo con ciclo, no se puede ordenar')
            return False
        else:
            orden.append(siguiente) 
            visitados[siguiente] = True
    return orden 