documentSchema = {
  "properties": {
    "question": {"type": "text"},
    "question_vector": {
      "type": "dense_vector",
      "dims": 768,
      "index": True,
      "similarity": "cosine",
    },
    "answer": {"type": "text"},
    "answer_vector": {
      "type": "dense_vector",
      "dims": 768,
      "index": True,
      "similarity": "cosine",
    },
  },
}

