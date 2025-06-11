import ast
import json
import re


event = {
        "Error": "Exception",
        "Cause": "{\"errorMessage\": \"{'message': 'Failed to get status snapshoot: 200 - {\\\"id\\\":\\\"snap_mbgsy3ny1ieqjnr1wc\\\",\\\"created\\\":\\\"2025-06-03T17:38:14.926Z\\\",\\\"status\\\":\\\"scheduled\\\",\\\"dataset_id\\\":\\\"gd_l1viktl72bvl7bjuj0\\\",\\\"customer_id\\\":\\\"hl_17516f51\\\",\\\"cost\\\":0,\\\"initiation_type\\\":\\\"filter_api_snapshot\\\"}', 'snapshoot_id': 'snap_mbgsy3ny1ieqjnr1wc', 'event': {'_id': '683f32e5c0060cd2f216f591', 'created_at': '2025-06-03T17:37:41.303166', 'updated_at': '2025-06-03T17:37:41.303169', 'deleted_at': None, 'status': 'in_progress', 'type': 'profiles_search', 'execution_arn': None, 'user_id': '67afdebf61e9a6c463e46c9c', 'pipe_id': None, 'position_id': '683f32e5c0060cd2f216f590', 'business_id': '679077da2d6626a2b007f8f9', 'process_filters': {'role': 'Ingeniero de Alimentos', 'seniority': 'Senior', 'country_code': 'PE', 'city': 'Cusco', 'description': '\\u00bfEres Ingeniero de Alimentos y te apasiona transformar procesos en resultados de alto impacto? En esta posici\\u00f3n tendr\\u00e1s la oportunidad de liderar mejoras clave en la producci\\u00f3n, asegurar la calidad de productos que llegan a millones de personas y participar activamente en el desarrollo de nuevas soluciones alimentarias. Formar\\u00e1s parte de un equipo t\\u00e9cnico comprometido, con poder de decisi\\u00f3n real y espacio para proponer, innovar y crecer. Si buscas un reto con prop\\u00f3sito en una empresa s\\u00f3lida y con visi\\u00f3n de futuro, este rol es para ti.', 'responsabilities': ['Supervisar y optimizar los procesos de producci\\u00f3n de alimentos, garantizando el cumplimiento de normas de calidad e inocuidad.', 'Desarrollar nuevos productos alimenticios alineados a tendencias del mercado y est\\u00e1ndares nutricionales.', 'Implementar y dar seguimiento a sistemas de gesti\\u00f3n de calidad (HACCP, ISO 22000, BPM).', 'Realizar auditor\\u00edas internas y coordinar con equipos de aseguramiento de calidad y operaciones.', 'Colaborar con \\u00e1reas de I+D, compras y log\\u00edstica para mejorar formulaciones y eficiencia en la cadena productiva.'], 'skills': [{'name': 'Normativas inocuidad', 'required': False}, {'name': 'Dise\\u00f1o de procesos', 'required': False}, {'name': 'An\\u00e1lisis de datos', 'required': False}, {'name': 'Liderazgo de equipos', 'required': False}, {'name': 'Mejora continua', 'required': False}], 'business_id': '679077da2d6626a2b007f8f9', 'position_id': '683f32e5c0060cd2f216f590', 'snapshot_id': 'snap_mbgsy3ny1ieqjnr1wc', 'url_profiles': []}, 'profiles': []}, 'process_id': '683f32e5c0060cd2f216f591'}\", \"errorType\": \"Exception\", \"requestId\": \"36f078f7-9628-4436-beb0-c5e83a26f675\", \"stackTrace\": [\"  File \\\"/var/task/aws_lambda_powertools/logging/logger.py\\\", line 545, in decorate\\n    return lambda_handler(event, context, *args, **kwargs)\\n\", \"  File \\\"/var/task/src/adapters/primary/profile/query_brightdata/check_snaphot_status.py\\\", line 84, in lambda_handler\\n    raise e\\n\", \"  File \\\"/var/task/src/adapters/primary/profile/query_brightdata/check_snaphot_status.py\\\", line 76, in lambda_handler\\n    validate_status_profile_query_use_case(profile_process_entity)\\n\", \"  File \\\"/var/task/src/use_cases/profile/validate_status_profile_query.py\\\", line 23, in validate_status_profile_query_use_case\\n    response = scraping_profile_filter_process_repository.get_status(\\n\", \"  File \\\"/var/task/src/repositories/scraping/scraping_profile_filter_process.py\\\", line 30, in get_status\\n    return self._adapter.get_status(entity)\\n\", \"  File \\\"/var/task/src/adapters/secondary/scraping/brigthdata_adapter.py\\\", line 161, in get_status\\n    raise Exception(error)\\n\"]}"
    }

def clean_string_regex(string_dict):
    # Elimina la coma y el process_id al final
    cleaned = re.sub(r',\s*\'process_id\':\s*\'[^\']+\'\s*}$', '}', string_dict)
    return cleaned

# Método 2: Usando manipulación de strings
def clean_string_manual(string_dict):
    # Encuentra la última llave de cierre
    last_brace = string_dict.rfind('}')
    # Toma todo hasta la última llave de cierre
    cleaned = string_dict[:last_brace + 1]
    return cleaned

def handler(event, context):
    try:
        # El evento está dentro de Cause que es un string JSON
        cause = json.loads(event['Cause'])
        print("-------------CAUSE-------------------")
        print(cause)
        # Dentro de errorMessage hay otro string JSON
        start_event = cause["errorMessage"].split("\'event\': ")
        cleaned_string = clean_string_manual(start_event[1])
        # o
        # cleaned_string = clean_string_manual(string_dict)

        # Convertir a diccionario
        original_event = ast.literal_eval(cleaned_string)
        # error_message = json.loads(error_message_str)
        # print("-------------ERROR MESSAGE-------------------")
        # print(error_message)
        # # Finalmente, el evento original está en la clave 'event'
        # original_event = error_message['event']
        # print("-------------- ORIGINAL EVENT ------------------")
        # print(original_event)
        # Ahora puedes usar original_event que contiene el evento limpio
        return original_event
        
    except Exception as e:
        # Manejo de errores si algo falla en la extracción
        raise Exception(f"Error al extraer el evento: {str(e)}")
    
print(handler(event, None))