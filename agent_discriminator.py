# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
import os
from IPython.display import Markdown

from openai import AsyncOpenAI
from config import OPENAI_API_KEY
import asyncio
from utils import queue_response, get_next_response

class VoiceBiteLLM:
    def __init__(self, asr_queue, tts):
        self.aclient = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.system_prompt = """You are a helpful assistant..."""
        self.messages = [{'role': 'system', 'content': self.system_prompt}]
        self.asr_queue = asr_queue
        self.tts = tts
        self.short_response_mode = False

    def set_short_response_mode(self, enable):
        """Enable or disable short response mode."""
        self.short_response_mode = enable

    async def chat(self, query):
        self.messages.append({'role': 'user', 'content': query})
        response = await self.aclient.chat.completions.create(
            model="gpt-4o-mini", messages=self.messages,
            max_tokens=32 if self.short_response_mode else 64,
            temperature=0.2, stream=True)

        async def text_iterator():
            full_ai = ""
            async for chunk in response:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        full_ai = f"{full_ai} {delta.content}"
                        yield delta.content
            self.messages.append({'role': 'assistant', 'content': full_ai})

    async def run(self):
        while True:
            result = await self.asr_queue.get()
            if result['result']['is_final']:
                await self.chat(result['result']['alternatives'][0]['transcript'])






