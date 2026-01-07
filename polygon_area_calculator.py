zones = [
    {'name': 'public', 
     'polygon': [(0, 0), (10, 0), (10.0, 10.5), (0.0, 10.5)]
     }, 
     {
     'name': 'private', 
     'polygon': [(0.0, 10.5), (10.0, 10.5), (10.0, 22.5), (0.0, 22.5)]
     }, 
     {
     'name': 'service', 
     'polygon': [(0.0, 22.5), (10.0, 22.5), (10, 30), (0, 30)]
     }
     ]


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

print(zones)
