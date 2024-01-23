import json

from maker import get_animation_id, get_element_id, init_data

BASE_PATH = "<YOUR RMMZ PATH ex. C:/work/RMMZ>"
GAME_NAME = "<YOUR RPG FOLDER NAME ex. EternalQuest>"
data, gpt = init_data(BASE_PATH, GAME_NAME)

members = gpt["members"]
skills = gpt["skills"]


def get_effect_dict(effect_name, rate=0):
    # 状態伊集回復
    if effect_name == "状態異常回復":
        return [
            {"code": 22, "dataId": 4, "value1": 1, "value2": 0},
            {"code": 22, "dataId": 5, "value1": 1, "value2": 0},
            {"code": 22, "dataId": 8, "value1": 1, "value2": 0},
            {"code": 22, "dataId": 6, "value1": 1, "value2": 0},
            {"code": 22, "dataId": 7, "value1": 1, "value2": 0},
            {"code": 22, "dataId": 10, "value1": 1, "value2": 0},
            {"code": 22, "dataId": 12, "value1": 1, "value2": 0},
            {"code": 22, "dataId": 13, "value1": 1, "value2": 0},
        ]
    elif effect_name == "戦闘不能回復":
        return [[{"code": 22, "dataId": 1, "value1": 1, "value2": 0}]]
    # アップ・ダウンの判定
    status = {"攻撃": 2, "防御": 3, "魔攻": 4, "魔防": 5, "素早さ": 6, "運": 7}
    updown = {"アップ": 31, "ダウン": 32}
    for s in status.keys():
        for b in ["", "大"]:
            for ud in updown.keys():
                if effect_name == f"{s}{b}{ud}":
                    if b == "":
                        return [{"code": updown[ud], "dataId": status[s], "value1": 5, "value2": 0}]
                    else:
                        return [
                            {"code": updown[ud], "dataId": status[s], "value1": 5, "value2": 0},
                            {"code": updown[ud], "dataId": status[s], "value1": 5, "value2": 0},
                        ]
    # ステートの取得
    try:
        id = [s["id"] for s in data["states"][1:] if s["name"] == effect_name][0]
    except Exception as e:
        print(f"error {effect_name}")
        raise e
    return [
        {"code": 21, "dataId": id, "value1": rate / 100, "value2": 0},
    ]


for skill_info in skills:
    effects = []
    # animationId
    animation_id = get_animation_id(data, skill_info["animation"])
    # elementId
    element_id = get_element_id(data, skill_info["element"])
    # variance
    variance = skill_info["variance"]
    # description
    description = skill_info["description"]
    # effects
    for effect_name in skill_info["target_add_state"]:
        effects.extend(get_effect_dict(effect_name, skill_info["target_add_state_rate"]))
    # name
    name = skill_info["name"]
    # tp
    tp = skill_info["tp"]
    # formula
    formula = skill_info["formula"].replace("user.", "a.").replace("target.", "b.")
    # type
    effect_type = skill_info["effect_type"]
    if effect_type == "全回復":
        effects.append({"code": 11, "dataId": 0, "value1": 1, "value2": 0})
        type = 0
    elif effect_type == "TP回復":
        effects.append({"code": 11, "dataId": 0, "value1": 20, "value2": 0})
        type = 0
    elif effect_type == "TPダメージ":
        formula = "b.gainTp(-20)"
    elif effect_type == "":
        type = 0
    else:
        type_dict = {"なし": 0, "HPダメージ": 1, "HP回復": 3, "MP回復": 4, "HP吸収": 5, "MP吸収": 6}
        type = type_dict[skill_info["effect_type"]]
    # hitType
    if skill_info["type"] == "物理":
        hit_type = 1
    else:
        hit_type = 0
    # iconIndex
    icon_index = skill_info["icon_index"]
    # message1
    if skill_info["type"] == "物理":
        message1 = "%1は%2を放った！"
    elif skill_info["type"] == "魔法":
        message1 = "%1は%2を唱えた！"
    else:
        message1 = "%1は%2を使った！"
    # note
    note = json.dumps(skill_info, indent=2, ensure_ascii=False)
    # repeats
    repeats = skill_info["repeats"]
    # scope
    scope_dict = {"自分": 11, "敵単体": 1, "敵全体": 2, "味方単体": 7, "味方全体": 8}
    scope = scope_dict[skill_info["scope"]]
    # tpCost
    tp_cost = skill_info["tp"]

    # 追加
    data["skills"].append(
        {
            "id": len(data["skills"]),
            "animationId": animation_id,
            "damage": {
                "critical": False,
                "elementId": element_id,
                "formula": formula,
                "type": type,
                "variance": variance,
            },
            "description": description,
            "effects": effects.copy(),
            "hitType": hit_type,
            "iconIndex": icon_index,
            "message1": message1,
            "message2": "",
            "mpCost": 0,
            "name": name,
            "note": note,
            "occasion": 1,
            "repeats": repeats,
            "requiredWtypeId1": 0,
            "requiredWtypeId2": 0,
            "scope": scope,
            "speed": 0,
            "stypeId": 3,
            "successRate": 100,
            "tpCost": tp_cost,
            "tpGain": 0,
            "messageType": 1,
        }
    )

with open(f"{BASE_PATH}/{GAME_NAME}/data/Skills.json", mode="w", encoding="utf8") as f:
    json.dump(data["skills"], f, indent=2, ensure_ascii=False)
