CLONE_PIPES = """
mutation ClonePipes($input: ClonePipesInput!) {
    clonePipes(input: $input) {
        pipes {
            id
        }
    }
}
"""

GET_PIPE = """
query GetPipe($id: ID!) {
    pipe(id: $id) {
        id
        name
        description
        phases {
            id
            name
            cards {
                totalCount
            }
        }
        webhooks {
            id
        }
    }
}
"""
