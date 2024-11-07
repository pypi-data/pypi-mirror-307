from FoundationDesign.foundationdesign import padFoundationDesign, PadFoundation

fdn = PadFoundation(
    foundation_length=3600,
    foundation_width=3000,
    column_length=450,
    column_width=450,
    col_pos_xdir=1800,
    col_pos_ydir=1500,
    soil_bearing_capacity=150,
)

z = fdn.foundation_loads(
    foundation_thickness=550,
    soil_depth_abv_foundation=0,
    soil_unit_weight=18,
    concrete_unit_weight=24,
)
fdn.column_axial_loads(permanent_axial_load=770, imposed_axial_load=330)
fdn.column_horizontal_loads_xdir(
    permanent_horizontal_load_xdir=35, imposed_horizontal_load_xdir=15
)
fdn.column_moments_xdir(permanent_moment_xdir=78, imposed_moment_xdir=34)


fdn_design = padFoundationDesign(
    fdn, fck=30, fyk=500, concrete_cover=30, bar_diameterX=16, bar_diameterY=16
)

# fdn_design.plot_foundation_loading_X()
# fdn_design.plot_foundation_loading_Y()
# fdn_design.plot_bending_moment_X()
# fdn_design.plot_bending_moment_Y()
# fdn_design.plot_shear_force_Y()
# print(fdn_design.get_design_moment_X())
# print(fdn_design.get_design_moment_Y())
# print(fdn_design.get_design_shear_force_X())
# print(fdn_design.area_of_steel_reqd_X_dir())
# print(fdn_design.area_of_steel_reqd_Y_dir())
print(fdn_design.reinforcement_provision_flexure_X_dir())
print(fdn_design.reinforcement_provision_flexure_Y_dir())

#print(fdn_design.punching_shear_column_face())
#print(fdn_design.punching_shear_check_1d())
#print(fdn_design.punching_shear_check_2d())
#print(fdn_design.tranverse_shear_check_Xdir())
#print(fdn_design.tranverse_shear_check_Ydir())
#print(fdn_design.sliding_resistance_check())


# outputs
# print(fdn.area_of_foundation())
# print(fdn.total_force_X_dir_sls())
# print(fdn.total_force_Y_dir_sls())
# print(fdn.total_force_Z_dir_sls())
# print(fdn.total_moments_X_direction_sls())
# print(fdn.total_moments_Y_direction_sls())
# print(fdn.eccentricity_X_direction_sls())
# print(fdn.eccentricity_Y_direction_sls())
# print(fdn.pad_base_pressures_sls())
# print(fdn.pad_base_pressures_uls())
# print(fdn.total_force_X_dir_uls())
# print(fdn.total_force_Y_dir_uls())
# print(fdn.total_force_Z_dir_uls())
# print(fdn.total_moments_X_direction_uls())
# print(fdn.total_moments_Y_direction_uls())
# print(fdn.eccentricity_X_direction_uls())
# print(fdn.eccentricity_Y_direction_uls())
