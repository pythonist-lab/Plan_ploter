import matplotlib.pyplot as plt

import matplotlib.patches as patches

ZONE_COLORS = {

    "public": "#8ecae6",

    "private": "#b7e4c7",

    "service": "#ffd166"

}

ROOM_COLORS = {

    "living_room": "#219ebc",

    "dining": "#ffb703",

    "bedroom": "#52b788",

    "kitchen": "#f77f00",

    "toilet": "#adb5bd"

}

def draw_layout(best_layout, envelope=None):

    fig, ax = plt.subplots(figsize=(8, 12))

    ax.set_aspect("equal")

    ax.set_title("Generated Floor Plan", fontsize=14)

    # ---- Envelope ----

    if envelope:

        env = patches.Polygon(

            envelope,

            facecolor="none",

            edgecolor="black",

            linewidth=2

        )

        ax.add_patch(env)

    # ---- Zones ----

    for z in best_layout:

        zone_poly = patches.Polygon(

            z["polygon"],

            facecolor=ZONE_COLORS.get(z["name"], "#dddddd"),

            edgecolor="black",

            alpha=0.4

        )

        ax.add_patch(zone_poly)

        # Zone label

        cx = sum(x for x, y in z["polygon"]) / len(z["polygon"])

        cy = sum(y for x, y in z["polygon"]) / len(z["polygon"])

        ax.text(cx, cy, z["name"].upper(), ha="center", va="center", fontsize=10)

        # ---- Rooms ----

        for room, rect in z.get("room_rects", {}).items():

            room_patch = patches.Polygon(

                rect,

                facecolor=ROOM_COLORS.get(room, "#cccccc"),

                edgecolor="black",

                linewidth=1

            )

            ax.add_patch(room_patch)

            rcx = sum(x for x, y in rect) / 4

            rcy = sum(y for x, y in rect) / 4

            ax.text(rcx, rcy, room, ha="center", va="center", fontsize=8)

    ax.autoscale()

    ax.invert_yaxis()  # architectural convention

    plt.show()

coor = [(0, 0), (10, 0), (10, 30),(0,30)]


best_layout = [{'name': 'public', 
                'polygon': [(0, 0), (10, 0), (10.0, 10.5), (0.0, 10.5)], 
                'area': 105.0, 
                'rooms': ['living_room', 'dining'], 
                'remaining_area': 83.0, 
                'room_rects': {
                    'living_room': [(3.5, 0), (6.5, 0), (6.5, 4.0), (3.5, 4.0)], 
                    'dining': [(3.5, 4.0), (6.5, 4.0), (6.5, 7.0), (3.5, 7.0)]}}, 
                {'name': 'private', 
                 'polygon': [(0.0, 10.5), (10.0, 10.5), (10.0, 22.5), (0.0, 22.5)], 
                 'area': 120.0, 
                 'rooms': ['bedroom'], 
                 'remaining_area': 108.5, 
                 'room_rects': {
                     'bedroom': [(3.5, 10.5), (6.5, 10.5), (6.5, 14.1), (3.5, 14.1)]}}, 
                {'name': 'service', 
                 'polygon': [(0.0, 22.5), (10.0, 22.5), (10, 30), (0, 30)], 
                 'area': 75.0, 
                 'rooms': ['kitchen', 'toilet'], 
                 'remaining_area': 67.0, 
                 'room_rects': {
                     'kitchen': [(4.1, 22.5), (5.9, 22.5), (5.9, 25.0), (4.1, 25.0)], 
                     'toilet': [(4.45, 25.0), (5.55, 25.0), (5.55, 26.5), (4.45, 26.5)]}}]


draw_layout(
    best_layout,
    envelope=coor
)
