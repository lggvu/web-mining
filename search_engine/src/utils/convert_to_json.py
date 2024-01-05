import convertText
import pandas as pd 
from tqdm import tqdm
from json import loads, dumps

df = pd.read_csv("../../db_csv/full_qa.csv")
# df=df[:10]
q_vectors = []
a_vectors = []
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
    question_vector = convertText.convert_text_to_vector(row["question"])
    answer_vector = convertText.convert_text_to_vector(row["answer"])
    q_vectors.append(question_vector)
    a_vectors.append(answer_vector)


df["question_vector"] = q_vectors
df["answer_vector"] = a_vectors

# # output_json = "/Users/lggvu/Programming/web-mining/db_csv/output.json"
# print(df)
results = df.to_json(orient="records", force_ascii=False)
parsed = loads(results)
json_result = dumps(parsed, indent=4, ensure_ascii=False)

with open("/Users/lggvu/Programming/web-mining/search_engine/public/output.json", "w") as f:
    f.write(json_result)    




