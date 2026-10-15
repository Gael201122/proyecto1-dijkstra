"""Proyecto 1: Algoritmo de Dijkstra
Programación III - 2026B

Encuentra la ruta más corta en un grafo ponderado (red de transporte)
usando Programación Orientada a Objetos.
"""

import heapq


class Nodo:
    """Representa un nodo (estación/ciudad) del grafo."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # {Nodo: peso}

    def agregar_vecino(self, vecino, peso):
        self.vecinos[vecino] = peso

    def __repr__(self):
        return f"Nodo({self.nombre})"


class Grafo:
    """Grafo ponderado no dirigido."""

    def __init__(self):
        self.nodos = {}  # {nombre: Nodo}

    def agregar_nodo(self, nombre):
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)
        return self.nodos[nombre]

    def agregar_arista(self, origen, destino, peso):
        if peso < 0:
            raise ValueError("Dijkstra no admite pesos negativos")
        a = self.agregar_nodo(origen)
        b = self.agregar_nodo(destino)
        a.agregar_vecino(b, peso)
        b.agregar_vecino(a, peso)  # no dirigido

    def dijkstra(self, origen, destino):
        """Devuelve (distancia_total, ruta) o (inf, []) si no hay camino."""
        if origen not in self.nodos or destino not in self.nodos:
            raise KeyError("Origen o destino no existe en el grafo")

        inicio = self.nodos[origen]
        fin = self.nodos[destino]

        distancias = {n: float("inf") for n in self.nodos.values()}
        previo = {}
        distancias[inicio] = 0
        cola = [(0, inicio.nombre)]  # (distancia, nombre) -> evita comparar Nodos
        visitados = set()

        while cola:
            dist_actual, nombre = heapq.heappop(cola)
            actual = self.nodos[nombre]
            if actual in visitados:
                continue
            visitados.add(actual)
            if actual is fin:
                break
            for vecino, peso in actual.vecinos.items():
                nueva = dist_actual + peso
                if nueva < distancias[vecino]:
                    distancias[vecino] = nueva
                    previo[vecino] = actual
                    heapq.heappush(cola, (nueva, vecino.nombre))

        if distancias[fin] == float("inf"):
            return float("inf"), []

        ruta = []
        nodo = fin
        while nodo is not inicio:
            ruta.append(nodo.nombre)
            nodo = previo[nodo]
        ruta.append(inicio.nombre)
        ruta.reverse()
        return distancias[fin], ruta


def main():
    # Red de transporte de ejemplo (pesos en km)
    g = Grafo()
    g.agregar_arista("Guadalajara", "Zapopan", 10)
    g.agregar_arista("Guadalajara", "Tlaquepaque", 8)
    g.agregar_arista("Guadalajara", "Tonalá", 14)
    g.agregar_arista("Zapopan", "Tesistán", 15)
    g.agregar_arista("Tlaquepaque", "Tonalá", 7)
    g.agregar_arista("Tlaquepaque", "El Salto", 20)
    g.agregar_arista("Tonalá", "Zapotlanejo", 25)
    g.agregar_arista("Tesistán", "Tala", 30)
    g.agregar_arista("El Salto", "Zapotlanejo", 40)
    g.agregar_arista("Zapotlanejo", "Tala", 55)

    print("Nodos disponibles:", ", ".join(g.nodos))
    origen = input("Nodo origen: ").strip() or "Guadalajara"
    destino = input("Nodo destino: ").strip() or "Zapotlanejo"

    try:
        distancia, ruta = g.dijkstra(origen, destino)
    except KeyError as e:
        print("Error:", e)
        return

    if not ruta:
        print(f"No existe camino entre {origen} y {destino}.")
    else:
        print(f"\nDistancia/costo total: {distancia}")
        print("Ruta: " + " -> ".join(ruta))


if __name__ == "__main__":
    main()
