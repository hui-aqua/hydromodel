"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import workPath


# >>>>>>>>>>>>>>> Start to write input file>>>>>>>>>>>>
def head(handel, cwd):
    handel.write('''# ----------------------------------
# --   University of Stavanger    --
# --           Hui Cheng          --
# ----------------------------------
# Any questions about this code,
# please email: hui.cheng@uis.no
import sys
import os
import time
sys.path.append("''' + workPath.forceModel_path + '''")
import hydrodynamicModule as hdm
import nettingFSI as fsi
import seacondition as sc
cwd="''' + cwd + '''/"
DEBUT(PAR_LOT='NON',
IGNORE_ALARM=("SUPERVIS_25","DISCRETE_26","UTILITAI8_56")
)
INCLUDE(UNITE=90)
mesh = LIRE_MAILLAGE(UNITE=20)''')
    handel.write('\n')


# >>>>>>>>>>>>>>>    AFFE_MODELE       >>>>>>>>>>>>
def define_model(handel, weight_type):
    if weight_type in ['sinkers', 'allfixed']:
        handel.write('''
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'),
                             MODELISATION=('CABLE'),
                             PHENOMENE='MECANIQUE'),
                          ),
                    MAILLAGE=mesh)
    ''')
    elif weight_type in ['sinkerTube', 'sinkerTube+centerweight', 'tube']:
        handel.write('''
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'),
                             MODELISATION=('CABLE'),
                             PHENOMENE='MECANIQUE'),
                          _F(GROUP_MA=('bottomring'),
                             MODELISATION=('POU_D_E'),
                             PHENOMENE='MECANIQUE')
                          ),
                    MAILLAGE=mesh)
    ''')
    else:
        print("Warning!!! >>>>>AFFE_MODELE")


def define_model_fishFarm(handel, twine_section, Fb_node):
    handel.write('''
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines','anchorLines','frameLines','bridlesH','bridlesV','buoyLines'),
                             MODELISATION=('CABLE'),
                             PHENOMENE='MECANIQUE'),
                          _F(GROUP_MA=('topRings','bottomRings','links'),
                             MODELISATION=('POU_D_E'),
                             PHENOMENE='MECANIQUE')
                          ),
                    MAILLAGE=mesh)
                    
elemprop = AFFE_CARA_ELEM(CABLE=(_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=''' + str(twine_section) + '''),
                                _F(GROUP_MA=('anchorLines','frameLines'),
                                   N_INIT=60000.0,
                                   SECTION=0.002),
                                _F(GROUP_MA=('bridlesH','bridlesV','buoyLines'),
                                   N_INIT=10.0,
                                   SECTION=0.002),   
                                ),
                          POUTRE=_F(GROUP_MA=('topRings','bottomRings','links' ),
                                    SECTION='CERCLE',
                                    CARA=('R', 'EP'),
                                    VALE=(0.25, 0.25)),                                   
                          MODELE=model)

net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                     ELAS=_F(E=100000000, NU=0.2,RHO=1125.0)) 
                      
rope = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.001963495),
                     ELAS=_F(E=1000000000, NU=0.2,RHO=1100.0))  

hdpe1 = DEFI_MATERIAU(ELAS=_F(E=900000000,
                           NU=0.3,
                           RHO=989.0))   
                              
hdpe2 = DEFI_MATERIAU(ELAS=_F(E=900000000,
                           NU=0.3,
                           RHO=1038.0)) 
                                                                                          
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines',),
                                 MATER=(net)),
                               _F(GROUP_MA=('anchorLines','frameLines','bridlesH','bridlesV','buoyLines'),
                                 MATER=(rope)),                                 
                               _F(GROUP_MA=('topRings','links',),
                                 MATER=(hdpe1)),
                               _F(GROUP_MA=('bottomRings',),
                                 MATER=(hdpe2)),  
                               ),
                         MODELE=model)
                                              
# load
gF = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                       GRAVITE=9.81,
                                       GROUP_MA=('topRings','bottomRings','links','twines','anchorLines','frameLines','bridlesH','bridlesV','buoyLines')),
                      MODELE=model)

buoyF= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=("net_nodes"),
                                      FX=0,
                                      FY=0,
                                      FZ=''' + str(Fb_node) + ''',
                                      ),
                      MODELE=model)
            
fixed = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_NO=("anchor"),
                                   LIAISON='ENCASTRE'),
                             MODELE=model)

sealevel = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_NO=("net_top","buoy"),
                                      DZ=0.0,),
                             MODELE=model)       
                                                
sinkF1= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=("net_tip"),
                                      FX=0,
                                      FY=0,
                                      FZ=-981,
                                      ),
                      MODELE=model)

sinkF2= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=("plate"),
                                      FX=0,
                                      FY=0,
                                      FZ=-98.1,
                                      ),
                      MODELE=model)                                                                   
             
    ''')


# >>>>>>>>>>>>>>>    AFFE_CARA_ELEM       >>>>>>>>>>>>
def define_element(handel, weight_type, twine_section, bottom_radius=0):
    if weight_type in ['sinkers', 'allfixed']:
        handel.write('''
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=''' + str(twine_section) + '''),
                          MODELE=model)
''')
    elif weight_type in ['sinkerTube', 'sinkerTube+centerweight', 'tube']:
        handel.write('''
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=''' + str(twine_section) + '''),
                          POUTRE=_F(GROUP_MA=('bottomring', ),
                                    SECTION='CERCLE',
                                    CARA=('R', 'EP'),
                                    VALE=(''' + str(bottom_radius) + ''', ''' + str(bottom_radius) + ''')),
                          MODELE=model)
''')
    else:
        print("Warning!!! >>>>>AFFE_CARA_ELEM")


# >>>>>>>>>>>>>>>    DEFI_MATERIAU       >>>>>>>>>>>>
def define_material(handel, weight_type, net_module, net_rho, bottom_module=0, bottom_rho=0):
    if weight_type in ['sinkers', 'allfixed']:
        handel.write('''
net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(net_module) + ''', NU=0.2,RHO=''' + str(net_rho) + '''))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0))
''')
    elif weight_type in ['sinkerTube', 'sinkerTube+centerweight', 'tube']:
        handel.write('''
net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(net_module) + ''', NU=0.2,RHO=''' + str(net_rho) + '''))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0))
fe = DEFI_MATERIAU(ELAS=_F(E=''' + str(bottom_module) + ''',
                           NU=0.3,
                           RHO=''' + str(bottom_rho) + '''))
''')
    else:
        print("Warning!!! >>>>>DEFI_MATERIAU")


# >>>>>>>>>>>>>>>    AFFE_MATERIAU       >>>>>>>>>>>>
def assign_material(handel, weight_type):
    if weight_type in ['sinkers', 'allfixed']:
        handel.write('''
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(net)),
                               ),
                         MODELE=model)
''')
    elif weight_type in ['sinkerTube', 'sinkerTube+centerweight', 'tube']:
        handel.write('''
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(net)),
                               _F(GROUP_MA=('bottomring'),
                                 MATER=(fe)),
                               ),
                         MODELE=model)
''')
    else:
        print("Warning!!! >>>>>AFFE_MATERIAU")


# >>>>>>>>>>>>>>>    AFFE_CHAR_MECA       >>>>>>>>>>>>
def assign_bc_gravity(handel, arg, gravity, element_name):
    """
    :param arg: indicate the boundary condition name
    :param handel:  a handel to write the input file
    :param gravity: the gravitational acceleration. Usually, we use 9.81 [m/s^2].
    :param element_name:  a group name of element. e.g., 'twines','bottomring','topring'
    :return: write the gravity statement to the input file
    """
    handel.write('''
''' + str(arg) + ''' = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                       GRAVITE=''' + str(float(gravity)) + ''',
                                       GROUP_MA=("''' + str(element_name) + '''")),
                      MODELE=model)
''')


# >>>>>>>>>>>>>>>    AFFE_CHAR_MECA    fixed >>>>>>>>>>>>
def assign_bc_fixed(handel, arg, fixed_position):
    """
    :param arg: indicate the boundary condition name
    :param handel: a handel to write the input file
    :param fixed_position: a group name of nodes. e.g., 'allnodes','topnodes','bottomnodes'
    :return: write the fixed statement to the input file
    """
    handel.write('''
''' + str(arg) + ''' = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_NO=("''' + str(fixed_position) + '''"),
                                         LIAISON='ENCASTRE'),
                             MODELE=model)
        ''')


def assign_bc_force_on_nodes(handel, arg, name_of_nodes, force):
    """
    :param arg: indicate the boundary condition name
    :param handel: a handel to write the input file
    :param name_of_nodes: a group name of nodes. e.g., 'allnodes','topnodes','bottomnodes'
    :param force:  [fx,fy,fz], Unit:[N].
    :return: write the fixed statement to the input file
    """
    handel.write('''
''' + str(arg) + '''= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=("''' + str(name_of_nodes) + '''"),
                                      FX=''' + str(force[0]) + ''',
                                      FY=''' + str(force[1]) + ''',
                                      FZ=''' + str(force[2]) + ''',
                                      ),
                      MODELE=model)
            ''')


# >>>>>>>>>>>>>>>    DEFI_LIST_INST       >>>>>>>>>>>>
def define_time_scheme(handel, time_step, time_length, number_of_velocity):
    handel.write('''
dt=''' + str(time_step) + '''      # time step
# itimes is the total iterations
duration=''' + str(time_length) + '''      # time step
itimes=''' + str(int(time_length / time_step * number_of_velocity)) + '''
tend=itimes*dt

listr = DEFI_LIST_REEL(DEBUT=0.0,
                       INTERVALLE=_F(JUSQU_A=tend,PAS=dt))

times = DEFI_LIST_INST(DEFI_LIST=_F(LIST_INST=listr,PAS_MINI=1e-8),
                       METHODE='AUTO')

''')


def set_hydrodynamic_model_fishFarm(handel, velocities, fluidDensity, Sn, dwh, dw0):
    handel.write('''
Uinput = ''' + str(velocities) + '''
hdm.row = ''' + str(fluidDensity) + '''  # [kg/m3]   sea water density

Fnh= []
NODEnumber=meshinfo['numberOfNodes_netting']+meshinfo['numberOfNodes_mooring']
l=['None']*((NODEnumber+1))
con_mooring = meshinfo['Lines_mooring']
sur_netting = meshinfo['surfs_netting']


hydroModel_netting=hdm.screenModel.forceModel("S1",sur_netting,+ ''' + str(Sn) + ''',''' + str(dwh) + ''',''' + str(
        dw0) + ''')
hydroModel_mooring=hdm.morisonModel.forceModel("M4",con_mooring,0.5,0.05,0.05)
netWakeModel=hdm.wakeModel.net2net("factor-1",meshinfo['Nodes_mooring']+meshinfo['Nodes_netting'],sur_netting,Uinput[0],[0,0,0],0.002,0.27)
        
with open(cwd+'/positionOutput/element_in_wake.txt', "w") as file:
    file.write(str(netWakeModel.get_element_in_wake()))
file.close()
with open(cwd+'/positionOutput/hydro_elements.txt', "w") as file:
    file.write(str(hydroModel_netting.output_hydro_element()))
file.close()

for k in range(0,itimes):
    INCLUDE(UNITE=91,INFO=0)

IMPR_RESU(FORMAT='MED',
          RESU=_F(CARA_ELEM=elemprop,
                  LIST_INST=listr,
                  NOM_CHAM=('DEPL' ,'SIEF_ELGA'),
                  # TOUT_CMP=(DEPL','ACCE','VITE' ),
                  RESULTAT=resn,
                  TOUT_CMP='OUI'),
          UNITE=80)

stat = CALC_CHAMP(CONTRAINTE=('SIEF_ELNO', ),
                  FORCE=('REAC_NODA', ),
                  RESULTAT=resn)

reac1 = POST_RELEVE_T(ACTION=_F(GROUP_NO=("anchor"),
                               INTITULE='sum reactions',
                               MOMENT=('DRX', 'DRY', 'DRZ'),
                               NOM_CHAM=('REAC_NODA'),
                               OPERATION=('EXTRACTION', ),
                               POINT=(0.0, 0.0, 0.0),
                               RESULTANTE=('DX', 'DY', 'DZ'),
                               RESULTAT=stat))

IMPR_TABLE(FORMAT_R='1PE12.3',
           TABLE=reac1,
           UNITE=8)

reac2 = POST_RELEVE_T(ACTION=_F(GROUP_NO=("net_top"),
                               INTITULE='sum reactions',
                               MOMENT=('DRX', 'DRY', 'DRZ'),
                               NOM_CHAM=('REAC_NODA'),
                               OPERATION=('EXTRACTION', ),
                               POINT=(0.0, 0.0, 0.0),
                               RESULTANTE=('DX', 'DY', 'DZ'),
                               RESULTAT=stat))
                               
IMPR_TABLE(FORMAT_R='1PE12.3',
           TABLE=reac2,
           UNITE=9)  

reac3 = POST_RELEVE_T(ACTION=_F(GROUP_NO=("buoy"),
                               INTITULE='sum reactions',
                               MOMENT=('DRX', 'DRY', 'DRZ'),
                               NOM_CHAM=('REAC_NODA'),
                               OPERATION=('EXTRACTION', ),
                               POINT=(0.0, 0.0, 0.0),
                               RESULTANTE=('DX', 'DY', 'DZ'),
                               RESULTAT=stat))
                               
IMPR_TABLE(FORMAT_R='1PE12.3',
           TABLE=reac3,
           UNITE=10)                    

FIN()
            
    
    
    
    
    ''')


def set_hydrodynamic_model(handel, hydroModel, wake_model, Sn, dwh, dw0, velocities, fluidDensity):
    handel.write('''
NODEnumber=meshinfo['numberOfNodes']
Uinput = ''' + str(velocities) + '''
Fnh= []
l=['None']*((NODEnumber+1))
con = meshinfo['netLines']
sur = meshinfo['netSurfaces']
hdm.row = ''' + str(fluidDensity) + '''  # [kg/m3]   sea water density

    ''')
    if hydroModel.split("-")[1] in ["UDV"]:
        handel.write('''
hdm.screenModel.CD_udv=''' + hydroModel.split('-')[2] + '''
hdm.screenModel.CL_udv=''' + hydroModel.split('-')[3] + '''

        ''')
    if hydroModel.split('-')[0] in ["Screen"]:
        handel.write('''
hydroModel=hdm.screenModel.forceModel("''' + hydroModel.split('-')[1] + '''",sur,''' + str(Sn) + ''',''' + str(dwh) + ''',''' + str(dw0) + ''')
netWakeModel=hdm.wakeModel.net2net("''' + str(wake_model) + '''",meshinfo['netNodes'],sur,Uinput[0],[0,0,0],''' + str(
            dw0) + ''',''' + str(Sn) + ''')
        ''')
    elif hydroModel.split('-')[0] in ["Morison"]:
        handel.write('''
hydroModel=hdm.morisonModel.forceModel("''' + hydroModel.split('-')[1] + '''",con,''' + str(Sn) + ''',''' + str(dwh) + ''',''' + str(dw0) + ''')
netWakeModel=hdm.wakeModel.net2net("''' + str(wake_model) + '''",meshinfo['netNodes'],con,Uinput[0],[0,0,0],''' + str(
            dw0) + ''',''' + str(Sn) + ''')
       ''')
    else:
        print("The selected hydrodynamic model: " + hydroModel.split('-')[0] + " is not supported")
        exit()

    handel.write('''
with open(cwd+'/positionOutput/element_in_wake.txt', "w") as file:
    file.write(str(netWakeModel.get_element_in_wake()))
file.close()
with open(cwd+'/positionOutput/hydro_elements.txt', "w") as file:
    file.write(str(hydroModel.output_hydro_element()))
file.close()

for k in range(0,itimes):
    time_start=time.time()

    INCLUDE(UNITE=91,INFO=0)

    time_end3=time.time()
    time_str = [k, time_end1-time_start,time_end2-time_start,time_end3-time_start]
    
    with open(cwd + '/timing.txt', 'a+') as output_file:
        output_file.write(str(time_str) + os.linesep)
    output_file.close()

IMPR_RESU(FORMAT='MED',
          RESU=_F(CARA_ELEM=elemprop,
                  LIST_INST=listr,
                  NOM_CHAM=('DEPL' ,'SIEF_ELGA'),
                  # TOUT_CMP=(DEPL','ACCE','VITE' ),
                  RESULTAT=resn,
                  TOUT_CMP='OUI'),
          UNITE=80)

stat = CALC_CHAMP(CONTRAINTE=('SIEF_ELNO', ),
                  FORCE=('REAC_NODA', ),
                  RESULTAT=resn)
        ''')


# >>>>>>>>> reaction force >>>>>>>>>>>>
def reaction_force(handel, name_of_nodes):
    handel.write('''
reac = POST_RELEVE_T(ACTION=_F(GROUP_NO=("''' + str(name_of_nodes) + '''"),
                               INTITULE='sum reactions',
                               MOMENT=('DRX', 'DRY', 'DRZ'),
                               NOM_CHAM=('REAC_NODA'),
                               OPERATION=('EXTRACTION', ),
                               POINT=(0.0, 0.0, 0.0),
                               RESULTANTE=('DX', 'DY', 'DZ'),
                               RESULTAT=stat))
IMPR_TABLE(FORMAT_R='1PE12.3',
           TABLE=reac,
           UNITE=8)

FIN()
        ''')


#
# # >>>>>>>>>>>>>>>    DEFI_LIST_INST       >>>>>>>>>>>>
def apply_boundary(handel, loads):
    """
    :param handel: a handel to write the input file
    :param loads: [bc1,bc2,bc3...] a list of bc names
    :return: write the fixed statement to the input fil
    """
    handel.write('''
loadr=[]
                ''')
    for load in loads:
        handel.write('''
loadr.append( _F(CHARGE=''' + str(load) + '''), )
        ''')


# >>>>>>>>>>>>>>>    DYNA_NON_LINE       >>>>>>>>>>>>
def set_dyna_solver(handel, weight_type, maximum_iteration, residuals, method, alpha):
    handel.write('''
if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                    CHAM_MATER=fieldmat,
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),''')
    if weight_type in ['sinkerTube', 'sinkerTube+centerweight', 'tube']:
        handel.write('''
                                  _F(DEFORMATION='PETIT',
                                    GROUP_MA=('bottomring', ),
                                    RELATION='ELAS')''')
    handel.write('''
                                 ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=''' + str(maximum_iteration) + ''' ,
                                   RESI_GLOB_RELA=''' + str(residuals) + ''' ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines',
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="''' + str(method) + '''",
                                   ALPHA=-0.1,
                                   ),
                                   #add damping stablize the oscilations Need to study in the future
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model)
else:
    Fnh=tuple(Fnh)
    for i in range (1,NODEnumber+1):
        grpno = 'node%01g' %i
        l[i]=AFFE_CHAR_MECA( FORCE_NODALE=_F(GROUP_NO= (grpno),
                         FX= Fnh[i-1][0],
                         FY= Fnh[i-1][1],
                         FZ= Fnh[i-1][2],),
                         MODELE=model)
    for i in range (1,NODEnumber+1):
        loadr.append( _F(CHARGE=l[i],), )

    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
    				            CHAM_MATER=fieldmat,
    				            reuse=resn,
                    ETAT_INIT=_F(EVOL_NOLI=resn),
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),''')
    if weight_type in ['sinkerTube', 'sinkerTube+centerweight', 'tube']:
        handel.write('''
                                  _F(DEFORMATION='PETIT',
                                    GROUP_MA=('bottomring', ),
                                    RELATION='ELAS')''')
    handel.write('''
                                 ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=''' + str(maximum_iteration) + ''' ,
                                   RESI_GLOB_RELA=''' + str(residuals) + ''' ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines',
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="''' + str(method) + '''",
                                    ALPHA=-''' + str(alpha) + '''
                                   ),
                                   #add damping stablize the oscilations Need to study in the future
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model,
                    )
        ''')


#
# # >>>>>>>>>>>>>>>>>>>>>> Coupling >>>>>>>>>>>>>>>>>>>
def set_coupling(handel, coupling_switcher, time_thread=0):
    handel.write('''
tblp = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                          INTITULE='Nodal Displacements',    # Name of the table in .resu file
                          RESULTAT=resn,                     # The result from which values will be extracted(STAT_NON_LINE)
                          NOM_CHAM=('DEPL'),                 # Field to extract. DEPL = Displacements
                          #TOUT_CMP='OUI',
                          NOM_CMP=('DX','DY','DZ'),          # Components of DISP to extract
                          GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                          INST=(1+k)*dt,                     # STAT_NON_LINE calculates for 10 INST. I want only last INST
                           ),),
                  );
         
tblp2 = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                          INTITULE='Nodal Displacements',    # Name of the table in .resu file
                          RESULTAT=resn,                     # The result from which values will be extracted(STAT_NON_LINE)
                          NOM_CHAM=('VITE'),                 # Field to extract. VITE = velocity,
                          #TOUT_CMP='OUI',
                          NOM_CMP=('DX','DY','DZ'),          # Components of DISP to extract
                          GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                          INST=(1+k)*dt,                     # STAT_NON_LINE calculates for 10 INST. I want only last INST
                           ),),
                  );
time_end1=time.time()                  
posi=fsi.get_position_aster(tblp)
velo_nodes=fsi.get_velocity_aster(tblp2)
with open(cwd+'/positionOutput/velo_'+str(round((k)*dt,3))+'.txt', "w") as file:
    file.write(str(velo_nodes))
file.close()

    
if k < itimes-1:
    del Fnh
    ''')
    if time_thread in ["0", "false", "no"]:
        handel.write('''
force_increasing_factor=1.0
            ''')
    else:
        handel.write('''
if k*dt< ''' + str(time_thread) + ''':
    force_increasing_factor=k*dt/''' + str(time_thread) + '''
else:
    force_increasing_factor=1.0    
                ''')

    if coupling_switcher in ["False"]:
        handel.write('''
U=Uinput[int(k*dt/duration)]
force_on_element=hydroModel.force_on_element(netWakeModel,posi,U)
Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'],force_increasing_factor)
with open(cwd+'/positionOutput/posi_'+str(round((k)*dt,3))+'.txt', "w") as file:
    file.write(str(posi))
file.close()

        ''')

    elif coupling_switcher in ["simiFSI"]:
        handel.write('''
if k == 0:
    fsi.write_element(hydroModel.output_hydro_element(),cwd)

timeFE=dt*k
U=Uinput[int(k*dt/duration)]
force_on_element=hydroModel.force_on_element(netWakeModel,posi,U,velo_nodes)
Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'],force_increasing_factor)

fsi.write_position(posi,cwd)
fsi.write_fh(force_on_element,timeFE,cwd)

with open(cwd+'/positionOutput/posi_'+str(round((k)*dt,3))+'.txt', "w") as file:
    file.write(str(posi))
file.close()
        ''')

    elif coupling_switcher in ["FSI"]:
        handel.write('''
timeFE=dt*k

if k == 0:
    hydro_element=hydroModel.output_hydro_element()
    Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'],force_increasing_factor)
    force_on_element=hydroModel.force_on_elements
    
    fsi.write_fh(force_on_element,timeFE,cwd)
    fsi.write_element(hydro_element,cwd)
    fsi.write_position(meshinfo['netNodes'],cwd)
else:

    U=fsi.get_velocity(cwd,len(hydro_element),timeFE)
    force_on_element=hydroModel.screen_fsi(posi,U,velo_nodes)
    Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'],force_increasing_factor)

    fsi.write_position(posi,cwd)
    fsi.write_fh(force_on_element,timeFE,cwd)
    with open(cwd+'/positionOutput/posi_'+str(round((k)*dt,3))+'.txt', "w") as file:
        file.write(str(posi))
    file.close()
        ''')


# # >>>>>>>>>>>>>>> midOutput >>>>>>>>>>>>>>>>>>>>>>>>>
def set_save_midresults(handel, saveMid_result):
    if saveMid_result is not False:
        handel.write('''
if ((1+k)*dt)%''' + str(float(saveMid_result)) + '''==0:
    filename = "REPE_OUT/output-"+str((1+k)*dt)+".rmed"
    DEFI_FICHIER(FICHIER=filename, UNITE=180+k,TYPE='BINARY')
    IMPR_RESU(FORMAT='MED',
          UNITE=180+k,
          RESU=_F(CARA_ELEM=elemprop,
                  NOM_CHAM=('DEPL' ,'SIEF_ELGA'),
                  # LIST_INST=listr,
                  INST=(1+k)*dt,
                  RESULTAT=resn,
                  TOUT_CMP='OUI'),
          )
    DEFI_FICHIER(ACTION='LIBERER', UNITE=180+k)


    stat = CALC_CHAMP(CONTRAINTE=('SIEF_ELNO', ),
                      FORCE=('REAC_NODA', ),
                      RESULTAT=resn)
    reac = POST_RELEVE_T(ACTION=_F(GROUP_NO=('topnodes'),
                                   INTITULE='sum reactions',
                                   MOMENT=('DRX', 'DRY', 'DRZ'),
                                   NOM_CHAM=('REAC_NODA'),
                                   OPERATION=('EXTRACTION', ),
                                   POINT=(0.0, 0.0, 0.0),
                                   RESULTANTE=('DX', 'DY', 'DZ'),
                                   RESULTAT=stat))
    IMPR_TABLE(FORMAT_R='1PE12.3',
               TABLE=reac,
               UNITE=9)
    DETRUIRE(CONCEPT=_F( NOM=(stat)))
    DETRUIRE(CONCEPT=_F( NOM=(reac)))
        ''')
    handel.write('''
time_end2=time.time()    
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
DETRUIRE(CONCEPT=_F( NOM=(tblp2)))
if k!=0:
    if k < itimes-1:
        for i in range (1,NODEnumber+1):
            DETRUIRE(CONCEPT=_F( NOM=(l[i])))
        ''')


def set_dyna_solver_fishFarm(handel, alpha, time_thread, coupling_switcher):
    handel.write('''
loadr=[]               
loadr.append( _F(CHARGE=gF), )       
loadr.append( _F(CHARGE=fixed), )       
loadr.append( _F(CHARGE=buoyF), )
loadr.append( _F(CHARGE=sealevel), )
loadr.append( _F(CHARGE=sinkF1), )
loadr.append( _F(CHARGE=sinkF2), )
        
if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                    CHAM_MATER=fieldmat,
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines','anchorLines','frameLines','bridlesH','bridlesV','buoyLines'),
                                    RELATION='CABLE'),
                                  _F(DEFORMATION='PETIT',
                                    GROUP_MA=('topRings','bottomRings','links'),
                                    RELATION='ELAS')
                                 ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=1000 ,
                                   RESI_GLOB_RELA=2e-05 ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines',
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="HHT",
                                   ALPHA=-0.1,
                                   ),
                                   #add damping stablize the oscilations Need to study in the future
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model)
else:
    Fnh=tuple(Fnh)
    for i in range (1,NODEnumber+1):
        grpno = 'node%01g' %i
        l[i]=AFFE_CHAR_MECA( FORCE_NODALE=_F(GROUP_NO= (grpno),
                         FX= Fnh[i-1][0],
                         FY= Fnh[i-1][1],
                         FZ= Fnh[i-1][2],),
                         MODELE=model)
    for i in range (1,NODEnumber+1):
        loadr.append( _F(CHARGE=l[i],), )

    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
    				     CHAM_MATER=fieldmat,
    				     reuse=resn,
                    ETAT_INIT=_F(EVOL_NOLI=resn),
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines','anchorLines','frameLines','bridlesH','bridlesV','buoyLines'),
                                    RELATION='CABLE'),
                                  _F(DEFORMATION='PETIT',
                                    GROUP_MA=('topRings','bottomRings','links'),
                                    RELATION='ELAS')
                                 ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=1000 ,
                                   RESI_GLOB_RELA=2e-05 ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines',
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="HHT",
                                    ALPHA=-''' + str(alpha) + '''
                                   ),
                                   #add damping stablize the oscilations Need to study in the future
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model,
                    )
        
tblp = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                          INTITULE='Nodal Displacements',    # Name of the table in .resu file
                          RESULTAT=resn,                     # The result from which values will be extracted(STAT_NON_LINE)
                          NOM_CHAM=('DEPL'),                 # Field to extract. DEPL = Displacements
                          #TOUT_CMP='OUI',
                          NOM_CMP=('DX','DY','DZ'),          # Components of DISP to extract
                          GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                          INST=(1+k)*dt,                     # STAT_NON_LINE calculates for 10 INST. I want only last INST
                           ),),
                  )
tblp2 = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                          INTITULE='Nodal Displacements',    # Name of the table in .resu file
                          RESULTAT=resn,                     # The result from which values will be extracted(STAT_NON_LINE)
                          NOM_CHAM=('VITE'),                 # Field to extract. VITE = velocity,
                          #TOUT_CMP='OUI',
                          NOM_CMP=('DX','DY','DZ'),          # Components of DISP to extract
                          GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                          INST=(1+k)*dt,                     # STAT_NON_LINE calculates for 10 INST. I want only last INST
                           ),),
                  )

posi=fsi.get_position_aster(tblp)
velo_nodes=fsi.get_velocity_aster(tblp2)


if k < itimes-1:
    del Fnh
        ''')

    if time_thread in ["0", "false", "no"]:
        handel.write('''
force_increasing_factor=1.0
            ''')
    else:
        handel.write('''
if k*dt< ''' + str(time_thread) + ''':
    force_increasing_factor=k*dt/''' + str(time_thread) + '''
else:
    force_increasing_factor=1.0    
                ''')

    if coupling_switcher in ["False"]:
        handel.write('''
U=Uinput[int(k*dt/duration)]

force_on_netting=hydroModel_netting.force_on_element(netWakeModel,posi,U)
force_on_mooring=hydroModel_mooring.force_on_element(netWakeModel,posi,U)

Fnh=hydroModel_netting.distribute_force(NODEnumber,force_increasing_factor)+hydroModel_mooring.distribute_force(NODEnumber)
with open(cwd+'/positionOutput/posi'+str(round((k)*dt,3))+'.txt', "w") as file:
    file.write(str(posi))
file.close()
    ''')
    elif coupling_switcher in ["simiFSI"]:
        handel.write('''
if k == 0:
    hydro_element=hydroModel_netting.output_hydro_element()
    fsi.write_element(hydro_element,cwd)
    
timeFE=dt*k
U=Uinput[int(k*dt/duration)]
force_on_netting=hydroModel_netting.force_on_element(netWakeModel,posi,U,velo_nodes)
force_on_mooring=hydroModel_mooring.force_on_element(netWakeModel,posi,U)
Fnh=hydroModel_netting.distribute_force(NODEnumber,force_increasing_factor)+hydroModel_mooring.distribute_force(NODEnumber)

fsi.write_position(posi,cwd)
fsi.write_fh(force_on_netting,timeFE,cwd)

with open(cwd+'/positionOutput/posi_'+str(round((k)*dt,3))+'.txt', "w") as file:
    file.write(str(posi))
file.close()
            ''')

    elif coupling_switcher in ["FSI"]:
        handel.write('''
timeFE=dt*k
if k == 0:
    hydro_element=hydroModel_netting.output_hydro_element()
    force_on_netting=hydroModel_netting.force_on_elements
    Fnh=hydroModel_netting.distribute_force(NODEnumber,force_increasing_factor)+hydroModel_mooring.distribute_force(NODEnumber)
    
    fsi.write_fh(force_on_netting,timeFE,cwd)
    fsi.write_element(hydro_element,cwd)
    fsi.write_position(posi,cwd)
else:

    U=fsi.get_velocity(cwd,len(hydro_element),timeFE)
    force_on_netting=hydroModel.screen_fsi(posi,U,velo_nodes)
    force_on_mooring=hydroModel_mooring.force_on_element(netWakeModel,posi,Uinput[int(k*dt/duration)])
    
    Fnh=hydroModel_netting.distribute_force(NODEnumber,force_increasing_factor)+hydroModel_mooring.distribute_force(NODEnumber)

    fsi.write_position(posi,cwd)
    fsi.write_fh(force_on_netting,timeFE,cwd)
    with open(cwd+'/positionOutput/posi_'+str(round((k)*dt,3))+'.txt', "w") as file:
        file.write(str(posi))
    file.close()
        ''')

    handel.write('''      
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
DETRUIRE(CONCEPT=_F( NOM=(tblp2)))
if k!=0:
    if k < itimes-1:
        for i in range (1,NODEnumber+1):
            DETRUIRE(CONCEPT=_F( NOM=(l[i])))
    ''')

# >>>>>>>>>>>>>>>    ASTERRUN.export       >>>>>>>>>>>>
def set_export(handel, rdnumber, hostname, username, cwd, solver_version, mesh_name):
    handel.write('''P actions make_etude
P aster_root ''' + workPath.aster_path[:-25] + '''
P consbtc oui
P corefilesize unlimited
P cpresok RESNOOK
P debug nodebug
P display ''' + str(hostname) + ''':0
P facmtps 1
P lang en
P mclient ''' + str(hostname) + '''
P memjob 5224448
P memory_limit 5102.0
P mode interactif
P mpi_nbcpu 1
P mpi_nbnoeud 1
P nbmaxnook 5
P ncpus 2
P noeud ''' + str(hostname) + '''
P nomjob astk
P origine ASTK 2019.0.final
P platform LINUX64
P profastk ''' + str(username) + '''@''' + str(hostname) + ''':''' + cwd + '''/run.astk
P protocol_copyfrom asrun.plugins.server.SCPServer
P protocol_copyto asrun.plugins.server.SCPServer
P protocol_exec asrun.plugins.server.SSHServer
P proxy_dir /tmp
P rep_trav /tmp/hui-UiS-interactif_1''' + str(rdnumber) + '''
P serveur ''' + str(hostname) + '''
P soumbtc oui
P time_limit 9000060.0
P tpsjob 1501
P uclient ''' + str(username) + '''
P username ''' + str(username) + '''
P version ''' + str(solver_version) + '''
A args
A memjeveux 637.75
A tpmax 9000000.0
F mmed ''' + cwd + '''/asterinput/''' + str(mesh_name) + ''' D 20
F comm ''' + cwd + '''/asterinput/ASTER1.py D 1
F libr ''' + cwd + '''/asterinput/ASTER2.py D 91
F libr ''' + cwd + '''/asterinput/meshInformation.py D 90
R repe ''' + cwd + '''/midOutput/REPE_OUT D  0
R repe ''' + cwd + '''/midOutput/REPE_OUT R  0
F resu ''' + cwd + '''/midOutput/reactionforce.txt R 9
F rmed ''' + cwd + '''/asteroutput/paravisresults.rmed R 80
F resu ''' + cwd + '''/asteroutput/reactionforce.txt R 8
F mess ''' + cwd + '''/asteroutput/mess.log R 6\n''')

# might be used in export file
# P classe
# P depart
# P after_job
# P distrib
# P exectool
# P multiple
# P only_nook
