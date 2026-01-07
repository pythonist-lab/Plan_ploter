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
        if room_name in z.get("rooms", []):
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
    print("SOFT SCORE:", score)
    print("DETAILS:", details)
 
 