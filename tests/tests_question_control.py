import unittest
from unittest.mock import MagicMock, patch, mock_open

import sys
import os

# Agrega el directorio raíz del proyecto a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Asegúrate de que estas rutas coincidan con tu estructura
from question_control import *
from question import Question
from dificultQuestion import DificultQuestion
import random


class TestQuestionControl(unittest.TestCase):

    # Inicializar la lista de preguntas antes de cada prueba
    def setUp(self):
        global questions
        questions = []  # Reiniciar la lista de preguntas

    # Simula la creación de una nueva pregunta
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    def test_add_question(self, mock_post_to_chat, mock_mc_create):
        # Prepara la simulación de la creación de la conexión Minecraft
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()

        # Nueva pregunta a añadir
        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"

        # Añadir la pregunta
        global questions
        questions = add_question(questions, question, answer, reward, punishment)

        # Verificar que la pregunta fue añadida correctamente
        self.assertEqual(len(questions), 1)  # Debería haber 5 preguntas (4 iniciales + 1 nueva)
        self.assertEqual(questions[-1].get_question(), question)

    # Simula una respuesta correcta
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    @patch.object(Question, 'apply_reward', lambda x, y: None) #Hacer que la función `apply_reward` no haga nada
    def test_check_answer_correct(self, mock_post_to_chat, mock_mc_create):
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()

        # Crear una pregunta y agregarla a la lista
        global questions
        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"
        questions = []
        questions = add_question(questions, question, answer, reward, punishment)

        # Responder correctamente
        player_id = 12345
        current_question = questions[0]
        current_question.active = True
        result, _, _ = check_answer(player_id, answer,current_question, questions)
        # Verificar que la respuesta haya sido correcta
        self.assertTrue(result)

    # Simula una respuesta incorrecta
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    @patch.object(Question, 'apply_punishment', lambda x, y: None) #Hacer que la función `apply_punishment` no haga nada
    def test_check_answer_incorrect(self, mock_post_to_chat, mock_mc_create):
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()

        # Crear una pregunta y agregarla a la lista
        global questions
        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"
        questions = []
        questions = add_question(questions, question, answer, reward, punishment)

        # Responder correctamente
        player_id = 12345
        current_question = questions[0]
        current_question.active = True

        result, _, _ = check_answer(player_id, "5", questions[0], questions)

        # Verificar que la respuesta haya sido incorrecta
        self.assertFalse(result)
        mock_post_to_chat.assert_called_with(f"¡Incorrecto! {player_id} recibe un castigo.")

    # Simula la conversión de una pregunta en difícil después de 2 respuestas incorrectas
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    @patch.object(Question, 'apply_punishment', lambda x, y: None) #Hacer que la función `apply_punishment` no haga nada
    def test_convert_question_to_difficult(self, mock_post_to_chat, mock_mc_create):
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()

        # Crear una pregunta y agregarla a la lista
        global questions
        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"
        questions = add_question(questions, question, answer, reward, punishment)

        # Simular dos intentos incorrectos
        player_id = 12345
        current_question = questions[0]
        current_question.active = True

        # Responder incorrectamente dos veces
        _,_, questions = check_answer(player_id, "5", current_question, questions)  # Primer intento incorrecto
        _,_, questions = check_answer(player_id, "6", current_question, questions)  # Segundo intento incorrecto
        _,_, questions = check_answer(player_id, "6", current_question, questions)  # Tercer intento incorrecto

        # Verificar que la pregunta se convirtió en difícil después de 2 intentos fallidos
        self.assertIsInstance(questions[0], DificultQuestion)


    # Simula la carga de preguntas desde un archivo CSV
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    @patch('builtins.open', new_callable=mock_open, read_data="pregunta,respuesta,recompensa,castigo\n¿Cuánto es 2 + 2?, 4, diamond, prision\n¿Cuál es la raíz cuadrada de 81?, 9, diamond, lava")
    def test_load_questions_from_csv(self, mock_open, mock_post_to_chat, mock_mc_create):
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()
        global questions
        questions = []

        # Simula la carga desde un archivo CSV
        questions = load_questions_from_csv("!p math")

        # Verifica que la pregunta se haya cargado correctamente
        self.assertEqual(len(questions), 2)  # Debería haber 2 preguntas cargadas
    # Simula cambiar el tiempo entre preguntas
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    def test_change_question_delay(self, mock_post_to_chat, mock_mc_create):
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()

        # Cambiar el tiempo entre preguntas
        question_delay = change_question_delay("!t 10")

        # Verificar que el tiempo de espera ha cambiado
        self.assertEqual(question_delay, 10)  # Ensure this variable is modified correctly

    # Simula aumentar la dificultad de preguntas con un castigo específico
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    def test_increase_difficulty_by_punishment(self, mock_post_to_chat, mock_mc_create):
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()

        # Añadir una pregunta con un castigo específico
        global questions
        questions=[]
        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"
        questions = add_question(questions, question, answer, reward, punishment)

        # Aumentar la dificultad de las preguntas con castigo 'tnt'
        questions = increase_difficulty_by_punishment("tnt", questions)

        # Verificar que la dificultad haya aumentado para la pregunta
        self.assertIsInstance(questions[0], DificultQuestion)

    # Simula mostrar la ayuda
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('question_control.mc.postToChat')
    def test_show_help(self, mock_post_to_chat, mock_mc_create):
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        mock_post_to_chat.reset_mock()

        # Mostrar ayuda
        show_help()

        # Verificar que se muestra la ayuda
        mock_post_to_chat.assert_any_call("Comandos disponibles:")
        mock_post_to_chat.assert_any_call("Para responder una pregunta activa: r <respuesta>")
        mock_post_to_chat.assert_any_call("Para insertar una pregunta: !q <pregunta>_<respuesta>_<recompensa>_<castigo>")

if __name__ == "__main__":
    unittest.main()
