import pandas as pd
import pickle
import faiss
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

# 🔹 Load Dataset
print("Reading dataset...")
df = pd.read_csv("data/products.csv")

texts = (df["name"] + " " + df["desc"]).tolist()
image_paths = df["image"].tolist()

# 🔹 TEXT EMBEDDINGS
print("Creating text embeddings...")
text_embeddings = text_model.encode(texts)

# 🔹 IMAGE EMBEDDINGS
print("Creating image embeddings...")
image_embeddings = []

for path in image_paths:
    try:
        if os.path.exists(path):
            image = Image.open(path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")
            outputs = clip_model.get_image_features(**inputs)
            emb = outputs.detach().numpy()[0]
            image_embeddings.append(emb)
        else:
            print(f"Image not found: {path}")
            image_embeddings.append(np.zeros(512))
    except Exception as e:
        print(f"Error processing {path}: {e}")
        image_embeddings.append(np.zeros(512))

# 🔹 SAVE DATA (IMPORTANT CHANGE HERE)
print("Saving embeddings...")

# Save text + image paths together
with open("embeddings/text.pkl", "wb") as f:
    pickle.dump((texts, image_paths, text_embeddings), f)

with open("embeddings/image.pkl", "wb") as f:
    pickle.dump(image_embeddings, f)

# 🔹 FAISS INDEX (TEXT)
print("Creating FAISS index (text)...")
t_index = faiss.IndexFlatL2(len(text_embeddings[0]))
t_index.add(np.array(text_embeddings))
faiss.write_index(t_index, "embeddings/faiss_text.index")

# 🔹 FAISS INDEX (IMAGE)
print("Creating FAISS index (image)...")
i_index = faiss.IndexFlatL2(len(image_embeddings[0]))
i_index.add(np.array(image_embeddings))
faiss.write_index(i_index, "embeddings/faiss_image.index")

print("✅ Embeddings + FAISS indexes created successfully!")