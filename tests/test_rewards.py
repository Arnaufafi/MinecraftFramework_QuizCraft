import unittest
from unittest.mock import MagicMock, patch
from mcpi.minecraft import Minecraft
import sys
import os

# Agrega el directorio raíz del proyecto a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from rewards import spawn_item, diamond, gold, food, D_diamond, D_gold, D_food
from question_control import get_mc_instance


class TestRewards(unittest.TestCase):
    @patch('mcpi.minecraft.Minecraft.create', return_value=MagicMock())
    @patch('rewards.MCRcon')
    def setUp(self, mock_mc_create, mock_mcrcon):
        """
        Inicializa el entorno antes de cada prueba.
        Crea una nueva instancia de mc usando get_mc_instance().
        """
        global mc
        mc = get_mc_instance()
        mc.postToChat = MagicMock()  # Mock para evitar interacciones reales en el chat de Minecraft
        mc.entity.getTilePos = MagicMock()  # Mock para las funciones de entidades

        # Simulamos la posición del jugador como un objeto con coordenadas x, y, z
        self.mock_pos = MagicMock()
        self.mock_pos.x = 100
        self.mock_pos.y = 64
        self.mock_pos.z = 200
        mc.entity.getTilePos.return_value = self.mock_pos

        # Mock para el MCRcon para evitar la conexión real
        self.mock_mcrcon_instance = MagicMock()
        mock_mcrcon.return_value = self.mock_mcrcon_instance
        self.mock_mcrcon_instance.__enter__.return_value = self.mock_mcrcon_instance
        self.mock_mcrcon_instance.command.return_value = ""  # Simula que no se lanza ninguna excepción en el comando

    @patch('rewards.MCRcon')
    def test_spawn_item(self, mock_mcrcon):
        player = 12345
        item_id = "diamond"

        # Configuración del mock para el contexto de MCRcon
        mock_mcrcon_instance = MagicMock()
        mock_mcrcon.return_value = mock_mcrcon_instance
        mock_mcrcon_instance.__enter__.return_value = mock_mcrcon_instance

        # Llamar a la función
        spawn_item(player, item_id, mc)

        # Verificar que la posición del jugador fue obtenida correctamente
        mc.entity.getTilePos.assert_called_with(player)

        # Verificar que el comando de invocar el ítem fue enviado correctamente
        expected_command = (
            f"summon item {self.mock_pos.x} {self.mock_pos.y} {self.mock_pos.z} "
            f"{{Item:{{id:\"minecraft:{item_id}\",Count:1}}}}"
        )
        mock_mcrcon_instance.command.assert_called_with(expected_command)

        # Verificar que el mensaje de chat fue enviado correctamente
        mc.postToChat.assert_called_with(f"¡Se ha generado un {item_id} para {player}!")


    @patch('rewards.spawn_item')
    def test_diamond(self, mock_spawn_item):
        player = 12345

        # Llamar a la función
        diamond(player, mc)

        # Verificar que spawn_item fue llamado con "diamond"
        mock_spawn_item.assert_called_once_with(player, "diamond", mc)

    @patch('rewards.spawn_item')
    def test_gold(self, mock_spawn_item):
        player = 12345

        # Llamar a la función
        gold(player, mc)

        # Verificar que spawn_item fue llamado con "gold_ingot"
        mock_spawn_item.assert_called_once_with(player, "gold_ingot", mc)

    @patch('rewards.spawn_item')
    def test_food(self, mock_spawn_item):
        player = 12345

        # Llamar a la función
        food(player, mc)

        # Verificar que spawn_item fue llamado con "cooked_beef"
        mock_spawn_item.assert_called_once_with(player, "cooked_beef", mc)

    @patch('rewards.spawn_item')
    def test_D_diamond(self, mock_spawn_item):
        player = 12345

        # Llamar a la función
        D_diamond(player, mc)

        # Verificar que spawn_item fue llamado con "diamond"
        mock_spawn_item.assert_any_call(player, "diamond", mc)
        # Verificar que spawn_item fue llamado con "diamond_block"
        mock_spawn_item.assert_any_call(player, "diamond_block", mc)

    @patch('rewards.spawn_item')
    def test_D_gold(self, mock_spawn_item):
        player = 12345

        # Llamar a la función
        D_gold(player, mc)

        # Verificar que spawn_item fue llamado con "gold_ingot"
        mock_spawn_item.assert_any_call(player, "gold_ingot", mc)
        # Verificar que spawn_item fue llamado con "gold_block"
        mock_spawn_item.assert_any_call(player, "gold_block", mc)

    @patch('rewards.spawn_item')
    def test_D_food(self, mock_spawn_item):
        player = 12345

        # Llamar a la función
        D_food(player, mc)

        # Verificar que spawn_item fue llamado con "apple"
        mock_spawn_item.assert_any_call(player, "apple", mc)
        # Verificar que spawn_item fue llamado con "cake"
        mock_spawn_item.assert_any_call(player, "cake", mc)


if __name__ == "__main__":
    unittest.main()
