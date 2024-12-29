from question import Question  
import rewards  
import punishments 
from mcpi.minecraft import Minecraft  
# Crea una conexión con el mundo de Minecraft



class DificultQuestion(Question):
    """
    Clase que hereda de la clase Question y modifica su comportamiento para manejar preguntas difíciles.

    Las preguntas difíciles tienen una versión modificada de recompensas y castigos.
    """
    def __init__(self, original_question):
        """
        Inicializa una nueva instancia de DificultQuestion usando una pregunta original.

        Args:
            original_question (Question): La pregunta original que se convierte en una versión difícil.
        """
        super().__init__(
            original_question.get_question(),
            original_question.answer,
            original_question.reward,  
            original_question.punishment,  
            original_question.mc
        )
        self.failed_attempts = original_question.failed_attempts

    def apply_reward(self, player):
        """
        Aplica la recompensa difícil al jugador, utilizando una versión especial de la recompensa.

        Args:
            player (int): El identificador del jugador que responde correctamente.
        """
        # Intenta obtener la función de recompensa difícil (prefijada con "D_") desde el módulo 'rewards'
        reward_function = getattr(rewards, f"D_{self.reward}", None)
        if reward_function:
            reward_function(player, self.mc)  # Llama a la función de recompensa difícil
        else:
            # Si no se encuentra la recompensa difícil, muestra un mensaje de error en el chat de Minecraft
            self.mc.postToChat(f"Error: Recompensa difícil 'f D_{self.reward}' no válida.")

    def apply_punishment(self, player):
        """
        Aplica el castigo difícil al jugador, utilizando una versión especial del castigo.

        Args:
            player (int): El identificador del jugador que responde incorrectamente.
        """
        # Intenta obtener la función de castigo difícil (prefijada con "D_") desde el módulo 'punishments'
        punishment_function = getattr(punishments, f"D_{self.punishment}", None)
        if punishment_function:
            punishment_function(player, self.mc)  # Llama a la función de castigo difícil
        else:
            # Si no se encuentra el castigo difícil, muestra un mensaje de error en el chat de Minecraft
            self.mc.postToChat(f"Error: Castigo difícil 'fD_{self.punishment}' no válido.")
