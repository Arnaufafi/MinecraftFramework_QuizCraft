# rewards.py
from mcrcon import MCRcon
from mcpi.minecraft import Minecraft


def spawn_item(player, item_id, mc):
    """Genera un ítem como orbe en la posición del jugador."""
    pos = mc.entity.getTilePos(player)
    command = f"summon item {pos.x} {pos.y} {pos.z} {{Item:{{id:\"minecraft:{item_id}\",Count:1}}}}"
    try:
        with MCRcon("localhost", "1234", port=25575) as mcr:
            mcr.command(command)
        mc.postToChat(f"¡Se ha generado un {item_id} para {player}!")
    except Exception as e:
        mc.postToChat(f"Error al generar el ítem: {str(e)}")

def diamond(player, mc):
    """Genera un diamante como ítem."""
    spawn_item(player, "diamond", mc)

def gold(player, mc):
    """Genera un lingote de oro como ítem."""
    spawn_item(player, "gold_ingot", mc)

def food(player, mc):
    """Genera comida para el jugador."""
    spawn_item(player, "cooked_beef", mc)

# Versión difícil

def D_diamond(player, mc):
    """Genera un diamante y un bloque de diamante como recompensa difícil."""
    spawn_item(player, "diamond", mc)
    spawn_item(player, "diamond_block", mc)  # Añadir un bloque de diamante como recompensa adicional

def D_gold(player, mc):
    """Genera un lingote de oro y un bloque de oro como recompensa difícil."""
    spawn_item(player, "gold_ingot", mc)
    spawn_item(player, "gold_block", mc)  # Añadir un bloque de oro como recompensa adicional

def D_food(player, mc):
    """Genera comida de calidad (como una tarta) como recompensa difícil."""
    spawn_item(player, "apple", mc)
    spawn_item(player, "cake", mc)  # Añadir un pastel como recompensa adicional
