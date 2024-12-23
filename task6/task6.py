import argparse
import json
import numpy as np
import os
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def task(temp_mf_json, heat_mf_json, rules_json, current_temp):
    temp_mf_data = json.loads(temp_mf_json)
    heat_mf_data = json.loads(heat_mf_json)
    rule_data = json.loads(rules_json)

    temp_range = [float('inf'), float('-inf')]
    heat_range = [float('inf'), float('-inf')]

    for mf in temp_mf_data["температура"]:
        for point in mf["points"]:
            temp_range[0] = min(temp_range[0], point[0])
            temp_range[1] = max(temp_range[1], point[0])

    for mf in heat_mf_data["уровень нагрева"]:
        for point in mf["points"]:
            heat_range[0] = min(heat_range[0], point[0])
            heat_range[1] = max(heat_range[1], point[0])

    temperature = ctrl.Antecedent(np.arange(temp_range[0], temp_range[1], 1), 'temperature')
    heating = ctrl.Consequent(np.arange(heat_range[0], heat_range[1], 0.1), 'heating')

    for mf in temp_mf_data["температура"]:
        points = np.array(mf["points"])
        temperature[mf["id"]] = fuzz.trapmf(temperature.universe, points[:, 0])

    for mf in heat_mf_data["уровень нагрева"]:
        points = np.array(mf["points"])
        heating[mf["id"]] = fuzz.trapmf(heating.universe, points[:, 0])

    activated_rules = []
    for rule in rule_data:
        if rule[0] in temperature.terms and rule[1] in heating.terms:
            membership = fuzz.interp_membership(temperature.universe, temperature[rule[0]].mf, current_temp)
            if membership > 0:
                activated_rules.append((membership, rule[1]))

    aggregated_mf = np.zeros_like(heating.universe)
    for level, term in activated_rules:
        aggregated_mf = np.maximum(aggregated_mf, np.minimum(level, heating[term].mf))

    if np.any(aggregated_mf):
        return fuzz.defuzz(heating.universe, aggregated_mf, 'centroid')
    else:
        raise ValueError("Нет активных выходных значений.")


def load_json_data(source, default):
    try:
        if os.path.isfile(source):
            with open(source, 'r') as file:
                return json.load(file)
        return json.loads(source)
    except Exception:
        return default


if __name__ == "__main__":
    default_temp_mf = {
        "температура": [
            {"id": "холодно", "points": [[0, 0], [5, 1], [10, 1], [12, 0]]},
            {"id": "комфортно", "points": [[18, 0], [22, 1], [24, 1], [26, 0]]},
            {"id": "жарко", "points": [[24, 0], [26, 1], [40, 1], [50, 0]]}
        ]
    }

    default_heat_mf = {
        "уровень нагрева": [
            {"id": "слабый", "points": [[0, 0], [0, 1], [5, 1], [8, 0]]},
            {"id": "умеренный", "points": [[5, 0], [8, 1], [13, 1], [16, 0]]},
            {"id": "интенсивный", "points": [[13, 0], [18, 1], [23, 1], [26, 0]]}
        ]
    }

    default_rules = [
        ['холодно', 'интенсивный'],
        ['комфортно', 'умеренный'],
        ['жарко', 'слабый']
    ]

    default_current_temp = 15

    parser = argparse.ArgumentParser()
    parser.add_argument('--temp_file', type=str)
    parser.add_argument('--heat_file', type=str)
    parser.add_argument('--rules_file', type=str)
    parser.add_argument('--current_temp', type=int, default=default_current_temp)
    args = parser.parse_args()

    temp_mf_json = load_json_data(args.temp_file, json.dumps(default_temp_mf))
    heat_mf_json = load_json_data(args.heat_file, json.dumps(default_heat_mf))
    rules_json = load_json_data(args.rules_file, json.dumps(default_rules))
    current_temp = args.current_temp

    try:
        result = task(temp_mf_json, heat_mf_json, rules_json, current_temp)
        print(f"{result:.2f}")
    except ValueError as e:
        print(f"Ошибка: {e}")
