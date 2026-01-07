import matplotlib.pyplot as plt
import matplotlib.patches as patches

coor = [(0, 0), (10, 0), (10, 30),(0,30)]

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

colors = {
    "public": "#9ecae1",
    "private": "#a1d99b",
    "service": "#bdbdbd"
}

fig, ax = plt.subplots()
ax.set_aspect("equal")

# Draw envelope outline
env = patches.Polygon(coor, fill=False, edgecolor="black", linewidth=2)
ax.add_patch(env)
ax.autoscale_view()
# Draw zones

for z in zones:
    poly = patches.Polygon(
        z["polygon"],
        closed=True,
        facecolor=colors[z["name"]],
        edgecolor="black",
        alpha=0.7
    )

    ax.add_patch(poly)

    if z['room_rect']:
        room_patch = patches.Polygon(
            z['room_rect'],
            closed=True,
            facecolor="none",
            edgecolor="red",
            linewidth=1
        )
        ax.add_patch(room_patch)

        cx = sum(x for x,y in z['room_rect']) / 4
        cy = sum(y for x,y in z['room_rect']) / 4
        ax.text(cx, cy, z["room"], ha='center', va='center', fontsize=8, color='red')
    # Label zone
    cx = sum(x for x, y in z["polygon"]) / len(z["polygon"])
    cy = sum(y for x, y in z["polygon"]) / len(z["polygon"])
    ax.text(cx , cy-3, z["name"], ha="center", va="center", fontsize=10, weight="bold")


plt.show()