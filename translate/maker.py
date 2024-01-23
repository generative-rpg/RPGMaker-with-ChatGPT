import json


def init_data(base_path, game_name):
    with open(f"{base_path}/{game_name}/data/Skills.json", mode="r", encoding="utf8") as f:
        skills = json.load(f)
    with open(f"{base_path}/{game_name}/data/Items.json", mode="r", encoding="utf8") as f:
        items = json.load(f)
    with open(f"{base_path}/{game_name}/data/Weapons.json", mode="r", encoding="utf8") as f:
        weapons = json.load(f)
    with open(f"{base_path}/{game_name}/data/Armors.json", mode="r", encoding="utf8") as f:
        armors = json.load(f)

    with open(f"{base_path}/{game_name}/data/Actors.json", mode="r", encoding="utf8") as f:
        actors = json.load(f)
    with open(f"{base_path}/{game_name}/data/Classes.json", mode="r", encoding="utf8") as f:
        classes = json.load(f)

    with open(f"{base_path}/{game_name}/data/Enemies.json", mode="r", encoding="utf8") as f:
        enemies = json.load(f)
    with open(f"{base_path}/{game_name}/data/Troops.json", mode="r", encoding="utf8") as f:
        troops = json.load(f)

    with open(f"{base_path}/{game_name}/data/Map001.json", mode="r", encoding="utf8") as f:
        map001 = json.load(f)

    with open(f"{base_path}/{game_name}/data/Animations.json", mode="r", encoding="utf8") as f:
        animations = json.load(f)
    with open(f"{base_path}/{game_name}/data/States.json", mode="r", encoding="utf8") as f:
        states = json.load(f)
    with open(f"{base_path}/{game_name}/data/System.json", mode="r", encoding="utf8") as f:
        system = json.load(f)

    # RPGMZに元からあるもの
    data = {
        "skills": skills,
        "items": items,
        "weapons": weapons,
        "armors": armors,
        "actors": actors,
        "classes": classes,
        "enemies": enemies,
        "troops": troops,
        "map001": map001,
        "animations": animations,
        "states": states,
        "system": system,
    }

    with open("./members.json", mode="r", encoding="utf8") as f:
        members = json.load(f)

    with open("./skills.json", mode="r", encoding="utf8") as f:
        skills = json.load(f)

    gpt = {"members": members, "skills": skills}
    return data, gpt


def get_animation_id(data, animation_name):
    try:
        animation_id = [
            animation["id"] for animation in data["animations"][1:] if animation["effectName"] == animation_name
        ][0]
    except Exception as e:
        print(f"not found animation_name {animation_name}")
        raise e
    return animation_id


def get_element_id(data, element_name):
    if element_name == "なし":
        element_id = 0
    else:
        try:
            element_id = [i for i, element in enumerate(data["system"]["elements"]) if element == element_name][0]
        except Exception as e:
            print(f"not found element_name {element_name}")
            raise e
    return element_id


def get_effect_dict(data, effect_name, rate=0):
    # 状態異常回復
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
        print(f"not found effect_name {effect_name}")
        raise e
    return [
        {"code": 21, "dataId": id, "value1": rate / 100, "value2": 0},
    ]
