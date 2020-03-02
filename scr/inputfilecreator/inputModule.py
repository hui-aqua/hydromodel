"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import os
import sys
import random as rd
import workPath
import numpy as np
import socket
import getpass


cwd = os.getcwd()
argument = sys.argv

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = eval(content)

with open(cwd + '/meshinfomation.txt', 'r') as f:
    content = f.read()
    meshInfo = eval(content)
switcher = cageInfo['Solver']['coupling']
hydroModel = str(cageInfo['Net']['HydroModel'])

Fbuoy = meshInfo['horizontalElementLength'] * meshInfo['verticalElementLength'] * cageInfo['Net']['Sn'] / \
        cageInfo['Net']['twineDiameter'] * 0.25 * np.pi * pow(cageInfo['Net']['twineDiameter'], 2) * 9.81 * float(
    cageInfo['Environment']['fluidDensity'])
# Buoyancy force to assign on each nodes
dwh = meshInfo['horizontalElementLength'] * meshInfo['verticalElementLength'] * cageInfo['Net']['Sn'] / (
        meshInfo['horizontalElementLength'] + meshInfo['verticalElementLength'])
# hydrodynamic diameter to calculate the hydrodynamic coefficient.
lam1 = meshInfo['horizontalElementLength'] / cageInfo['Net']['meshLength']
lam2 = meshInfo['verticalElementLength'] / cageInfo['Net']['meshLength']
dws = np.sqrt(2 * lam1 * lam2 / (lam1 + lam2)) * cageInfo['Net']['twineDiameter']
twineSection = 0.25 * np.pi * pow(dws, 2)
dt = cageInfo['Solver']['timeStep']  # time step

# >>>>>>>>>>>>>>>>> Sequence run >>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>> Start to write input file>>>>>>>>>>>>
output_file = open(cwd + '/ASTER1.comm', 'w')
output_file.write('''
import sys
import numpy as np
sys.path.append("''' + workPath.forceModel_path + '''")
import hydro4c1 as hy
import fsimapping as fsi
cwd="''' + cwd + '''/"
DEBUT(PAR_LOT='NON',
IGNORE_ALARM=("SUPERVIS_25","DISCRETE_26","UTILITAI8_56") 
)
mesh = LIRE_MAILLAGE(UNITE=20)''')
output_file.write('\n')
output_file.close()

# >>>>>>>>>>>>>>>    AFFE_MODELE       >>>>>>>>>>>>
if cageInfo['Weight']['weightType'] in ['sinkers', 'allfixed']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'),
                             MODELISATION=('CABLE'),
                             PHENOMENE='MECANIQUE'),
                          ),
                    MAILLAGE=mesh)
''')
    output_file.close()
elif cageInfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'), 
                             MODELISATION=('CABLE'), 
                             PHENOMENE='MECANIQUE'), 
                          _F(GROUP_MA=('bottomring'), 
                             MODELISATION=('POU_D_E'), 
                             PHENOMENE='MECANIQUE')
                          ), 
                    MAILLAGE=mesh)
''')
    output_file.close()
else:
    print("Warning!!! >>>>>AFFE_MODELE")
    print("The present weight type '" + cageInfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")

# >>>>>>>>>>>>>>>    AFFE_CARA_ELEM       >>>>>>>>>>>>
if cageInfo['Weight']['weightType'] in ['sinkers', 'allfixed']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=''' + str(twineSection) + '''),
                          MODELE=model)
''')
    output_file.close()
elif cageInfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=''' + str(twineSection) + '''),
                          POUTRE=_F(GROUP_MA=('bottomring', ), 
                                    SECTION='CERCLE', 
                                    CARA=('R', 'EP'), 
                                    VALE=(''' + str(cageInfo['Weight']["bottomRingRadius"]) + ''', ''' + str(
        cageInfo['Weight']["bottomRingRadius"]) + ''')),
                          MODELE=model)
''')
    output_file.close()
else:
    print("Warning!!! >>>>>AFFE_CARA_ELEM")
    print("The present weight type '" + cageInfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")

# >>>>>>>>>>>>>>>    DEFI_MATERIAU       >>>>>>>>>>>>
if cageInfo['Weight']['weightType'] in ['sinkers', 'allfixed']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(cageInfo['Net']["netYoungmodule"]) + ''', NU=0.2,RHO=''' + str(
        cageInfo['Net']["netRho"]) + '''))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0)) 
''')
    output_file.close()
elif cageInfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(cageInfo['Net']["netYoungmodule"]) + ''', NU=0.2,RHO=''' + str(
        cageInfo['Net']["netRho"]) + '''))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0)) 
fe = DEFI_MATERIAU(ELAS=_F(E=''' + str(cageInfo['Weight']["bottomRingYoungModule"]) + ''', 
                           NU=0.3,
                           RHO=''' + str(cageInfo['Weight']["bottomRingRho"]) + '''))  
''')
    output_file.close()
else:
    print("Warning!!! >>>>>DEFI_MATERIAU")
    print("The present weight type '" + cageInfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")

# >>>>>>>>>>>>>>>    AFFE_MATERIAU       >>>>>>>>>>>>
if cageInfo['Weight']['weightType'] in ['sinkers', 'allfixed']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(net)),
                               ),
                         MODELE=model) 
''')
    output_file.close()
elif cageInfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(net)),
                               _F(GROUP_MA=('bottomring'),
                                 MATER=(fe)),
                               ),
                         MODELE=model) 
''')
    output_file.close()
else:
    print("Warning!!! >>>>>AFFE_MATERIAU")
    print("The present weight type '" + cageInfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")

# >>>>>>>>>>>>>>>    AFFE_CHAR_MECA       >>>>>>>>>>>>
output_file = open(cwd + '/ASTER1.comm', 'a')
output_file.write('''
selfwigh = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                       GRAVITE=9.81,
                                       GROUP_MA=('twines')),
                      MODELE=model)  
buoyF= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('allnodes'),
                                      FZ=''' + str(Fbuoy) + '''), 
                      MODELE=model)                                         
''')
output_file.close()
# >>>>>>>>>>>>>>>    AFFE_CHAR_MECA    fixed >>>>>>>>>>>>
if cageInfo['Mooring']['mooringType'] in ['None']:
    if cageInfo['Weight']['weightType'] in ['allfixed']:
        output_file = open(cwd + '/ASTER1.comm', 'a')
        output_file.write('''
fix = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_NO=('allnodes'),
                                         LIAISON='ENCASTRE'),
                             MODELE=model)
        ''')
        output_file.close()
    else:
        output_file = open(cwd + '/ASTER1.comm', 'a')
        output_file.write('''
fix = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_MA=('topring'),
                                             LIAISON='ENCASTRE'),
                                 MODELE=model)
            ''')
        output_file.close()

else:
    print("Warning!!! >>>>>AFFE_CHAR_MECA    fixed ")
    print('need to update the script')
    exit()

# >>>>>>>>>>>>>>>    AFFE_CHAR_MECA    weight   >>>>>>>>>>>>
if cageInfo['Weight']['weightType'] in ['sinkers']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
sinkF = AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('sinkers'),  
                                      FZ=-''' + str(cageInfo['Weight']["sinkerWeight"]) + ''',
                                      FX=0,
                                      FY=0,
                                      ), 
                      MODELE=model) 
    ''')
    output_file.close()
elif cageInfo['Weight']['weightType'] in ['sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
sinkF = AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('bottomtip'),  
                                      FZ=-''' + str(cageInfo['Weight']["tipWeight"]) + ''',
                                      FX=0,
                                      FY=0,
                                      ), 
                      MODELE=model) 
    ''')
    output_file.close()
else:
    pass

# >>>>>>>>>>>>>>>    DEFI_LIST_INST       >>>>>>>>>>>>
output_file = open(cwd + '/ASTER1.comm', 'a')
output_file.write('''
dt=''' + str(dt) + '''      # time step
# itimes is the total iterations
itimes=''' + str(
    int(cageInfo['Solver']['timeLength'] / dt * int(np.array(cageInfo['Environment']['current']).size / 3))) + '''   
tend=itimes*dt

listr = DEFI_LIST_REEL(DEBUT=0.0,
                       INTERVALLE=_F(JUSQU_A=tend,PAS=dt))

times = DEFI_LIST_INST(DEFI_LIST=_F(LIST_INST=listr,PAS_MINI=1e-8),
                       METHODE='AUTO')
                       
NODEnumber=''' + str(meshInfo["numberOfNodes"]) + '''
Fnh= np.zeros((NODEnumber,3)) # initial hydrodynamic forces=0
l=['None']*((len(Fnh)+1))

for k in range(0,itimes):
    Fnh=tuple(Fnh)    
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
output_file.close()

# >>>>>>>>> reaction force >>>>>>>>>>>>
if cageInfo['Mooring']['mooringType'] in ['None']:
    if cageInfo['Weight']['weightType'] in ['allfixed']:
        output_file = open(cwd + '/ASTER1.comm', 'a')
        output_file.write('''
reac = POST_RELEVE_T(ACTION=_F(GROUP_NO=('allnodes'),
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
        output_file.close()
    else:
        output_file = open(cwd + '/ASTER1.comm', 'a')
        output_file.write('''
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
           UNITE=8)

FIN()  
            ''')
    output_file.close()

else:
    print("Warning!!! >>>>>reaction force")
    print('need to update the script')

# >>>>>>>>>>>>>>>    DEFI_LIST_INST       >>>>>>>>>>>>
output_file = open(cwd + "/ASTER2.comm", 'w')
output_file.write('''
for i in range (1,len(Fnh)+1):
    grpno = 'node%01g' %i
    l[i]=AFFE_CHAR_MECA( FORCE_NODALE=_F(GROUP_NO= (grpno),
                         FX= Fnh[i-1][0],
                         FY= Fnh[i-1][1],
                         FZ= Fnh[i-1][2],),
                         MODELE=model)    
loadr=[]
loadr.append( _F(CHARGE=fix), )
loadr.append( _F(CHARGE=selfwigh), )
loadr.append( _F(CHARGE=buoyF), )
for i in range (1,len(Fnh)+1):    
    loadr.append( _F(CHARGE=l[i],), )
''')
output_file.close()
if cageInfo['Weight']['weightType'] in ['sinkers', 'sinkerTube+centerweight']:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
loadr.append( _F(CHARGE=sinkF), )
    ''')
    output_file.close()
else:
    pass

# >>>>>>>>>>>>>>>    DYNA_NON_LINE       >>>>>>>>>>>>
if cageInfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                    CHAM_MATER=fieldmat,
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                  _F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('bottomring', ),
                                    RELATION='ELAS')
                                  ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=''' + str(cageInfo['Solver']['MaximumIteration']) + ''' ,
                                   RESI_GLOB_RELA=''' + str(cageInfo['Solver']['Residuals']) + ''' ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="''' + str(cageInfo['Solver']['method']) + '''",
                                   ALPHA=-0.1,
                                   ),
                                   #add damping stablize the oscilations Need to study in the future                        
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model)
else:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
    				            CHAM_MATER=fieldmat,
    				            reuse=resn,
                    ETAT_INIT=_F(EVOL_NOLI=resn),
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                  _F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('bottomring', ),
                                    RELATION='ELAS')
                                  ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=''' + str(cageInfo['Solver']['MaximumIteration']) + ''' ,
                                   RESI_GLOB_RELA=''' + str(cageInfo['Solver']['Residuals']) + ''' ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="''' + str(cageInfo['Solver']['method']) + '''",
                                    ALPHA=-''' + str(cageInfo['Solver']['alptha']) + '''
                                   ),
                                   #add damping stablize the oscilations Need to study in the future                        
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model,
                    )
        ''')
    output_file.close()
else:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                    CHAM_MATER=fieldmat,
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                  ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=''' + str(cageInfo['Solver']['MaximumIteration']) + ''' ,
                                   RESI_GLOB_RELA=''' + str(cageInfo['Solver']['Residuals']) + ''' ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="''' + str(cageInfo['Solver']['method']) + '''",
                                   ALPHA=-0.1,
                                   ),
                                   #add damping stablize the oscilations Need to study in the future                        
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model)
else:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
    				CHAM_MATER=fieldmat,
    				reuse=resn,
                    ETAT_INIT=_F(EVOL_NOLI=resn),
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                  ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=''' + str(cageInfo['Solver']['MaximumIteration']) + ''' ,
                                   RESI_GLOB_RELA=''' + str(cageInfo['Solver']['Residuals']) + ''' ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="''' + str(cageInfo['Solver']['method']) + '''",
                                    ALPHA=-''' + str(cageInfo['Solver']['alptha']) + '''
                                   ),
                                   #add damping stablize the oscilations Need to study in the future                        
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model,
                    )         
    ''')
    output_file.close()

# >>>>>>>>>>>>>>>    POST_RELEVE_T       >>>>>>>>>>>>
output_file = open(cwd + "/ASTER2.comm", 'a')
output_file.write('''
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

if k < itimes-1:
    del Fnh
posi=hy.get_position(tblp)  
velo_nodes=hy.get_velocity(tblp2)

if k==0:
    con=''' + str(meshInfo['netLines']) + ''' 
    sur=''' + str(meshInfo['netSurfaces']) + '''
    Uinput=''' + str(cageInfo['Environment']['current']) + '''
    hydroModel=hy.Hydro''' + hydroModel.split('-')[0] + '''("''' + hydroModel.split('-')[1] + '''",posi,sur,''' + str(
    cageInfo['Net']['Sn']) + ''',np.array(Uinput[0]),''' + str(
    dwh) + ''',''' + str(
    cageInfo['Net']['twineDiameter']) + ''')
    elementinwake=hydroModel.output_element_in_wake()
    np.savetxt(cwd+'/positionOutput/elementinwake.txt', elementinwake)       
    hydro_element=hydroModel.output_hydro_element()
    ''')
output_file.close()

# >>>>>>>>>>>>>>>>>>>>>> Coupling >>>>>>>>>>>>>>>>>>>
if switcher in ["False"]:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
U=np.array(Uinput[int(k*dt/10.0)])
force_on_element=hydroModel.force_on_element(posi,velo_nodes,U)
Fnh=hydroModel.distribute_force()
np.savetxt(cwd+'positionOutput/posi'+str((k)*dt)+'.txt', posi)
        ''')
    output_file.close()


elif switcher in ["simiFSI"]:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
    fsi.write_element(hydro_element,cwd)
timeFE=dt*k    
U=np.array(Uinput[int(k*dt/10.0)])
force_on_element=hydroModel.force_on_element(posi,velo_nodes,U)
Fnh=hydroModel.distribute_force()
fsi.write_position(posi,cwd)
np.savetxt(cwd+'positionOutput/posi'+str((k)*dt)+'.txt', posi)
        ''')
    output_file.close()

elif switcher in ["FSI"]:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
    fsi.write_position(posi,cwd)
    fsi.write_element(hydro_element,cwd)
    U=np.array(Uinput[0])
    fsi.write_fh(np.zeros((len(hydro_element),3)),0,cwd)
    

timeFE=dt*k
U=fsi.get_velocity(cwd,len(hydro_element),timeFE)
force_on_element=hydroModel.screen_fsi(posi,U,velo_nodes)
Fnh=hydroModel.distribute_force()
fsi.write_position(posi,cwd)
fsi.write_fh(force_on_element,timeFE,cwd)
np.savetxt(cwd+'positionOutput/posi'+str((k)*dt)+'.txt', posi)
        ''')
    output_file.close()
# >>>>>>>>>>>>>>> midOutput >>>>>>>>>>>>>>>>>>>>>>>>>

output_file = open(cwd + "/ASTER2.comm", 'a')
output_file.write('''

filename = "REPE_OUT/output.rmed"
DEFI_FICHIER(FICHIER=filename, UNITE=180,TYPE='BINARY')
IMPR_RESU(FORMAT='MED', 
          UNITE=180, 
          RESU=_F(CARA_ELEM=elemprop,
                  NOM_CHAM=('DEPL' ,'SIEF_ELGA'),
                  LIST_INST=listr, 
                  RESULTAT=resn,
                  TOUT_CMP='OUI'),
          )
DEFI_FICHIER(ACTION='LIBERER', UNITE=180)

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
        
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
DETRUIRE(CONCEPT=_F( NOM=(tblp2)))
DETRUIRE(CONCEPT=_F( NOM=(stat)))
DETRUIRE(CONCEPT=_F( NOM=(reac)))

if k < itimes-1:
    for i in range (1,len(Fnh)+1):
        DETRUIRE(CONCEPT=_F( NOM=(l[i])))
        ''')
output_file.close()

# >>>>>>>>>>>>>>>    ASTERRUN.export       >>>>>>>>>>>>
suffix = rd.randint(1, 10000)
output_file = open(cwd + '/ASTERRUN.export', 'w')
output_file.write('''P actions make_etude
P aster_root ''' + workPath.aster_path[:-25] + '''
P consbtc oui
P corefilesize unlimited
P cpresok RESNOOK
P debug nodebug
P display ''' + socket.gethostname() + ''':0
P facmtps 1
P lang en
P mclient ''' + socket.gethostname() + '''
P memjob 5224448
P memory_limit 5102.0
P mode interactif
P mpi_nbcpu 1
P mpi_nbnoeud 1
P nbmaxnook 5
P ncpus 10
P noeud ''' + socket.gethostname() + '''
P nomjob astk
P origine ASTK 2019.0.final
P platform LINUX64
P profastk ''' + getpass.getuser()+ '''@''' + socket.gethostname() + ''':''' + cwd + '''/run.astk
P protocol_copyfrom asrun.plugins.server.SCPServer
P protocol_copyto asrun.plugins.server.SCPServer
P protocol_exec asrun.plugins.server.SSHServer
P proxy_dir /tmp
P rep_trav /tmp/hui-UiS-interactif_1''' + str(suffix) + '''
P serveur ''' + socket.gethostname() + '''
P soumbtc oui
P time_limit 9000060.0
P tpsjob 1501
P uclient ''' + getpass.getuser()+ '''
P username ''' + getpass.getuser()+ '''
P version ''' + str(cageInfo['Solver']['version']) + '''
A args 
A memjeveux 637.75
A tpmax 9000000.0
F mmed ''' + cwd + '''/asterinput/''' + str(meshInfo['meshName']) + ''' D 20
F comm ''' + cwd + '''/asterinput/ASTER1.comm D 1
F libr ''' + cwd + '''/asterinput/ASTER2.comm D 91
R repe ''' + cwd + '''/midOutput/REPE_OUT D  0
R repe ''' + cwd + '''/midOutput/REPE_OUT R  0
F resu ''' + cwd + '''/midOutput/reactionforce.txt R 9
F rmed ''' + cwd + '''/asteroutput/paravisresults.rmed R 80
F resu ''' + cwd + '''/asteroutput/reactionforce.txt R 8
F mess ''' + cwd + '''/asteroutput/mess.log R 6\n''')
output_file.write('\n')
output_file.close()

# might be used in export file
# P classe
# P depart
# P after_job
# P distrib
# P exectool
# P multiple
# P only_nook
