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


# >>>>>>>>>>>>>>>    AFFE_CARA_ELEM       >>>>>>>>>>>>
def define_element(handel, weight_type, twine_section, bottom_radius):
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
def define_material(handel, weight_type, net_module, net_rho, bottom_module, bottom_rho):
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

NODEnumber=meshinfo['numberOfNodes']
''')
def set_hydrodynamic_model(handel,hydroModel, wake_model, Sn, dwh, dw0, velocities,fluidDensity):
    handel.write('''
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
def set_coupling(handel, coupling_switcher):
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
posi=fsi.get_position_aster(tblp)
velo_nodes=fsi.get_velocity_aster(tblp2)

if k < itimes-1:
    del Fnh

    ''')
    if coupling_switcher in ["False"]:
        handel.write('''
U=Uinput[int(k*dt/duration)]
force_on_element=hydroModel.force_on_element(netWakeModel,posi,U)
Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'])
with open(cwd+'/positionOutput/posi'+str((k)*dt)+'.txt', "w") as file:
    file.write(str(posi))
file.close()

        ''')

    elif coupling_switcher in ["simiFSI"]:
        handel.write('''
if k == 0:
    fsi.write_element(hydroModel.output_hydro_element(),cwd)

timeFE=dt*k
U=Uinput[int(k*dt/duration)]
force_on_element=hydroModel.force_on_element(netWakeModel,posi,U)
Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'])

fsi.write_position(posi,cwd)
fsi.write_fh(force_on_element,timeFE,cwd)

with open(cwd+'/positionOutput/posi'+str((k)*dt)+'.txt', "w") as file:
    file.write(str(posi))
file.close()
        ''')

    elif coupling_switcher in ["FSI"]:
        handel.write('''
if k == 0:
    hydro_element=hydroModel.output_hydro_element()
    Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'])

    fsi.write_element(hydro_element,cwd)
    fsi.write_position(meshinfo['netNodes'],cwd)
else:
    timeFE=dt*k
    U=fsi.get_velocity(cwd,len(hydro_element),timeFE)
    force_on_element=hydroModel.screen_fsi(posi,U,velo_nodes)
    Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'])

    fsi.write_position(posi,cwd)
    fsi.write_fh(force_on_element,timeFE,cwd)
    with open(cwd+'/positionOutput/posi'+str((k)*dt)+'.txt', "w") as file:
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
P ncpus 10
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
