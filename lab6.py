import warnings
warnings.filterwarnings("ignore")

from crewai import Agent, Task, Crew
import os
from intro.utils import get_openai_api_key, pretty_print_result

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["SERPER_API_KEY"] = get_openai_api_key()

from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# Initialize the tools
search_tool = SerperDevTool() ## Hacer busquedas de Google
scrape_tool = ScrapeWebsiteTool() # entrar a sitios web y obtener su contenido

# Agent 1: Venue Coordinator
venue_coordinator = Agent(
    role="Venue Coordinator",
    goal="Identify and book an appropriate venue "
    "based on event requirements",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "With a keen sense of space and "
        "understanding of event logistics, "
        "you excel at finding and securing "
        "the perfect venue that fits the event's theme, "
        "size, and budget constraints."
    )
)
# Coordinardor de eventos
# Que puede organizar eventos
#Objetivo > Identificar y reservar un lugar apropiado
# Entonces va a buscar en internet y encontrar esos lugares para nosotros


 # Agent 2: Logistics Manager
logistics_manager = Agent(
    role='Logistics Manager',
    goal=(
        "Manage all logistics for the event "
        "including catering and equipmen"
    ),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Organized and detail-oriented, "
        "you ensure that every logistical aspect of the event "
        "from catering to equipment setup "
        "is flawlessly executed to create a seamless experience."
    )
)
# Este es un Agente de Logistica del evento.

# Agent 3: Marketing and Communications Agent
marketing_communications_agent = Agent(
    role="Marketing and Communications Agent",
    goal="Effectively market the event and "
         "communicate with participants",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Creative and communicative, "
        "you craft compelling messages and "
        "engage with potential attendees "
        "to maximize event exposure and participation."
    )
)

# El tercer agente es un agente de Marketing
# este agente va a pensar como podemos comercializar este evento
# Como podemos conseguir la mayor cantidad de gente Asistiendo hoy?

from pydantic import BaseModel
# Define a Pydantic model for venue details 
# (demonstrating Output as Pydantic)
class VenueDetails(BaseModel):
    name: str
    address: str
    capacity: int
    booking_status: str

# Ahora esto es nuevo, creamos un objeto pydantic 
# "Esta es una nueva caracteristica"
# Importamos el Base Model y creamos la clase Venue Details que hereda Base Model y los lugares van a tener 4 atributos: nombre, direcccion, capacidad y estado de reserva.
# La razon de crear esto es para que los agentes puedan trabajar con esta clase, llenar este modelo y crear instancias de este mientras trabajan.
# Este es un gran ejemplo de como usar salidas imprecisas a salidas fuertemente tipadas.

# Pydantic es una herramienta para crear modelos y trabajar con variables fuertemente tipadas de manera facil

venue_task = Task(
    description="Find a venue in {event_city} "
                "that meets criteria for {event_topic}.",
    expected_output="All the details of a specifically chosen"
                    "venue you found to accommodate the event.",
    human_input=True,
    output_json=VenueDetails,
    output_file="venue_details.json",  
      # Outputs the venue details as a JSON file
    agent=venue_coordinator
)

# Primera tarea encontrar un lugar para nuestro evento
#  Espera como entrada una ciudad del evento y un tema del evento
# Observa la salida "output_json" >> estamos enviando un Json a la herrramienta VenueDetails.

logistics_task = Task(
    description="Coordinate catering and "
                 "equipment for an event "
                 "with {expected_participants} participants "
                 "on {tentative_date}.",
    expected_output="Confirmation of all logistics arrangements "
                    "including catering and equipment setup.",
    human_input=True,
    async_execution=True,
    agent=logistics_manager
)

# Esta es una tarea Logistica, es la responsable de coordinar el Catering y el evento.
# en esta tarea se están esperando dos inputs.
# Cual es la fecha y la cantidad de paarticipantes.
# Asi que estamos usando el input humano
#     async_execution=True, con input humano la tarea se detendra y no se completará hasta que haya input humano, y al ser una ejecución asyncrona
# esta se ejecutara en paralelo despuesde una tarea anterior, pero depende del resultado de la tarea de Venue_task por que la ubicacion va a influir

marketing_task = Task(
    description="Promote the {event_topic} "
                "aiming to engage at least"
                "{expected_participants} potential attendees.",
    expected_output="Report on marketing activities "
                    "and attendee engagement formatted as markdown.",
    async_execution=True,
    output_file="marketing_report.md",  # Outputs the report as a text file
    agent=marketing_communications_agent
)

# La tarea final es la tarea de Marketing, que ayuda a promover este evento.
# ENTONCES DEBEMOS ENTENDER EL FLUJO DE FUNCINOAMIENTO
# La primera tarea que es Find_venue (se ejecuta por si sola)
# Luego las tareas de Logistics y MMarketing se ejecutan en paralelo 
#       Por que la tarea de LOGISTIC NO NECESITA de la otra
# Como tal Marketing se está extrayendo un archivo markdown file


# Define the crew with agents and tasks
event_management_crew = Crew(
    agents=[venue_coordinator, 
            logistics_manager, 
            marketing_communications_agent],
    
    tasks=[venue_task, 
           logistics_task, 
           marketing_task],
    
    verbose=True
)


event_details = {
    'event_topic': "Tech Innovation Conference",
    'event_description': "A gathering of tech innovators "
                         "and industry leaders "
                         "to explore future technologies.",
    'event_city': "San Francisco",
    'tentative_date': "2024-09-15",
    'expected_participants': 500,
    'budget': 20000,
    'venue_type': "Conference Hall"
}


