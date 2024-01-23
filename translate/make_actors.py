import json
import random

import numpy as np
from maker import init_data

BASE_PATH = "<YOUR RMMZ PATH ex. C:/work/RMMZ>"
GAME_NAME = "<YOUR RPG FOLDER NAME ex. EternalQuest>"
data, gpt = init_data(BASE_PATH, GAME_NAME)

members = gpt["members"]
skills = gpt["skills"]

for num, actor_info in enumerate(members):
    class_ = actor_info["class"]
    # learnings
    learnings = []
    class_skills = [s["name"] for s in skills if s["class"] == class_]
    for skill_name in class_skills:
        skill_id = [skill["id"] for skill in data["skills"][1:] if skill_name in skill["name"]][0]
        learnings.append({"level": 1, "skillId": skill_id, "note": ""})

        # traits
        traits = [
            {"code": 23, "dataId": 0, "value": 1},
            {"code": 22, "dataId": 0, "value": 0.95},
            {"code": 22, "dataId": 1, "value": 0.05},
            {"code": 22, "dataId": 2, "value": 0.04},
            {"code": 41, "dataId": 3, "value": 1},  # スキルタイプ
        ]
        # params
        params = [
            [actor_info["hp"]],
            [0],
            [actor_info["atk"]],
            [actor_info["def"]],
            [actor_info["mat"]],
            [actor_info["mdf"]],
            [actor_info["agi"]],
            [actor_info["luk"]],
        ]
        for i, param_name in enumerate(["hp", "mp", "atk", "def", "mat", "mdf", "agi", "luk"]):
            param_100 = int(actor_info[param_name] * 8 * random.randrange(80, 120) / 100) if param_name != "mp" else 0
            a, b, c = np.polyfit([0, 99], [params[i][0], param_100], 2)
            for level in range(1, 100):
                params[i].append(int(a * (level + 1) ** 2 + (b * level + 1) + c))

    # 追加
    if len([c for c in data["classes"][1:] if c["name"] == actor_info["class"]]) == 0:
        data["classes"].append(
            {
                "id": len(data["classes"]),
                "expParams": [30, 20, 30, 30],
                "traits": traits,
                "learnings": learnings,
                "name": actor_info["class"],
                "note": "",
                "params": params,
            }
        )
    class_id = [c for c in data["classes"][1:] if c["name"] == actor_info["class"]][0]["id"]
    if len([a for a in data["actors"][1:] if a["name"] == actor_info["name"]]) == 0:
        data["actors"].append(
            {
                "id": len(data["actors"]),
                "battlerName": "",
                "characterIndex": 0,
                "characterName": "",
                "classId": class_id,
                "equips": [0, 0, 0, 0, 0],
                "faceIndex": (num % 8),
                "faceName": f"grid{int(num/8) + 1}",
                "traits": traits,
                "initialLevel": 1,
                "maxLevel": 99,
                "name": actor_info["name"],
                "nickname": "",
                "note": "",
                "profile": "",
            }
        )


with open(f"{BASE_PATH}/{GAME_NAME}/data/Classes_new.json", mode="w", encoding="utf8") as f:
    json.dump(data["classes"], f, indent=2, ensure_ascii=False)
with open(f"{BASE_PATH}/{GAME_NAME}/data/Actors_new.json", mode="w", encoding="utf8") as f:
    json.dump(data["actors"], f, indent=2, ensure_ascii=False)
