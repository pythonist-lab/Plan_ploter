import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def polygon_coordinates(x,y,width,length): #Gives coordinates with input of start points(x,y) and length, width
    return [
        [x,y],
        [x + width,y],
        [x + width, y+length],
        [x,y+length]
    ]

def draw(coordinates): #Create polygon with the coordinates from function polygon_coordinates
    all_poly = []
    poly = Polygon(coordinates,closed =True,facecolor = "b",edgecolor="black",alpha=0.6)
    all_poly.append(poly)
    return(all_poly)

def show_plot(poly,plot_width,plot_length): #Show/display the polygons
    fig, ax = plt.subplots()
    ax.set_xlim(0,plot_width)
    ax.set_ylim(0,plot_length)
    ax.add_patch(poly)
    ax.set_aspect("equal")
    plt.show()

def cover_area(plot_wid, plot_len, front_spacing, left_spacing, right_spacing, back_spacing): #Calculate cover area details from givrn land length, width and spacings output a dict
    len_cover_area = plot_len - (front_spacing + back_spacing)
    wid_cover_area = plot_wid - (left_spacing + right_spacing)
    cover_area = len_cover_area * wid_cover_area
    start_cordinate = (left_spacing, front_spacing)
    return {
        "Start":start_cordinate,
        "Cover area length":len_cover_area,
        "Cover area width":wid_cover_area,
        "Cover area":cover_area
    }


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

for x,y,width,length in building_details:
    cover_coor = polygon_coordinates(x,y,width,length)
    
print(cover_coor)

