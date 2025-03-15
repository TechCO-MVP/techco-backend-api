CREATE_CARD = """
mutation createCard($input: CreateCardInput!) {
    createCard(input: $input) {
        card {
            id
            current_phase {
                id
                name
            }
        }
    }
}
"""

GET_CARD = """
query getCard($id: ID!) {
    card(id: $id) {
        id
        current_phase {
            id
        }
    }
}
"""
