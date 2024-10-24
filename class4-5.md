# Revisamos la pagina de CrewAI
Role
Goal
Backstory
LLM usar varios LLM pcada agente con un diferente LLM, eso podría ser.
Tools Esto depende de las herramientas de cada LLM
Function Callingg LLM El modelo de lenguage usado por el agente.
Max iter Numero maximo maximo de iteraciones
Max RPM número maximo de iteraciones por minuto
Verbose Ver que esta sucediendo
Allow Delegation Agentes pueden delegar la tarea por otros agentes
Step Callback o retorno de llamada


## Task
Description Una tarea tiene una descripcion clara y concisa Aqui se puede agregar parametros de entrada o variables que podrían reconocer
Expected Output Salida esperada En la variable esperada se podría usar variables explicando el resultado que obtuvo
Tools Aqui enviamos herramientas para realizar esta tarea (probablemente no necesita herramientas)
Agent Indicamos que agente va a realizar esta tarea
Async Exceution Es realizar una tarea sin que el otro agente tenga finalizado su ejecución __ Aqui realizar un trabajo paralelo (pero evaluar bien si el proceso es secuencial o en paralelo)
Context 
Output_file El archivo donde quisiera que lo guarde y el formato => ./outlput/xxx.md
    Output JSON
    Output Pydantic

## Tools
utility las tools tiene una utilidad
integrations las tools mejora las capacidades del agente
customizability ofrece la flexibilidad

## Process
Sequential un proceso sequncial
Hierarchical siguiendo una estructura herarquica
Consensual (ellos indican que está en desarrollo)

## Crew
Un conjunto colaborativo de agents y tareas

Agents = [...],
Task = [...],
Process = Process.hierarchical, Un proceso herrarquico orpitimiza las cosas (El Manager) es quien orquesta a los agentes /  Aqui podrías agregar una herarquia de Crew, colocando    procesos        #Optional:tarea Sequencial es ejecutada por default

manager_LLM = groq_LLM,
cache=True
max_rpm = 29 La maxima cantidad de repeticiones por minuto, en caso de Groq es 30 es por eso que colocamos solo 29
verbose = 2 
...

crew.kickoff
inputs Son los parametros que enviamos ={...}