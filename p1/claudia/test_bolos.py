import unittest
from bolos import Partida

class TestBolos(unittest.TestCase):

    def setUp(self):
        self.partida = Partida()
        self.partida.empezar_partida()

    def test_una_partida_10_rondas(self):
        self.assertEqual(self.partida.contar_rondas(), 10)

    def test_primera_partida_0_bolos(self):
        for _ in range(10):
            ronda = (0, 0)
            self.partida.registrar_ronda(ronda)
        self.assertEqual(self.partida.obtener_puntuacion_total(), 0)

    def test_primera_partida_1_bolos(self):
        for _ in range(10):
            ronda = (1, 0)
            self.partida.registrar_ronda(ronda)
        self.assertEqual(self.partida.obtener_puntuacion_total(), 10)

    def test_spare_suma_bonus_de_siguiente_tiro(self):
        self.partida.registrar_ronda((5, 5))
        self.partida.registrar_ronda((3, 4))
        self.assertEqual(self.partida.obtener_puntuacion_total(), 20)


    def test_strike_suma_dos_partidas(self):
        self.partida.registrar_ronda((10,0))
        self.partida.registrar_ronda((3,4))
        self.assertEqual(self.partida.obtener_puntuacion_total(),24)
