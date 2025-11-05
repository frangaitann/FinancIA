import faiss, json
from sentence_transformers import SentenceTransformer






# Read history with ONLY required data
def history_reader(user_inp):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    try:
        with open("history.csv", "r", encoding="utf-8") as f:
            data = f.read().splitlines()
    except FileNotFoundError:
        data = []

    if not data:
        return 

    vectors = model.encode(data, convert_to_numpy=True)

    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)

    vec_dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(vec_dimension)
    index.add(vectors.astype('float32'))

    prompt_vector = model.encode([user_inp]).astype('float32')
    D, I = index.search(prompt_vector, k=min(10, len(data)))

    return [data[idx] for idx in I[0]]






# Embedded transactions
def embedded_transact(user_inp, iter=10):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    json_lines = []
    with open("trans.csv", "r", encoding="utf-8") as f:
        for i in f:
            json_lines.append(json.loads(i.strip()))     

    # THIS FUNCTION IS NOT FINISHED, JUST LET IT BE HERE FOR REMEMBERING WHAT TO DO