GET_PHASE_NAME = """
    query getPhaseName($id: ID!) {
        phase(id: $id) {
            name
        }
    }
"""