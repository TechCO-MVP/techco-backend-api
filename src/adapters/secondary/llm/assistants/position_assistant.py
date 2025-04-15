# flake8: noqa: E501

config = {
    "name": "Position Assistant - V1",
    "model": "o1",
    "instructions": """
Asistente de creación de vacante para completar la información requerida según un esquema JSON. Realiza preguntas necesarias y ofrece sugerencias.

Puedes hacerme preguntas sobre la vacante, acepto solo preguntas relacionadas. Proporcionaré sugerencias u opciones según sea necesario. Llamaré el servicio de obtener usuarios solo cuando este sea necesario. Una vez recopilada toda la información, devolveré los datos en el formato del esquema JSON definido para tu confirmación.

# JSON SCHEMA VACANTE
{'$defs': {'COUNTRY_CODE': {'enum': ['CO', 'PE', 'MX'], 'title': 'COUNTRY_CODE', 'type': 'string'}, 'LEVEL': {'enum': ['high', 'medium', 'low'], 'title': 'LEVEL', 'type': 'string', 'description': 'Indica la importancia o urgencia de la vacante'}, 'Languages': {'properties': {'name': {'title': 'Name', 'type': 'string'}, 'level': {'title': 'Level', 'type': 'string'}}, 'required': ['name', 'level'], 'title': 'Languages', 'type': 'object'}, 'PositionStakeholders': {'properties': {'user_id': {'title': 'User Id', 'type': 'string'}, 'can_edit': {'title': 'Can Edit', 'type': 'boolean'}}, 'required': ['user_id', 'can_edit'], 'title': 'PositionStakeholders', 'type': 'object', 'description': 'A list of user ids, this field is get based on a list of users'}, 'Range': {'properties': {'min': {'title': 'Min', 'type': 'string'}, 'max': {'title': 'Max', 'type': 'string'}}, 'required': ['min', 'max'], 'title': 'Range', 'type': 'object'}, 'Salary': {'properties': {'currency': {'title': 'Currency', 'type': 'string'}, 'salary': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Salary'}, 'salary_range': {'anyOf': [{'$ref': '#/$defs/Range'}, {'type': 'null'}], 'default': None}}, 'required': ['currency'], 'title': 'Salary', 'type': 'object'}, 'Skill': {'properties': {'name': {'title': 'Name', 'type': 'string'}, 'required': {'title': 'Required', 'type': 'boolean'}}, 'required': ['name', 'required'], 'title': 'Skill', 'type': 'object'}, 'WORK_MODE': {'enum': ['REMOTE', 'HYBRYD', 'ON_SITE'], 'title': 'WORK_MODE', 'type': 'string'}}, 'properties': {'business_id': {'default': '', 'title': 'Business Id', 'type': 'string'}, 'recruiter_user_id': {'title': 'Recruiter User Id', 'type': 'string', 'description': 'The recruiter id, this field is get based on a list of users'}, 'responsible_users': {'items': {'$ref': '#/$defs/PositionStakeholders'}, 'title': 'Responsible Users', 'type': 'array'}, 'role': {'title': 'Role', 'type': 'string'}, 'seniority': {'title': 'Seniority', 'type': 'string'}, 'country_code': {'$ref': '#/$defs/COUNTRY_CODE'}, 'city': {'title': 'City', 'type': 'string'}, 'description': {'title': 'Description', 'type': 'string'}, 'responsabilities': {'items': {'type': 'string'}, 'minItems': 1, 'title': 'Responsabilities', 'type': 'array'}, 'skills': {'items': {'$ref': '#/$defs/Skill'}, 'minItems': 1, 'title': 'Skills', 'type': 'array'}, 'languages': {'items': {'$ref': '#/$defs/Languages'}, 'minItems': 1, 'title': 'Languages', 'type': 'array'}, 'hiring_priority': {'$ref': '#/$defs/LEVEL'}, 'work_mode': {'$ref': '#/$defs/WORK_MODE'}, 'status': {'$ref': '#/$defs/POSITION_STATUS', 'default': 'DRAFT'}, 'benefits': {'anyOf': [{'items': {'type': 'string'}, 'type': 'array'}, {'type': 'null'}], 'title': 'Benefits'}, 'salary': {'anyOf': [{'$ref': '#/$defs/Salary'}, {'type': 'null'}], 'default': None}, 'required': ['recruiter_user_id', 'role', 'seniority', 'country_code', 'city', 'description', 'responsabilities', 'skills', 'languages', 'hiring_priority', 'work_mode'], 'title': 'PositionDTO', 'type': 'object'}

# Pasos 

1. Revisar el esquema JSON proporcionado para identificar los campos requeridos.
2. Formular preguntas dirigidas al analista para llenar los campos vacíos según el esquema JSON.
3. Sugerir opciones o brindar asistencia para completar la información, estas opciones deben estar tanto en el mensaje como en la propiedad de options.
4. A medida que recibo respuestas, actualizo los datos según el formato JSON adecuado.
5. Si el usuario solicita configurar un campo que requiera un id de usuario (recruiter_user_id o responsible_users) debes llamar la función de get_all_users
6. En cada respuesta retornaré a su vez el estado actual de la posición, incluidos los campos faltantes por completar.
7. Una vez recopilados todos los datos, proporcionaré el JSON final para confirmación.

# Formato de Respuesta

- Comunicaciones en preguntas y respuestas.
- JSON final para la confirmación del usuario.
- En caso de tener que ofrecer un listado de opciones, estos deben estar ubicados dentro del listado de opciones del JSON

# Ejemplos

**Usuario:**
"Necesito crear una vacante para desarrollador."

**Asistente:**
"¿Cuál es el nivel de experiencia requerido para el desarrollador? ¿Junior, Mid, o Senior?"

**Usuario:**
"Mid."

**Asistente:**
"¿Puedes darme más detalles sobre las responsabilidades del puesto?"

(Procesar respuesta y seguir recopilando datos según el esquema JSON.)

# Notas

- Asegúrate de que toda la información proporcionada coincida con el formato del esquema JSON.
- Solo responde a preguntas relacionadas con la creación de vacantes. 
- Ofrece sugerencias u opciones cuando sea posible para facilitar la elaboración de la vacante.
- Debes tener en cuenta de que los skills deben ser deben ser frases de no más de 2 o 3 palabras, por ejemplo: python, R, comunicación asertiva, excel, etc.
- Adicionalmente nunca debes olvidar preguntar si un skill es requerido o no
- Debes completar los datos que consideres con inferencias, es decir, si la ciudad es Lima, debes asumir que el pais es Perú
    """,
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "response_schema",
            "strict": False,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "El mensaje que se debe mostrar al usuario.",
                    },
                    "response_type": {
                        "type": "string",
                        "description": "El tipo de respuesta, puede ser selección múltiple, única selección o confirmación final.",
                        "enum": [
                            "MULTIPLE_SELECTION",
                            "UNIQUE_SELECTION",
                            "OPEN_QUESTION",
                            "CURRENT_STATUS",
                            "FINAL_CONFIRMATION",
                        ],
                    },
                    "options": {
                        "type": "array",
                        "description": "Listado de opciones que el modelo sugiere.",
                        "items": {"type": "string", "description": "Una opción específica."},
                    },
                    "position": {"$ref": "#/$defs/PositionDTO"},
                },
                "required": ["message", "response_type", "options", "position"],
                "$defs": {
                    "COUNTRY_CODE": {
                        "enum": ["CO", "PE", "MX"],
                        "title": "COUNTRY_CODE",
                        "type": "string",
                    },
                    "LEVEL": {
                        "enum": ["high", "medium", "low"],
                        "title": "LEVEL",
                        "type": "string",
                    },
                    "Languages": {
                        "type": "object",
                        "title": "Languages",
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "level": {"type": "string", "title": "Level"},
                        },
                        "required": ["name", "level"],
                    },
                    "POSITION_STATUS": {
                        "enum": ["CANCELED", "ACTIVE", "FINISHED", "INACTIVE", "DRAFT"],
                        "title": "POSITION_STATUS",
                        "type": "string",
                    },
                    "PositionStakeholders": {
                        "type": "object",
                        "title": "PositionStakeholders",
                        "properties": {
                            "user_id": {"type": "string", "title": "User Id"},
                            "can_edit": {"type": "boolean", "title": "Can Edit"},
                        },
                        "required": ["user_id", "can_edit"],
                    },
                    "Range": {
                        "type": "object",
                        "title": "Range",
                        "properties": {
                            "min": {"type": "string", "title": "Min"},
                            "max": {"type": "string", "title": "Max"},
                        },
                        "required": ["min", "max"],
                    },
                    "Salary": {
                        "type": "object",
                        "title": "Salary",
                        "properties": {
                            "currency": {"type": "string", "title": "Currency"},
                            "salary": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "title": "Salary",
                            },
                            "salary_range": {
                                "anyOf": [{"$ref": "#/$defs/Range"}, {"type": "null"}],
                                "default": None,
                            },
                        },
                        "required": ["currency"],
                    },
                    "Skill": {
                        "type": "object",
                        "title": "Skill",
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "required": {"type": "boolean", "title": "Required"},
                        },
                        "required": ["name", "required"],
                    },
                    "WORK_MODE": {
                        "enum": ["REMOTE", "HYBRYD", "ON_SITE"],
                        "title": "WORK_MODE",
                        "type": "string",
                    },
                    "PositionDTO": {
                        "type": "object",
                        "title": "PositionDTO",
                        "properties": {
                            "business_id": {
                                "type": "string",
                                "default": "",
                                "title": "Business Id",
                            },
                            "recruiter_user_id": {"type": "string", "title": "Recruiter User Id"},
                            "responsible_users": {
                                "type": "array",
                                "title": "Responsible Users",
                                "items": {"$ref": "#/$defs/PositionStakeholders"},
                            },
                            "role": {"type": "string", "title": "Role"},
                            "seniority": {"type": "string", "title": "Seniority"},
                            "country_code": {"$ref": "#/$defs/COUNTRY_CODE"},
                            "city": {"type": "string", "title": "City"},
                            "description": {"type": "string", "title": "Description"},
                            "responsabilities": {
                                "type": "array",
                                "title": "Responsabilities",
                                "minItems": 1,
                                "items": {"type": "string"},
                            },
                            "skills": {
                                "type": "array",
                                "title": "Skills",
                                "minItems": 1,
                                "items": {"$ref": "#/$defs/Skill"},
                            },
                            "languages": {
                                "type": "array",
                                "title": "Languages",
                                "minItems": 1,
                                "items": {"$ref": "#/$defs/Languages"},
                            },
                            "hiring_priority": {"$ref": "#/$defs/LEVEL"},
                            "work_mode": {"$ref": "#/$defs/WORK_MODE"},
                            "benefits": {
                                "anyOf": [
                                    {"type": "array", "items": {"type": "string"}},
                                    {"type": "null"},
                                ],
                                "title": "Benefits",
                            },
                            "salary": {
                                "anyOf": [{"$ref": "#/$defs/Salary"}, {"type": "null"}],
                                "default": None,
                            },
                        },
                        "required": [
                            "recruiter_user_id",
                            "role",
                            "seniority",
                            "country_code",
                            "city",
                            "description",
                            "responsabilities",
                            "skills",
                            "languages",
                            "hiring_priority",
                            "work_mode",
                        ],
                    },
                },
            },
        },
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_all_users",
                "description": "Retrieves a list of all users from the database",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                    "required": [],
                },
            },
        }
    ],
}
