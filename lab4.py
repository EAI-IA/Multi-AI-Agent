# L4: Tools for a Customer Outreach Campaign

# In this lesson, you will learn more about Tools. You'll focus on three key elements of Tools:
# - Versatility
# - Fault Tolerance
# - Caching

# Warning Control
import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
import os
from intro.utils import get_openai_api_key, pretty_print_result
from intro.utils import get_serper_api_key
import config


server_api = config.SERPER_API_KEY
openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["SERPER_API_KEY"] = server_api ## Serper te permite hacer serach en google

## Crearemos un agente de ventas
sales_rep_agent = Agent(
    role="Sales Representative",
    goal="Identify high-value leads that match "
         "our ideal customer profile",
    backstory=(
        "As a part of the dynamic sales team at CrewAI, "
        "your mission is to scour "
        "the digital landscape for potential leads. "
        "Armed with cutting-edge tools "
        "and a strategic mindset, you analyze data, "
        "trends, and interactions to "
        "unearth opportunities that others might overlook. "
        "Your work is crucial in paving the way "
        "for meaningful engagements and driving the company's growth."
    ),
    allow_delegation=False,
    verbose=True
)

# En los objetivos usa la palabra clave ICP, Ideal Customer Profile
# tambien notaras que este agente no se le permite delegar ningũn trabajo ni hacer preguntas.
# y ese sera nuetro agente principal de ventas

lead_sales_rep_agent = Agent(
    role="Lead Sales Representative",
    goal="Nurture leads with personalized, compelling communications",
    backstory=(
        "Within the vibrant ecosystem of CrewAI's sales department, "
        "you stand out as the bridge between potential clients "
        "and the solutions they need."
        "By creating engaging, personalized messages, "
        "you not only inform leads about our offerings "
        "but also make them feel seen and heard."
        "Your role is pivotal in converting interest "
        "into action, guiding leads through the journey "
        "from curiosity to commitment."
    ),
    allow_delegation=False,
    verbose=True
)

# El objetivo del lider de ventas, es el contenido personalizado y contruir una comunicacion personalizada,
# con este cliente potencial.


from crewai_tools import DirectoryReadTool, \
                         FileReadTool, \
                         SerperDevTool

directory_read_tool = DirectoryReadTool(directory='./instructions')
file_read_tool = FileReadTool()
search_tool = SerperDevTool()

# Botamos un directorio local, para que pueda leer, solo este directorio local de instrucciones
# Aqui se colocaron una serie de instrucciones, como archivos markdown sobre como manejar empresas grandes y pequeñas.
# El ejemplo de instrucctions en MD es un buen ejemplo de lo que se desea

from crewai_tools import BaseTool

# Base tools, permite personalizar una herramienta, cada framwork te dá un patrón.

# Nuestra herramienta se llamará herramienta de analisis de sentimientos 
class SentimentAnalysisTool(BaseTool):
    name: str ="Sentiment Analysis Tool"
    description: str = ("Analyzes the sentiment of text "
         "to ensure positive and engaging communication.")


# y para implementar la herramienta lo que tienes que hacer es crear esta funcion. 
    def _run(self, text: str) -> str:
        # Your custom code tool goes here
        return "positive"
    

# Esta es un clase que hereda dentro de crewAI, que serã nuestra herramienta, que hereda de esa clase. 
# Esta clase un analisis de sentimiento, pero en realidad podrĩa ser una llamada de API externa o lo que deses.
 
#  La class de analisis de sentimiento retorna un positive, pero podrĩa retorna mas cosas.
# Ahora podemos pasarla a tus agentes y tareas
sentiment_analysis_tool = SentimentAnalysisTool()

# La primera tarea que vamos a crear, es la tarea de perfilado de leads
# para realizar un analizis de un lead sobre un sector, que tan grande es.

lead_profiling_task = Task(
    description=(
        "Conduct an in-depth analysis of {lead_name}, "
        "a company in the {industry} sector "
        "that recently showed interest in our solutions. "
        "Utilize all available data sources "
        "to compile a detailed profile, "
        "focusing on key decision-makers, recent business "
        "developments, and potential needs "
        "that align with our offerings. "
        "This task is crucial for tailoring "
        "our engagement strategy effectively.\n"
        "Don't make assumptions and "
        "only use information you absolutely sure about."
    ),
    expected_output=(
        "A comprehensive report on {lead_name}, "
        "including company background, "
        "key personnel, recent milestones, and identified needs. "
        "Highlight potential areas where "
        "our solutions can provide value, "
        "and suggest personalized engagement strategies."
    ),
    tools=[directory_read_tool, file_read_tool, search_tool],
    agent=sales_rep_agent,
)

personalized_outreach_task = Task(
    description=(
        "Using the insights gathered from "
        "the lead profiling report on {lead_name}, "
        "craft a personalized outreach campaign "
        "aimed at {key_decision_maker}, "
        "the {position} of {lead_name}. "
        "The campaign should address their recent {milestone} "
        "and how our solutions can support their goals. "
        "Your communication must resonate "
        "with {lead_name}'s company culture and values, "
        "demonstrating a deep understanding of "
        "their business and needs.\n"
        "Don't make assumptions and only "
        "use information you absolutely sure about."
    ),
    expected_output=(
        "A series of personalized email drafts "
        "tailored to {lead_name}, "
        "specifically targeting {key_decision_maker}."
        "Each draft should include "
        "a compelling narrative that connects our solutions "
        "with their recent achievements and future goals. "
        "Ensure the tone is engaging, professional, "
        "and aligned with {lead_name}'s corporate identity."
    ),
    tools=[sentiment_analysis_tool, search_tool],
    agent=lead_sales_rep_agent,
)

crew = Crew(
    agents=[sales_rep_agent, 
            lead_sales_rep_agent],
    
    tasks=[lead_profiling_task, 
           personalized_outreach_task],
	
    verbose=2,
	memory=True
)


inputs = {
    "lead_name": "DeepLearningAI",
    "industry": "Online Learning Platform",
    "key_decision_maker": "Andrew Ng",
    "position": "CEO",
    "milestone": "product launch"
}

result = crew.kickoff(inputs=inputs)

# Entonces el manejo de excepciones es importante, porque cuando explota una excepción detiene la ejecución de tu agente.
# Eso significa que las hora que se completaron hasta ahora se pierden.
# eso significa que debes de añadir una capa adicional
    # ya sea iniciar con el agente desde cero
    # o hacer algo con el error
# pero se podría encontrar otro framworks que elijan permitir excepciones.
# como quieras manejar las excepciones al usar herramientas es algo importante para los agentes.
