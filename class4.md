# Elementos clave de agent tools
hay que las herramientas sean geniales, trea cosas.
- Herramientas versatile (versatiles)
- Herramientas Fault-tolerant (Tolerante a fallos)
- Herramientas Caching (implementan almacenamiento en caché)

## Versatiles
Poder aceptar diferentes tipos de solicitudes (entradas difusas)
- Es versatil
    si diferencia de tipos de solicitudes
    tratar bien la entrada que llega al LLM
- Ser Tolerante a fallos
    a medida que pasa informacion a las herramientas
    si falla la herramienta, no se detiene el sistemapueden ocurrir errores
    en caso pueda quebrarse, puedan autorepararse
    y no detern la ejecucion
- Almacenamiento cache
    usar un cache inteligente
        almacenamiento cache entre agentes
            Si un agente intenta usar una herramienta con un conjunto de argumentos
            y otro agente intenta  usar otra herramienta con el mismo conjunto de argumentos
            incluso si son diferentes agentes van a usar una capa cachẽ
            Asi que si intentan usar una herramienta, no van a hacer esa llamada a la API. (Eso es una gran diferencia)

Existen muchos ejemplos de TOOLS
    - search intenet
    - scrape
    - connect to a database
    - call an API
    - Send notifications
        and many more
        