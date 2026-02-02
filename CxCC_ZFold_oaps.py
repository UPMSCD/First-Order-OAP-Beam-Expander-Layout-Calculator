import math
import pprint

def calculate_oap_zemax_params(d_in, magnification, f1_parent):
    """
    Calculates Zemax LDE parameters for a 90-degree 2-mirror OAP expander.
    
    :param d_in: Input beam diameter (mm)
    :param magnification: Expansion ratio (M)
    :param f1_parent: Parent focal length of the first (convex) mirror (mm)
    """
    #################################################
    # 1. Fundamental Optical Properties
    f2_parent = f1_parent * magnification
    r1 = 2 * f1_parent # Radius of Curvature for M1
    r2 = 2 * f2_parent # Radius of Curvature for M2
    # 2. Off-Axis Distances (OAD) for 90-degree fold
    # For a 90-deg OAP, OAD = Radius of Curvature
    oad1 = r1
    oad2 = r2
    separation_dist = r2 - r1
    #################################################







    #################################################
    #M1
    x_half_width = (d_in / 2)
    y_half_width = x_half_width
    m1_LDE_Decenter_Y = abs(r1) * (1 + ((magnification - 1) * 0.5)) - abs(r1)
    #################################################



    #################################################
    # For the second mirror, the beam is stretched and shifted
    x_half_width_m2 = (d_in * magnification / 2)
    y_half_width_m2 = x_half_width_m2
    #################################################

    #################################################
    #DT stuff
    DT_Swing_Radius = abs(r1) + separation_dist + y_half_width_m2
    DT_Swing_Radius_edge = math.sqrt(DT_Swing_Radius**2 + x_half_width_m2**2)

    DT_Swing_Radius_m1_inside = abs(r1) - x_half_width
    DT_Swing_Radius_m1_outside = abs(r1) + x_half_width
    DT_Swing_Radius_m1_edge = math.sqrt(DT_Swing_Radius_m1_outside**2 + x_half_width**2)

    DT_Swing_Radius_m2_inside = abs(r1) + separation_dist - y_half_width_m2
    #################################################



    return {
        "M1": {
            "ROC": r1, # Negative for convex in Zemax
            "Conic": -1,
            "m1_LDE_Decenter_Y": -oad1,
            "Aperture_Decenter_Y": oad1,
            "X_Half_Width": x_half_width,
            "Y_Half_Width": y_half_width,
            "m2_LDE_Decenter_Y": m1_LDE_Decenter_Y,

        },
        "Inter_Mirror_Dist": separation_dist,
        "M2": {
            "ROC": r2, # Positive for concave
            "Conic": -1,
            "Aperture_Decenter_Y": r2,
            "X_Half_Width": x_half_width_m2,
            "Y_Half_Width": y_half_width_m2,
            "image_LDE_Decenter_y": r2,

        },
        "Diamond_Turning_Swing_Radius_at_center":DT_Swing_Radius,
        "Diamond_Turning_Swing_Radius_at_edge":DT_Swing_Radius_edge,

        "DT_Swing_Radius_m1_inside":DT_Swing_Radius_m1_inside,
        "DT_Swing_Radius_m1_outside":DT_Swing_Radius_m1_outside,
        "DT_Swing_Radius_m1_edge":DT_Swing_Radius_m1_edge,

        "DT_Swing_Radius_m2_inside":DT_Swing_Radius_m2_inside,

    }

# --- Example Run (Using your EO numbers) ---
# EO has R1=50.8, so f1=25.4. Magnification = 2.
params = calculate_oap_zemax_params(d_in=50, magnification=2.25, f1_parent=51.5)






pprint.pprint(params)