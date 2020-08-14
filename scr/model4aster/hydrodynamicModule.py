import hydrodynamicModels.morisonModel as morisonModel
import hydrodynamicModels.screenModel as screenModel
import wakeModel as wakeModel

row = 1025  # [kg/m3]   sea water density
kinematic_viscosity = 1.004e-6  # when the water temperature is 20 degree.
dynamic_viscosity = 1.002e-3  # when the water temperature is 20 degree.

morisonModel.row_fluid = row
morisonModel.kinematic_viscosity = kinematic_viscosity
morisonModel.dynamic_viscosity = dynamic_viscosity
screenModel.row_fluid = row
screenModel.kinematic_viscosity = kinematic_viscosity
screenModel.dynamic_viscosity = dynamic_viscosity
