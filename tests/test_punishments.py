import unittest
from unittest.mock import MagicMock, patch
from mcpi.minecraft import Minecraft
import sys
import os

# Agrega el directorio raíz del proyecto a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from punishments import spawn_mob, lava, tnt, zombie, prison, D_lava, D_tnt, D_zombie, D_prison
from question_control import get_mc_instance

class TestPunishments(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create', return_value=MagicMock())
    @patch('punishments.MCRcon')  # Aquí estamos parchando la clase MCRcon para evitar la conexión real
    def setUp(self, mock_mcrcon, mock_mc_create):
        """
        Inicializa el entorno antes de cada prueba.
        Crea una nueva instancia de mc usando get_mc_instance().
        """
        global mc, questions
        mc = get_mc_instance()
        mc.postToChat = MagicMock()  # Mock para evitar interacciones reales en el chat de Minecraft
        mc.setBlock = MagicMock()  # Mock para la función setBlock
        mc.entity.getTilePos = MagicMock()  # Mock para las funciones de entidades
        questions = []  # Reinicia la lista de preguntas para cada prueba

        # Simulamos la posición del jugador como un objeto con coordenadas x, y, z
        self.mock_pos = MagicMock()
        self.mock_pos.x = 100
        self.mock_pos.y = 64
        self.mock_pos.z = 200
        mc.entity.getTilePos.return_value = self.mock_pos

        # Mock para el MCRcon para evitar la conexión real
        mock_mcrcon_instance = MagicMock()
        mock_mcrcon.return_value = mock_mcrcon_instance
        mock_mcrcon_instance.__enter__.return_value = mock_mcrcon_instance  # Simula el comportamiento de 'with'
        mock_mcrcon_instance.command.return_value = ""  # Simula que no se lanza ninguna excepción en el comando

    @patch('punishments.MCRcon')  # Parchamos solo cuando la función lo requiera
    def test_spawn_mob(self, mock_mcrcon):
        player = 12345
        mob_type = "Zombie"
    
        # Llamar a la función
        spawn_mob(player, mob_type, mc)
    
        # Verificar que la posición del jugador y el comando de invocar mob fueron correctos
        mc.entity.getTilePos.assert_called_with(player)
        mc.postToChat.assert_called_with(f"Se ha invocado un {mob_type} en la posición de {player}.")
    
    
    def test_lava(self):
        player = 12345
        
        # Llamar a la función
        lava(player, mc)
        
        # Verificar que el bloque de lava fue colocado en la posición correcta
        mc.setBlock.assert_called_with(self.mock_pos.x, self.mock_pos.y, self.mock_pos.z, 10)  # Lava en la posición exacta

    def test_tnt(self):
        player = 12345
        
        # Llamar a la función
        tnt(player, mc)
        
        # Verificar que se colocaron bloques TNT y fuego en la posición correcta
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y, self.mock_pos.z, 46)  # TNT
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y + 1, self.mock_pos.z, 51)  # Fuego

    @patch('punishments.MCRcon')  # Parchamos solo cuando la función lo requiera
    def test_zombie(self, mock_mcrcon):
        player = 12345
        
        # Llamar a la función
        zombie(player, mc)
        
        # Verificar que se haya invocado un zombie
        mc.entity.getTilePos.assert_called_with(player)
        mc.postToChat.assert_any_call(f"Se ha invocado un Zombie en la posición de {player}.")  # Posición de ejemplo

    def test_prison(self):
        player = 12345
        
        # Llamar a la función
        prison(player, mc)
        
        # Verificar que se hayan colocado los bloques de piedra y agua en las posiciones correctas
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                for dy in range(0, 2):  # Cubrir las dos alturas (debajo y encima del jugador)
                    mc.setBlock.assert_any_call(self.mock_pos.x + dx, self.mock_pos.y + dy, self.mock_pos.z + dz, 1)  # Piedra
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y + 2, self.mock_pos.z, 1)  # Piedra sobre el jugador
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y + 1, self.mock_pos.z, 9)  # Agua sobre el jugador
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y, self.mock_pos.z, 9)  # Agua donde está el jugador
        mc.postToChat.assert_called_with(f"¡{player} ha sido enviado a prisión y está a punto de ahogarse!")

    def test_D_lava(self):
        player = 12345
    
        # Llamar a la función
        D_lava(player, mc)
    
        # Verificar que se colocaron bloques de lava en un área alrededor del jugador
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                mc.setBlock.assert_any_call(self.mock_pos.x + dx, self.mock_pos.y, self.mock_pos.z + dz, 10)  # Lava en un área 5x5

    def test_D_tnt(self):
        player = 12345
        
        # Llamar a la función
        D_tnt(player, mc)
        
        # Verificar que se colocaron TNT y fuego en las posiciones correctas alrededor del jugador
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                mc.setBlock.assert_any_call(self.mock_pos.x + dx, self.mock_pos.y, self.mock_pos.z + dz, 46)  # TNT
                mc.setBlock.assert_any_call(self.mock_pos.x + dx, self.mock_pos.y + 1, self.mock_pos.z + dz, 51)  # Fuego
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y, self.mock_pos.z, 30)  # Bloque de tierra para la explosión

    @patch('punishments.MCRcon')  # Parchamos solo cuando la función lo requiera
    def test_D_zombie(self, mock_mcrcon):
       player = 12345
        
        # Llamar a la función
       D_zombie(player, mc)
        
        # Verificar que se invocaron zombies en un área alrededor del jugador
       for dx in range(-2, 3):
            for dz in range(-2, 3):
                mc.entity.getTilePos.assert_any_call(player)
                mc.postToChat.assert_any_call(f"Se ha invocado un Zombie en la posición de {player}.")  # Posición de ejemplo

    def test_D_prison(self):
        player = 12345
        
        # Llamar a la función
        D_prison(player, mc)
        
        # Verificar que se hayan colocado los bloques de piedra y agua en las posiciones correctas
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                mc.setBlock.assert_any_call(self.mock_pos.x + dx, self.mock_pos.y, self.mock_pos.z + dz, 49)  # Piedra
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y + 2, self.mock_pos.z, 49)  # Piedra sobre el jugador
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y + 1, self.mock_pos.z, 9)  # Agua sobre el jugador
        mc.setBlock.assert_any_call(self.mock_pos.x, self.mock_pos.y, self.mock_pos.z, 9)  # Agua donde está el jugador
        mc.postToChat.assert_called_with(f"¡{player} ha sido enviado a prisión y está a punto de ahogarse!")

if __name__ == "__main__":
    unittest.main()
