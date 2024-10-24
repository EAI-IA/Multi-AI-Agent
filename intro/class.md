
# Multi Ai Agent con CREW AI

> Joao Moura creador de crew AI


- Trabajar con MultiAgent es dividir el trabajo
- enfocarse en? juego de roles, memoria, usos de herramientas, barreras de segurdad y colaboraciones.

Role-playing: Assign specialized roles to agents 
Memory: Provide agents with short-term, long-term, and shared memory
Tools: Assign pre-built and custom tools to each agent (e.g. for web search)
Focus: Break down the tasks, goals, and tools and assign to multiple AI agents for better performance
Guardrails: Effectively handle errors, hallucinations, and infinite loops
Cooperation: Perform tasks in series, in parallel, and hierarchically


Como es la automatización Agent?
antes >> diagrama de estados
        condiciones y programa extendo.


### Fuzzy inputs, transformations, outputs

|                              | Traditional Software Development                                   | AI Software Development                                   |
|------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------|
| **Inputs**                    | - text (string) with defined set ("happy", "calm")<br> - numeric (int, float) | **Fuzzy inputs**: Open-ended text<br> - Tabular data<br> - Markdown<br> - Text<br> - Math operation |
| **Transformations**           | - Math calculation (+ - ÷ ✖)<br> - f"Hello {first_name}, how are you?"<br> - if, elif, else<br> - for/while loops | **Fuzzy transformations**:<br> - Extract list of key words<br> - Rewrite as a paragraph<br> - Answer a question<br> - Brainstorm new ideas<br> - Perform logic/math reasoning |
| **Outputs**                   | - text (string) with defined set ("Positive", "Neutral")<br> - numeric (int, float) | **Fuzzy outputs**:<br> - Paragraph<br> - Number(s)<br> - JSON<br> - Markdown |
| **Notes**                     | - Can be replicated                                               | - Probabilistic: can be different every time               |




Lo interesante de los modelos de IA es la imprecision de las entrada y las salidas, se sabe que ellas pueden hacer una secuencia de operaciones para devolver una salida pero no es necesario la precisión de las entradas pero si podemos determinar la estructura de la salida, pero con amoldamiento de la entrada.

## AGENTS

Interaccion  comenzando con un LLM
- **Agent**: un modelo de IA que puede interactuar con el usuario
las dificulatedes de la interaccion con un LLM es ue tiene respuestas extensas.
la forma de corregir las interaccions es conversar más y darle instrucciones para que sean más precisos.

para entrenar un red neoraal it needs a big data base its ne
the robots reasoning consist of reducing of knowledge capacity to fine especfiic focus

### LLMs (Large Language Models)

- **LLMs**:  
  Providers:  
  - OpenAI  
  - HuggingFace  
  - Ollama  
  - and more...

## Key Concepts:
- **Predict the next most likely token** (create content)
  
- **Implies a kind of cognition**:  
  - Reasonably react

El agent se crea desde el momento en que interactuas con el LLM, le das contenido y le indicas que haga un razonamiento y un tipo de cognición. (reasonably react)

### BUILD AGENTS
para eso usaremos Crew AI como plataforma Open Source.
Porq CREW  AI
 - descompone todos los conceptos en estructuras muy faciles.
 - Proporciona un patron para unir sistemas.
 - proporciona muchas herramientas.
 - Da herramientas para construir un modelo Agent


 ### L2: Create Agents to Research and write an Article
 
 - lab1.py

 Primero Aprendimos que los agentes rinden mejor cuando actuan como roles
 Second debes enfocarte en objetivos, expectativas cuando creas o asignas tareas a tus agentes, desbes asegurarte  de configurarlos de manera que sepan lo que estan haciendo y lo que se espera de ellos.
Tercero un agente puede realiuzar multiples tareas si asi lo deseas.
Los agentes deben ser granulares, vimos como enfocar cada agente en una tarea muy especifica.
Las taareas se pueden ejecutar de diferentes maneras, paralelo, secuencuial o jerarquica.


#### Hugging Face (HuggingFaceHub endpoint)

```Python
from langchain_community.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token="<HF_TOKEN_HERE>",
    task="text-generation",
)

### you will pass "llm" to your agent function
```

#### Mistral API

```Python
OPENAI_API_KEY=your-mistral-api-key
OPENAI_API_BASE=https://api.mistral.ai/v1
OPENAI_MODEL_NAME="mistral-small"
```

#### Cohere

```Python
from langchain_community.chat_models import ChatCohere
# Initialize language model
os.environ["COHERE_API_KEY"] = "your-cohere-api-key"
llm = ChatCohere()

### you will pass "llm" to your agent function
```