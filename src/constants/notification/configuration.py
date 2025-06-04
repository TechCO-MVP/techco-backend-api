from src.domain.notification import PHASE_TYPE

mapping_phase_name = {
    "Candidatos sugeridos": PHASE_TYPE.INFORMATIVE.value,
    "Oferta enviada": PHASE_TYPE.INFORMATIVE.value,
    "Filtro inicial": PHASE_TYPE.ACTION_CALL.value,
    "Primera entrevista solicitada": PHASE_TYPE.INFORMATIVE.value,
    "Primera entrevista programada": PHASE_TYPE.INFORMATIVE.value,
    "Resultado primer entrevista": PHASE_TYPE.ACTION_CALL.value,
    "Assessment fit Cultural": PHASE_TYPE.INFORMATIVE.value,
    "Resultado Fit Cultural": PHASE_TYPE.ACTION_CALL.value,
    "Assessment técnico": PHASE_TYPE.INFORMATIVE.value,
    "Resultado Assessment técnico": PHASE_TYPE.ACTION_CALL.value,
    "Entrevista final solicitada": PHASE_TYPE.INFORMATIVE.value,
    "Entrevista final programada": PHASE_TYPE.INFORMATIVE.value,
    "Resultado entrevista final": PHASE_TYPE.ACTION_CALL.value,
    "Finalistas": PHASE_TYPE.ACTION_CALL.value,
    "Candidato seleccionado": PHASE_TYPE.INFORMATIVE.value,
    "Descartados": PHASE_TYPE.INFORMATIVE.value,
}
