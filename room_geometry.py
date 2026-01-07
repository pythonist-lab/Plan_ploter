zones = [{
    'name': 'public', 
    'polygon': [(0, 0), (10, 0), (10.0, 10.5), (0.0, 10.5)], 
    'area': 105.0, 
    'room': 'living_room'},

    {'name': 'private', 
     'polygon': [(0.0, 10.5), (10.0, 10.5), (10.0, 22.5), (0.0, 22.5)], 
     'area': 120.0, 
     'room': 'bedroom'}, 

    {'name': 'service', 
    'polygon': [(0.0, 22.5), (10.0, 22.5), (10, 30), (0, 30)], 
    'area': 75.0, 
    'room': 'kitchen'
    }]

room_rules = {
    "living_room": {"min_width": 3.0, "min_length": 4.0},
    "bedroom":     {"min_width": 3.0, "min_length": 3.6},
    "kitchen":     {"min_width": 1.8, "min_length": 2.5},
    "toilet":      {"min_width": 1.1, "min_length": 1.5}
}
 
def bounding_box(poly):
    xs = [x for x,y in poly]
    ys = [y for x,y in poly]
    return min(xs), min(ys), max(xs), max(ys)

def place_room_in_zone(zone, room_rules):
    room = zone.get("room")
    if not room:
        return None
    
    min_w = room_rules[room]["min_width"]
    min_l = room_rules[room]["min_length"]

    zx1, zy1, zx2, zy2 = bounding_box(zone["polygon"])
    z_width = zx2 - zx1
    z_length = zy2 - zy1

    if z_width < min_w or z_length < min_l:
        return None
    
    cx = (zx1 + zx2) / 2
    cy = (zy1 + zy2) / 2

    x1 = cx - min_w / 2
    x2 = cx + min_w / 2
    y1 = cy - min_l / 2
    y2 = cy + min_l / 2

    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

for z in zones:
    z["room_rect"] = place_room_in_zone(z, room_rules)

print(zones)
