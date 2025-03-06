CREATE_WEBHOOK = """
mutation createWebhook($input: CreateWebhookInput!) {
  createWebhook(input: $input) {
    webhook {
      id
    }
  }
}
"""

DELETE_WEBHOOK = """
mutation deleteWebhook($input: DeleteWebhookInput!) {
  deleteWebhook(input: $input) {
    success
  }
}
"""
