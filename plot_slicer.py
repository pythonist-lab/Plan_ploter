import math

# -----------------------------

# INPUT: Buildable envelope

# -----------------------------

coor = [(0, 0), (10, 0), (10, 30),(0,30)]

zone_ratio = {

    "public": 0.35,

    "private": 0.40,

    "service": 0.25

}

# -----------------------------

# Utility: reorder polygon vertices

# -----------------------------

def reorder_polygon(poly):

    cx = sum(x for x, y in poly) / len(poly)
    cy = sum(y for x, y in poly) / len(poly)

    return sorted(

        poly,

        key=lambda p: math.atan2(p[1] - cy, p[0] - cx)

    )

# -----------------------------

# Polygon clipping (horizontal)

# -----------------------------

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

# -----------------------------

# Compute slicing bands

# -----------------------------

min_y = min(y for x, y in coor)

max_y = max(y for x, y in coor)

depth = max_y - min_y

cuts = []

current_y = min_y

for name, ratio in zone_ratio.items():

    next_y = current_y + ratio * depth

    cuts.append((name, current_y, next_y))

    current_y = next_y

# -----------------------------

# Generate zones

# -----------------------------

zones = []

for name, y1, y2 in cuts:

    zone_poly = clip_polygon_y(coor, y1, y2)

    if zone_poly:

        zones.append({

            "name": name,

            "polygon": zone_poly

        })








print(zones)
