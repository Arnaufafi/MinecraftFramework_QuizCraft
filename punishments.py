# punishments.py
from mcrcon import MCRcon
from mcpi.minecraft import Minecraft
import time


def spawn_mob(player, mob_type, mc):
    """Invoca un mob en la posición del jugador utilizando RCON."""
    pos = mc.entity.getTilePos(player)
    command = f"summon {mob_type} {pos.x} {pos.y} {pos.z}"
    try:
        with MCRcon("localhost", "1234", port=25575) as mcr:
            mcr.command(command)
        mc.postToChat(f"Se ha invocado un {mob_type} en la posición de {player}.")
    except Exception as e:
        mc.postToChat(f"Error invocando mob: {str(e)}")

def lava(player, mc):
    """Coloca un bloque de lava en la posición del jugador."""
    pos = mc.entity.getTilePos(player)
    mc.setBlock(pos.x, pos.y, pos.z, 10)  # Lava en Minecraft

def tnt(player, mc):
    """Coloca TNT repetidamente durante 5 segundos en la posición del jugador y las enciende con fuego."""
    start_time = time.time()
    while time.time() - start_time < 5:
        pos = mc.entity.getTilePos(player)
        mc.setBlock(pos.x, pos.y, pos.z, 46)  # TNT central
        mc.setBlock(pos.x, pos.y + 1, pos.z, 51)  # Encender TNT con fuego
        time.sleep(1)

def zombie(player, mc):
    """Invoca un zombie en la posición del jugador."""
    spawn_mob(player, "Zombie", mc)

def prison(player, mc):
    """Rodea al jugador con bloques de piedra y coloca un bloque de agua donde está, para que se ahogue."""
    pos = mc.entity.getTilePos(player)

    # Rodear al jugador con bloques de piedra (en un cubo de 3x3 alrededor del jugador)
    for dx in range(-1, 2):  # -1, 0, 1
        for dz in range(-1, 2):  # -1, 0, 1
            for dy in range(0, 2):  # Cubrir las dos alturas (debajo y encima del jugador)
                mc.setBlock(pos.x + dx, pos.y + dy, pos.z + dz, 1)  # Bloques de piedra (ID 1)

    mc.setBlock(pos.x, pos.y + 2, pos.z, 1) 
    # Colocar agua en la posición exacta del jugador para que se ahogue
    mc.setBlock(pos.x, pos.y + 1, pos.z, 9)  # Bloque de agua (ID 9)
    mc.setBlock(pos.x, pos.y , pos.z, 9)  # Bloque de agua (ID 9)

    # Añadir un mensaje de chat
    mc.postToChat(f"¡{player} ha sido enviado a prisión y está a punto de ahogarse!")



# Versión difícil de los castigos

def D_lava(player, mc):
    """Coloca un gran campo de lava alrededor del jugador como castigo difícil."""
    pos = mc.entity.getTilePos(player)
    # Colocar lava en un área más grande alrededor del jugador
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            mc.setBlock(pos.x + dx, pos.y, pos.z + dz, 10)  # Lava en un área 5x5

def D_tnt(player, mc):
    """Coloca múltiples TNT alrededor del jugador durante 10 segundos y las enciende."""
    start_time = time.time()
    while time.time() - start_time < 2:
        pos = mc.entity.getTilePos(player)
        # Colocar TNT y encender fuego en todas las direcciones alrededor del jugador
        for dx in range(-1, 2):  # Menos TNT, solo un área de 3x3
            for dz in range(-1, 2): 
                mc.setBlock(pos.x + dx, pos.y, pos.z + dz, 46)  # TNT
                mc.setBlock(pos.x + dx, pos.y + 1, pos.z + dz, 51)  # Fuego
        
        mc.setBlock(pos.x, pos.y, pos.z, 30)
        
        time.sleep(5)

def D_zombie(player, mc):
    """Invoca múltiples zombies alrededor del jugador como castigo difícil."""
    pos = mc.entity.getTilePos(player)
    # Invocar varios zombies en un área alrededor del jugador
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            spawn_mob(player, "Zombie", mc)  # Invocar un zombie en las posiciones alrededor del jugador

def D_prison(player, mc):
    """Rodea al jugador con bloques de piedra y coloca un bloque de agua donde está, para que se ahogue."""
    pos = mc.entity.getTilePos(player)

    # Rodear al jugador con bloques de piedra (en un cubo de 3x3 alrededor del jugador)
    for dx in range(-1, 2):  # -1, 0, 1
        for dz in range(-1, 2):  # -1, 0, 1
            for dy in range(0, 2):  # Cubrir las dos alturas (debajo y encima del jugador)
                mc.setBlock(pos.x + dx, pos.y + dy, pos.z + dz, 49)  # Bloques de piedra (ID 1)

    # Colocar agua en la posición exacta del jugador para que se ahogue
    mc.setBlock(pos.x, pos.y + 2, pos.z, 49) 
    mc.setBlock(pos.x, pos.y + 1, pos.z, 9)  # Bloque de agua (ID 9)
    mc.setBlock(pos.x, pos.y , pos.z, 9)  # Bloque de agua (ID 9)

    # Añadir un mensaje de chat
    mc.postToChat(f"¡{player} ha sido enviado a prisión y está a punto de ahogarse!")

