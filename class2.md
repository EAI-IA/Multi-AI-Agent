# Key elements of Ai Agents in Multiagents

- Role Playing (Rol que desempeñan)
- Focus (Enfoque)
- Tools (Herramientas)
- Cooperation (Coperación)
- Guardrails (Barandas de Protección)
- Memory (Memor ia)


## Role Playing
Es modificar el tipo de respuesta que te va a entrgar el agente.
Indicar el rol que va a tomar el agente es muy importante, ya que toma la posición de hablar con experiencia. 
Entonces existen 3 puntos importantes a considerar con esto:
- Roles (Roles)
- Goals (Objetivos)
- Backstory (Historia)


## Focus
Es el enfoque que va a tener el agente, aprovachamos las grandes ventanas de contexto pero demasiada informacion de reetorno da opcion a alucionaciones.
Lo mejor es proponer multiples agentes a corregir patrones de correción.

## Tools
Existen muchas herramientas, pero el enfoque debe ser solo proporcionar las herramientas clave que van a necesitar los agents. 

## Cooperate
Este es un foco importante, donde trabaja sobre cambiar ideas entre ellos. Consideran muy importante: 
- Take feedback
- Delegate Tasks

## Guardrails
Sobre todo en las aplicaciones de IA, aplicando (Entradas difusas, transformaciones difusas y salidas difusas) Significa que no obtinen resultados fuertemente tipiados.
evitar atascos, o que se quede conversando repetivimante o usen las mismas herramientas.

implementamos carrilles para no desbarrancar los objetivos, y la mayoria de estos estan implementados a nivel de framework.
Esto te asegura a construir herramientas personalizadas, e prevenir alucionaciones y obtener resultados confiables y consistentes.

## Memory
Capacidad de recordar lo que hicieron en el pasado.
Se tiene tres tipos de memory:
- Long-term memory
- Short-term memory
- Entity memory

### Short-term Memory
Es la memoria que se borra, solo se inicializa en la ejecucióon de Crew.
Es util por que a medida que los diferentes agentes intentan lograr diferentes tareas, almacenan diferentes cosas.
Esta memory se comparte entre todos los agentes
Esto ayuda a compartir CONTEXTO

### Long-term Memory
La memoria de largo permanece aun despues que el equipo termine.
Esta se almacena en una base de datos localmente, y eso permite que tus agentes aprendan de ejecuciones anteriores.
Cada vez que al agente completa una tarea se autoevalúa para aprender que debe hacer mejor,  y almacena esa información para que pueda volver a acceder a eso cuando se ejecute una vez más, y usar ese conocimiento.

### Entity Memory
La memoria de entidad, es de corta duración, así que solo se necesita durante la ejecución. Almaceno quienes son los sujetos y que estan discutiendo, Entonces en caso estan analizando una empresa pueden almacenas la empresa como un sujeto en esta base de datos.