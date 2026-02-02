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
    # The Anamorphic Width (The "Stretch" on the mirror surface)
    # For 90 degree fold, the beam hits at 45 degrees.
    y_footprint_half_m2 = (d_in * magnification / 2) * math.sqrt(2)

    h = d_in / 2 #semi diameter
    y_top_ray = r2 * (h / (r1 - h))
    y_bot_ray = r2 * (-h / (r1 + h))
    
    real_y_width_m2 = y_top_ray - y_bot_ray
    real_y_shift_m2 = (y_top_ray + y_bot_ray) / 2
    # 3. Anamorphic Stretch Factor
    y_stretch_factor = real_y_width_m2 / (d_in * magnification)
    Anamorphic_stretch_Ratio = f"{round(((y_stretch_factor - 1) * 100) , 4)}%"

    x_compression_factor = 1 / y_stretch_factor
    x_min_half_width_m2 = (d_in * magnification / 2) * x_compression_factor
    System_Anamorphic_Ratio = ((y_stretch_factor - 1) * 2) + 1
    #################################################





    #################################################
    #M1
    x_half_width = (d_in / 2)
    y_half_width = x_half_width
    m1_LDE_Decenter_Y = abs(r1) * (1 + ((magnification - 1) * 0.5))
    #################################################




    #################################################
    # For the second mirror, the beam is stretched and shifted
    x_half_width_m2 = (d_in * magnification / 2) * y_stretch_factor
    y_half_width_m2 = x_half_width_m2
    m2_LDE_Decenter_Y = (abs(r2) * -1) - real_y_shift_m2
    Aperture_Decenter_Y_m2 = (abs(r2) * -1) - real_y_shift_m2
    #################################################

    #################################################
    #DT stuff
    DT_Swing_Radius = abs(r1) + separation_dist + y_half_width_m2 + real_y_shift_m2
    DT_Swing_Radius_edge = math.sqrt(DT_Swing_Radius**2 + x_half_width_m2**2)

    DT_Swing_Radius_m1_inside = abs(r1) - x_half_width
    DT_Swing_Radius_m1_outside = abs(r1) + x_half_width
    DT_Swing_Radius_m1_edge = math.sqrt(DT_Swing_Radius_m1_outside**2 + x_half_width**2)

    DT_Swing_Radius_m2_inside = abs(r1) + separation_dist - y_half_width_m2 + real_y_shift_m2
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
            "Aperture_Decenter_Y": Aperture_Decenter_Y_m2,
            "X_Half_Width": x_half_width_m2,
            "Y_Half_Width": y_half_width_m2,
            "image_LDE_Decenter_y": m2_LDE_Decenter_Y,
            "X_Min_Half_Width":x_min_half_width_m2,
            "Anamorphic_stretch_Ratio_Y":Anamorphic_stretch_Ratio,
            "System_Anamorphic_Ratio":System_Anamorphic_Ratio,

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
params = calculate_oap_zemax_params(d_in=50, magnification=2.25, f1_parent=46)






pprint.pprint(params)