zones = [{
    'name': 'public', 
    'polygon': [(0, 0), (10, 0), (10.0, 10.5), (0.0, 10.5)], 
    'area': 105.0}, 
    {
    'name': 'private', 
    'polygon': [(0.0, 10.5), (10.0, 10.5), (10.0, 22.5), (0.0, 22.5)], 
    'area': 120.0}, 
    {
    'name': 'service', 
    'polygon': [(0.0, 22.5), (10.0, 22.5), (10, 30), (0, 30)], 
    'area': 75.0
    }]

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
    z["room"] = None

for room, zone_name in assignments.items():
    for z in zones:
        if z["name"] == zone_name:
            z["room"] = room

print(zones)


