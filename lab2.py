# L3: Multi-agent Customer Support Automation
# In this lesson, you will learn about the six key elements which help make Agents perform even better:

# Role Playing
# Focus
# Tools
# Cooperation
# Guardrails
# Memory
# Maultiagent Customer Support Automation
import warnings # Para que las advertencias no interfieran
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
import os
from intro.utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

 #### Ya que vamos a construir un sistema multiagent, entonces primero construimos un sistemas Multiagent
support_agent = Agent(
    role="Senior Support Representative",
	goal="Be the most friendly and helpful "
        "support representative in your team",
	backstory=(
		"You work at crewAI (https://crewai.com) and "
        " are now working on providing "
		"support to {customer}, a super important customer "
        " for your company."
		"You need to make sure that you provide the best support!"
		"Make sure to provide full complete answers, "
        " and make no assumptions."
	),
	allow_delegation=False,
	verbose=True
)


# Colocamos un role de Senior, obj, super friendly and servicial, backstory, esta ayudando a un cliente especifico. 
# En backstory colocamos una interpolación para responder una pregunta específica.

# Vamos a tener otro agente de garantía de calidad  para verifiicar que este agente este haciendo bien.


support_quality_assurance_agent = Agent(
	role="Support Quality Assurance Specialist",
	goal="Get recognition for providing the "
    "best support quality assurance in your team",
	backstory=(
		"You work at crewAI (https://crewai.com) and "
        "are now working with your team "
		"on a request from {customer} ensuring that "
        "the support representative is "
		"providing the best support possible.\n"
		"You need to make sure that the support representative "
        "is providing full"
		"complete answers, and make no assumptions."
	),
	verbose=True
)

## Este agente de calidad de soporte, sirve para veridivar todo lo que dice.
# El agente puede delegar and trabajar de vuelta al agente de soporte original si decide hacerlo.
# La pregunta es saber que es razonable delegar trabajo a otro, o hacer preguntas a otro == esta es una diferencia entre la ingenieria regular, y la ingenieria regunlar.
# Entonces Allow_delegation?  confiamos en los LLMs en tomar decisiones correctas, los LLMs tienen un nivel de cognici{on porque entienden el lenguaje.

# Designe Pattenr:
# Quality Assurance:
    # Do task --> Agent
    # Review Task --> QA Agent
#  RECOMENDACION >> considerar un agent de QA de algũn tipo.



# ...................... Guardrails, tools and Memory .........................
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool

# Aqui herramientas simples de hacer busquedas de internet, y herramientas mas complejas RAG sobre GitHUb.
# Herramienta de Scraping, Search and desarrollo de servidor. 
# Desarrollo del servidor, servicio externo byscar en google.
# Scrapping, el agent hace scraper simple  acceder a una URL dada.
    # Con esto hacer RAG de un sitio web.
        # RAG: busqueda semantica sobre el contenido de este sitio.

# OTRAS HERRAMIENTAS QUE PODEMOS USAR.
# 1. Cargar datos de clientes que se conectan a conversaciones anteriores.
# 2. Cargar datos de un CRM
# 3. Load Customer data
# 4. Verificar si existen bugs
# 5. Solicitudes de tickes en curso.
# 6. other

 # Para usar una herramienta
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
## Por ejemplo si solo queremos que haga scrape en un solo site, hacemos los siguiente.
docs_scrape_tool = ScrapeWebsiteTool(
    te_url= "http://docs.crewai.com")


# Como damos a nuestros agentes esas herramientas?
# Dos formas:
    # - Asignar herramientas a nivel de agente
    # - Asignar herramientas a nivel de tarea
# Si el agente tiene la herramienta, el puede usarla para la tera que lo requiera.
# Si das la herramienta a nivel de tarea, el agente usarã la herramienta para esa tarea especĩfica.


# FIRST TASK : Tarea de resoluciõn de consultas.
# aqui agregamos más interpolación.
inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
	    "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
		"Make sure to use everything you know "
        "to provide the best support possible."
		"You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
    ),
    expected_output=(
	    "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
		"leaving no questions unanswered, and maintain a helpful and friendly "
		"tone throughout."
    ),
	tools=[docs_scrape_tool],
    agent=support_agent,
)




quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
		"high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
		"thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
		"ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
		"relevant feedback and improvements.\n"
		"Don't be too formal, we are a chill and cool company "
	    "but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent,
)

# Como vemos quality_assurance no tiene herramientas disponibles, lo que significa que el agente QA,
# Esto significa que estã evaluando puramente cuâç es la respuesta real que escribio el agente de soporte.


# Ahora creamos el systemas de multiagents.
crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    verbose=2,
    memory=True
)

# El sistema de multiagentes está configurado para utilizar dos agentes y dos tareas.
# Configuramos la entrada
inputs = {
    "customer": "DeepLearningAI",
    "person": "Andrew Ng",
    "inquiry": "I need help with setting up a Crew "
               "and kicking it off, specifically "
               "how can I add memory to my crew? "
               "Can you provide guidance?"
}
result = crew.kickoff(inputs=inputs)




## ME QUEDÊ INTERESADO EN SABER COMO PERSONALOZAR HERRAMIENTAS
