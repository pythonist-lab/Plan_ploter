import itertools
import copy

zones = [{
    'name': 'public', 
    'polygon': [(0, 0), (10, 0), (10.0, 10.5), (0.0, 10.5)], 
    'area': 105.0, 
    'room': 'living_room', 
    'room_rect': [(3.5, 3.25), (6.5, 3.25), (6.5, 7.25), (3.5, 7.25)]}, 
    {
    'name': 'private', 
    'polygon': [(0.0, 10.5), (10.0, 10.5), (10.0, 22.5), (0.0, 22.5)], 
    'area': 120.0, 
    'room': 'bedroom', 
    'room_rect': [(3.5, 14.7), (6.5, 14.7), (6.5, 18.3), (3.5, 18.3)]}, 
    {
    'name': 'service', 
    'polygon': [(0.0, 22.5), (10.0, 22.5), (10, 30), (0, 30)], 
    'area': 75.0, 
    'room': 'kitchen', 
    'room_rect': [(4.1, 25.0), (5.9, 25.0), (5.9, 27.5), (4.1, 27.5)]
    }]

zone_adjacency = {
    "public": ["private", "service"],
    "private": ["public", "service"],
    "service": ["public", "private"]
}

SOFT_RULES = [
    ("kitchen", "living_room", +5),
    ("bedroom", "toilet", +3),
    ("bedroom", "living_room", -3)
]

room_min_area = {
    'living_room': 12.0,
    'bedroom': 11.5,
    'kitchen': 5.0,
    'toilet': 3.0,
    'dining': 10.0
}

HARD_RULES = [
    ("toilet", "kitchen"),
]

required_room = [
    'living_room',
    'bedroom',
    'kitchen',
    'toilet',
    'dining'
]

zone_room_map = {
    "public": ["living_room","dining"],
    "private": ["bedroom","study"],
    "service": ["kitchen","toilet","utility"]
}

rooms_sorted = sorted(
    required_room,
    key=lambda r: room_min_area[r],
    reverse=True
)

def check_hard_rules(zones, zone_adjacency, hard_rules):
    for room_a, room_b in hard_rules:
        za = zone_of_rooms(zones, room_a)
        zb = zone_of_rooms(zones, room_b)

        if not za or not zb:
            continue

        if zb in zone_adjacency.get(za, []):
            return False, f"HARD RULE VIOLATION: {room_a} adjacent to {room_b}"
        
    return True, "OK"

def zone_of_rooms(zones, room_name):
    for z in zones:
        if room_name in z.get("rooms", []):
            return z["name"]
    return None

score = 2
details = [('kitchen', 'living_room', 5), ('bedroom', 'living_room', -3)]

def score_layout(zones, zone_adjacency, soft_rules):
    # Adjacency score
    adj_score, _ = score
    # Area efficiency: sum(room_area / zone_area)
    eff_score = 0
    for z in zones:
        if z.get("room"):
            room = z["room"]
            eff_score += min(1.0, room_min_area[room] / z["area"])

    # Penalty for empty zones
    empty_penalty = -2 * sum(1 for z in zones if not z.get("room"))
    total = adj_score + eff_score * 5 + empty_penalty
    return total

def compatible_zones(room, zones, zone_room_map):
    return [z for z in zones if room in zone_room_map.get(z["name"], [])]
 
def all_rooms_assigned(zones, required_rooms):
        assigned = set()
        for z in zones:
            assigned.update(z.get("rooms",[]))
        return all(room in assigned for room in required_rooms)

def generate_layout_variations(zones, rooms, room_min_area, zone_room_map):
    variations = []

    # all possible room → zone choices
    choices = []
    for room in rooms:
        choices.append([z["name"] for z in compatible_zones(room, zones, zone_room_map)])
    for assignment in itertools.product(*choices):
        #if len(set(assignment)) != len(assignment):
            #continue  # one room per zone

        new_zones = copy.deepcopy(zones)

        for z in new_zones:
            z["rooms"] = []

        for room, zone_name in zip(rooms, assignment):
            for z in new_zones:
                if z["name"] == zone_name and z["area"] >= room_min_area[room]:
                    z["rooms"].append(room)
        
        if not all_rooms_assigned(new_zones,required_room):
            continue

        variations.append(new_zones)

    return variations
 
def is_valid_layout(zones, zone_adjacency, hard_rules):
    ok, _ = check_hard_rules(zones, zone_adjacency, hard_rules)
    return ok
 
layouts = generate_layout_variations(
    zones,
    rooms_sorted,
    room_min_area,
    zone_room_map
)
print("Generated layout:", len(layouts))
scored = []
for layout in layouts:
    if not is_valid_layout(layout, zone_adjacency, HARD_RULES):
        continue

    score = score_layout(layout, zone_adjacency, SOFT_RULES)
    scored.append((score, layout))


if not scored:
    raise ValueError("No valid layouts generated — check rules, areas, or compatibility")
 
scored.sort(key=lambda x: x[0], reverse=True)
best_score, best_layout = scored[0]
print("BEST SCORE:", best_score)

for z in best_layout:
    print(z["name"], "→", z.get("room"))

