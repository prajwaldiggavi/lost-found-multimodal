import pandas as pd

data = [
    {"name": "AirPods Max", "desc": "Wireless headphones", "image": "images/airpods.jpg"},
    {"name": "Black Backpack", "desc": "Laptop bag black", "image": "images/bag.jpg"},
    {"name": "Casio Watch", "desc": "Digital watch waterproof", "image": "images/watch.jpg"}
]

df = pd.DataFrame(data)
df.to_csv("data/products.csv", index=False)

print("Dataset created")