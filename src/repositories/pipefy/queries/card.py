CREATE_CARD = """
mutation createCard($input: CreateCardInput!) {
    createCard(input: $input) {
        card {
            id
        }
    }
}
"""
