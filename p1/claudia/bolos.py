
class Partida:
    def __init__(self):
        self.rondas = []

    def empezar_partida(self):
        self.rondas = []

    def contar_rondas(self):
        return 10

    def registrar_ronda(self, ronda):
        self.rondas.append(ronda)

    def obtener_puntuacion_total(self):
        total = 0
        i = 0
        while i < len(self.rondas):
            ronda = self.rondas[i]

        # STRIKE
            if ronda[0] == 10:
                if i + 1 < len(self.rondas):
                    siguiente = self.rondas[i + 1]
                    total += 10 + siguiente[0] + siguiente[1]
                else:
                    total += 10
                i += 1  # pasa solo una ronda
                continue

        # SPARE
            if ronda[0] + ronda[1] == 10:
                if i + 1 < len(self.rondas):
                    total += 10 + self.rondas[i + 1][0]
                else:
                    total += 10
                i += 1
                continue

        # RONDA NORMAL
            total += sum(ronda)
            i += 1

        return total

