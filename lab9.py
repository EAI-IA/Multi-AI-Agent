# CREW INTERESTING

# ----------- Aplicaciõn especifica de CREW -------------

# Objetive, maximizar tus posibilidades de conseguir una entrevista.

# CUal es el proceso?
# - aprender requisitos del trabajo
# - Cruzar esos requisitos on tu conjunto especifico de habilidades y experinecias
# - Reformular tu CV para resaltar tus areas relevantes
# - reeescribit ese CV con lenguaje apropiado.


import warnings
warnings.filterwarnings("ignore")

from crewai import Agent, Task, Crew
import os
from intro.utils import get_openai_api_key, pretty_print_result

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["SERPER_API_KEY"] = get_openai_api_key()

from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool
)

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='./fake_resume.md')
semantic_search_resume = MDXSearchTool(mdx='./fake_resume.md')

# Website Tool, rastrea sitios web
# Busqueda MDX
# Serper dev.

# FileReadTool >> Es una herramienta de lectura de archivos
# MDXSerachTool >> Es la herramienta de busqueda MDX
        # Esto permito usar RAG sobre nuestro currĩculum falso.
        # Hacemos busquedas semanticas


# read_resume = FileReadTool(file_path='./fake_resume.md')
    # Es un fake errado
    # El CV no resalta lo suficiente, debido a q no hace enfasis en sus logros.


# Agent 1: Researcher
researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job posting to help job applicants",
    tools = [scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in "
        "navigating and extracting critical "
        "information from job postings is unmatched."
        "Your skills help pinpoint the necessary "
        "qualifications and skills sought "
        "by employers, forming the foundation for "
        "effective application tailoring."
    )
)

# Agente investigador, >> OBJ. Asegurar de realizar un analisis de oferta.

# Agent 2: Profiler
profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Do increditble research on job applicants "
         "to help them stand out in the job market",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Equipped with analytical prowess, you dissect "
        "and synthesize information "
        "from diverse sources to craft comprehensive "
        "personal and professional profiles, laying the "
        "groundwork for personalized resume enhancements."
    )
)

# Perfilador >> Obj. investiga a los solicitantes de empleo, y entiende las coincidencias.

# Agent 3: Resume Strategist
resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a "
         "resume stand out in the job market.",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you "
        "excel at refining resumes to highlight the most "
        "relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    )
)

# Agente de Estrategia >> Obj. Encargado de actualizar realmente le CV, va a conocer las ofertas de trabajo aprender sobre las habilidades de la persona.

# IMPORTANTE >>>> Los tres agents tienen acceso a varias herramientas de desarrollo.

# Agent 4: Interview Preparer
interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points "
         "based on the resume and job requirements",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of "
        "interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, "
        "ensuring they can confidently address all aspects of the "
        "job they are applying for."
    )
)
# El ultimo agente es importante, por que es el preparador de entrevistas de ingenieria. 
    # Este elabora preguntas y respuestas y puntos de discusion a abordar.

# Aplicamos la Interpolación que aprendimos anteriormente.
# Task for Researcher Agent: Extract Job Requirements
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher,
    async_execution=True
)

# >> AQUI ESPERA UNA URL de la oferta de trabajo.

# Task for Profiler Agent: Compile Comprehensive Profile
profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub ({github_url}) URLs, and personal write-up "
        "({personal_writeup}). Utilize tools to extract and "
        "synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=profiler,
    async_execution=True
)
# >> Es responsable de cruzar informacion sobre tĩ.
# Hay otras variables que estas interpolando.
    # Inlcuso una nota personal 
    # Inlcuyendo las cosas que estuviste haiendo como profesional

# Task for Resume Strategist Agent: Align Resume with Job Requirements
resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "inlcuding the initial summary, work experience, skills, "
        "and education. All to better reflrect the candidates "
        "abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist
)
# Esta tarea serã responsable actualizar el CV, este entregarã un CV personalizado. " output_file="tailored_resume.md","

# Task for Interview Preparer Agent: Develop Interview Materials
interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these question and talking points to "
        "help the candiadte highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)

# La tarea encarga de creaar los temas de conversación.

job_application_crew = Crew(
    agents=[researcher,
            profiler,
            resume_strategist,
            interview_preparer],

    tasks=[research_task,
           profile_task,
           resume_strategy_task,
           interview_preparation_task],

    verbose=True
)

# Despues de crear los agentes y tareas, es importante cubirir todos los inpputs y  todas las interpolaciones que esperábamos.

job_application_inputs = {
    'job_posting_url': 'https://jobs.lever.co/AIFund/6c82e23e-d954-4dd8-a734-c0c2c5ee00f1?lever-origin=applied&lever-source%5B%5D=AI+Fund',
    'github_url': 'https://github.com/joaomdmoura',
    'personal_writeup': """Noah is an accomplished Software
    Engineering Leader with 18 years of experience, specializing in
    managing remote and in-office teams, and expert in multiple
    programming languages and frameworks. He holds an MBA and a strong
    background in AI and data science. Noah has successfully led
    major tech initiatives and startups, proving his ability to drive
    innovation and growth in the tech industry. Ideal for leadership
    roles that require a strategic and innovative approach."""
}

### this execution will take a few minutes to run
result = job_application_crew.kickoff(inputs=job_application_inputs)

########################################################################################################################################

# RECAPS ___ Usar Crew es práctico

# from IPython.display import Markdown, display
# display(Markdown("./tailored_resume.md"))

# display(Markdown("./interview_materials.md"))