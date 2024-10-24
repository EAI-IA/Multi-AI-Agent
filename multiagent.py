import warnings  # Para que las advertencias no interfieran
warnings.filterwarnings('ignore')

from crewai import Agent, Crew, Task

# Agente Clasificador 
class ClassifierAgent(Agent):
    def act(self, inquiry, history):
        if not inquiry or len(inquiry.split()) < 2:
            return "False"  # vacio o few words
        
        if "?" not in inquiry or len(inquiry.split()) < 5:
            return "Ambiguous"  # poca claridad
        return "True"  # correcto


# Agente de Redirección
class RedirectAgent(Agent):
    def act(self, inquiry, coherence):
        if coherence == "False" or coherence == "Ambiguous":
            return None  # next interacao
        
        return "Listo."  # Respuesta rápida y concisa

# Agente Clasificador
classifier_agent = ClassifierAgent(
    role="Intent Classifier",
    goal="Quickly identify the intent behind user inquiries and determine coherence.",
    backstory="You analyze user input quickly and request clarification when necessary.",
    allow_delegation=False,
    verbose=True
)

# Agente de Redirección
redirect_agent = RedirectAgent(
    role="Inquiry Redirector",
    goal="Respond only to coherent inquiries, keeping interaction fast.",
    backstory="You guide users and respond instantly when inquiries are coherent.",
    allow_delegation=False,
    verbose=True
)

# Tareas de los agentes
classify_inquiry = Task(
    description="Analyze the user inquiry to determine its coherence:\n{inquiry}\n",
    expected_output="Classify inquiry as coherent, ambiguous, or incoherent.",
    agent=classifier_agent
)

redirect_inquiry = Task(
    description="Provide an instant response or wait based on coherence classification:\n{inquiry}\n",
    expected_output="Response or silence based on classification.",
    agent=redirect_agent
)

# # Agente Clasificador
# classifier_agent = Agent(
#     role="Intent Classifier",
#     goal="Identify the intent behind user inquiries and assess their coherence.",
#     backstory=(
#         "You are a smart assistant designed to analyze user input "
#         "and determine whether the questions make sense in context."
#     ),
#     allow_delegation=False,
#     verbose=True
# )

# # Agente de Redirección o Escalado
# redirect_agent = Agent(
#     role="Inquiry Redirector",
#     goal="Redirect users to appropriate resources when inquiries are incoherent.",
#     backstory=(
#         "You assist users by guiding them to the right resources or "
#         "agents when their inquiries cannot be resolved directly."
#     ),
#     allow_delegation=False,
#     verbose=True
# )

# # Tarea de Clasificación de Intención
# classify_inquiry = Task(
#     description="Analyze the user inquiry to determine its coherence:\n{inquiry}\n",
#     expected_output="Classification of the inquiry as either coherent or incoherent.",
#     agent=classifier_agent
# )

# # Tarea de Redirección
# redirect_inquiry = Task(
#     description="Redirect the user to appropriate resources if the inquiry is incoherent:\n{inquiry}\n",
#     expected_output="Guidance or response based on the coherence classification.",
#     agent=redirect_agent
# )

crew = Crew(
    agents=[classifier_agent, redirect_agent],
    tasks=[classify_inquiry, redirect_inquiry],  
    verbose=2,
    memory=True 
)

while True:
    iii = input("> ")
    if iii.lower() == "salir":
        break

    # Entradas para el sistema
    inputs = {
        "inquiry": iii
    }

    # Ejecutar el equipo de agentes
    result = crew.kickoff(inputs=inputs)

    # Mostrar el resultado final
    print(result)






    # --------------------------------------


    # STATE MANAGER 

# state_manager.py

# from enum import Enum, auto
# from asr import DeepGramASR
# import time

# class SystemState(Enum):
#     IDLE = auto()
#     LISTENING = auto()
#     THINKING = auto()
#     SPEAKING = auto()
#     INTERRUPTING = auto()

# class StateManager:
#     def __init__(self):
#         self.current_state = SystemState.IDLE
#         self.speech_detection_time = None

#     def set_state(self, new_state):
#         print(f"Transitioning from {self.current_state.name} to {new_state.name}")
#         self.current_state = new_state

#     def get_state(self):
#         return self.current_state

#     def is_state(self, state):
#         return self.current_state == state

#     async def handle_state(self, vad, tts, asr, llm, audio_buffer):
#         """
#         Update the system state based on VAD, TTS, and ASR inputs.
#         """
#         if self.is_state(SystemState.IDLE):
#             # Transition directly to LISTENING if speech is detected consistently
#             if vad.is_speech(audio_buffer):
#                 if self.speech_detection_time is None:
#                     self.speech_detection_time = time.time()
#                 elif time.time() - self.speech_detection_time > 0.3:  # 300ms threshold
#                     print("Consistent speech detected, transitioning to LISTENING")
#                     self.set_state(SystemState.LISTENING)
#             else:
#                 # Reset detection time if no speech is detected
#                 self.speech_detection_time = None

#         elif self.is_state(SystemState.LISTENING):
#             if vad.is_speech(audio_buffer):
#                 print("Detected speech, transitioning to THINKING")
#                 self.set_state(SystemState.THINKING)
#             elif not vad.is_speech(audio_buffer) and self._is_long_silence(audio_buffer):
#                 print("No speech detected for a while, transitioning to IDLE")
#                 self.set_state(SystemState.IDLE)

#         elif self.is_state(SystemState.THINKING):
#             if asr.is_final_transcription_available():
#                 print("ASR final result detected, sending input to LLM")
#                 transcription = asr.fetch_final_transcription()
#                 if transcription:
#                     await llm.chat(transcription['result']['alternatives'][0]['transcript'])

#             if llm.has_final_response() and not tts.is_speaking:
#                 print("LLM has final response, transitioning to SPEAKING")
#                 self.set_state(SystemState.SPEAKING)

#         elif self.is_state(SystemState.SPEAKING):
#             if tts.is_speaking and vad.is_speech(audio_buffer) and self._is_significant_interruption(audio_buffer):
#                 print("User interrupted during TTS, transitioning to INTERRUPTING")
#                 self.set_state(SystemState.INTERRUPTING)
#             elif not tts.is_speaking:
#                 print("TTS finished speaking, transitioning to LISTENING")
#                 self.set_state(SystemState.LISTENING)

#     def _is_significant_interruption(self, audio_buffer):
#         interruption_duration = len(audio_buffer) / 16000.0
#         return interruption_duration > 0.5

#     def _is_long_silence(self, audio_buffer):
#         silence_duration = len(audio_buffer) / 16000.0
#         return silence_duration > 2.0
