# ----------------------------------
# --   University of Stavanger    --
# --           Hui Cheng          --
# ----------------------------------
# Any questions about this code,
# please email: hui.cheng@uis.no
# Net panel(s)

{
    'MeshLib': 'panel',
    'Environment':
        {
            'current': [[0.5, 0, 0]],  # A list of currents
            'waterDepth': 0.4,  # [m] the water depth
            'waves': 'False',  # wave type : will be add in next version
            'fluidDensity': 1000.0,  # [kg/m3] fluid density
        },
    'Net':
        {
            'nettingType': 'square',  # rhombus
            'normalVector': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],  # inflowAngle=0; AOA=90,
            # 'normalVector':[[0.965926,0.258819,0],[-0.258819,0.965926,0],[0,0,1]], # inflowAngle=15
            # 'normalVector':[[0.866025,0.5,0],       [-0.5,0.866025,0],[0,0,1]], # inflowAngle=30
            # 'normalVector':[[0.707107,0.707107,0],[-0.707107,0.707107,0],[0,0,1]], # inflowAngle; AOA=45
            # 'normalVector':[[0.5,0.866025,0],     [-0.866025,0.5,0],     [0,0,1]], # inflowAngle=60
            # 'normalVector':[[0.258819,0.965926,0],[-0.965926,0.258819,0],[0,0,1]], # inflowAngle=75
            'netHeight': 1.0,  # [m]
            'netWidth': 1.0,  # [m]
            'meshOverHeight': 10,
            'meshOverWidth': 10,
            'Sn': 0.20,  # solidity ratio
            'twineDiameter': 2.8e-3,  # [m]the twine diameter of the physical net
            'meshLength': 29e-3,  # [m]the half mesh length
            'netYoungmodule': 40000000,  # [Pa]
            'netRho': 1140.0,  # [kg/m3] density of the net material
        },
    'TopBar':
        {
            'barCenter': [[0, 0, -0.732]],
            'barRadius': 3e-3,  # [m] the pipe diameter of the floating pipe
            'topBarRho': 6e3,
            'topBarYoungModule': 9e11,
        },
    'Boundary':
        {
            'hydroModel': 'Screen-UDV-0.258-0',  # 'Morison-M1'
            'wakeModel': 'factor-1',
            'fixed': 'allnodes',  # 'sidenodes', #'bottomnodes' 'allnodes'. 'topnodes',
            'gravity': 9.81,
        },
    'Weight':
        {
            'weightType': 'tube',  # sinkers or tube
            'bottomBarRadius': 3e-3,  # [m] the pipe diameter of the sinker tube
            'bottomBarRho': 7.87e3,
            'bottomBarYoungModule': 9e11,
            #  	 'numOfSinkers':2,
            #  	 'sinkerWeight':4.48, #[N]
        },
    'Solver':
        {
            'version': 'stable',
            'coupling': 'FSI',  # 'FSI', # 'FSI', 'simiFSI'
            'method': 'HHT',  # [m] the length of the buoy line, distance between the buoy and plate
            'alpha': 24.3,
            'timeStep': 0.1,  # [s] time step for simulations
            'timeLength': 50,  # [s] length of time for each current velocity
            'MaximumIteration': 100,
            'Residuals': 2e-5,  # [N] the Maximum bouncy force that the buoy can provide
            'saveMid_result': False,
            # [s] save the mid results every 30 second. Will slow down the simulation significantly.
        },
}
