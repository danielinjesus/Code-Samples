from google.cloud import firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

db = firestore.Client(project="upstageailab5-llm-pjt")

doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada"})