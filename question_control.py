import time
import random
import csv
import os
from mcpi.minecraft import Minecraft  
from question import Question
from dificultQuestion import DificultQuestion  


mc = None  # No inicializamos inmediatamente

# Función que obtiene la instancia de Minecraft, si no está creada aún
def get_mc_instance():
    global mc
    if mc is None:
        mc = Minecraft.create()  # Solo crea la instancia si no existe
    return mc


# Variables globales
current_question = None  
questions = []  # Lista que almacena todas las preguntas disponibles
question_delay = 15  # Tiempo por defecto de espera en segundos entre preguntas

def add_question(questions, question, answer, reward, punishment):
    """
    Añadir una nueva pregunta al conjunto de preguntas.

    Args:
        questions (list): La lista de preguntas actuales.
        question (str): El texto de la pregunta.
        answer (str): La respuesta correcta.
        reward (str): La recompensa para una respuesta correcta.
        punishment (str): El castigo para una respuesta incorrecta.

    Returns:
        list: La lista actualizada de preguntas, incluyendo la nueva pregunta.
    """
    new_question = Question(question, answer, reward, punishment,mc)  
    return questions + [new_question] 

def check_answer(player, answer, current_question, questions):
    """
    Verificar la respuesta de un jugador y aplicar recompensa o castigo, devolviendo el nuevo estado.

    Args:
        player (int): El identificador del jugador.
        answer (str): La respuesta dada por el jugador.
        current_question (Question): La pregunta actual activa.
        questions (list): La lista de todas las preguntas disponibles.

    Returns:
        tuple: Un tupla con tres valores:
            - Un booleano que indica si la respuesta fue correcta.
            - La pregunta actual (o None si se ha completado).
            - La lista actualizada de preguntas.
    """
    if not current_question or not current_question.is_active():  
        mc.postToChat(f"No hay pregunta activa o el tiempo ha expirado. Espera a la siguiente.")
        return False, current_question, questions 

    if current_question.check_answer(answer):  
        mc.postToChat(f"¡Correcto! {player} gana una recompensa.")
        current_question.apply_reward(player)  # Aplica la recompensa al jugador
        
        questions = [q for q in questions if q != current_question]  # Elimina la pregunta respondida de la lista
        current_question.deactivate()  # Desactiva la pregunta
        return True, None, questions  
    
    else:  # Si la respuesta es incorrecta
        mc.postToChat(f"¡Incorrecto! {player} recibe un castigo.")
        current_question.apply_punishment(player)  # Aplica el castigo al jugador

        # Si la pregunta ha fallado dos veces y no es una pregunta difícil, la convierte en difícil
        if current_question.failed_attempts == 2 and not isinstance(current_question, DificultQuestion):
            mc.postToChat(f"La pregunta '{current_question.get_question()}' se convierte en difícil.")
            questions = [DificultQuestion(q) if q == current_question else q for q in questions]

        return False, current_question, questions 

def question_loop():
    """
    Mostrar preguntas aleatorias cada 'question_delay' segundos.

    Este bucle selecciona una nueva pregunta si no hay ninguna activa y la muestra en el chat. 
    Si la pregunta está activa durante más tiempo del esperado, la desactiva y selecciona una nueva.
    
    Este método se ejecuta indefinidamente.
    """
    advertisementCounter = 0

    global current_question
    while True:
        if not current_question or not current_question.is_active():  # Si no hay pregunta activa o está inactiva
            if questions: 
                advertisementCounter = 0
                current_question = random.choice(questions)  # Selecciona una pregunta aleatoria
                current_question.activate()  # Activa la pregunta
                mc.postToChat(f"Pregunta: {current_question.get_question()}")  # Muestra la pregunta en el chat
            elif advertisementCounter == 0:
                    mc.postToChat("No hay más preguntas disponibles. Añade nuevas para continuar.")  # Si no hay preguntas, lo indica
                    advertisementCounter = advertisementCounter + 1
    
        time.sleep(question_delay)  # Espera durante el tiempo especificado antes de mostrar otra pregunta
        
        if current_question and current_question.is_active():  # Si la pregunta sigue activa
            current_question.deactivate()  # Desactiva la pregunta
            mc.postToChat("El tiempo para esta pregunta ha terminado. Se seleccionará otra.")  
            current_question = None  # Establece la pregunta activa como None

def add_example_questions():

    """
    Agregar preguntas iniciales al conjunto de preguntas.

    Esto permite tener un conjunto inicial de preguntas antes de que el usuario agregue nuevas preguntas.
    """
    global questions
    get_mc_instance()
    # Añade algunas preguntas de ejemplo al principio
    questions = add_question(questions, "¿Cuánto es 2 + 2?", "4", "diamond", "tnt")
    questions = add_question(questions, "¿Cuál es la capital de Francia?", "Paris", "gold", "zombie")
    questions = add_question(questions, "¿Cuánto es 5x5?", "25", "food", "prison")
    questions = add_question(questions, "¿Cuánto es 2^2?", "4", "food", "lava")

def add_questions_from_csv(csv_file):
    """
    Leer preguntas desde un archivo CSV y añadirlas a la lista de preguntas.

    Args:
        csv_file (str): El nombre del archivo CSV que contiene las preguntas.
    
    Esta función procesará el archivo CSV y añadirá cada pregunta, respuesta, recompensa y castigo a la lista de preguntas.
    """
    try:
        with open(csv_file, newline='', encoding='utf-8') as file:  # Abre el archivo CSV
            reader = csv.reader(file) 
            next(reader)            
            for row in reader:  # Procesa cada fila del CSV
                if len(row) == 4:  
                    question, answer, reward, punishment = row
                    global questions
                    questions = add_question(questions, question.strip(), answer.strip(), reward.strip(), punishment.strip())  # Añade la pregunta a la lista
                    mc.postToChat(f"Pregunta añadida desde CSV: {question}") 
                else:
                    mc.postToChat(f"Fila inválida en el archivo CSV: {row}") 
    except Exception as e:
        mc.postToChat(f"Error al leer el archivo CSV: {str(e)}")  

def increase_difficulty_by_punishment(punishment, questions):
    """
    Aumentar la dificultad de todas las preguntas con un castigo específico.

    Args:
        punishment (str): El castigo que se usará para identificar las preguntas a las que se les aumentará la dificultad.
    """
    questions
    # Reemplaza las preguntas que tienen un castigo específico por su versión difícil
    questions = list(map(
        lambda q: DificultQuestion(q) if q.punishment == punishment and not isinstance(q, DificultQuestion) else q,
        questions
    ))
    mc.postToChat(f"Dificultad aumentada para preguntas con castigo: {punishment}") 
    return questions

def show_help():
    """
    Mostrar los comandos disponibles en el chat del juego.

    Los jugadores pueden usar estos comandos para interactuar con el sistema de preguntas y respuestas.
    """
    mc.postToChat("Comandos disponibles:")
    mc.postToChat("Para responder una pregunta activa: r <respuesta>")
    mc.postToChat("Para insertar una pregunta: !q <pregunta>_<respuesta>_<recompensa>_<castigo>")
    mc.postToChat("Para ajustar el tiempo entre preguntas: !t <periodo_en_segundos>")
    mc.postToChat("Para insertar un lote de preguntas: !p <nombre_lote>")
    mc.postToChat("Para mostrar lotes disponibles: !ps")
    mc.postToChat("Para aumentar la dificultad por castigo: !d <castigo>")
    mc.postToChat("Para disminuir la dificultad por castigo: !e <castigo>")

def add_question_command(message):
    """
    Procesar el comando para agregar una nueva pregunta.

    Args:
        message (str): El mensaje recibido del jugador, que debe seguir el formato de comando correcto.
    """
    try:
        _, content = message.split(" ", 1)  
        parts = content.split("_")  # Usamos "_" como separador

        if len(parts) != 4:  
            mc.postToChat("Formato incorrecto. Usa: !q <pregunta>_<respuesta>_<recompensa>_<castigo>")
            return

        question, answer, reward, punishment = parts
        global questions
        questions = add_question(questions, question, answer, reward, punishment)  # Añade la nueva pregunta

        mc.postToChat(f"Pregunta añadida: {question}") 
    except ValueError:
        mc.postToChat("Error procesando el comando. Usa el formato correcto.")  

def respond_to_question(player, message):
    """
    Procesar la respuesta a la pregunta activa.

    Args:
        player (int): El identificador del jugador que responde.
        message (str): El mensaje que contiene la respuesta del jugador.
    """
    try:
        _, answer = message.split(" ", 1)  # Extrae la respuesta del mensaje
        global questions, current_question
        _, current_question, questions = check_answer(player, answer, current_question, questions)  # Verifica la respuesta

    except ValueError:
        mc.postToChat("Formato incorrecto. Usa: !r <respuesta>") 

def load_questions_from_csv(message):
    """
    Cargar preguntas desde un archivo CSV.

    Args:
        message (str): El mensaje recibido que contiene el nombre del archivo CSV a cargar.
    """
    try:
        _, csv_file = message.split(" ", 1)  # Extrae el nombre del archivo CSV
        csv_file = csv_file.strip()  

        if not csv_file.endswith('.csv'):  # Si el archivo no tiene extensión '.csv', la agrega
            csv_file += '.csv'

        current_directory = os.path.dirname(__file__)  # Obtiene el directorio actual
        parent_directory = os.path.dirname(current_directory)  # Obtiene el directorio padre
        csv_path = os.path.join(parent_directory, 'MinecraftFramework_QuizCraft', 'csvs', csv_file)  # Construye la ruta completa al archivo CSV

        if os.path.exists(csv_path): 
            add_questions_from_csv(csv_path)  # Carga las preguntas desde el archivo CSV
            return questions
        else:
            mc.postToChat(f"El archivo '{csv_path}' no existe en la carpeta 'csvs'.")  
    except ValueError:
        mc.postToChat("Formato incorrecto. Usa: !p <nombre_csv>")  

def change_question_delay(message):
    """
    Cambiar el intervalo de tiempo entre preguntas.

    Args:
        message (str): El mensaje recibido que contiene el nuevo periodo en segundos.
    """
    try:
        _, time_str = message.split(" ", 1)  # Extrae el tiempo del mensaje
        new_delay = int(time_str.strip())  # Convierte el tiempo a entero

        if new_delay <= 0:  
            mc.postToChat("El tiempo debe ser mayor que cero.")
        else:
            global question_delay
            question_delay = new_delay  # Actualiza el tiempo de espera entre preguntas
            mc.postToChat(f"El tiempo entre preguntas ha sido cambiado a {question_delay} segundos.") 
            return question_delay 
    except ValueError:
        mc.postToChat("Formato incorrecto. Usa: !t <segundos>")  

def adjust_difficulty_command(message, increase=True):
    """
    Aumentar o disminuir la dificultad de las preguntas según su castigo.

    Args:
        message (str): El mensaje recibido que contiene el castigo.
        increase (bool): Si es True, aumenta la dificultad, si es False, disminuye la dificultad.
    """
    try:
        global questions
        _, punishment = message.split(" ", 1)  # Extrae el castigo del mensaje
        punishment = punishment.strip()  # Elimina espacios adicionales
        questions = increase_difficulty_by_punishment(punishment, questions)  # Llama a la función para aumentar o disminuir la dificultad

    except ValueError:
        command = "!d"
        mc.postToChat(f"Formato incorrecto. Usa: {command} <castigo>")  

def list_csv_files():
    """
    Listar todos los archivos CSV en la carpeta 'csvs'.

    Returns:
        list: Lista de nombres de archivos CSV disponibles en la carpeta 'csvs'.
    """
    current_directory = os.path.dirname(__file__)  # Obtiene el directorio actual
    parent_directory = os.path.dirname(current_directory)  # Obtiene el directorio padre
    csv_directory = os.path.join(parent_directory, 'scriptsPython', 'csvs')  # Ruta de la carpeta 'csvs'

    try:
        # Lista todos los archivos en la carpeta 'csvs' y filtra solo los archivos con extensión '.csv'
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
        
        if csv_files:
            # Enviar cada archivo CSV en una nueva línea
            for file in csv_files:
                mc.postToChat(file)
        else:
            mc.postToChat("No se encontraron archivos CSV en la carpeta 'csvs'.")
    except Exception as e:
        mc.postToChat(f"Error al listar los archivos CSV: {str(e)}")


def handle_chat():
    """
    Manejar los mensajes del chat del juego.

    Este bucle procesa los mensajes recibidos en el chat y ejecuta los comandos correspondientes.
    """
    while True:
        try:
            chat_events = mc.events.pollChatPosts()  # Obtiene los mensajes del chat
            for event in chat_events:
                message = event.message.strip()  # Extrae el mensaje y lo limpia de espacios adicionales
                player = int(event.entityId)  # Obtiene el ID del jugador

                if message.startswith("!h"):  # Si el mensaje comienza con '!h', muestra la ayuda
                    show_help()
                elif message.startswith("!q"):  # Si el mensaje es para añadir una pregunta, procesa el comando
                    questions = add_question_command(message)
                elif message.startswith("!r"):  # Si el mensaje es para responder, procesa la respuesta
                    respond_to_question(player, message)
                elif message.startswith("!p"):  # Si el mensaje es para cargar un archivo CSV, procesa el comando
                    load_questions_from_csv(message)
                elif message.startswith("!t"):  # Si el mensaje es para cambiar el tiempo, ajusta el periodo
                    change_question_delay(message)
                elif message.startswith("!d"):  # Si el mensaje es para aumentar la dificultad, procesa el comando
                    adjust_difficulty_command(message, increase=True)
                elif message.startswith("!sp"):  # Si el mensaje es para mostrar los archivos CSV, procesa el comando
                    list_csv_files()

        except Exception as e:
            mc.postToChat(f"Error inesperado: {str(e)}")  
        time.sleep(0.1)  # Espera un pequeño intervalo antes de procesar el siguiente mensaje para no sobrecargar el servidor