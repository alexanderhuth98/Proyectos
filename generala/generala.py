import random

class Dado:
    def __init__(self):
        self.valor = None

    def tirar(self):
        self.valor = random.randint(1, 6)
        return self.valor

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntaje_total = 0
        self.puntaje_ronda = 0
        self.historial_tiradas = []
        self.categorias_completadas = set()

    def guardar_dados(self, dados, indices):
        for i in indices:
            if isinstance(dados[i - 1], Dado):
                dados[i - 1] = (dados[i - 1].valor, "guardado")  # Guardar el valor del dado
        return dados

    def desguardar_dados(self, dados, indices):
        for i in indices:
            if isinstance(dados[i - 1], tuple):
                dados[i - 1] = Dado()
        return dados

    def anotar_combinacion(self, combinacion, puntos):
        if combinacion not in self.categorias_completadas:
            self.puntaje_ronda += puntos
            self.historial_tiradas.append(f"Combinación: {combinacion}, Puntos: {puntos}")
            self.categorias_completadas.add(combinacion)

    def reset_puntaje_ronda(self):
        self.puntaje_total += self.puntaje_ronda
        self.puntaje_ronda = 0

class Marcador:
    def __init__(self, jugadores):
        self.puntajes = {jugador.nombre: jugador.puntaje_total for jugador in jugadores}

    def actualizar_puntaje(self, jugador):
        self.puntajes[jugador.nombre] = jugador.puntaje_total

    def mostrar_ranking(self):
        ranking = sorted(self.puntajes.items(), key=lambda item: item[1], reverse=True)
        print("Ranking:")
        for nombre, puntaje in ranking:
            print(f"{nombre}: {puntaje} puntos")

def mostrar_mensaje(mensaje):
    print(mensaje)

def solicitar_entrada(prompt):
    return input(prompt)

def mostrar_historial(jugador, resultados=None):
    print(f"Historial de tiradas de {jugador.nombre}:")
    for entrada in jugador.historial_tiradas:
        print(entrada)
    if resultados:
        print(f"Tirada actual: {resultados}")
    print()

def inicializar_juego():
    num_jugadores = int(solicitar_entrada("Ingrese el número de jugadores: "))
    jugadores = []
    for i in range(num_jugadores):
        nombre = solicitar_entrada(f"Ingrese el nombre del jugador {i + 1}: ")
        jugadores.append(Jugador(nombre))
    marcador = Marcador(jugadores)
    return jugadores, marcador

def calcular_puntaje(resultados, tirada_numero):
    contador = {i: resultados.count(i) for i in set(resultados)}

    if 5 in contador.values():
        if tirada_numero == 1:
            return "Generala Servida", 60, True
        return "Generala", 60, False
    if 4 in contador.values():
        return "Poker", 45 if tirada_numero == 1 else 40, False
    if 3 in contador.values() and 2 in contador.values():
        return "Full", 35 if tirada_numero == 1 else 30, False
    if set([1, 2, 3, 4, 5]) == set(resultados) or set([2, 3, 4, 5, 6]) == set(resultados):
        return "Escalera", 25 if tirada_numero == 1 else 20, False

    return "Sin combinación", 0, False

def jugar_turno(jugador):
    dados = [Dado() for _ in range(5)]
    combinaciones_logradas = []
    for tirada in range(3):
        if tirada > 0:
            decision = solicitar_entrada("¿Desea tirar todos los dados (t), tirar solo dados libres (l), guardar dados (g) o mostrar dados guardados (m)?: ")
            if decision.lower() == 't':
                dados = [Dado() for _ in range(5)]
            elif decision.lower() == 'l':
                dados = [dado if isinstance(dado, tuple) else Dado() for dado in dados]
            elif decision.lower() == 'g':
                indices_guardados = list(map(int, solicitar_entrada("Ingrese los índices de los dados a guardar (1-5) separados por espacios: ").split()))
                dados = jugador.guardar_dados(dados, indices_guardados)
                if len([dado for dado in dados if isinstance(dado, tuple)]) == 5:
                    volver_tirar = solicitar_entrada("¿Desea volver a tirar algún dado guardado? (s/n): ")
                    if volver_tirar.lower() == 's':
                        indices_desguardados = list(map(int, solicitar_entrada("Ingrese los índices de los dados guardados que desea volver a tirar (1-5) separados por espacios: ").split()))
                        dados = jugador.desguardar_dados(dados, indices_desguardados)
                    else:
                        mostrar_mensaje(f"Combinaciones logradas en este turno: {combinaciones_logradas}")
                        return False  # Termina el turno
            elif decision.lower() == 'm':
                mostrar_dados_guardados(dados)
                volver_tirar = solicitar_entrada("¿Desea volver a tirar algún dado guardado? (s/n): ")
                if volver_tirar.lower() == 's':
                    indices_desguardados = list(map(int, solicitar_entrada("Ingrese los índices de los dados guardados que desea volver a tirar (1-5) separados por espacios: ").split()))
                    dados = jugador.desguardar_dados(dados, indices_desguardados)
        resultados = [f"{dado.tirar()}*" if isinstance(dado, tuple) else dado.tirar() for dado in dados]
        mostrar_historial(jugador, resultados)
        mostrar_mensaje(f"Tirada {tirada + 1}: {resultados}")
        if tirada < 2:
            decision = solicitar_entrada("¿Desea guardar algunos dados? (s/n): ")
            if decision.lower() == 's':
                indices_guardados = list(map(int, solicitar_entrada("Ingrese los índices de los dados a guardar (1-5) separados por espacios: ").split()))
                dados = jugador.guardar_dados(dados, indices_guardados)
            else:
                dados = [Dado() if dado == "guardado" else dado for dado in dados]
        else:
            combinacion, puntos, servida = calcular_puntaje(resultados, tirada + 1)
            if combinacion == "Generala Servida":
                mostrar_mensaje(f"{jugador.nombre} ha logrado una {combinacion} y ha ganado el juego!")
                return True  # El juego termina
            elif combinacion != "Sin combinación":
                jugador.anotar_combinacion(combinacion, puntos)
                combinaciones_logradas.append((combinacion, puntos))
            else:
                numero = solicitar_entrada("Ingrese el número para anotar puntos (1-6): ")
                if numero.isdigit() & 1 <= int(numero) <= 6:
                    puntos = resultados.count(int(numero)) * int(numero)
                    jugador.anotar_combinacion(numero, puntos)
                    combinaciones_logradas.append((numero, puntos))
            mostrar_mensaje(f"Combinación obtenida: {combinacion}, Puntos: {puntos}")
        print()  # Salto de línea

    mostrar_mensaje(f"Combinaciones logradas en este turno: {combinaciones_logradas}")
    return False  # El juego no termina

def mostrar_dados_guardados(dados):
    guardados = [(i + 1, dado[0]) for i, dado in enumerate(dados) if isinstance(dado, tuple)]
    if guardados:
        print("Dados guardados:")
        for idx, valor in guardados:
            print(f"Dado {idx}: {valor}*")

def jugar_ronda(jugadores, marcador):
    turno = 0
    while True:
        jugador = jugadores[turno % len(jugadores)]
        mostrar_mensaje(f"Turno de {jugador.nombre}")
        if jugar_turno(jugador):
            return True  # El juego termina
        jugador.reset_puntaje_ronda()
        marcador.actualizar_puntaje(jugador)
        mostrar_historial(jugador)
        turno += 1
        if all(jugador.categorias_completadas for jugador in jugadores):
            break
    return False  # El juego no termina

def finalizar_juego(jugadores, marcador):
    mostrar_mensaje("Juego finalizado. Puntuaciones finales:")
    marcador.mostrar_ranking()
    ganador = max(jugadores, key=lambda jugador: jugador.puntaje_total)
    mostrar_mensaje(f"El ganador es {ganador.nombre} con {ganador.puntaje_total} puntos")

def main():
    jugadores, marcador = inicializar_juego()
    while True:
        if jugar_ronda(jugadores, marcador):
            break  # El juego termina por generala servida
        marcador.mostrar_ranking()
    finalizar_juego(jugadores, marcador)

if __name__ == "__main__":
    main()
