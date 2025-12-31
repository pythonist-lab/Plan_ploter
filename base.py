import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from room_rules import minimum_room_sizes_india

def draw(coordinates): #Create polygon with the coordinates from function polygon_coordinates
    #all_poly = []
    poly = Polygon(coordinates,closed =True,facecolor = "b",edgecolor="black",alpha=0.6)
    #all_poly.append(poly)
    return(poly)

def show_plot(polygons,plot_width,plot_length): #Show/display the polygons
    fig, ax = plt.subplots()

    ax.set_xlim(0,plot_width)
    ax.set_ylim(0,plot_length)
    ax.set_aspect("equal")

    for poly in polygons:
        ax.add_patch(poly)
    
    plt.show()

def cover_area(plot_wid, plot_len, front_spacing, left_spacing, right_spacing, back_spacing): #Calculate cover area details from givrn land length, width and spacings
    len_cover_area = plot_len - back_spacing
    wid_cover_area = plot_wid - left_spacing
    cover_area = len_cover_area * wid_cover_area
    start_cordinate = (left_spacing, front_spacing)
    return {
        "Start":start_cordinate,
        "Cover area length":len_cover_area,
        "Cover area width":wid_cover_area,
        "Cover area":cover_area
    }

def zone(x,y,cover_len,cover_wid): #Gives coord for 4 zones, inputs - cover start,length, width
    wid_center = (x+cover_wid)/2
    len_center = (y+cover_len)/2
    buttom_left = [x,y]
    top_right = [cover_wid,cover_len]
    top_left = [x,cover_len]
    buttom_right = [cover_wid,y]
    AB_center = [wid_center,y]
    DA_center = [x,len_center]
    BC_center = [cover_wid,len_center]
    CD_center = [wid_center,cover_len]
    center = [wid_center,len_center]

    zone_coord = []
    for i in range(4):
        if i == 0:
            zone1_coord = [buttom_left,AB_center,center,DA_center]
            zone_coord.append(zone1_coord)
        elif i == 1:
            zone2_coord = [AB_center,buttom_right,BC_center,center]
            zone_coord.append(zone2_coord)
        elif i == 2:
            zone3_coord = [center,BC_center,top_right,CD_center]
            zone_coord.append(zone3_coord)
        elif i == 3:
            zone4_coord = [CD_center,top_left,DA_center,center]
            zone_coord.append(zone4_coord)

    return zone_coord

def zone_storage(zone_cod):
    zone_data = {}
    for i, coords in enumerate(zone_cod, start=1):
        Length = round(abs((coords[0][1])-(coords[-1][1])),2)
        Width = round(abs((coords[0][0])-(coords[1][0])),2)
        zone_data[f"zone_{i}"] = {
            "Coordinates": coords,
            "Length": Length,
            "Width": Width,
            "Area": Length*Width
        }
    return zone_data

#Inputs ---
plot_length = 20
plot_width = 10
front_spacing = 1.2
left_side_spacing = 1.2
right_side_spacing = 1.2
back_spacing = 3
#Inputs end --

cover_details = cover_area(plot_width, plot_length, front_spacing, left_side_spacing, right_side_spacing, back_spacing)

building_details =[
        [
        cover_details['Start'][0],
        cover_details['Start'][1],
        cover_details['Cover area length'],
        cover_details['Cover area width']
        ]
    ]

zone_cod = zone(building_details[0][0],building_details[0][1],building_details[0][2],building_details[0][3])

all_polys = []

for i in range(len(zone_cod)):
    poly = draw(zone_cod[i])
    all_polys.append(poly)

show_plot(all_polys, plot_width,plot_length)

