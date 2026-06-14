import json
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    avg_scores = {}
    for student in data["students"]:        
        name = student["name"]
        scores = student["scores"]          
        avg_scores[name] = sum(scores) / len(scores)     
        sorted_avg_scores = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
    for name, avg in sorted_avg_scores:
        print(f"{name}: {avg:.2f}")