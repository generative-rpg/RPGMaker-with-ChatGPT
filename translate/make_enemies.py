import json

from maker import BASE_PATH, GAME_NAME, get_element_id, get_skills_id, init_data

# 属性による弱点関係の定義(ゲームにより微修正)
elements = [
    {"name": "炎", "weak": "氷"},
    {"name": "氷", "weak": "炎"},
    {"name": "雷", "weak": "水"},
    {"name": "水", "weak": "雷"},
    {"name": "風", "weak": "土"},
    {"name": "土", "weak": "風"},
    {"name": "光", "weak": "闇"},
    {"name": "闇", "weak": "光"},
]


def make_enemies():
    data, gpt = init_data()
    enemies = gpt["enemies"]
    enemy_skills = gpt["enemy_skills"]

    for i, enemy_info in enumerate(enemies):
        enemy_name = enemy_info["name"]
        # traits
        traits = []
        # element
        element_name = enemy_info["element"]
        element_id = get_element_id(data, element_name)
        regist_trait = {"code": 11, "dataId": element_id, "value": 0.5}
        weak_element_name = [e["weak"] for e in elements if e["name"] == element_name][0]
        weak_element_id = get_element_id(data, weak_element_name)
        weak_trait = {"code": 11, "dataId": weak_element_id, "value": 2}
        traits.append(regist_trait)
        traits.append(weak_trait)
        # actions(スキルの発動を定義)
        actions = [{"conditionParam1": 0, "conditionParam2": 0, "conditionType": 0, "rating": 5, "skillId": 1}]
        for skill_name in [skill["name"] for skill in enemy_skills if skill["enemy"] == enemy_name]:
            skill_id = get_skills_id(data, skill_name)
            actions.append(
                {"conditionParam1": 0, "conditionParam2": 0, "conditionType": 0, "rating": 4, "skillId": skill_id}
            )
        # battler_name(enemy001, enemy002で順番に仮決めhah)
        battler_name = f"enemy{str(i+1).zfill(3)}"

        # 敵追加
        data["enemies"].append(
            {
                "id": len(data["enemies"]),
                "actions": actions,
                "battlerHue": 0,
                "battlerName": battler_name,
                "dropItems": [],
                "exp": 0,
                "traits": traits,
                "gold": 0,
                "name": enemy_name,
                "note": "",
                "params": [
                    enemy_info["hp"] if "hp" in enemy_info else 0,
                    enemy_info["mp"] if "mp" in enemy_info else 0,
                    enemy_info["atk"] if "atk" in enemy_info else 0,
                    enemy_info["def"] if "def" in enemy_info else 0,
                    enemy_info["mat"] if "mat" in enemy_info else 0,
                    enemy_info["mdf"] if "mdf" in enemy_info else 0,
                    enemy_info["agi"] if "agi" in enemy_info else 0,
                    enemy_info["luk"] if "luk" in enemy_info else 0,
                ],
            }
        )

    with open(f"{BASE_PATH}/{GAME_NAME}/data/Enemies.json", mode="w", encoding="utf8") as f:
        json.dump(data["enemies"], f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    make_enemies()
