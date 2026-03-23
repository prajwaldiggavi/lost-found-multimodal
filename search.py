import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import os

# 🔹 Load Models
print("Loading models...")
text_model = SentenceTransformer('all-MiniLM-L6-v2')
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 🔹 Load Data (UPDATED FORMAT)
print("Loading embeddings...")
texts, image_paths, text_embeddings = pickle.load(open("embeddings/text.pkl", "rb"))
image_embeddings = pickle.load(open("embeddings/image.pkl", "rb"))

# 🔹 Load FAISS Index
t_index = faiss.read_index("embeddings/faiss_text.index")
i_index = faiss.read_index("embeddings/faiss_image.index")


# 🔹 TEXT SEARCH
def search_text(query):
    q_emb = text_model.encode([query])
    D, I = t_index.search(np.array(q_emb), k=5)
    return I[0], D[0]


# 🔹 IMAGE SEARCH
def search_image(img_path):
    try:
        if os.path.exists(img_path):
            image = Image.open(img_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")
            emb = clip_model.get_image_features(**inputs).detach().numpy()

            D, I = i_index.search(emb, k=5)
            return I[0], D[0]
        else:
            print("Image not found:", img_path)
            return [], []
    except Exception as e:
        print("Image error:", e)
        return [], []


# 🔹 MULTI-MODAL SEARCH
def multimodal_search(query=None, image_path=None):
    results = {}

    # TEXT SEARCH
    if query:
        idxs, scores = search_text(query)
        for i, idx in enumerate(idxs):
            results[idx] = results.get(idx, 0) + (1 / (1 + scores[i]))

    # IMAGE SEARCH
    if image_path:
        idxs, scores = search_image(image_path)
        for i, idx in enumerate(idxs):
            results[idx] = results.get(idx, 0) + (1 / (1 + scores[i]))

    # SORT RESULTS
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # 🔹 FINAL OUTPUT (WITH IMAGE + TEXT)
    output = []
    for idx, score in sorted_results[:5]:
        output.append({
            "item": texts[idx],
            "image": image_paths[idx],
            "score": float(score)
        })

    return output