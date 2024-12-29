from mcpi.minecraft import Minecraft
import rewards  
import punishments  

class Question:
    def __init__(self, question, answer, reward, punishment, mc):
        """
        Constructor de la clase Question.

        Args:
            question (str): El texto de la pregunta.
            answer (str): La respuesta correcta.
            reward (str): El nombre de la recompensa para la respuesta correcta.
            punishment (str): El nombre del castigo para la respuesta incorrecta.
        """
        self.question = question  
        self.answer = answer  
        self.reward = reward  
        self.punishment = punishment  
        self.failed_attempts = 0  
        self.active = False  
        self.mc = mc

    def get_question(self):
        """
        Retorna la pregunta.

        Returns:
            str: La pregunta almacenada.
        """
        return self.question

    def check_answer(self, answer):
        """
        Comprobar si la respuesta proporcionada es correcta.

        Args:
            answer (str): La respuesta proporcionada por el jugador.

        Returns:
            bool: True si la respuesta es correcta, False si es incorrecta.
        """
        if self.answer.strip().lower() == answer.strip().lower():
            return True
        self.increment_failed_attempts()  
        return False

    def apply_reward(self, player):
        """
        Aplica la recompensa correspondiente al jugador si la respuesta es correcta.

        Args:
            player (int): El identificador del jugador que ha respondido correctamente.
        """
        reward_function = getattr(rewards, self.reward, None)
        if reward_function:
            reward_function(player, self.mc)  # Llama a la función de recompensa
        else:
           self.mc.postToChat(f"Error: Recompensa '{self.reward}' no válida.")  # Si la recompensa no es válida, muestra un mensaje de error

    def apply_punishment(self, player):
        """
        Aplica el castigo correspondiente al jugador si la respuesta es incorrecta.

        Args:
            player (int): El identificador del jugador que ha respondido incorrectamente.
        """
        punishment_function = getattr(punishments, self.punishment, None)
        if punishment_function:
            punishment_function(player,self.mc)  # Llama a la función de castigo
        else:
            self.mc.postToChat(f"Error: Castigo '{self.punishment}' no válido.")  # Si el castigo no es válido, muestra un mensaje de error

    def increment_failed_attempts(self):
        """
        Incrementa el contador de intentos fallidos por una respuesta incorrecta.
        """
        self.failed_attempts += 1

    def reset_failed_attempts(self):
        """
        Resetea el contador de intentos fallidos, reiniciándolo a 0.
        """
        self.failed_attempts = 0

    def activate(self):
        """
        Activa la pregunta, indicando que está disponible para ser respondida.
        """
        self.active = True

    def deactivate(self):
        """
        Desactiva la pregunta, indicando que ya no está disponible para ser respondida.
        """
        self.active = False

    def is_active(self):
        """
        Verifica si la pregunta está activa.

        Returns:
            bool: True si la pregunta está activa, False si no lo está.
        """
        return self.active
