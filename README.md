# 🔍 Lost & Found AI

A **production-style multi-modal semantic search system** for Lost & Found items using AI.

This project solves the real-world problem of poor item tracking ("black bag", "unknown item") by combining:

* 🧠 Text understanding (NLP)
* 🖼️ Image understanding (CLIP)
* ⚡ Fast similarity search (FAISS)
* 💡 Explainable AI results

---

## 🚨 Problem Statement

Traditional Lost & Found systems fail because:

* Item descriptions are vague and inconsistent
* Images are not searchable
* Matching is manual and keyword-based
* Items remain unclaimed or get lost

👉 This system fixes it using **AI-powered search**

Users can search using:

* Text only
* Image only
* Text + Image together

---

## 🚀 Approach

This project is built as a complete pipeline:

### 📦 Data Layer

* Store items (name, description, image) in CSV
* Maintain local image dataset

### 🧠 Embeddings

* Text → Sentence Transformers
* Image → CLIP model
* Convert everything into vectors

### ⚡ Search Engine

* FAISS used for fast similarity search
* Finds nearest matching items

### 🔍 Retrieval

* Text search → semantic similarity
* Image search → visual similarity
* Multi-modal → combined ranking

### 💡 Explainability

* Each result includes explanation
* Based on semantic + visual similarity

### 🌐 UI

* Flask backend
* Modern responsive frontend

---

## 🏗️ Architecture

User (Web UI)
↓
Flask App
↓
Search Engine
├── Text Encoder (Sentence Transformers)
├── Image Encoder (CLIP)
├── FAISS Index
└── Ranking + Explanation

---

## 🤖 Why CLIP?

CLIP enables:

* Text ↔ Image matching
* Image ↔ Image retrieval
* Multi-modal understanding

👉 Both text & images exist in the **same vector space**

---

## ⚙️ Retrieval Strategy

### 🔹 Text Query

* Encode using Sentence Transformer
* Search FAISS index

### 🔹 Image Query

* Encode using CLIP
* Search FAISS index

### 🔹 Multi-Modal Query

* Combine text + image scores
* Rank results

---

## 📊 Confidence Score

We convert similarity into readable score:

```
confidence = 1 / (1 + distance)
```

👉 Higher score = better match

---

## 📁 Project Structure

```
lost-found-multimodal/
│
├── app.py
├── search.py
├── embedder.py
├── explain.py
│
├── data/
│   └── products.csv
│
├── images/
│   ├── airpods.jpg
│   ├── bag.jpg
│   └── watch.jpg
│
├── templates/
│   └── index.html
│
├── embeddings/
```

---

## ⚙️ Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run Project

```
python embedder.py
python app.py
```

Open in browser:
👉 http://127.0.0.1:5000

---

## ✨ Features

* ✅ Multi-modal search (text + image)
* ✅ Semantic understanding
* ✅ Visual similarity matching
* ✅ Confidence scoring
* ✅ AI explanation
* ✅ Modern UI

---

## 📈 Performance

Improve accuracy by:

* Increasing dataset size
* Using better CLIP models

Improve speed by:

* Reducing search results
* Optimizing embeddings

---

## 🛠️ Troubleshooting

Images not showing → Check `/images` folder
Search not working → Run `embedder.py` again
Low accuracy → Improve dataset quality

---

## 📌 Current Status

✔ Multi-modal search implemented
✔ CLIP + NLP embeddings
✔ FAISS indexing
✔ Flask UI integration

👉 Fully working demo system

---

## 🎤 Viva Answer

> This project is a multi-modal semantic search system using CLIP for image-text understanding and FAISS for efficient similarity retrieval.

---

## 👨‍💻 Author

**Prajwal Diggavi** 🚀
