# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew

import os
from utils import get_openai_api_key
from IPython.display import Markdown

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

## Build AGENT Planificador
# 3 parametros el rol que debe coincidir con lo que queremos que haga
planner = Agent(
    role="Planificador de contenido", #que va a hacer
    goal="Mejorar el plan y facticamente preciso en un tema {topic}", #el objetivo claro de lo que tiene que hacer
    backstory ="Tu estas trabajando en planificar un articulo de blog"
                "acerda del topico: {topic}."
                "Tu coleccionas informacion que ayuda a la audiencia aprender algunas cosas"
                "y toma decisiones. "
                "Tu trabajo es basicamente escribir contenido para un articulo on este topico.",
    allow_delegation = False, ## Otras actividades más que tambien puede hacer
    verbose = True  
    )       

## Build AGENT Escritor
# 3 parametros el rol que debe coincidir con lo que queremos que haga
writer = Agent(
    role="Escritor de contenido",
    goal="Escribir un artículo de opinión perspicaz y factualmente preciso "
         "sobre el tema: {topic}",
    backstory="Tu estás trabajando en la redacción "
                "de un nuevo artículo de opinión sobre el tema: {topic}. "
                "Basas tu escritura en el trabajo del "
                "Planificador de Contenidos, quien proporciona un esquema "
                "y contexto relevante sobre el tema. "
                "Sigues los objetivos principales y "
                "la dirección del esquema, "
                "según lo proporcionado por el Planificador de Contenidos. "
                "También ofreces perspectivas objetivas e imparciales "
                "y las respaldas con información "
                "proporcionada por el Planificador de Contenidos. "
                "Reconoces en tu artículo de opinión "
                "cuándo tus afirmaciones son opiniones "
                "en contraposición a afirmaciones objetivas.",
    allow_delegation = False,
    verbose = True
)
## Build AGENT editor
# 3 parametros el rol que debe coincidir con lo que queremos que haga
editor = Agent(
    role = "Editor de contenido",
    goal ="Editar una publicación de blog dada para alinearla con "
         "el estilo de escritura de la organización.",
    backstory="Eres un editor que recibe una publicación de blog "
                  "del Escritor de Contenidos. "
                  "Tu objetivo es revisar la publicación de blog "
                  "para asegurarte de que siga las mejores prácticas periodísticas, "
                  "proporcione puntos de vista equilibrados "
                  "cuando presente opiniones o afirmaciones, "
                  "y también evite temas o opiniones controvertidos "
                  "cuando sea posible.",
    allow_delegation=False,
    verbose=True
)


## Todo esto interpolación en cuanto a una sola variable {topic}.

## Ahora la Task esta esperando 3 atributos, La descripcion, la salida esperada y el agente.

plan = Task(
    description=(
        "1. Priorizar las últimas tendencias, actores clave, "
            "y noticias destacadas sobre {topic}."
        "2. Identificar la audiencia objetivo, considerando "
            "sus intereses y puntos de dolor."
        "3. Desarrollar un esquema de contenido detallado que incluya "
            "una introducción, puntos clave y un llamado a la acción."
        "4. Incluir palabras clave para SEO y datos o fuentes relevantes."
    ),
    expected_output="Un documento de plan de contenido integral "
        "con un esquema, análisis de audiencia, "
        "palabras clave para SEO y recursos.",
    agent=planner,
)


write = Task(
    description=(
        "1. Utilizar el plan de contenido para redactar una publicación de blog convincente "
            "sobre {topic}.\n"
        "2. Incorporar palabras clave para SEO de manera natural.\n"
        "3. Las secciones/subtítulos están correctamente nombrados "
            "de manera atractiva.\n"
        "4. Asegurarse de que la publicación esté estructurada con una "
            "introducción atractiva, un cuerpo perspicaz, "
            "y una conclusión que resuma.\n"
        "5. Revisar en busca de errores gramaticales y "
            "alineación con la voz de la marca.\n"
    ),
    expected_output="Una publicación de blog bien escrita "
        "en formato markdown, lista para su publicación, "
        "cada sección debe tener 2 o 3 párrafos.",
    agent=writer,
)

edit = Task(
    description=("Revisar la publicación de blog dada en busca de "
                 "errores gramaticales y "
                 "alineación con la voz de la marca."),
    expected_output="Una publicación de blog bien escrita en formato markdown, "
                       "lista para su publicación, "
                       "cada sección debe tener 2 o 3 párrafos.",
    agent=editor
)

## Ahora el que orquesta todos los agentes será CrewAI
## DESTACAR que por defecto Creq opera secuencialmente, lo que significa que una tarea se ejecutará despues de la sigueinte
## - Entonces el orden de las tareas es importante, dado que la salida de uno será coomo parte de la entrada siguiente.
## más adelante aprenderemos a modificar eso.
## si las tareas quieres que se ejecuten en paraleleo.
## Verbose indica la clarida de la salida del programa, el nodo verbose con 1, 2
## verás todos los logs posible o solo un subconjunto de ellos.

crew = Crew(
    agents = [planner, writer, editor],
    tasks = [plan, write, edit],
    verbose=2
)

## Para ejecutar usamos el metodo kickoff de Crew para nuestro System Multiagente .
## Luego pasamos un dict al metodo de entrada

result = crew.kickoff(inputs={"topic": "Artificial Inteligence"})

Markdown(result)





# __________________________________________________________ RESPONSE __________________________________________________________

# (PENDING) ealchat@ealchat:~/Multi_AI_Agent/intro$ python lab1.py 
#  [DEBUG]: == Working Agent: Planificador de contenido
#  [INFO]: == Starting Task: 1. Priorizar las últimas tendencias, actores clave, y noticias destacadas sobre Artificial Inteligence.2. Identificar la audiencia objetivo, considerando sus intereses y puntos de dolor.3. Desarrollar un esquema de contenido detallado que incluya una introducción, puntos clave y un llamado a la acción.4. Incluir palabras clave para SEO y datos o fuentes relevantes.


# > Entering new CrewAgentExecutor chain...
# I now can give a great answer

# Final Answer: 

# **Plan de Contenido: Artificial Intelligence**

# **Introducción:**
# La inteligencia artificial (IA) es una de las tecnologías más revolucionarias de la actualidad, con un impacto significativo en diversos sectores. En este artículo, exploraremos las últimas tendencias, actores clave y noticias destacadas sobre IA, centrándonos en su relevancia para la audiencia interesada en tecnología y negocios.

# **Puntos Clave:**
# 1. **Tendencias en IA:** Analizaremos las tendencias más recientes en IA, como el aprendizaje automático, el procesamiento del lenguaje natural y la visión por computadora. También destacaremos avances en áreas como la robótica y la automatización.
# 2. **Actores Clave:** Identificaremos a las empresas líderes en el campo de la IA, como Google, Amazon, Microsoft y Tesla, y analizaremos sus proyectos e innovaciones más recientes.
# 3. **Noticias Destacadas:** Comentaremos noticias relevantes en el ámbito de la IA, como lanzamientos de productos, alianzas estratégicas y avances científicos.

# **Audiencia Objetivo:**
# Nuestra audiencia objetivo son profesionales del sector tecnológico y empresarial interesados en estar al tanto de las últimas novedades en inteligencia artificial. También nos dirigimos a estudiantes y entusiastas de la tecnología que desean aprender más sobre este tema fascinante.

# **Esquema de Contenido:**
# 1. Introducción a la IA y su importancia en la actualidad.
# 2. Tendencias destacadas en IA: machine learning, NLP, visión por computadora.
# 3. Actores clave en el campo de la IA y sus proyectos más recientes.
# 4. Noticias destacadas en el mundo de la IA: lanzamientos, alianzas y avances científicos.
# 5. Conclusión y llamado a la acción para seguir aprendiendo sobre IA.

# **Palabras Clave para SEO:**
# - Inteligencia Artificial
# - Tendencias en IA
# - Actores clave en IA
# - Noticias de IA
# - Tecnología y negocios

# **Recursos:**
# - Informes de investigación de empresas líderes en IA.
# - Artículos de noticias sobre avances en inteligencia artificial.
# - Publicaciones en blogs de expertos en tecnología.
# - Libros y cursos online sobre IA.

# Con este plan de contenido integral, esperamos ofrecer a nuestra audiencia una visión completa y actualizada sobre el apasionante mundo de la inteligencia artificial. ¡No te pierdas las últimas tendencias y noticias en IA!

# > Finished chain.
#  [DEBUG]: == [Planificador de contenido] Task output: **Plan de Contenido: Artificial Intelligence**

# **Introducción:**
# La inteligencia artificial (IA) es una de las tecnologías más revolucionarias de la actualidad, con un impacto significativo en diversos sectores. En este artículo, exploraremos las últimas tendencias, actores clave y noticias destacadas sobre IA, centrándonos en su relevancia para la audiencia interesada en tecnología y negocios.

# **Puntos Clave:**
# 1. **Tendencias en IA:** Analizaremos las tendencias más recientes en IA, como el aprendizaje automático, el procesamiento del lenguaje natural y la visión por computadora. También destacaremos avances en áreas como la robótica y la automatización.
# 2. **Actores Clave:** Identificaremos a las empresas líderes en el campo de la IA, como Google, Amazon, Microsoft y Tesla, y analizaremos sus proyectos e innovaciones más recientes.
# 3. **Noticias Destacadas:** Comentaremos noticias relevantes en el ámbito de la IA, como lanzamientos de productos, alianzas estratégicas y avances científicos.

# **Audiencia Objetivo:**
# Nuestra audiencia objetivo son profesionales del sector tecnológico y empresarial interesados en estar al tanto de las últimas novedades en inteligencia artificial. También nos dirigimos a estudiantes y entusiastas de la tecnología que desean aprender más sobre este tema fascinante.

# **Esquema de Contenido:**
# 1. Introducción a la IA y su importancia en la actualidad.
# 2. Tendencias destacadas en IA: machine learning, NLP, visión por computadora.
# 3. Actores clave en el campo de la IA y sus proyectos más recientes.
# 4. Noticias destacadas en el mundo de la IA: lanzamientos, alianzas y avances científicos.
# 5. Conclusión y llamado a la acción para seguir aprendiendo sobre IA.

# **Palabras Clave para SEO:**
# - Inteligencia Artificial
# - Tendencias en IA
# - Actores clave en IA
# - Noticias de IA
# - Tecnología y negocios

# **Recursos:**
# - Informes de investigación de empresas líderes en IA.
# - Artículos de noticias sobre avances en inteligencia artificial.
# - Publicaciones en blogs de expertos en tecnología.
# - Libros y cursos online sobre IA.

# Con este plan de contenido integral, esperamos ofrecer a nuestra audiencia una visión completa y actualizada sobre el apasionante mundo de la inteligencia artificial. ¡No te pierdas las últimas tendencias y noticias en IA!


#  [DEBUG]: == Working Agent: Escritor de contenido
#  [INFO]: == Starting Task: 1. Utilizar el plan de contenido para redactar una publicación de blog convincente sobre Artificial Inteligence.
# 2. Incorporar palabras clave para SEO de manera natural.
# 3. Las secciones/subtítulos están correctamente nombrados de manera atractiva.
# 4. Asegurarse de que la publicación esté estructurada con una introducción atractiva, un cuerpo perspicaz, y una conclusión que resuma.
# 5. Revisar en busca de errores gramaticales y alineación con la voz de la marca.



# > Entering new CrewAgentExecutor chain...
# I now can give a great answer

# Final Answer:

# # El Impacto de la Inteligencia Artificial en la Actualidad

# La inteligencia artificial (IA) ha revolucionado la forma en que interactuamos con la tecnología en la actualidad. Con un impacto significativo en diversos sectores, la IA ha demostrado ser una herramienta poderosa para la innovación y el desarrollo. En este artículo, exploraremos las últimas tendencias, actores clave y noticias relevantes sobre IA, centrándonos en su importancia para profesionales del sector tecnológico y empresarial, así como para entusiastas de la tecnología.

# ## Tendencias Destacadas en IA

# En el campo de la inteligencia artificial, las tendencias más recientes incluyen avances en el aprendizaje automático, el procesamiento del lenguaje natural y la visión por computadora. Estas tecnologías han permitido la creación de sistemas inteligentes capaces de analizar grandes cantidades de datos, interpretar información y tomar decisiones de manera autónoma. Además, la robótica y la automatización han experimentado un crecimiento significativo gracias a la IA, transformando la forma en que trabajamos y vivimos.

# ## Actores Clave en el Campo de la IA

# Empresas líderes como Google, Amazon, Microsoft y Tesla han desempeñado un papel fundamental en el avance de la inteligencia artificial. A través de proyectos e innovaciones revolucionarias, estas compañías han impulsado el desarrollo de tecnologías disruptivas que han cambiado la forma en que percibimos la IA. Desde asistentes virtuales hasta vehículos autónomos, los productos y servicios basados en IA continúan sorprendiendo a la audiencia con su nivel de sofisticación y utilidad.

# ## Noticias Destacadas en el Mundo de la IA

# En el ámbito de la IA, las noticias relevantes abarcan desde lanzamientos de productos innovadores hasta alianzas estratégicas entre empresas líderes. Además, los avances científicos en el campo de la inteligencia artificial han generado un interés creciente en la comunidad tecnológica y empresarial. Estas noticias reflejan el dinamismo y la constante evolución de la IA, mostrando cómo esta tecnología continúa transformando el mundo que nos rodea.

# En conclusión, la inteligencia artificial se ha convertido en un pilar fundamental en la sociedad actual, con un impacto profundo en áreas como la tecnología y los negocios. A medida que continuamos explorando las posibilidades de la IA, es crucial mantenerse informado sobre las últimas tendencias y noticias en este campo apasionante. ¡No te pierdas la oportunidad de aprender más sobre la inteligencia artificial y su impacto en el mundo actual!

# > Finished chain.
#  [DEBUG]: == [Escritor de contenido] Task output: # El Impacto de la Inteligencia Artificial en la Actualidad

# La inteligencia artificial (IA) ha revolucionado la forma en que interactuamos con la tecnología en la actualidad. Con un impacto significativo en diversos sectores, la IA ha demostrado ser una herramienta poderosa para la innovación y el desarrollo. En este artículo, exploraremos las últimas tendencias, actores clave y noticias relevantes sobre IA, centrándonos en su importancia para profesionales del sector tecnológico y empresarial, así como para entusiastas de la tecnología.

# ## Tendencias Destacadas en IA

# En el campo de la inteligencia artificial, las tendencias más recientes incluyen avances en el aprendizaje automático, el procesamiento del lenguaje natural y la visión por computadora. Estas tecnologías han permitido la creación de sistemas inteligentes capaces de analizar grandes cantidades de datos, interpretar información y tomar decisiones de manera autónoma. Además, la robótica y la automatización han experimentado un crecimiento significativo gracias a la IA, transformando la forma en que trabajamos y vivimos.

# ## Actores Clave en el Campo de la IA

# Empresas líderes como Google, Amazon, Microsoft y Tesla han desempeñado un papel fundamental en el avance de la inteligencia artificial. A través de proyectos e innovaciones revolucionarias, estas compañías han impulsado el desarrollo de tecnologías disruptivas que han cambiado la forma en que percibimos la IA. Desde asistentes virtuales hasta vehículos autónomos, los productos y servicios basados en IA continúan sorprendiendo a la audiencia con su nivel de sofisticación y utilidad.

# ## Noticias Destacadas en el Mundo de la IA

# En el ámbito de la IA, las noticias relevantes abarcan desde lanzamientos de productos innovadores hasta alianzas estratégicas entre empresas líderes. Además, los avances científicos en el campo de la inteligencia artificial han generado un interés creciente en la comunidad tecnológica y empresarial. Estas noticias reflejan el dinamismo y la constante evolución de la IA, mostrando cómo esta tecnología continúa transformando el mundo que nos rodea.

# En conclusión, la inteligencia artificial se ha convertido en un pilar fundamental en la sociedad actual, con un impacto profundo en áreas como la tecnología y los negocios. A medida que continuamos explorando las posibilidades de la IA, es crucial mantenerse informado sobre las últimas tendencias y noticias en este campo apasionante. ¡No te pierdas la oportunidad de aprender más sobre la inteligencia artificial y su impacto en el mundo actual!


#  [DEBUG]: == Working Agent: Editor de contenido
#  [INFO]: == Starting Task: Revisar la publicación de blog dada en busca de errores gramaticales y alineación con la voz de la marca.


# > Entering new CrewAgentExecutor chain...
# I now can give a great answer

# Final Answer:
# # El Impacto de la Inteligencia Artificial en la Actualidad

# La inteligencia artificial (IA) ha revolucionado la forma en que interactuamos con la tecnología en la actualidad. Con un impacto significativo en diversos sectores, la IA ha demostrado ser una herramienta poderosa para la innovación y el desarrollo. En este artículo, exploraremos las últimas tendencias, actores clave y noticias relevantes sobre IA, centrándonos en su importancia para profesionales del sector tecnológico y empresarial, así como para entusiastas de la tecnología.

# ## Tendencias Destacadas en IA

# En el campo de la inteligencia artificial, las tendencias más recientes incluyen avances en el aprendizaje automático, el procesamiento del lenguaje natural y la visión por computadora. Estas tecnologías han permitido la creación de sistemas inteligentes capaces de analizar grandes cantidades de datos, interpretar información y tomar decisiones de manera autónoma. Además, la robótica y la automatización han experimentado un crecimiento significativo gracias a la IA, transformando la forma en que trabajamos y vivimos.

# ## Actores Clave en el Campo de la IA

# Empresas líderes como Google, Amazon, Microsoft y Tesla han desempeñado un papel fundamental en el avance de la inteligencia artificial. A través de proyectos e innovaciones revolucionarias, estas compañías han impulsado el desarrollo de tecnologías disruptivas que han cambiado la forma en que percibimos la IA. Desde asistentes virtuales hasta vehículos autónomos, los productos y servicios basados en IA continúan sorprendiendo a la audiencia con su nivel de sofisticación y utilidad.

# ## Noticias Destacadas en el Mundo de la IA

# En el ámbito de la IA, las noticias relevantes abarcan desde lanzamientos de productos innovadores hasta alianzas estratégicas entre empresas líderes. Además, los avances científicos en el campo de la inteligencia artificial han generado un interés creciente en la comunidad tecnológica y empresarial. Estas noticias reflejan el dinamismo y la constante evolución de la IA, mostrando cómo esta tecnología continúa transformando el mundo que nos rodea.

# En conclusión, la inteligencia artificial se ha convertido en un pilar fundamental en la sociedad actual, con un impacto profundo en áreas como la tecnología y los negocios. A medida que continuamos explorando las posibilidades de la IA, es crucial mantenerse informado sobre las últimas tendencias y noticias en este campo apasionante. ¡No te pierdas la oportunidad de aprender más sobre la inteligencia artificial y su impacto en el mundo actual!

# > Finished chain.
#  [DEBUG]: == [Editor de contenido] Task output: # El Impacto de la Inteligencia Artificial en la Actualidad

# La inteligencia artificial (IA) ha revolucionado la forma en que interactuamos con la tecnología en la actualidad. Con un impacto significativo en diversos sectores, la IA ha demostrado ser una herramienta poderosa para la innovación y el desarrollo. En este artículo, exploraremos las últimas tendencias, actores clave y noticias relevantes sobre IA, centrándonos en su importancia para profesionales del sector tecnológico y empresarial, así como para entusiastas de la tecnología.

# ## Tendencias Destacadas en IA

# En el campo de la inteligencia artificial, las tendencias más recientes incluyen avances en el aprendizaje automático, el procesamiento del lenguaje natural y la visión por computadora. Estas tecnologías han permitido la creación de sistemas inteligentes capaces de analizar grandes cantidades de datos, interpretar información y tomar decisiones de manera autónoma. Además, la robótica y la automatización han experimentado un crecimiento significativo gracias a la IA, transformando la forma en que trabajamos y vivimos.

# ## Actores Clave en el Campo de la IA

# Empresas líderes como Google, Amazon, Microsoft y Tesla han desempeñado un papel fundamental en el avance de la inteligencia artificial. A través de proyectos e innovaciones revolucionarias, estas compañías han impulsado el desarrollo de tecnologías disruptivas que han cambiado la forma en que percibimos la IA. Desde asistentes virtuales hasta vehículos autónomos, los productos y servicios basados en IA continúan sorprendiendo a la audiencia con su nivel de sofisticación y utilidad.

# ## Noticias Destacadas en el Mundo de la IA

# En el ámbito de la IA, las noticias relevantes abarcan desde lanzamientos de productos innovadores hasta alianzas estratégicas entre empresas líderes. Además, los avances científicos en el campo de la inteligencia artificial han generado un interés creciente en la comunidad tecnológica y empresarial. Estas noticias reflejan el dinamismo y la constante evolución de la IA, mostrando cómo esta tecnología continúa transformando el mundo que nos rodea.

# En conclusión, la inteligencia artificial se ha convertido en un pilar fundamental en la sociedad actual, con un impacto profundo en áreas como la tecnología y los negocios. A medida que continuamos explorando las posibilidades de la IA, es crucial mantenerse informado sobre las últimas tendencias y noticias en este campo apasionante. ¡No te pierdas la oportunidad de aprender más sobre la inteligencia artificial y su impacto en el mundo actual!

# ---------------------------------------------------------------------------------- FINISH ----------------------------------------------------------------------------------

