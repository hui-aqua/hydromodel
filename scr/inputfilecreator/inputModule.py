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

switcher = str(sys.argv[1])
if switcher not in ["FE", "FSI", "simiFSI"]:
    print("The argument are not recognized by the program, Please use one of the following argements: \n"
          "Available arguments:\n"
          "1. FE\n"
          "2. FSI\n"
          "3. simiFSI\n")
    exit()
cwd = os.getcwd()
with open(cwd + '/meshinfomation.txt', 'r') as f:
    content = f.read()
    meshinfo = eval(content)

with open(cwd + '/cageDict', 'r') as f:
    content = f.read()
    cageinfo = eval(content)

Fbuoy = meshinfo['horizontalElementLength'] * meshinfo['verticalElementLength'] * cageinfo['Net']['Sn'] / \
        cageinfo['Net']['twineDiameter'] * 0.25 * np.pi * pow(cageinfo['Net']['twineDiameter'], 2) * 9.81 * float(
    cageinfo['Environment']['fluidDensity'])
# Buoyancy force to assign on each nodes
dwh = meshinfo['horizontalElementLength'] * meshinfo['verticalElementLength'] * cageinfo['Net']['Sn'] / (
        meshinfo['horizontalElementLength'] + meshinfo['verticalElementLength'])
# hydrodynamic diameter to calculate the hydrodynamic coefficient.
lam1 = meshinfo['horizontalElementLength'] / cageinfo['Net']['meshLength']
lam2 = meshinfo['verticalElementLength'] / cageinfo['Net']['meshLength']
dws = np.sqrt(2 * lam1 * lam2 / (lam1 + lam2)) * cageinfo['Net']['twineDiameter']
twineSection = 0.25 * np.pi * pow(dws, 2)
dt = 0.01  # time step


# >>>>>>>>>>>>>>>>> Sequence run >>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>> Start to write input file>>>>>>>>>>>>
output_file = open(cwd + '/ASTER1.comm', 'w')
output_file.write('''
import sys
import numpy as np
sys.path.append("''' + workPath.forceModel_path + '''")
import hydro4c1 as hy
cwd="''' + cwd + '''/"
DEBUT(PAR_LOT='NON',
IGNORE_ALARM=("SUPERVIS_25","DISCRETE_26") )
mesh = LIRE_MAILLAGE(UNITE=20)''')
output_file.write('\n')
output_file.close()

# >>>>>>>>>>>>>>>    AFFE_MODELE       >>>>>>>>>>>>
if cageinfo['Weight']['weightType'] in ['sinkers']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'),
                             MODELISATION=('CABLE'),
                             PHENOMENE='MECANIQUE'),
                          ),
                    MAILLAGE=mesh)
''')
    output_file.close()
elif cageinfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
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
    print("The present weight type '" + cageinfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")


# >>>>>>>>>>>>>>>    AFFE_CARA_ELEM       >>>>>>>>>>>>
if cageinfo['Weight']['weightType'] in ['sinkers']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=''' + str(twineSection) + '''),
                          MODELE=model)
''')
    output_file.close()
elif cageinfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=''' + str(twineSection) + '''),
                          POUTRE=_F(GROUP_MA=('bottomring', ), 
                                    SECTION='CERCLE', 
                                    CARA=('R', 'EP'), 
                                    VALE=(''' + str(cageinfo['Weight']["bottomRingRadius"]) + ''', ''' + str(
            cageinfo['Weight']["bottomRingRadius"]) + ''')),
                          MODELE=model)
''')
    output_file.close()
else:
    print("The present weight type '" + cageinfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")

# >>>>>>>>>>>>>>>    DEFI_MATERIAU       >>>>>>>>>>>>
if cageinfo['Weight']['weightType'] in ['sinkers']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(cageinfo['Net']["netYoungmodule"]) + ''', NU=0.2,RHO=''' + str(
            cageinfo['Net']["netRho"]) + '''))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0)) 
''')
    output_file.close()
elif cageinfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(cageinfo['Net']["netYoungmodule"]) + ''', NU=0.2,RHO=''' + str(
            cageinfo['Net']["netRho"]) + '''))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0)) 
fe = DEFI_MATERIAU(ELAS=_F(E=''' + str(cageinfo['Weight']["bottomRingYoungModule"]) + ''', 
                           NU=0.3,
                           RHO=''' + str(cageinfo['Weight']["bottomRingRho"]) + '''))  
''')
    output_file.close()
else:
    print("The present weight type '" + cageinfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")


# >>>>>>>>>>>>>>>    AFFE_MATERIAU       >>>>>>>>>>>>
if cageinfo['Weight']['weightType'] in ['sinkers']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(net)),
                               ),
                         MODELE=model) 
''')
    output_file.close()
elif cageinfo['Weight']['weightType'] in ['sinkerTube', 'sinkerTube+centerweight']:
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
    print("The present weight type '" + cageinfo['Weight']['weightType'] + "' is not included in the present program, "
                                                                           "Please check the guide for input file.")



# >>>>>>>>>>>>>>>    AFFE_CHAR_MECA       >>>>>>>>>>>>
output_file = open(cwd + '/ASTER1.comm', 'a')
output_file.write('''
fix = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_MA=('topring'),
                                 LIAISON='ENCASTRE'),
                     MODELE=model)
selfwigh = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                       GRAVITE=9.81,
                                       GROUP_MA=('twines')),
                      MODELE=model)  
buoyF= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('allnodes'),
                                      FZ=''' + str(Fbuoy) + '''), 
                      MODELE=model)                                         
''')
output_file.close()
if cageinfo['Weight']['weightType'] in ['sinkers']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
sinkF = AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('sinkers'),  
                                      FZ=-''' + str(cageinfo['Weight']["sinkerWeight"]) + ''',
                                      FX=0,
                                      FY=0,
                                      ), 
                      MODELE=model) 
    ''')
    output_file.close()
elif cageinfo['Weight']['weightType'] in ['sinkerTube+centerweight']:
    output_file = open(cwd + '/ASTER1.comm', 'a')
    output_file.write('''
sinkF = AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('bottomtip'),  
                                      FZ=-''' + str(cageinfo['Weight']["tipWeight"]) + ''',
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
dt=''' + str(dt) + '''      # frequency to update the hydrodynamic forces
itimes=''' + str(int(1.0 / dt * len(cageinfo['Environment']['current']))) + '''   
tend=itimes*dt

listr = DEFI_LIST_REEL(DEBUT=0.0,
                       INTERVALLE=_F(JUSQU_A=tend,PAS=dt))

times = DEFI_LIST_INST(DEFI_LIST=_F(LIST_INST=listr,PAS_MINI=1e-8),
                       METHODE='AUTO')
                       
NODEnumber=''' + str(meshinfo["numberOfNodes"]) + '''
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

# >>>>>>>>>>>>>>>    DEFI_LIST_INST       >>>>>>>>>>>>
output_file = open(cwd+"/ASTER2.comm", 'w')
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
if cageinfo['Weight']['weightType'] in ['sinkers','sinkerTube+centerweight']:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
loadr.append( _F(CHARGE=sinkF), )
    ''')
    output_file.close()
else:
    pass

# >>>>>>>>>>>>>>>    DYNA_NON_LINE       >>>>>>>>>>>>
if cageinfo['Weight']['weightType'] in ['sinkerTube','sinkerTube+centerweight']:
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
                    CONVERGENCE=_F(ITER_GLOB_MAXI=1000,
                                   RESI_GLOB_RELA=2e-05),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+0.10,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA='HHT',
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
                   CONVERGENCE=_F(ITER_GLOB_MAXI=1000,
                                  RESI_GLOB_RELA=2e-05),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+0.10,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA='HHT',
                                    ALPHA=-24.4,
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
                    CONVERGENCE=_F(ITER_GLOB_MAXI=1000,
                                   RESI_GLOB_RELA=2e-05),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+0.10,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA='HHT',
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
                   CONVERGENCE=_F(ITER_GLOB_MAXI=1000,
                                  RESI_GLOB_RELA=2e-05),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines', 
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+0.10,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA='HHT',
                                    ALPHA=-24.3,
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
tblp = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',   # For Extraction of values
                          INTITULE='Nodal Displacements', # Name of the table in .resu file
                          RESULTAT=resn,                   # The result from which values will be extracted(STAT_NON_LINE)
                          NOM_CHAM=('DEPL'),              # Field to extract. DEPL = Displacements
                          #TOUT_CMP='OUI',
                          NOM_CMP=('DX','DY','DZ'),       # Components of DISP to extract
                          GROUP_NO='allnodes',                 # Extract only for nodes of group DISP
                          INST=(1+k)*dt,                     # STAT_NON_LINE calculates for 10 INST. I want only last INST
                           ),),
                  );
if k < itimes-1:
    del Fnh
posi=hy.Get_posi(tblp)  
if k==0:
    con=''' + str(meshinfo['netLines']) + ''' 
    sur=''' + str(meshinfo['netSurfaces']) + '''
    Uinput=''' + str(cageinfo['Environment']['current']) + '''
    hymo=hy.HydroScreen(posi,sur,''' + str(cageinfo['Net']['Sn']) + ''',np.array(Uinput[0]),''' + str(
        dwh) + ''',''' + str(
        cageinfo['Net']['twineDiameter']) + ''')
    elementinwake=hymo.Save_ref()
    np.savetxt(cwd+'/asteroutput/elementinwake.txt', elementinwake)                 
    ''')
output_file.close()
if switcher in ["FE", "simiFSI"]:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
U=np.array(Uinput[int(k*dt/10.0)])
hymo.screenForce(posi,U)
Fnh=hymo.distributeForce()
np.savetxt(cwd+'asteroutput/posi'+str((k)*dt)+'.txt', posi)
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
if k < itimes-1:
    for i in range (1,len(Fnh)+1):
        DETRUIRE(CONCEPT=_F( NOM=(l[i])))
        ''')
    output_file.close()
elif switcher in ["FSI"]:
    output_file = open(cwd + "/ASTER2.comm", 'a')
    output_file.write('''
re=cwd+'velo.pkl'
timeFE=dt*k
U=hy.FSI_mapvelocity(re,timeFE)
Fh_elem=hymo.screenFsi(posi,U)
Fnh=hymo.distributeForce()
np.save(cwd+'posi.npy', posi)
np.save(cwd+'Fh.npy', Fh_elem)
np.savetxt(cwd+'asteroutput/posi'+str((k)*dt)+'.txt', posi)
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
if k < itimes-1:
    for i in range (1,len(Fnh)+1):
        DETRUIRE(CONCEPT=_F( NOM=(l[i])))
        ''')
    output_file.close()


# >>>>>>>>>>>>>>>    ASTERRUN.export       >>>>>>>>>>>>
suffix = rd.randint(1, 10000)
output_file = open(cwd+'/ASTERRUN.export', 'w')
output_file.write('''P actions make_etude
P aster_root ''' + workPath.aster_path[:-25] + '''
P consbtc oui
P corefilesize unlimited
P cpresok RESNOOK
P debug nodebug
P display UiS.D202.D202:0
P facmtps 1
P lang en
P mclient UiS.D202
P memjob 5224448
P mode interactif
P mpi_nbcpu 1
P mpi_nbnoeud 1
P nbmaxnook 5
P ncpus 10
P noeud localhost
P nomjob astk
P origine ASTK 2019.0.final
P platform LINUX64
P profastk hui@UiS.D202:''' + cwd + '''/run.astk
P protocol_copyfrom asrun.plugins.server.SCPServer
P protocol_copyto asrun.plugins.server.SCPServer
P protocol_exec asrun.plugins.server.SSHServer
P proxy_dir /tmp
P serveur localhost
P soumbtc oui
P tpsjob 1501
P uclient hui
P username hui
P version stable
A args 
A memjeveux 637.75
A tpmax 90000.0
P classe 
P depart 
P after_job 
P distrib 
P exectool 
P multiple 
P only_nook 
P rep_trav /tmp/hui-UiS-interactif_1''' + str(suffix) + '''
F mmed ''' + cwd + '''/asterinput/''' + str(meshinfo['meshName']) + ''' D 20
F comm ''' + cwd + '''/asterinput/ASTER1.comm D 1
F comm ''' + cwd + '''/asterinput/ASTER2.comm D 91
F rmed ''' + cwd + '''/asteroutput/paravisresults.rmed R 80
F resu ''' + cwd + '''/asteroutput/reactionforce.txt R 8
F mess ''' + cwd + '''/asteroutput/mess.log R 6\n''')
output_file.write('\n')
output_file.close()


















