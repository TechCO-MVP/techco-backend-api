# flake8: noqa: E501

from src.domain.position_configuration import FLOW_TYPE
from src.domain.business import PositionFlow, PHASE_CLASSIFICATION

base_position_flows: dict[FLOW_TYPE, PositionFlow] = {
    FLOW_TYPE.HIGH_PROFILE_FLOW: PositionFlow(
        flow_type=FLOW_TYPE.HIGH_PROFILE_FLOW,
        pipe_id=305713420,
        groups=[
            {
                "name": "Filtro inicial",
                "phases": [
                    {
                        "name": "Candidatos sugeridos",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {"title": "", "subtitle": "", "description": "", "button_text": ""}
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Hola! Estás en la primera fase del proceso.",
                                    "subtitle": "Activamos nuestra base de datos inteligente para identificar, de forma automática, a candidatos que se ajusten a tu vacante.",
                                    "description": "Este candidato ha sido contactado para que participe en el proceso. Te avisaremos cuando acepte.\nMientras tanto, puedes compartir el enlace de la vacante desde el botón del tablero para llegar a más personas.",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Oferta enviada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {"title": "", "subtitle": "", "description": "", "button_text": ""}
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Logramos contactar a tu candidato!",
                                    "subtitle": "Ya le enviamos la invitación para que participe en el proceso. Apenas la acepte, podrá iniciar su primer filtro y sabrás qué tan buen match hace con tu vacante.",
                                    "description": "Mientras tanto, nuestro sistema hará seguimiento para motivarlo a que avance cuanto antes.\n\nTe avisaremos tan pronto tengamos novedades. ¡Vamos por buen camino!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Filtro inicial",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Gracias por completar esta información!",
                                    "subtitle": "Estamos revisando tus respuestas con atención. Muy pronto te contaremos cuál es el siguiente paso en este proceso: una breve evaluación de afinidad cultural, que nos ayudará a conocerte mejor y asegurarnos de que esta oportunidad encaje contigo.",
                                    "description": "Queremos que vivas esta experiencia con claridad, seguridad y a tu propio ritmo.\n\nRecuerda que este es un proceso pensado también para que tú evalúes si esta oportunidad hace sentido contigo.\n\nTe avisaremos por correo si avanzas a la siguiente etapa.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡El candidato aceptó participar en el proceso!",
                                    "subtitle": "Ya analizamos su perfil con nuestro sistema de preselección automática.",
                                    "description": "Si consideras que puede avanzar, confírmalo desde el formulario de la derecha y enviaremos de inmediato su Assessment de fit cultural. Ten en cuenta en qué momento le envías la prueba puesto que el candidato tendrá 24 horas para completarla.\nEsta fue su calificación inicial:",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "name": "Fit cultural",
                "phases": [
                    {
                        "name": "Assessment fit Cultural",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Buenas noticias!",
                                    "subtitle": "Revisamos tu información y pasaste el primer filtro del proceso.",
                                    "description": "Ahora queremos invitarte a dar el siguiente paso: una evaluación de afinidad cultural. Esta etapa nos ayudará a entender mejor cómo encajas con nuestro equipo y nuestra forma de trabajar.\nEs una herramienta sencilla y rápida que te permitirá avanzar en el proceso de manera más personalizada.",
                                    "button_text": "Adjuntar prueba",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Tu candidato ya está a un paso más de avanzar!",
                                    "subtitle": "Le avisamos que su Assessment de fit cultural está listo. Podrá iniciarlo cuando se sienta preparado, y desde ese momento tendrá una hora para responderlo.",
                                    "description": "Las preguntas se mostrarán solo al hacer clic en “Iniciar”, para que llegue con toda la concentración.\nTiene 24 horas para completarlo, si no lo hace, nuestro sistema le enviará hasta 2 recordatorios automáticos, uno por día.\nTe avisaremos apenas tengamos su resultado. ¡Vamos bien!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Resultado Fit Cultural",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Gracias por completar la evaluación!",
                                    "subtitle": "Ya recibimos tus respuestas y en este momento las estamos revisando con atención.",
                                    "description": "Esta etapa nos ayuda a entender mejor si compartimos valores y formas de trabajar.\n\nSi encontramos que hay afinidad cultural, te estaremos contactando muy pronto para enviarte la fecha y hora de una entrevista, donde podremos conocernos mejor.\n\nTe avisaremos por correo con los próximos pasos.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡El candidato completó el test de fit cultural!",
                                    "subtitle": "Evaluamos habilidades y valores alineados con lo que buscas, y ya puedes ver qué tan buen match hizo con tu vacante.",
                                    "description": "Si el resultado cumple con tus expectativas, este es el momento de agendar la primer entrevista.\nEn el formulario de la derecha, ingresa hasta 5 opciones de horario. Nosotros nos encargamos de notificárselo y hacer seguimiento para que elija lo más pronto posible.\n¡Vamos avanzando!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "name": "Primer entrevista",
                "phases": [
                    {
                        "name": "Primera entrevista solicitada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Queremos seguir conociéndote!",
                                    "subtitle": "Tu perfil se ajusta a nuestras expectativas y queremos dar el siguiente paso.",
                                    "description": "La próxima entrevista será con nuestro equipo de selección, donde profundizaremos un poco más sobre tu experiencia y lo que esperas del rol.\n\nPara que sea sencillo para ti, elige el día y la hora que mejor te convenga. Ten en cuenta que la entrevista tendrá una duración aproximada de 45 minutos.\n\nInstrucción sobre las opciones:\nSelecciona una de las opciones disponibles para agendar tu entrevista. Te confirmaremos el horario por correo una vez que completes la selección.",
                                    "button_text": "Agendar",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Todo listo para que se conozcan!",
                                    "subtitle": "Ya le enviamos al candidato las opciones de horario que propusiste. Ahora estamos esperando a que seleccione la que más le convenga.",
                                    "description": "Te notificaremos en cuanto confirme la cita.\n¡Vamos con buen ritmo!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Primera entrevista programada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Entrevista agendada con éxito!",
                                    "subtitle": "Tu entrevista ha quedado programada para la fecha y hora que elegiste.",
                                    "description": 'Te estaremos enviando recordatorios para que lo tengas presente y llegues con total tranquilidad.\n\nTenemos muchas ganas de conocerte y seguir descubriendo todo lo que puedes aportar."',
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Ya casi se conocen!",
                                    "subtitle": "No olvides agendarla en tu calendario para que nada se cruce en el camino.\n¡Esperamos que tengan una gran conversación!",
                                    "description": "El candidato confirmó su entrevista para la siguiente fecha:",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Resultado primer entrevista",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Ya pasó tu entrevista!",
                            "subtitle": "Ya pasó la fecha y hora que habías agendado, así que suponemos que tuviste la oportunidad de conversar con nuestro equipo.",
                            "description": "De ser así, en este momento estamos revisando cómo te fue en la entrevista para definir los próximos pasos.\nSi avanzas en el proceso, muy pronto te estaremos contactando para invitarte a uno de los últimos pasos: la evaluación técnica.",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Cuéntanos cómo te fue con el candidato!",
                            "subtitle": "¿Cumplió tus expectativas y quieres que continúe al Assessment técnico?",
                            "description": "Cuéntanos en el formulario de la derecha.\nApenas nos confirmes, le avisaremos que puede continuar con el Assessment técnico. ¡Así seguimos avanzando sin perder ritmo!",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Assessment técnico",
                "phases": [
                    {
                        "name": "Assessment técnico",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡La entrevista nos dejó muy emocionados!",
                                    "subtitle": "Nos encantó conocerte y ver todo lo que podrías aportar al equipo.",
                                    "description": "Por eso, queremos invitarte a dar el siguiente paso: una evaluación técnica.\n\nEsta etapa nos ayudará a profundizar en tus habilidades y ver en acción tu forma de pensar y resolver desafíos.\nEs una herramienta clara y sencilla, pensada para que puedas mostrar tu talento de forma auténtica.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Tu candidato está a un paso de la entrevista final!",
                                    "subtitle": "Le avisamos que su reto técnico ya está disponible y que debe resolverlo lo antes posible para no perder tiempo en el proceso.",
                                    "description": "Las instrucciones ya están visibles, así que puede empezar de inmediato.\nTiene 72 horas para completarlo y, mientras tanto, nuestro sistema le enviará recordatorios automáticos para mantenerlo enfocado.\nTe avisaremos tan pronto tengamos su resultado. ¡Cada vez más cerca del match perfecto!",
                                    "button_text": "Adjuntar prueba",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Resultado Assessment técnico",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Gracias por completar la evaluación técnica!",
                                    "subtitle": "Ya recibimos tus respuestas y en este momento las estamos revisando con atención.",
                                    "description": "Esta etapa nos permite conocer más a fondo tus habilidades y tu forma de enfrentar desafíos.\n\nSi todo va bien y vemos que es un buen match, muy pronto te estaremos llamando para agendar la entrevista final del proceso.\n\nTe avisaremos por correo con los próximos pasos. ¡Gracias por seguir con nosotros!",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Listo! Evaluamos las  habilidades técnicas y la capacidad para afrontar los retos reales de la vacante.",
                                    "subtitle": "Ya puedes ver cómo se desempeñó y qué tan bien se alinea con los skills que necesitas.",
                                    "description": "Si crees que este es el match ideal, ¡es momento de dar el siguiente paso!\nEn el formulario de la derecha, ingresa hasta 5 opciones de horario para la entrevista final. Nosotros le notificaremos y haremos seguimiento para que escoja lo más pronto posible.\n\n¡Cada vez más cerca de encontrar a la persona perfecta para el rol!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "name": "Entrevista final",
                "phases": [
                    {
                        "name": "Entrevista final solicitada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Felicitaciones!",
                            "subtitle": "Tu evaluación técnica fue excelente y estamos muy emocionados de seguir adelante contigo.",
                            "description": "Queremos invitarte a la entrevista final del proceso, donde podremos conocernos mejor y conversar sobre lo que podría venir.\n\nPara que sea cómodo para ti, elige el día y la hora que mejor te convenga.\nTen en cuenta que esta entrevista tendrá una duración aproximada de 45 minutos.",
                            "button_text": "Agendar",
                        },
                        "interviewer_data": {
                            "title": "¡Tu candidato está a un paso de la entrevista final!",
                            "subtitle": "Ya recibió tus opciones de horario y ahora estamos esperando a que escoja el que mejor le funcione.",
                            "description": "Muy pronto podrás tener esa conversación clave que te ayudará a tomar la decisión final.\n\n¡Estamos muy cerca! Te avisaremos apenas confirme la cita.",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Entrevista final programada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Entrevista final agendada con éxito!",
                            "subtitle": "Tu entrevista ha quedado programada para la fecha y hora que elegiste.",
                            "description": "Te enviaremos recordatorios para que estés completamente preparado y puedas llegar con tranquilidad.\n\nEstamos muy emocionados de llegar a esta etapa contigo y de conocer tus ideas finales para sumar al equipo. ¡Esta es la oportunidad para brillar y mostrar todo tu potencial!",
                            "button_text": "statement_pipefy",
                        },
                        "interviewer_data": {
                            "title": "¡Entrevista final confirmada!",
                            "subtitle": "Es el momento clave para decidir si es el match perfecto.",
                            "description": "No olvides agendar la reunión en tu calendario para no perderte nada.\n\n¡Vamos con todo en esta última etapa!\nTu candidato ya agendó la entrevista final para:",
                            "button_text": "statement_pipefy",
                        },
                    },
                    {
                        "name": "Resultado entrevista final",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Tu entrevista final ya fue!",
                            "subtitle": "La fecha y hora que habías agendado ya pasó, y esperamos que hayas tenido una buena conversación con nuestro equipo.",
                            "description": "En este momento estamos evaluando tu desempeño para tomar la decisión final.\nMuy pronto te contactaremos para compartirte el resultado y, si pasaste, los pasos a seguir.\n\n¡Gracias por haber llegado hasta aquí y por todo el interés que has demostrado en ser parte de nuestro equipo!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Terminó la entrevista final!",
                            "subtitle": "¡Qué emoción! El candidato completó la entrevista final, y ahora viene la decisión más importante.",
                            "description": "Cuéntanos en el formulario de la derecha qué quieres hacer:\n\n¿Te encantó? Márcalo como Seleccionado y cerremos el proceso.\n¿Tienes dudas? Envíalo a la lista de finalistas para decidir después.\n¿No hizo match? Puedes descartarlo fácilmente.\n\n¡Tú tienes la última palabra!",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Finalistas",
                "phases": [
                    {
                        "name": "Finalistas",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Tu entrevista final ya fue!",
                            "subtitle": "La fecha y hora que habías agendado ya pasó, y esperamos que hayas tenido una buena conversación con nuestro equipo.",
                            "description": "En este momento estamos evaluando tu desempeño para tomar la decisión final.\nMuy pronto te contactaremos para compartirte el resultado y si pasaste, los pasos a seguir.\n\n¡Gracias por haber llegado hasta aquí y por todo el interés que has demostrado en ser parte de nuestro equipo!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Tu candidato está en la fase de finalistas!",
                            "subtitle": "Aún no has tomado la decisión final… y lo entendemos, no siempre es fácil cuando hay buenos perfiles sobre la mesa.",
                            "description": "Este candidato llegó lejos por una razón: tiene algo que lo hace una gran opción.\nDesde este punto, tú decides qué sigue:\n\n¿Quieres que se quede con el puesto? Márcalo como Seleccionado.\n¿Crees que no es el indicado? También puedes descartarlo.\n\n¡Estás a solo un clic de tomar la última palabra!",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Candidato seleccionado",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Felicitaciones!",
                            "subtitle": "Estamos muy emocionados de compartirte que has sido seleccionado para esta oportunidad.",
                            "description": "Nos encantaría que aceptes nuestra oferta y formes parte de este nuevo proyecto con nosotros.\n\nMuy pronto te contactaremos para darte todos los detalles y acompañarte en los próximos pasos. ¡Estamos ansiosos por lo que viene!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Felicitaciones! escogiste un candidato",
                            "subtitle": "Te deseamos lo mejor en esta nueva etapa.",
                            "description": "¡Gran elección!\n\nPodés estar tranquilo: hiciste un gran trabajo. Esta contratación fue objetiva, sin sesgos y con toda la información que necesitabas para tomar la mejor decisión.\n\n¿Tienes otra vacante?\nNo dudes en crearla con Tici. Estamos acá para ayudarte a encontrar al mejor talento, siempre.",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Descartados",
                "phases": [
                    {
                        "name": "Acción no completada",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Hola!",
                            "subtitle": "Vimos que no pudiste completar esta etapa del proceso dentro del tiempo esperado.\nEntendemos que pueden surgir imprevistos o que los horarios disponibles no se ajustaran a tu agenda.",
                            "description": "Si aún te interesa continuar, te invitamos a escribirle directamente a la persona que ha estado acompañando tu proceso.\nElla podrá ayudarte a revisar si es posible reprogramar o encontrar una alternativa.\n\n¡Gracias por tu interés y esperamos saber de ti pronto!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "El candidato no completó esta etapa del proceso",
                            "subtitle": "En algunos casos, por diferentes motivos, un candidato no logra avanzar a tiempo.\nEsto puede deberse a temas personales, falta de disponibilidad o que los horarios propuestos no se ajustaban a su agenda.",
                            "description": "¿Te gustaría darle una nueva oportunidad para completar esta etapa?\n\nGracias por seguir cada paso con atención y empatía.\n¡Seguimos contigo en la búsqueda del mejor talento!",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Abandonaron el proceso",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "Decidiste dar un paso al costado",
                            "subtitle": "Sabemos que tomar este tipo de decisiones no siempre es fácil, y respetamos completamente tu elección de no continuar en el proceso.",
                            "description": "Gracias por el interés que mostraste hasta aquí y por haber compartido un poco de tu historia con nosotros.\nOjalá podamos encontrarnos en otra oportunidad. ¡Te esperamos en futuras convocatorias!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "El candidato decidió no continuar",
                            "subtitle": "A veces, aunque el proceso fluya bien, pueden surgir razones personales o profesionales por las que un candidato prefiere no seguir adelante.",
                            "description": "Gracias por seguir cada etapa con atención y respeto.\n¡Seguimos contigo en la búsqueda del mejor talento!\n\nEn este caso, la persona decidió salir del proceso por el siguiente motivo:",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Descartados",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                    },
                ],
            },
        ],
    ),
    FLOW_TYPE.MEDIUM_PROFILE_FLOW: PositionFlow(
        flow_type=FLOW_TYPE.MEDIUM_PROFILE_FLOW,
        pipe_id=7676765,
        groups=[
            {
                "name": "Filtro inicial",
                "phases": [
                    {
                        "name": "Candidatos sugeridos",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {"title": "", "subtitle": "", "description": "", "button_text": ""}
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Hola! Estás en la primera fase del proceso.",
                                    "subtitle": "Activamos nuestra base de datos inteligente para identificar, de forma automática, a candidatos que se ajusten a tu vacante.",
                                    "description": "Este candidato ha sido contactado para que participe en el proceso. Te avisaremos cuando acepte.\nMientras tanto, puedes compartir el enlace de la vacante desde el botón del tablero para llegar a más personas.",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Oferta enviada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {"title": "", "subtitle": "", "description": "", "button_text": ""}
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Logramos contactar a tu candidato!",
                                    "subtitle": "Ya le enviamos la invitación para que participe en el proceso. Apenas la acepte, podrá iniciar su primer filtro y sabrás qué tan buen match hace con tu vacante.",
                                    "description": "Mientras tanto, nuestro sistema hará seguimiento para motivarlo a que avance cuanto antes.\n\nTe avisaremos tan pronto tengamos novedades. ¡Vamos por buen camino!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Filtro inicial",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Gracias por completar esta información!",
                                    "subtitle": "Estamos revisando tus respuestas con atención. Muy pronto te contaremos cuál es el siguiente paso en este proceso: una breve evaluación de afinidad cultural, que nos ayudará a conocerte mejor y asegurarnos de que esta oportunidad encaje contigo.",
                                    "description": "Queremos que vivas esta experiencia con claridad, seguridad y a tu propio ritmo.\n\nRecuerda que este es un proceso pensado también para que tú evalúes si esta oportunidad hace sentido contigo.\n\nTe avisaremos por correo si avanzas a la siguiente etapa.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡El candidato aceptó participar en el proceso!",
                                    "subtitle": "Ya analizamos su perfil con nuestro sistema de preselección automática.",
                                    "description": "Si consideras que puede avanzar, confírmalo desde el formulario de la derecha y enviaremos de inmediato su Assessment de fit cultural. Ten en cuenta en qué momento le envías la prueba puesto que el candidato tendrá 24 horas para completarla.\nEsta fue su calificación inicial:",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "name": "Fit cultural",
                "phases": [
                    {
                        "name": "Assessment fit Cultural",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Buenas noticias!",
                                    "subtitle": "Revisamos tu información y pasaste el primer filtro del proceso.",
                                    "description": "Ahora queremos invitarte a dar el siguiente paso: una evaluación de afinidad cultural. Esta etapa nos ayudará a entender mejor cómo encajas con nuestro equipo y nuestra forma de trabajar.\nEs una herramienta sencilla y rápida que te permitirá avanzar en el proceso de manera más personalizada.",
                                    "button_text": "Adjuntar prueba",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Tu candidato ya está a un paso más de avanzar!",
                                    "subtitle": "Le avisamos que su Assessment de fit cultural está listo. Podrá iniciarlo cuando se sienta preparado, y desde ese momento tendrá una hora para responderlo.",
                                    "description": "Las preguntas se mostrarán solo al hacer clic en “Iniciar”, para que llegue con toda la concentración.\nTiene 24 horas para completarlo, si no lo hace, nuestro sistema le enviará hasta 2 recordatorios automáticos, uno por día.\nTe avisaremos apenas tengamos su resultado. ¡Vamos bien!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Resultado Fit Cultural",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Gracias por completar la evaluación!",
                                    "subtitle": "Ya recibimos tus respuestas y en este momento las estamos revisando con atención.",
                                    "description": "Esta etapa nos ayuda a entender mejor si compartimos valores y formas de trabajar.\n\nSi encontramos que hay afinidad cultural, te estaremos contactando muy pronto para enviarte la fecha y hora de una entrevista, donde podremos conocernos mejor.\n\nTe avisaremos por correo con los próximos pasos.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡El candidato completó el test de fit cultural!",
                                    "subtitle": "Evaluamos habilidades y valores alineados con lo que buscas, y ya puedes ver qué tan buen match hizo con tu vacante.",
                                    "description": "Si el resultado cumple con tus expectativas, este es el momento de agendar la primer entrevista.\nEn el formulario de la derecha, ingresa hasta 5 opciones de horario. Nosotros nos encargamos de notificárselo y hacer seguimiento para que elija lo más pronto posible.\n¡Vamos avanzando!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "name": "Primer entrevista",
                "phases": [
                    {
                        "name": "Primera entrevista solicitada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Queremos seguir conociéndote!",
                                    "subtitle": "Tu perfil se ajusta a nuestras expectativas y queremos dar el siguiente paso.",
                                    "description": "La próxima entrevista será con nuestro equipo de selección, donde profundizaremos un poco más sobre tu experiencia y lo que esperas del rol.\n\nPara que sea sencillo para ti, elige el día y la hora que mejor te convenga. Ten en cuenta que la entrevista tendrá una duración aproximada de 45 minutos.\n\nInstrucción sobre las opciones:\nSelecciona una de las opciones disponibles para agendar tu entrevista. Te confirmaremos el horario por correo una vez que completes la selección.",
                                    "button_text": "Agendar",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Todo listo para que se conozcan!",
                                    "subtitle": "Ya le enviamos al candidato las opciones de horario que propusiste. Ahora estamos esperando a que seleccione la que más le convenga.",
                                    "description": "Te notificaremos en cuanto confirme la cita.\n¡Vamos con buen ritmo!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Primera entrevista programada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Entrevista agendada con éxito!",
                                    "subtitle": "Tu entrevista ha quedado programada para la fecha y hora que elegiste.",
                                    "description": 'Te estaremos enviando recordatorios para que lo tengas presente y llegues con total tranquilidad.\n\nTenemos muchas ganas de conocerte y seguir descubriendo todo lo que puedes aportar."',
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Ya casi se conocen!",
                                    "subtitle": "No olvides agendarla en tu calendario para que nada se cruce en el camino.\n¡Esperamos que tengan una gran conversación!",
                                    "description": "El candidato confirmó su entrevista para la siguiente fecha:",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Resultado primer entrevista",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Ya pasó tu entrevista!",
                            "subtitle": "Ya pasó la fecha y hora que habías agendado, así que suponemos que tuviste la oportunidad de conversar con nuestro equipo.",
                            "description": "De ser así, en este momento estamos revisando cómo te fue en la entrevista para definir los próximos pasos.\nSi avanzas en el proceso, muy pronto te estaremos contactando para invitarte a uno de los últimos pasos: la evaluación técnica.",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Cuéntanos cómo te fue con el candidato!",
                            "subtitle": "¿Cumplió tus expectativas y quieres que continúe al Assessment técnico?",
                            "description": "Cuéntanos en el formulario de la derecha.\nApenas nos confirmes, le avisaremos que puede continuar con el Assessment técnico. ¡Así seguimos avanzando sin perder ritmo!",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Assessment técnico manual",
                "phases": [
                    {
                        "name": "Assessment técnico manual",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡La entrevista nos dejó muy emocionados!",
                                    "subtitle": "Nos encantó conocerte y ver todo lo que podrías aportar al equipo.",
                                    "description": "Por eso, queremos invitarte a dar el siguiente paso: una evaluación técnica.\n\nEsta etapa nos ayudará a profundizar en tus habilidades y ver en acción tu forma de pensar y resolver desafíos.\nEs una herramienta clara y sencilla, pensada para que puedas mostrar tu talento de forma auténtica.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Tu candidato está a un paso de la entrevista final!",
                                    "subtitle": "Le avisamos que su reto técnico ya está disponible y que debe resolverlo lo antes posible para no perder tiempo en el proceso.",
                                    "description": "Las instrucciones ya están visibles, así que puede empezar de inmediato.\nTiene 72 horas para completarlo y, mientras tanto, nuestro sistema le enviará recordatorios automáticos para mantenerlo enfocado.\nTe avisaremos tan pronto tengamos su resultado. ¡Cada vez más cerca del match perfecto!",
                                    "button_text": "Adjuntar prueba",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Resultado Assessment técnico manual",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Gracias por completar la evaluación técnica!",
                            "subtitle": "Ya recibimos tus respuestas y en este momento las estamos revisando con atención.",
                            "description": "Esta etapa nos permite conocer más a fondo tus habilidades y tu forma de enfrentar desafíos.\n\nSi todo va bien y vemos que es un buen match, muy pronto te estaremos llamando para agendar la entrevista final del proceso. \n\nTe avisaremos por correo con los próximos pasos. ¡Gracias por seguir con nosotros!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "Es tu turno de evaluar el assessment",
                            "subtitle": "Aquí encontrarás el assessment que el candidato compartió como parte del proceso.",
                            "description": "Ahora necesitamos tu mirada experta para evaluar su desempeño en esta etapa.\n\nPor favor, califica las siguientes dimensiones del 1 al 5 en el formulario que aparece a la derecha:\n• Capacidad de análisis del problema\n• Relevancia y lógica de la solución propuesta\n• Priorización y enfoque\n• Claridad en la comunicación escrita\n• Creatividad o iniciativa\n• Alineación con los objetivos del rol o del negocio\n\nUna vez agregues la calificación, y crees que este es el match ideal, ¡es momento de dar el siguiente paso!\nEn el formulario de la derecha, ingresa hasta 5 opciones de horario para la entrevista final. Nosotros le notificaremos y haremos seguimiento para que escoja lo más pronto posible.\n\nTu evaluación es clave para saber si estamos frente al match que estamos buscando.\n¡Gracias por seguir impulsando este proceso con tanta dedicación!",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Entrevista final",
                "phases": [
                    {
                        "name": "Entrevista final solicitada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Felicitaciones!",
                            "subtitle": "Tu evaluación técnica fue excelente y estamos muy emocionados de seguir adelante contigo.",
                            "description": "Queremos invitarte a la entrevista final del proceso, donde podremos conocernos mejor y conversar sobre lo que podría venir.\n\nPara que sea cómodo para ti, elige el día y la hora que mejor te convenga.\nTen en cuenta que esta entrevista tendrá una duración aproximada de 45 minutos.",
                            "button_text": "Agendar",
                        },
                        "interviewer_data": {
                            "title": "¡Tu candidato está a un paso de la entrevista final!",
                            "subtitle": "Ya recibió tus opciones de horario y ahora estamos esperando a que escoja el que mejor le funcione.",
                            "description": "Muy pronto podrás tener esa conversación clave que te ayudará a tomar la decisión final.\n\n¡Estamos muy cerca! Te avisaremos apenas confirme la cita.",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Entrevista final programada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Entrevista final agendada con éxito!",
                            "subtitle": "Tu entrevista ha quedado programada para la fecha y hora que elegiste.",
                            "description": "Te enviaremos recordatorios para que estés completamente preparado y puedas llegar con tranquilidad.\n\nEstamos muy emocionados de llegar a esta etapa contigo y de conocer tus ideas finales para sumar al equipo. ¡Esta es la oportunidad para brillar y mostrar todo tu potencial!",
                            "button_text": "statement_pipefy",
                        },
                        "interviewer_data": {
                            "title": "¡Entrevista final confirmada!",
                            "subtitle": "Es el momento clave para decidir si es el match perfecto.",
                            "description": "No olvides agendar la reunión en tu calendario para no perderte nada.\n\n¡Vamos con todo en esta última etapa!\nTu candidato ya agendó la entrevista final para:",
                            "button_text": "statement_pipefy",
                        },
                    },
                    {
                        "name": "Resultado entrevista final",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Tu entrevista final ya fue!",
                            "subtitle": "La fecha y hora que habías agendado ya pasó, y esperamos que hayas tenido una buena conversación con nuestro equipo.",
                            "description": "En este momento estamos evaluando tu desempeño para tomar la decisión final.\nMuy pronto te contactaremos para compartirte el resultado y, si pasaste, los pasos a seguir.\n\n¡Gracias por haber llegado hasta aquí y por todo el interés que has demostrado en ser parte de nuestro equipo!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Terminó la entrevista final!",
                            "subtitle": "¡Qué emoción! El candidato completó la entrevista final, y ahora viene la decisión más importante.",
                            "description": "Cuéntanos en el formulario de la derecha qué quieres hacer:\n\n¿Te encantó? Márcalo como Seleccionado y cerremos el proceso.\n¿Tienes dudas? Envíalo a la lista de finalistas para decidir después.\n¿No hizo match? Puedes descartarlo fácilmente.\n\n¡Tú tienes la última palabra!",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Finalistas",
                "phases": [
                    {
                        "name": "Finalistas",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Tu entrevista final ya fue!",
                            "subtitle": "La fecha y hora que habías agendado ya pasó, y esperamos que hayas tenido una buena conversación con nuestro equipo.",
                            "description": "En este momento estamos evaluando tu desempeño para tomar la decisión final.\nMuy pronto te contactaremos para compartirte el resultado y si pasaste, los pasos a seguir.\n\n¡Gracias por haber llegado hasta aquí y por todo el interés que has demostrado en ser parte de nuestro equipo!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Tu candidato está en la fase de finalistas!",
                            "subtitle": "Aún no has tomado la decisión final… y lo entendemos, no siempre es fácil cuando hay buenos perfiles sobre la mesa.",
                            "description": "Este candidato llegó lejos por una razón: tiene algo que lo hace una gran opción.\nDesde este punto, tú decides qué sigue:\n\n¿Quieres que se quede con el puesto? Márcalo como Seleccionado.\n¿Crees que no es el indicado? También puedes descartarlo.\n\n¡Estás a solo un clic de tomar la última palabra!",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Candidato seleccionado",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Felicitaciones!",
                            "subtitle": "Estamos muy emocionados de compartirte que has sido seleccionado para esta oportunidad.",
                            "description": "Nos encantaría que aceptes nuestra oferta y formes parte de este nuevo proyecto con nosotros.\n\nMuy pronto te contactaremos para darte todos los detalles y acompañarte en los próximos pasos. ¡Estamos ansiosos por lo que viene!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Felicitaciones! escogiste un candidato",
                            "subtitle": "Te deseamos lo mejor en esta nueva etapa.",
                            "description": "¡Gran elección!\n\nPodés estar tranquilo: hiciste un gran trabajo. Esta contratación fue objetiva, sin sesgos y con toda la información que necesitabas para tomar la mejor decisión.\n\n¿Tienes otra vacante?\nNo dudes en crearla con Tici. Estamos acá para ayudarte a encontrar al mejor talento, siempre.",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Descartados",
                "phases": [
                    {
                        "name": "Acción no completada",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Hola!",
                            "subtitle": "Vimos que no pudiste completar esta etapa del proceso dentro del tiempo esperado.\nEntendemos que pueden surgir imprevistos o que los horarios disponibles no se ajustaran a tu agenda.",
                            "description": "Si aún te interesa continuar, te invitamos a escribirle directamente a la persona que ha estado acompañando tu proceso.\nElla podrá ayudarte a revisar si es posible reprogramar o encontrar una alternativa.\n\n¡Gracias por tu interés y esperamos saber de ti pronto!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "El candidato no completó esta etapa del proceso",
                            "subtitle": "En algunos casos, por diferentes motivos, un candidato no logra avanzar a tiempo.\nEsto puede deberse a temas personales, falta de disponibilidad o que los horarios propuestos no se ajustaban a su agenda.",
                            "description": "¿Te gustaría darle una nueva oportunidad para completar esta etapa?\n\nGracias por seguir cada paso con atención y empatía.\n¡Seguimos contigo en la búsqueda del mejor talento!",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Abandonaron el proceso",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "Decidiste dar un paso al costado",
                            "subtitle": "Sabemos que tomar este tipo de decisiones no siempre es fácil, y respetamos completamente tu elección de no continuar en el proceso.",
                            "description": "Gracias por el interés que mostraste hasta aquí y por haber compartido un poco de tu historia con nosotros.\nOjalá podamos encontrarnos en otra oportunidad. ¡Te esperamos en futuras convocatorias!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "El candidato decidió no continuar",
                            "subtitle": "A veces, aunque el proceso fluya bien, pueden surgir razones personales o profesionales por las que un candidato prefiere no seguir adelante.",
                            "description": "Gracias por seguir cada etapa con atención y respeto.\n¡Seguimos contigo en la búsqueda del mejor talento!\n\nEn este caso, la persona decidió salir del proceso por el siguiente motivo:",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Descartados",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                    },
                ],
            },
        ],
    ),
    FLOW_TYPE.LOW_PROFILE_FLOW: PositionFlow(
        flow_type=FLOW_TYPE.LOW_PROFILE_FLOW,
        pipe_id=7676765,
        groups=[
            {
                "name": "Filtro inicial",
                "phases": [
                    {
                        "name": "Candidatos sugeridos",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {"title": "", "subtitle": "", "description": "", "button_text": ""}
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Hola! Estás en la primera fase del proceso.",
                                    "subtitle": "Activamos nuestra base de datos inteligente para identificar, de forma automática, a candidatos que se ajusten a tu vacante.",
                                    "description": "Este candidato ha sido contactado para que participe en el proceso. Te avisaremos cuando acepte.\nMientras tanto, puedes compartir el enlace de la vacante desde el botón del tablero para llegar a más personas.",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Oferta enviada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {"title": "", "subtitle": "", "description": "", "button_text": ""}
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Logramos contactar a tu candidato!",
                                    "subtitle": "Ya le enviamos la invitación para que participe en el proceso. Apenas la acepte, podrá iniciar su primer filtro y sabrás qué tan buen match hace con tu vacante.",
                                    "description": "Mientras tanto, nuestro sistema hará seguimiento para motivarlo a que avance cuanto antes.\n\nTe avisaremos tan pronto tengamos novedades. ¡Vamos por buen camino!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Filtro inicial",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Gracias por completar esta información!",
                                    "subtitle": "Estamos revisando tus respuestas con atención. Muy pronto te contaremos cuál es el siguiente paso en este proceso: una breve evaluación de afinidad cultural, que nos ayudará a conocerte mejor y asegurarnos de que esta oportunidad encaje contigo.",
                                    "description": "Queremos que vivas esta experiencia con claridad, seguridad y a tu propio ritmo.\n\nRecuerda que este es un proceso pensado también para que tú evalúes si esta oportunidad hace sentido contigo.\n\nTe avisaremos por correo si avanzas a la siguiente etapa.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡El candidato aceptó participar en el proceso!",
                                    "subtitle": "Ya analizamos su perfil con nuestro sistema de preselección automática.",
                                    "description": "Si consideras que puede avanzar, confírmalo desde el formulario de la derecha y enviaremos de inmediato su Assessment de fit cultural. Ten en cuenta en qué momento le envías la prueba puesto que el candidato tendrá 24 horas para completarla.\nEsta fue su calificación inicial:",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "name": "Fit cultural",
                "phases": [
                    {
                        "name": "Assessment fit Cultural",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Buenas noticias!",
                                    "subtitle": "Revisamos tu información y pasaste el primer filtro del proceso.",
                                    "description": "Ahora queremos invitarte a dar el siguiente paso: una evaluación de afinidad cultural. Esta etapa nos ayudará a entender mejor cómo encajas con nuestro equipo y nuestra forma de trabajar.\nEs una herramienta sencilla y rápida que te permitirá avanzar en el proceso de manera más personalizada.",
                                    "button_text": "Adjuntar prueba",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡Tu candidato ya está a un paso más de avanzar!",
                                    "subtitle": "Le avisamos que su Assessment de fit cultural está listo. Podrá iniciarlo cuando se sienta preparado, y desde ese momento tendrá una hora para responderlo.",
                                    "description": "Las preguntas se mostrarán solo al hacer clic en “Iniciar”, para que llegue con toda la concentración.\nTiene 24 horas para completarlo, si no lo hace, nuestro sistema le enviará hasta 2 recordatorios automáticos, uno por día.\nTe avisaremos apenas tengamos su resultado. ¡Vamos bien!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                    {
                        "name": "Resultado Fit Cultural",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "sections": [
                                {
                                    "title": "¡Gracias por completar la evaluación!",
                                    "subtitle": "Ya recibimos tus respuestas y en este momento las estamos revisando con atención.",
                                    "description": "Esta etapa nos ayuda a entender mejor si compartimos valores y formas de trabajar.\n\nSi encontramos que hay afinidad cultural, te estaremos contactando muy pronto para enviarte la fecha y hora de una entrevista, donde podremos conocernos mejor.\n\nTe avisaremos por correo con los próximos pasos.",
                                    "button_text": "",
                                }
                            ]
                        },
                        "interviewer_data": {
                            "sections": [
                                {
                                    "title": "¡El candidato completó el test de fit cultural!",
                                    "subtitle": "Evaluamos habilidades y valores alineados con lo que buscas, y ya puedes ver qué tan buen match hizo con tu vacante.",
                                    "description": "Si el resultado cumple con tus expectativas, este es el momento de agendar la primer entrevista.\nEn el formulario de la derecha, ingresa hasta 5 opciones de horario. Nosotros nos encargamos de notificárselo y hacer seguimiento para que elija lo más pronto posible.\n¡Vamos avanzando!",
                                    "button_text": "",
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "name": "Entrevista final",
                "phases": [
                    {
                        "name": "Entrevista final solicitada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Felicitaciones!",
                            "subtitle": "Tu evaluación técnica fue excelente y estamos muy emocionados de seguir adelante contigo.",
                            "description": "Queremos invitarte a la entrevista final del proceso, donde podremos conocernos mejor y conversar sobre lo que podría venir.\n\nPara que sea cómodo para ti, elige el día y la hora que mejor te convenga.\nTen en cuenta que esta entrevista tendrá una duración aproximada de 45 minutos.",
                            "button_text": "Agendar",
                        },
                        "interviewer_data": {
                            "title": "¡Tu candidato está a un paso de la entrevista final!",
                            "subtitle": "Ya recibió tus opciones de horario y ahora estamos esperando a que escoja el que mejor le funcione.",
                            "description": "Muy pronto podrás tener esa conversación clave que te ayudará a tomar la decisión final.\n\n¡Estamos muy cerca! Te avisaremos apenas confirme la cita.",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Entrevista final programada",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Entrevista final agendada con éxito!",
                            "subtitle": "Tu entrevista ha quedado programada para la fecha y hora que elegiste.",
                            "description": "Te enviaremos recordatorios para que estés completamente preparado y puedas llegar con tranquilidad.\n\nEstamos muy emocionados de llegar a esta etapa contigo y de conocer tus ideas finales para sumar al equipo. ¡Esta es la oportunidad para brillar y mostrar todo tu potencial!",
                            "button_text": "statement_pipefy",
                        },
                        "interviewer_data": {
                            "title": "¡Entrevista final confirmada!",
                            "subtitle": "Es el momento clave para decidir si es el match perfecto.",
                            "description": "No olvides agendar la reunión en tu calendario para no perderte nada.\n\n¡Vamos con todo en esta última etapa!\nTu candidato ya agendó la entrevista final para:",
                            "button_text": "statement_pipefy",
                        },
                    },
                    {
                        "name": "Resultado entrevista final",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Tu entrevista final ya fue!",
                            "subtitle": "La fecha y hora que habías agendado ya pasó, y esperamos que hayas tenido una buena conversación con nuestro equipo.",
                            "description": "En este momento estamos evaluando tu desempeño para tomar la decisión final.\nMuy pronto te contactaremos para compartirte el resultado y, si pasaste, los pasos a seguir.\n\n¡Gracias por haber llegado hasta aquí y por todo el interés que has demostrado en ser parte de nuestro equipo!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Terminó la entrevista final!",
                            "subtitle": "¡Qué emoción! El candidato completó la entrevista final, y ahora viene la decisión más importante.",
                            "description": "Cuéntanos en el formulario de la derecha qué quieres hacer:\n\n¿Te encantó? Márcalo como Seleccionado y cerremos el proceso.\n¿Tienes dudas? Envíalo a la lista de finalistas para decidir después.\n¿No hizo match? Puedes descartarlo fácilmente.\n\n¡Tú tienes la última palabra!",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Finalistas",
                "phases": [
                    {
                        "name": "Finalistas",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Tu entrevista final ya fue!",
                            "subtitle": "La fecha y hora que habías agendado ya pasó, y esperamos que hayas tenido una buena conversación con nuestro equipo.",
                            "description": "En este momento estamos evaluando tu desempeño para tomar la decisión final.\nMuy pronto te contactaremos para compartirte el resultado y si pasaste, los pasos a seguir.\n\n¡Gracias por haber llegado hasta aquí y por todo el interés que has demostrado en ser parte de nuestro equipo!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Tu candidato está en la fase de finalistas!",
                            "subtitle": "Aún no has tomado la decisión final… y lo entendemos, no siempre es fácil cuando hay buenos perfiles sobre la mesa.",
                            "description": "Este candidato llegó lejos por una razón: tiene algo que lo hace una gran opción.\nDesde este punto, tú decides qué sigue:\n\n¿Quieres que se quede con el puesto? Márcalo como Seleccionado.\n¿Crees que no es el indicado? También puedes descartarlo.\n\n¡Estás a solo un clic de tomar la última palabra!",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Candidato seleccionado",
                        "phase_classification": PHASE_CLASSIFICATION.INFORMATIVE,
                        "candidate_data": {
                            "title": "¡Felicitaciones!",
                            "subtitle": "Estamos muy emocionados de compartirte que has sido seleccionado para esta oportunidad.",
                            "description": "Nos encantaría que aceptes nuestra oferta y formes parte de este nuevo proyecto con nosotros.\n\nMuy pronto te contactaremos para darte todos los detalles y acompañarte en los próximos pasos. ¡Estamos ansiosos por lo que viene!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "¡Felicitaciones! escogiste un candidato",
                            "subtitle": "Te deseamos lo mejor en esta nueva etapa.",
                            "description": "¡Gran elección!\n\nPodés estar tranquilo: hiciste un gran trabajo. Esta contratación fue objetiva, sin sesgos y con toda la información que necesitabas para tomar la mejor decisión.\n\n¿Tienes otra vacante?\nNo dudes en crearla con Tici. Estamos acá para ayudarte a encontrar al mejor talento, siempre.",
                            "button_text": "",
                        },
                    },
                ],
            },
            {
                "name": "Descartados",
                "phases": [
                    {
                        "name": "Acción no completada",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "¡Hola!",
                            "subtitle": "Vimos que no pudiste completar esta etapa del proceso dentro del tiempo esperado.\nEntendemos que pueden surgir imprevistos o que los horarios disponibles no se ajustaran a tu agenda.",
                            "description": "Si aún te interesa continuar, te invitamos a escribirle directamente a la persona que ha estado acompañando tu proceso.\nElla podrá ayudarte a revisar si es posible reprogramar o encontrar una alternativa.\n\n¡Gracias por tu interés y esperamos saber de ti pronto!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "El candidato no completó esta etapa del proceso",
                            "subtitle": "En algunos casos, por diferentes motivos, un candidato no logra avanzar a tiempo.\nEsto puede deberse a temas personales, falta de disponibilidad o que los horarios propuestos no se ajustaban a su agenda.",
                            "description": "¿Te gustaría darle una nueva oportunidad para completar esta etapa?\n\nGracias por seguir cada paso con atención y empatía.\n¡Seguimos contigo en la búsqueda del mejor talento!",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Abandonaron el proceso",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                        "candidate_data": {
                            "title": "Decidiste dar un paso al costado",
                            "subtitle": "Sabemos que tomar este tipo de decisiones no siempre es fácil, y respetamos completamente tu elección de no continuar en el proceso.",
                            "description": "Gracias por el interés que mostraste hasta aquí y por haber compartido un poco de tu historia con nosotros.\nOjalá podamos encontrarnos en otra oportunidad. ¡Te esperamos en futuras convocatorias!",
                            "button_text": "",
                        },
                        "interviewer_data": {
                            "title": "El candidato decidió no continuar",
                            "subtitle": "A veces, aunque el proceso fluya bien, pueden surgir razones personales o profesionales por las que un candidato prefiere no seguir adelante.",
                            "description": "Gracias por seguir cada etapa con atención y respeto.\n¡Seguimos contigo en la búsqueda del mejor talento!\n\nEn este caso, la persona decidió salir del proceso por el siguiente motivo:",
                            "button_text": "",
                        },
                    },
                    {
                        "name": "Descartados",
                        "phase_classification": PHASE_CLASSIFICATION.CALL_TO_ACTION,
                    },
                ],
            },
        ],
    ),
}
