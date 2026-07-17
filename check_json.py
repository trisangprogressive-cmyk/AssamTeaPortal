import json

with open("data/verified_display_database.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total records:", len(data))

print("\nFirst record:\n")
print(data[0])