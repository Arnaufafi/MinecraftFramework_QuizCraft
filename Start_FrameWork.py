# main.py
import time
import threading
import question_control

# Iniciar el programa
if __name__ == "__main__":
    # Inicializar las preguntas
    questions = question_control.add_example_questions()  # Llama a la función add_example_questions desde question_control para cargar preguntas predeterminadas
    current_question = None 

    chat_thread = threading.Thread(target=question_control.handle_chat)  # Crea un hilo para manejar los mensajes del chat
    question_thread = threading.Thread(target=question_control.question_loop)  # Crea un hilo para manejar la lógica de preguntas

    # Iniciar los hilos
    chat_thread.start()  
    question_thread.start()  

    # Esperar a que los hilos terminen
    chat_thread.join()  
    question_thread.join()  
