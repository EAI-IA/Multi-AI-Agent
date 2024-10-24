import asyncio
from collections import deque
import time
import random

# filler words to maintain engagement during an interruption
response_queue = asyncio.Queue()  # Create a queue for buffering AI responses

async def queue_response(response):
    """Add a response to the queue."""
    await response_queue.put(response)

async def get_next_response():
    """Get the next response from the queue."""
    return await response_queue.get()

interrupt_interjections = [
    "Oh, okay.", "Sure.", "Right.", "Got it.", "Alright.", "Okay.",
    "Uh-huh.", "Go on.", "Please, continue.", "Yes, go on.", 
    "Oh, go ahead.", "Oh, sorry, continue.", "Uh-huh, let's hear it.", 
    "Oh, please, go on."
]

# filler words to show the system is still capturing the voice
filler_words = [
    "Uh-huh", "I see", "Right", "Okay", "Got it", "I understand",
    "Mm-hmm.", "Uh-huh.", "Right.", "I see.", "Yeah.", 
    "Got it.", "Okay.", "Sure.", "Absolutely."
]

# seconds of silence accepted between a sentence to add a filler word while the user is talking to the AI
grace_period = 1.0

# Queue to track recent interruptions
recent_interruptions = deque(maxlen=10)  # Keep the last 10 interruptions

def register_interruption():
    """Register a user interruption."""
    current_time = time.time()
    recent_interruptions.append(current_time)

def get_interruption_frequency():
    """Calculate the frequency of user interruptions in the last 60 seconds."""
    current_time = time.time()
    # Only count interruptions within the last 60 seconds
    recent_interruptions_within_window = [
        t for t in recent_interruptions if current_time - t <= 60
    ]
    return len(recent_interruptions_within_window)

# Async generator function to provide filler words as an async iterable
async def filler_word_generator(filler):
    """Generate a filler word asynchronously."""
    yield filler



def handle_tts_state_change(tts, previous_speaking_state):
    """Handle changes in the TTS speaking state."""
    if tts.is_speaking != previous_speaking_state:
        if tts.is_speaking:
            print('TTS started speaking')
        else:
            print('TTS stopped speaking')
    return tts.is_speaking

def handle_vad_audio(audio_buffer, vad, speech_start_time, silence_start_time):
    """Process VAD audio input and return updated timing information."""
    if vad.is_speech(audio_buffer):
        if speech_start_time is None:
            speech_start_time = time.time()
        silence_start_time = None
    else:
        if silence_start_time is None:
            silence_start_time = time.time()
    return speech_start_time, silence_start_time

async def manage_interruption(tts, llm, interruption_duration, vad, audio_buffer, interrupt_interjections):
    """Handle a detected interruption based on its duration."""
    if tts.is_speaking and vad.is_speech(audio_buffer):  # Ensure the interruption is from the user and not while the system is talking
        if interruption_duration > 0.8:  # Significant interruption threshold
            print("Detected significant interruption. Stopping TTS.")
            tts.stop_speaking()
            # Queue a response and register the interruption
            await queue_response(random.choice(interrupt_interjections))
            register_interruption()
            return True
        else:
            print("Brief interruption detected. Continuing.")
            return False
    else:
        # If the AI is not speaking or there is no user speech detected, don't consider it an interruption
        return False



def adjust_response_mode(llm, interruption_frequency):
    """Adjust the response mode based on the interruption frequency."""
    if interruption_frequency >= 3:
        llm.set_short_response_mode(True)
        print("Short response mode activated.")
    else:
        llm.set_short_response_mode(False)
        print("Normal response mode activated.")