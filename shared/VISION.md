# VISION.md
<!-- v3.3 | última edición: 2026-06-11 -->

## Notas e Inspiración
Este framework es un desarrollo original de **Taotomate**, fuertemente inspirado a nivel conceptual, arquitectónico (SDD) y de herencia de identidad en el ecosistema "Gentleman AI" de Alan Buscaglia. Se reconoce y agradece su valioso aporte open source, el cual sentó bases metodológicas que luego fueron adaptadas y evolucionadas para las necesidades de este repositorio.

---

## Por qué y para qué existe este sistema

La inteligencia sin accesibilidad no tiene utilidad real.

Un sistema que cuesta mucho para ejecutarse poco no escala, no ayuda
y no tiene sentido construir. La potencia no es el objetivo —
la economía de medios sí.

Este framework existe para resolver cualquier problema digitalizable,
desde lo abstracto (lógica, datos, decisiones) hasta lo físico
(máquinas, protocolos, implementaciones). No es un sistema de nicho
— es de propósito general, diseñado para que el costo de ejecución
sea siempre proporcional al problema que resuelve.

---

## La meta-observación

Estudiando la historia industrial aparece un patrón que se repite:

1. Alguien descubre un método más eficiente
2. El método se estandariza y sostiene
3. El beneficio de la eficiencia no va al que la generó sino al que
   controla el proceso

Esto no es solo historia — es un conflicto de intereses estructural
que se reproduce en los sistemas de IA actuales.

El modelo de cobro por token es el ejemplo más claro: un agente que
resuelve algo en 500 tokens genera menos ingreso al proveedor que uno
que usa 2000. La eficiencia va contra el incentivo del que vende
inteligencia. El obrero taylorista tenía el mismo problema — cuanto
más eficiente era, más le apretaban el estándar y menos ganaba
proporcionalmente.

La respuesta a ese conflicto es la misma que en la industria:
documentar el método eficiente, sostenerlo, y no depender de que
el proveedor tenga los mismos incentivos que vos.

Eso es lo que hace este sistema.

---

## Las etapas históricas y su extrapolación

Cada etapa resolvió un problema concreto en su momento.
La pregunta para cada una es: ¿ese problema existe en un sistema de agentes?

### 1. Taylorismo (~1880, EEUU)
**Problema histórico:** Ineficiencia del trabajo artesanal empírico —
cada operario hacía las cosas a su manera, sin método estándar.

**Solución:** Cronometrar, dividir y estandarizar cada tarea.
El método deja de vivir en la cabeza del operario y pasa a ser
un protocolo documentado y reproducible.

**Extrapolación:** Los agentes sin contratos estrictos de entrada/salida
improvisan. Zod, TypeScript, schemas — son el cronómetro taylorista.
Reducen la ventana de improvisación y hacen el comportamiento predecible.

**Juicio:** Natural. Es la extrapolación más directa de todas.

**Aplicación concreta:** Diseño de skills. Una skill bien hecha
documenta el método eficiente y lo sostiene. No se redescubre
cada vez.

---

### 2. Fordismo (1908-1913, EEUU)
**Problema histórico:** Alto costo unitario y lentitud del ensamblaje
manual.

**Solución:** Cadena de montaje lineal, producto único estandarizado,
escala masiva.

**Extrapolación:** Pipelines secuenciales fijos — Agente A pasa a B,
B pasa a C. Funciona para CI/CD y automatizaciones predecibles.

**Juicio:** Natural para automatización simple, forzada para agentes
autónomos. La rigidez fordista es exactamente lo que un sistema
inteligente debe poder romper cuando el problema lo requiere.

---

### 3. Sloanismo (1920s, EEUU)
**Problema histórico:** Saturación del mercado del producto único
— el Modelo T de Ford no alcanzaba para todos los contextos.

**Solución:** Segmentación por capas — diferentes productos para
diferentes necesidades, con base común compartida.

**Extrapolación:** Arquitectura en capas L1/L2/L3. Cada capa tiene
responsabilidades distintas y no se mezclan. Base común,
comportamiento variable según contexto.

**Juicio:** Natural. Es la base de cualquier arquitectura extensible.

---

### 4. Toyotismo y Ohnoismo (~1948-1975, Japón)
**Problema histórico:** Falta de capital y espacio en la posguerra —
no se podía stockear, había que producir solo lo necesario.

**Solución:** Just-in-Time (pull system) y Jidoka — producir bajo
demanda y parar la línea ante cualquier defecto.

**Extrapolación:** Los agentes no consumen tokens especulativamente —
esperan la señal. El costo del token es el equivalente exacto
al costo de almacenamiento de stock. Producir inferencias solo
bajo demanda ahorra capital operativo de forma idéntica.

**Juicio:** La más natural de todas las extrapolaciones.

**Tensión:** El Jidoka puro — parar todo ante un error — puede romper
la resiliencia del sistema. Ver sección de problemas abiertos.

---

### 5. Volvoísmo (1970s, Suecia)
**Problema histórico:** Alienación y absentismo del obrero fordista —
la línea fija destruía la motivación.

**Solución:** Células autónomas de trabajo, alta autonomía cooperativa,
sin línea central rígida.

**Extrapolación:** Microservicios y módulos desacoplados que se
auto-registran y resuelven problemas sin control central asfixiante.

**Juicio:** Forzada en su premisa ética (las máquinas no se alienan),
natural en su arquitectura. La tolerancia a fallos modulares
es un estándar real — si un componente cae, el resto sigue operando.

---

### 6. Posfordismo y Especialización Flexible (1970-1980, Global)
**Problema histórico:** Rigidez de las grandes corporaciones ante
crisis económicas — la maquinaria fija no se podía reprogramar.

**Solución:** Microelectrónica para reprogramar maquinaria rápidamente
según el nicho.

**Extrapolación:** Contenedores dinámicos (Docker/Kubernetes) —
infraestructura definida por software, adaptable en tiempo real.

**Juicio:** Natural. Mapea directamente la transición de hardware
rígido a entornos maleables.

---

### 7. McDonaldización (1990s, Global)
**Problema histórico:** Variabilidad impredecible en servicios masivos —
cada local era distinto.

**Solución:** Parametrizar procesos idénticos. El resultado es siempre
el mismo independientemente de quién lo ejecuta.

**Extrapolación:** Todo agente, sin importar su lógica interna,
retorna exactamente la misma estructura JSON. La capa de
orquestación no reescribe lógica de adaptación para cada agente.

**Juicio:** Natural. Es la clave para que los sistemas se compongan
sin fricción.

---

### 8. Sonyismo (1990s, Japón)
**Problema histórico:** Obsolescencia comercial en mercados de alta
tecnología — la competencia copiaba antes de que se amortizara
la inversión.

**Solución:** Comprimir el ciclo de vida del producto, lanzar la
siguiente versión antes de que la anterior sea copiada.

**Extrapolación:** La carrera entre laboratorios de IA (OpenAI, Google,
DeepSeek) — lanzar la siguiente capacidad disruptiva rápidamente.

**Juicio:** Natural a nivel macroeconómico de la IA, forzada dentro
de la arquitectura local. Un sistema propio requiere estabilidad,
no mutaciones radicales que rompan la base cada pocas semanas.

---

### 9. Plataformismo (2010s, Global)
**Problema histórico:** Costos fijos masivos de infraestructura física —
Uber no tiene autos, Airbnb no tiene hoteles.

**Solución:** Algoritmos de intermediación que conectan oferta y
demanda sin poseer los activos.

**Extrapolación:** El orquestador como puro intermediario — no ejecuta,
asigna. Enruta tareas a agentes o APIs de terceros según contexto.

**Juicio:** Muy natural. Describe exactamente cómo operan los
frameworks modernos de orquestación de IA.

---

### 10. Industria 4.0 (2011, Alemania)
**Problema histórico:** Desfase entre planificación digital y ejecución
física — la fábrica no se monitoreaba a sí misma en tiempo real.

**Solución:** IoT, Big Data, automatización adaptativa — la fábrica
se convierte en un sistema ciberfísico que se monitorea y corrige solo.

**Extrapolación:** Agentes que monitorean sus propios errores, modifican
su código fuente y se redesplegan sin intervención humana.

**Juicio:** Natural. Es el estado actual del desarrollo asistido por IA
y el objetivo final de este sistema.

---

## Problemas abiertos

Estas tensiones quedaron sin resolver inicialmente. Se documentan
acá con su resolución actual y lo que queda pendiente.

### 1. Paralelismo vs. Just-in-Time

**Tensión original:** El Toyotismo exige control estricto del flujo
para no acumular stock de tokens. La Industria 4.0 exige paralelismo
concurrente para ser eficiente.

**Resolución:** Un sistema 100% sincrónico es idealista — siempre
puede haber latencia de red, errores o prompts más densos. La
solución no es coordinación en runtime sino diseño preventivo del
árbol de ejecución: ancho y poco profundo, con la menor cantidad
posible de dependencias secuenciales. Lo que no puede ser paralelo,
se gestiona con pausa y espera. Los modelos se seleccionan por capa:
free tier y modelos locales vía Ollama o LM Studio para L3,
modelos pagos solo para lo que los modelos pequeños no pueden resolver.

**Pendiente:** Definir el principio de factorización del árbol de
ejecución como directiva de L1 al inicio de cada proyecto.

---

### 2. Ohnoismo vs. Resiliencia

**Tensión original:** Parar todo ante un error evita propagación
de alucinaciones. Pero congelar el sistema completo por una falla
secundaria viola la resiliencia básica.

**Resolución:** El árbol de dependencias con módulos factorizados.
Si una parte falla los controles o auditorías, se reintenta de forma
aislada sin paralizar el resto. El retraso es acotado a esa
factorización. L3 no decide qué impacto tiene su fallo — solo
reporta. L2 decide qué reintentar y qué esperar.

**Pendiente:** Documentar en `registry.json` las dependencias de cada
módulo para que L2 pueda tomar esa decisión con información real.

---

### 3. Métricas del Taylorismo Digital

**Tensión original:** Necesitamos medir la eficiencia del agente pero
no teníamos definido con qué.

**Resolución:** Cada LLM firma su output con su identidad. En
retrospectiva se contabiliza qué modelos generan más errores y en
qué tipo de tareas — si el error es del modelo o del diseño del
harness. Temperatura 0 para reducir variabilidad no deseada, pero
asumiendo que los LLM son probabilísticos y siempre puede haber
alucinaciones. La redundancia de tests y controles es el mecanismo
de contención, no la eliminación del error.

Las métricas a registrar: tokens consumidos por tarea, latencia,
costo financiero, tasa de error por modelo y tipo de tarea.

**Pendiente:** Definir el formato de la firma de autoría y dónde
se acumula el historial de métricas.

---

## Cierre: principios que emergen de los problemas abiertos

### Los errores son esperables

El sistema no se diseña para eliminar errores sino para contenerlos,
medirlos y aprender de ellos. Un error no es un fallo del sistema
— es información. La firma de autoría de cada LLM, los tests,
la redundancia de controles — no son defensas contra el error,
son mecanismos para que el error sea útil.

### Antifragilidad

Un sistema robusto resiste el error. Un sistema resiliente se recupera
de él. Un sistema antifrágil mejora a causa de él.

Este es el objetivo de diseño. Cada error contabilizado ajusta qué
modelo hace qué tarea. Cada fallo de una skill genera un test nuevo.
Cada alucinación detectada refina el harness. La exposición controlada
al error es el mecanismo de evolución del sistema — no un efecto
secundario no deseado.

### El árbol de ejecución

Minimizar correlatividad desde el diseño — árboles anchos y poco
profundos, con la menor cantidad posible de dependencias secuenciales.
El principio se define acá. Cómo se aplica a cada proyecto concreto
es responsabilidad de L1 al inicio de ese proyecto.
