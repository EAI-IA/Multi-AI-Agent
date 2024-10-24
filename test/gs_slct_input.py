# main.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings('ignore')

import os
import openai
import time
# from openai import AsyncOpenAI
from config import OPENAI_API_KEY
# import asyncio
# from utils import queue_response, get_next_response

from crewai import Agent, Crew, Task

os.environ['OPENAI_API_KEY'] = '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'

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
    
    def call_open(self, inquiry):
        try:
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Responds in a concise manner: {inquiry}",
                max_tokens = 50
            )
            return completion.choices[0]
        except Exception as e:
            return f"Error LLM >>  {str(e)}"

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

crew = Crew(
    agents=[classifier_agent, redirect_agent],
    tasks=[classify_inquiry, redirect_inquiry],  
    verbose=2,
    memory=True 
)

# class VoiceBiteLLM:
#     def __init__(self, asr_queue, tts):
#         self.asr_queue = asr_queue
#         self.tts = tts
#         self.crew = Crew(
#             agents=[classifier_agent, redirect_agent],
#             tasks=[classify_inquiry, redirect_inquiry],
#             verbose=2,
#             memory=True
#         )

#     async def process_inquiry(self, query):
#         # Entradas para el sistema
#         inputs = {
#             "inquiry": query
#         }

#         # Ejecutar el equipo de agentes
#         result = await asyncio.to_thread(self.crew.kickoff, inputs=inputs)

#         # Mostrar el resultado final (si es necesario, para depuración)
#         print(result)

#         # Si hay respuesta, conviértela a voz
#         if result and isinstance(result, dict) and 'response' in result:
#             await self.tts.text_to_speech_input_streaming([result['response']])

#     async def run(self):
#         while True:
#             result = await self.asr_queue.get()
#             if result['result']['is_final']:
#                 await self.process_inquiry(result['result']['alternatives'][0]['transcript'])


def test_agents():
    test_queries = [
        "Hello?",
        "How to do it?",
        "sdi",
        "i am lov      e     o"

    ]


    for query in test_queries:
        start_time = time.time()

        print(f"Testing query: {query}")
        inputs = {"inquiry": query}
        result = crew.kickoff(inputs=inputs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Result: {result}")
        print(f"Tiempo de respuesta: {elapsed_time:.4f} segundos")


test_agents()
