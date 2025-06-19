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


UPDATE_CARD_FIELD = """
mutation updateCardField($input: UpdateCardFieldInput!) {
    updateCardField(input: $input) {
        card {
            id
            fields {
                field {
                    id
                    label
                }
                value
            }
        }
    }
}
"""
