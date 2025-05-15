from src.domain.notification import PHASE_TYPE

mapping_phase_name = {
    "Candidatos sugeridos": PHASE_TYPE.INFORMATIVE.value,
    "Oferta enviada": PHASE_TYPE.INFORMATIVE.value,
    "Filtro inicial": PHASE_TYPE.ACTION_CALL.value,
    "Primera entrevista solicitada": PHASE_TYPE.INFORMATIVE.value,
    "Primera entrevista programada": PHASE_TYPE.INFORMATIVE.value,
    "Feedback primera entrevista": PHASE_TYPE.ACTION_CALL.value,
    "Resultado primer entrevista": PHASE_TYPE.ACTION_CALL.value,
    "Test de fit Cultural": PHASE_TYPE.INFORMATIVE.value,
    "Resultado test Fit Cultural": PHASE_TYPE.ACTION_CALL.value,
    "Entrevista final solicitada": PHASE_TYPE.INFORMATIVE.value,
    "Entrevista final programada": PHASE_TYPE.INFORMATIVE.value,
    "Feedback entrevista final ": PHASE_TYPE.ACTION_CALL.value,
    "Resultado entrevista final": PHASE_TYPE.ACTION_CALL.value,
    "Finalistas": PHASE_TYPE.ACTION_CALL.value,
    "Candidato seleccionado": PHASE_TYPE.INFORMATIVE.value,
}
