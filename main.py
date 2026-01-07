import math
import itertools
import copy

coor = [(0, 0), (10, 0), (10, 30),(0,30)]

zone_ratio = {
    "public": 0.35,
    "private": 0.40,
    "service": 0.25
}

def reorder_polygon(poly):
    cx = sum(x for x, y in poly) / len(poly)
    cy = sum(y for x, y in poly) / len(poly)
    return sorted(
        poly,
        key=lambda p: math.atan2(p[1] - cy, p[0] - cx)
    )

def clip_polygon_y(poly, y_min, y_max):
    clipped = []
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]

        # Keep vertex if inside band

        if y_min <= y1 <= y_max:
            clipped.append((x1, y1))

        # Intersection with y_min

        if (y1 < y_min and y2 > y_min) or (y1 > y_min and y2 < y_min):
            t = (y_min - y1) / (y2 - y1)
            x = x1 + t * (x2 - x1)
            clipped.append((x, y_min))

        # Intersection with y_max

        if (y1 < y_max and y2 > y_max) or (y1 > y_max and y2 < y_max):
            t = (y_max - y1) / (y2 - y1)
            x = x1 + t * (x2 - x1)
            clipped.append((x, y_max))

    # Remove duplicates

    clipped = list(dict.fromkeys(clipped))
    if len(clipped) < 3:
        return []

    return reorder_polygon(clipped)

min_y = min(y for x, y in coor)
max_y = max(y for x, y in coor)
depth = max_y - min_y
cuts = []
current_y = min_y

for name, ratio in zone_ratio.items():
    next_y = current_y + ratio * depth
    cuts.append((name, current_y, next_y))
    current_y = next_y


zones = []
for name, y1, y2 in cuts:
    zone_poly = clip_polygon_y(coor, y1, y2)
    if zone_poly:
        zones.append({
            "name": name,
            "polygon": zone_poly
        })
##############################polygon area calculator##############################################################################

def polygon_area(poly):
    area =0
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area)/2

for z in zones:
    z["area"] = polygon_area(z["polygon"])

####################################Assign room to zone########################################################################

room_min_area = {
    'living_room': 12.0,
    'bedroom': 11.5,
    'kitchen': 5.0,
    'toilet': 3.0,
    'dining': 10.0
}

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

def assign_rooms_to_zones(zones, rooms, room_min_area, zone_room_map):
    assignments = {}

    for room in rooms:
        room_area = room_min_area[room]

        for zone in zones:
            zone_name = zone['name']

            # Check zone compatibility
            if room not in zone_room_map.get(zone_name, []):
                continue

            # Check area availability
            if zone["area"] >= room_area and zone_name not in assignments.values():
                assignments[room] = zone_name
                break
    
    return assignments

assignments = assign_rooms_to_zones(
    zones,
    rooms_sorted,
    room_min_area,
    zone_room_map
)

for z in zones:
    z["rooms"] = []


##################################################Room geometry####################################################################
room_rules = {
    "living_room": {"min_width": 3.0, "min_length": 4.0},
    "bedroom":     {"min_width": 3.0, "min_length": 3.6},
    "kitchen":     {"min_width": 1.8, "min_length": 2.5},
    "toilet":      {"min_width": 1.1, "min_length": 1.5},
    "dining":      {"min_width": 3.0, "min_length": 3.0}
}
 
def bounding_box(poly):
    xs = [x for x,y in poly]
    ys = [y for x,y in poly]
    return min(xs), min(ys), max(xs), max(ys)

def place_rooms_in_zone(zone, room_rules):
    rects = {}
    zx1, zy1, zx2, zy2 = bounding_box(zone["polygon"])
    z_width = zx2 - zx1
    z_length = zy2 - zy1
    cursor_y = zy1  # simple vertical stacking (for now)

    for room in zone.get("rooms", []):
        min_w = room_rules[room]["min_width"]
        min_l = room_rules[room]["min_length"]

        if z_width < min_w or cursor_y + min_l > zy2:
            continue  # room doesn't fit

        cx = (zx1 + zx2) / 2
        x1 = cx - min_w / 2
        x2 = cx + min_w / 2
        y1 = cursor_y
        y2 = cursor_y + min_l

        rects[room] = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

        cursor_y += min_l  # move down for next room

    return rects
 



#####################################################adjacency and privacy###################################################

#Which zone touch each other?
zone_adjacency = {
    "public": ["private", "service"],
    "private": ["public", "service"],
    "service": ["public", "private"]
}

# (room a, room b) must not touch each other
HARD_RULES = [
    ("toilet", "kitchen"),
]

# (room a, room b, weight) - higher weight = more important
SOFT_RULES = [
    ("kitchen", "living_room", +5),
    ("bedroom", "toilet", +3),
    ("bedroom", "living_room", -3)
]

def zone_of_rooms(zones, room_name):
    for z in zones:
        if room_name in z.get("rooms",[]):
            return z["name"]
    return None

def check_hard_rules(zones, zone_adjacency, hard_rules):
    for room_a, room_b in hard_rules:
        za = zone_of_rooms(zones, room_a)
        zb = zone_of_rooms(zones, room_b)

        if not za or not zb:
            continue

        if zb in zone_adjacency.get(za, []):
            return False, f"HARD RULE VIOLATION: {room_a} adjacent to {room_b}"
        
    return True, "OK"

def score_soft_rules(zones, zone_adjacency, soft_rules):
    score = 0
    details = []
    for room_a, room_b, weight in soft_rules:
        za = zone_of_rooms(zones, room_a)
        zb = zone_of_rooms(zones, room_b)
        if not za or not zb:
            continue
        if zb in zone_adjacency.get(za, []):
            score += weight
            details.append((room_a, room_b, weight))
    return score, details

is_valid, msg = check_hard_rules(zones, zone_adjacency, HARD_RULES)

if not is_valid:
    print(msg)

else:
    score, details = score_soft_rules(zones, zone_adjacency, SOFT_RULES)
    #print("SOFT SCORE:", score)
    #print("DETAILS:", details)

#######################################################scoring and variation##################################################################

def score_layout(zones, zone_adjacency, soft_rules):
    # Adjacency score
    adj_score, _ = score_soft_rules(zones, zone_adjacency, soft_rules)
    # Area efficiency: sum(room_area / zone_area)
    eff_score = 0
    for z in zones:
        for room in z.get("rooms", []):
            eff_score += min(1.0, room_min_area[room] / z["area"])

    # Penalty for empty zones
    empty_penalty = -2 * sum(1 for z in zones if not z.get("rooms"))
    return adj_score + eff_score * 5 + empty_penalty
    

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
            z["remaining_area"] = z["area"]   # ✅ number, not list

        for room, zone_name in zip(rooms, assignment):
            for z in new_zones:
                if z["name"] == zone_name:
                    if z["remaining_area"] >= room_min_area[room]:
                        z["rooms"].append(room)
                        z["remaining_area"] -= room_min_area[room]
 
        
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
#print("Generated layout:", len(layouts))
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
#print("BEST SCORE:", best_score)

for z in best_layout:
    z["room_rects"] = place_rooms_in_zone(z, room_rules)

for z in best_layout:
    print(z["name"], z["rooms"], z["room_rects"])



