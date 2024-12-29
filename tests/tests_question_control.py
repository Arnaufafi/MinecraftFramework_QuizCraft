# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock, patch, mock_open
from mcpi.minecraft import Minecraft

import sys
import os

# Agrega el directorio raíz del proyecto a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Importa módulos según tu estructura de proyecto
from question_control import (
    get_mc_instance, add_question, check_answer, load_questions_from_csv,
    change_question_delay, increase_difficulty_by_punishment, show_help
)
from question import Question
from dificultQuestion import DificultQuestion


class TestQuestionControl(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create', return_value=MagicMock())
    def setUp(self, mock_mc_create):
        """
        Inicializa el entorno antes de cada prueba.
        Crea una nueva instancia de mc usando get_mc_instance().
        """
        global mc, questions
        mc = get_mc_instance()
        mc.postToChat = MagicMock()  # Mock para evitar interacciones reales en el chat de Minecraft
        questions = []  # Reinicia la lista de preguntas para cada prueba

    @patch('mcpi.minecraft.Minecraft.create')
    def test_add_question(self, mock_mc_create):
        mock_mc_create.return_value = mc

        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"

        global questions
        questions = add_question(questions, question, answer, reward, punishment)

        self.assertEqual(len(questions), 1)  # Debería haber 1 pregunta
        self.assertEqual(questions[-1].get_question(), question)

    @patch('mcpi.minecraft.Minecraft.create')
    @patch.object(Question, 'apply_reward', lambda x, y: None) #Hacer que la función `apply_reward` no haga nada
    def test_check_answer_correct(self, mock_mc_create):
        mock_mc_create.return_value = mc

        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"

        global questions
        questions = add_question(questions, question, answer, reward, punishment)

        player_id = 12345
        current_question = questions[0]
        current_question.activate()
        result, _, _ = check_answer(player_id, answer, current_question, questions)

        self.assertTrue(result)

    @patch('mcpi.minecraft.Minecraft.create')
    @patch.object(Question, 'apply_punishment', lambda x, y: None) #Hacer que la función `apply_punishment` no haga nada
    def test_check_answer_incorrect(self, mock_mc_create):
        mock_mc_create.return_value = mc

        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"

        global questions
        questions = add_question(questions, question, answer, reward, punishment)

        player_id = 12345
        current_question = questions[0]
        current_question.activate()

        result, _, _ = check_answer(player_id, "5", current_question, questions)

        self.assertFalse(result)
        mc.postToChat.assert_called_with(f"¡Incorrecto! {player_id} recibe un castigo.")

    @patch('mcpi.minecraft.Minecraft.create')
    @patch.object(Question, 'apply_punishment', lambda x, y: None) #Hacer que la función `apply_punishment` no haga nada
    def test_convert_question_to_difficult(self, mock_mc_create):
        mock_mc_create.return_value = mc

        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"

        global questions
        questions = add_question(questions, question, answer, reward, punishment)

        player_id = 12345
        current_question = questions[0]
        current_question.activate()

        for _ in range(3):
            _, _, questions = check_answer(player_id, "5", current_question, questions)

        self.assertIsInstance(questions[0], DificultQuestion)

    @patch('mcpi.minecraft.Minecraft.create')
    @patch('builtins.open', new_callable=mock_open, read_data="pregunta,respuesta,recompensa,castigo\n¿Cuánto es 2 + 2?,4,diamond,prision\n¿Cuál es la raíz cuadrada de 81?,9,diamond,lava")
    def test_load_questions_from_csv(self, mock_open, mock_mc_create):
        mock_mc_create.return_value = mc

        global questions
        questions = []

        questions = load_questions_from_csv("!p math")

        self.assertEqual(len(questions), 2)

    @patch('mcpi.minecraft.Minecraft.create')
    def test_change_question_delay(self, mock_mc_create):
        mock_mc_create.return_value = mc

        question_delay = change_question_delay("!t 10")

        self.assertEqual(question_delay, 10)

    @patch('mcpi.minecraft.Minecraft.create')
    def test_increase_difficulty_by_punishment(self, mock_mc_create):
        mock_mc_create.return_value = mc

        global questions
        questions = []
        question = "¿Cuánto es 2 + 2?"
        answer = "4"
        reward = "diamond"
        punishment = "tnt"

        questions = add_question(questions, question, answer, reward, punishment)

        questions = increase_difficulty_by_punishment("tnt", questions)

        self.assertIsInstance(questions[0], DificultQuestion)

    @patch('mcpi.minecraft.Minecraft.create')
    def test_show_help(self, mock_mc_create):
        mock_mc_create.return_value = mc

        show_help()

        mc.postToChat.assert_any_call("Comandos disponibles:")
        mc.postToChat.assert_any_call("Para responder una pregunta activa: r <respuesta>")
        mc.postToChat.assert_any_call("Para insertar una pregunta: !q <pregunta>_<respuesta>_<recompensa>_<castigo>")


if __name__ == "__main__":
    unittest.main()
