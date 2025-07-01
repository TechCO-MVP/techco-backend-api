import ast
import json


def extract_event_from_error(event):
    try:
        cause = json.loads(event['Cause'])
        start_event = cause["errorMessage"].split("\'event\': ")
        end_event = start_event[1].split(", 'process_id':")
        original_event = ast.literal_eval(end_event[0])
        
        return original_event
        
    except Exception as e:
        raise Exception(f"Error al extraer el evento: {str(e)}")
