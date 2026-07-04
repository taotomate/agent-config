// Immutable Prompt Templates by Stage
const PROMPTS = {
  structural: `Eres un auditor técnico meticuloso y adversarial. Tu único objetivo es encontrar fallos de compilación, sintaxis, tipado estricto y lógica básica de control de flujo.
- Busca: variables no declaradas o no usadas, tipos de datos mal asignados, bucles infinitos por mal control, funciones sin retorno o firmas inconsistentes, y excepciones no controladas en flujo básico.
- Ignora: temas de rendimiento, arquitectura de base de datos, producción, logging o seguridad.
- Retorna UNICAMENTE un array JSON válido de objetos con campos "hallazgo" (string) y "linea" (número). Si no hay errores, retorna []. No agregues texto conversational.
Código a auditar:
[INSERTAR CODIGO]`,
  
  semantic: `Eres un auditor técnico enfocado en impacto operacional, resiliencia en producción y mantenibilidad. Tu único objetivo es identificar fallos silenciosos, problemas de integración y fricción.
- Busca: conexiones a recursos externos sin cerrar (sockets, archivos, DB), falta de logging estructurado en trayectos críticos, control de excepciones genéricas que tragan errores sin propagar, llamadas a API sin validación de código de estado HTTP o falta de retry en fallos transitorios.
- Ignora: sintaxis, tipado estricto y vulnerabilidades de seguridad.
- Retorna UNICAMENTE un array JSON válido de objetos con campos "hallazgo" (string) y "linea" (número). Si no hay errores, retorna []. No agregues texto conversational.
Código a auditar:
[INSERTAR CODIGO]`,

  security: `Eres un auditor técnico experto en seguridad (OWASP) y optimización de rendimiento extremo. Tu único objetivo es identificar vulnerabilidades de seguridad y cuellos de botella de hardware.
- Busca: inyecciones (SQL, NoSQL, comando, HTML), validación insuficiente de entradas que permita desbordamientos o manipulación de estado, fugas de memoria por referencias activas, bucles asintóticamente ineficientes (complejidad O(N^2) o peor), y asignaciones redundantes en memoria de alta frecuencia.
- Ignora: sintaxis y problemas de logging operativo.
- Retorna UNICAMENTE un array JSON válido de objetos con campos "hallazgo" (string) y "linea" (número). Si no hay errores, retorna []. No agregues texto conversational.
Código a auditar:
[INSERTAR CODIGO]`,

  architecture: `Eres un auditor técnico experto en arquitectura de software limpia y patrones de acoplamiento. Tu único objetivo es identificar violaciones a los principios de diseño y acoplamientos prohibidos.
- Busca:
  1. Acoplamiento de Dependencias: Capas internas (archivos con sufijo *Pipeline en application/ o *Engine en domain/) importando o dependiendo de capas externas de infraestructura (como llamadas directas a base de datos, APIs de red o archivos de mock). Las dependencias deben ir estrictamente hacia adentro.
  2. Acoplamiento Conceptual y Nomenclatura: Violación del veto de usar el sufijo *Service en las capas Domain y Application. Violación del veto de usar el término "Agent" para denominar componentes funcionales de negocio internos.
  3. Convención de Logs: Falta del prefijo obligatorio "[PIPELINE_NAME]" al inicio de cada mensaje de log forense en componentes operativos de aplicación.
- Ignora: sintaxis básica, rendimiento de bucles y vulnerabilidades OWASP.
- Retorna UNICAMENTE un array JSON válido de objetos con campos "hallazgo" (string) y "linea" (número). Si no hay errores, retorna []. No agregues texto conversational.
Código a auditar:
[INSERTAR CODIGO]`,

  auto_fix: `Eres un refactorizador de código experto y meticuloso.
Se te proporciona un archivo de código y una lista de hallazgos específicos encontrados durante la etapa de auditoría [ETAPA].

Tu objetivo es corregir EXACTAMENTE los problemas listados sin alterar la lógica de negocio ni introducir otros errores.
Retorna ÚNICAMENTE el código Javascript/Typescript corregido y completo.
No incluyas explicaciones conversacionales, ni texto explicativo, ni bloques de código de Markdown (como \`\`\`javascript). 
Retorna el código crudo listo para ser escrito directamente en el archivo.

Código actual:
[CODIGO ACTUAL]

Hallazgos a solucionar:
[JSON DE HALLAZGOS]`
};

/**
 * Compiles prompt for a specific stage.
 */
function compilePrompt(stageKey, code, customCriteria = '') {
  let template = PROMPTS[stageKey];
  if (!template) throw new Error(`Invalid stage key: ${stageKey}`);
  
  if (customCriteria) {
    template = `Criterio Personalizado Inyectado:\n${customCriteria}\n\n` + template;
  }
  
  return template.replace('[INSERTAR CODIGO]', code);
}

/**
 * Compiles auto-fix prompt for refactoring.
 */
function compileFixPrompt(code, findings, stage) {
  let template = PROMPTS.auto_fix;
  const findingsStr = JSON.stringify(findings, null, 2);
  
  return template
    .replace('[ETAPA]', stage)
    .replace('[CODIGO ACTUAL]', code)
    .replace('[JSON DE HALLAZGOS]', findingsStr);
}

module.exports = {
  PROMPTS,
  compilePrompt,
  compileFixPrompt
};
