# rewards.py
from mcrcon import MCRcon
from mcpi.minecraft import Minecraft

mc = Minecraft.create()

def spawn_item(player, item_id):
    """Genera un ítem como orbe en la posición del jugador."""
    pos = mc.entity.getTilePos(player)
    command = f"summon item {pos.x} {pos.y} {pos.z} {{Item:{{id:\"minecraft:{item_id}\",Count:1}}}}"
    try:
        with MCRcon("localhost", "1234", port=25575) as mcr:
            mcr.command(command)
        mc.postToChat(f"¡Se ha generado un {item_id} para {player}!")
    except Exception as e:
        mc.postToChat(f"Error al generar el ítem: {str(e)}")

def diamond(player):
    """Genera un diamante como ítem."""
    spawn_item(player, "diamond")

def gold(player):
    """Genera un lingote de oro como ítem."""
    spawn_item(player, "gold_ingot")

def food(player):
    """Genera comida para el jugador."""
    spawn_item(player, "cooked_beef")

# Versión difícil

def D_diamond(player):
    """Genera un diamante y un bloque de diamante como recompensa difícil."""
    spawn_item(player, "diamond")
    spawn_item(player, "diamond_block")  # Añadir un bloque de diamante como recompensa adicional

def D_gold(player):
    """Genera un lingote de oro y un bloque de oro como recompensa difícil."""
    spawn_item(player, "gold_ingot")
    spawn_item(player, "gold_block")  # Añadir un bloque de oro como recompensa adicional

def D_food(player):
    """Genera comida de calidad (como una tarta) como recompensa difícil."""
    spawn_item(player, "apple")
    spawn_item(player, "cake")  # Añadir un pastel como recompensa adicional
