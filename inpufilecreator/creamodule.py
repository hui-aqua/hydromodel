# writer: hui.cheng@uis.no
# Groupname:
# GROUP_NO: allnodes, sinkers
# GROUP_MA: bottomframe, twines, topring
# cwd is the working place
# NUMBER OF NODE=1512
# NUMBER OF TWINE=2952
import random as rd
Sn = 0.194
dw = 2.42e-3
a = 0.0255
weight = 4.48
E = 40000000
refa = 0.886


def CR_comm(filename, cwd, hm):

    output_file = open('./inputfiles/' + filename, 'w')
    # for the enviromentsetting
    output_file.write(
        '''
import sys
sys.path.append("/home/hui/GitCode/allcodesinbitbucket/coderepository/CodeAsterModule/Hydromodel")
import hydro4c2 as hy
import numpy as np
from numpy import pi
cwd="''' + cwd + '''/"
U=[0.10,0,0]              # current velocity[0.12 0.26 0.39 0.50 0.65 0.76 0.93]
wei=''' + str(weight) + '''                  # [N] sinker weight in the water
Sn=''' + str(Sn) + '''                  # solidity ratio, 
dw=''' + str(dw) + '''                # [mm]
hml=''' + str(a) +
        '''                # [mm] half mesh length of the physical net
L=0.0765                  # used to check the length of line element
hy.dwhydro = dw             # define to check the cd-re relation
hy.dwmesh = dw*L/hml      # define to calculate the hydro forces
hy.refa=''' + str(refa) +
        '''                # constant reduction factor
areaF=L*L/2               # used to check the area of a net plane
dwmg=dw*np.sqrt(L/hml)    # structural diameter for weight 
ta=0.25*pi*pow(dwmg,2)    # structural diameter
Fbuoy=L*L*Sn/dw*0.25*pi*pow(dw,2)*9.81*1025


DEBUT(PAR_LOT='NON',
IGNORE_ALARM=("SUPERVIS_25","DISCRETE_26") )
mesh = LIRE_MAILLAGE(UNITE=20)
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'), 
                             MODELISATION=('CABLE'), 
                             PHENOMENE='MECANIQUE'), 
                          # _F(GROUP_MA=('bottomring'), 
                          #    MODELISATION=('POU_D_E'), 
                          #    PHENOMENE='MECANIQUE')
                          ), 
                    MAILLAGE=mesh)
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=ta),
                          # POUTRE=_F(GROUP_MA=('bottomring', ), 
                          #           SECTION='CERCLE', 
                          #           CARA=('R', 'EP'), 
                          #           VALE=(0.005, 0.005)),
                          
                          MODELE=model)
mater = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(E) +
        ''',NU=0.2,RHO=1140.0))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0)) 
# fe = DEFI_MATERIAU(ELAS=_F(E=2e+11, 
#                            NU=0.3,
#                            RHO=7980.0))  
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(mater)),
                               # _F(GROUP_MA=('bottomring'),
                               #   MATER=(mater)),
                               ),
                         MODELE=model)

fix = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_MA=('topring'),
                                 LIAISON='ENCASTRE'),
                     MODELE=model)

selfwigh = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                       GRAVITE=9.81,
                                       GROUP_MA=('twines')),
                      MODELE=model)
sinkF = AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('sinkers'),
                                      FZ=-wei,
                                      FX=0,
                                      FY=0,
                                      ), 
                      MODELE=model)
buoyF= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('allnodes'),
                                      FZ=Fbuoy), 
                      MODELE=model)
itimes=1100    
dt=0.1       # Physically it simulates 110s
tend=itimes*dt

listr = DEFI_LIST_REEL(DEBUT=0.0,
                       INTERVALLE=_F(JUSQU_A=tend,PAS=dt))

times = DEFI_LIST_INST(DEFI_LIST=_F(LIST_INST=listr,PAS_MINI=1e-8),
                       METHODE='AUTO')
NODEnumber=1512
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
reac = POST_RELEVE_T(ACTION=_F(GROUP_NO=('node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8', 'node9', 'node10', 'node11', 'node12', 'node13', 'node14', 'node15', 'node16', 'node17', 'node18', 'node19', 'node20', 'node21', 'node22', 'node23', 'node24', 'node25', 'node26', 'node27', 'node28', 'node29', 'node30', 'node31', 'node32', 'node33', 'node34', 'node35', 'node36', 'node37', 'node38', 'node39', 'node40', 'node41', 'node42', 'node43', 'node44', 'node45', 'node46', 'node47', 'node48', 'node49', 'node50', 'node51', 'node52', 'node53', 'node54', 'node55', 'node56', 'node57', 'node58', 'node59', 'node60', 'node61', 'node62', 'node63', 'node64', 'node65', 'node66', 'node67', 'node68', 'node69', 'node70', 'node71', 'node72' ),
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

    \n''')
    output_file.write('\n')
    output_file.close()

    output_file = open("./inputfiles/assignF.comm", 'w')
    # for the enviromentsetting
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
loadr.append( _F(CHARGE=sinkF), )
loadr.append( _F(CHARGE=buoyF), )
for i in range (1,len(Fnh)+1):    
    loadr.append( _F(CHARGE=l[i],),)
    
if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                    CHAM_MATER=fieldmat,
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                  # _F(#DEFORMATION='GROT_GDEP',
                                  #   GROUP_MA=('bottomring', ),
                                  #   RELATION='ELAS')
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
                                  # _F(#DEFORMATION='GROT_GDEP',
                                  #   GROUP_MA=('bottomring', ),
                                  #   RELATION='ELAS')
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
if k==1:
    np.savetxt(cwd+'resufiles/positionsinstillwater1.txt', posi)
if k==2:
    np.savetxt(cwd+'resufiles/positionsinstillwater2.txt', posi)
if k%10==0:
    np.savetxt(cwd+'resufiles/posi'+str((k)*dt)+'.txt', posi)
# if k==800:
#     np.savetxt(cwd+'resufiles/posi'+str((k)*dt)+'.txt', posi)
# if k==900:
#     np.savetxt(cwd+'resufiles/posi'+str((k)*dt)+'.txt', posi)
if k==0:
    con=hy.Cal_connection(posi,L)
    sur=hy.Cal_screen(posi,con,areaF)
    refl=hy.Cal_shie_line_elem(posi, con, U)
    refs=hy.Cal_shie_screen_elem(posi, sur, U)
    np.savetxt(cwd+'/initialcondition/initialpositions.txt', posi)
    np.savetxt(cwd+'/initialcondition/flowreductionlines.txt', refl)
    np.savetxt(cwd+'/initialcondition/flowreductionscreens.txt', refs)
    np.savetxt(cwd+'/initialcondition/screenconnections.txt', sur)
    np.savetxt(cwd+'/initialcondition/lineconnections.txt', con)
U=np.array([np.fix(k*dt/10.0)/10.0+0.1,0.0,0.0])''')

    if hm[1] == "M":
        output_file.write('''
Fnh=hy.Cal_''' + hm + '''(posi,con,U,Sn,refs)   ''')
    else:
        output_file.write('''
Fnh=hy.Cal_''' + hm + '''(posi,sur,U,Sn,refs)   ''')
    output_file.write('''
# np.savetxt(cwd+'Fh1'+str((1+k)*dt)+'.txt', Fnh)    
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
if k < itimes-1:
    for i in range (1,len(Fnh)+1):
        DETRUIRE(CONCEPT=_F( NOM=(l[i])))

    \n''')
    output_file.write('\n')
    output_file.close()


def CR_export(filename1, fn2, cwd):
    suffix = rd.randint(1, 10000)
    output_file = open('./inputfiles/' + filename1, 'w')
    # for the enviromentsetting
    output_file.write('''
P actions make_etude
P aster_root /opt/aster
P consbtc oui
P corefilesize unlimited
P cpresok RESNOOK
P debug nodebug
P display hui:0
P facmtps 1
P lang en
P mclient hui
P memjob 5224448
P memory_limit 5102.0
P mode interactif
P mpi_nbcpu 1
P mpi_nbnoeud 1
P nbmaxnook 5
P ncpus 6
P noeud hui
P nomjob run4
P origine ASTK 2018.0.final
P platform LINUX64
P profastk hui@hui:''' + cwd + '''/run.astk
P protocol_copyfrom asrun.plugins.server.SCPServer
P protocol_copyto asrun.plugins.server.SCPServer
P protocol_exec asrun.plugins.server.SSHServer
P proxy_dir /tmp
P rep_trav /tmp/huicheng-gorina1-interactif_6''' + str(suffix) + '''
P serveur localhost
P soumbtc oui
P time_limit 90000.0
P tpsjob 1501
P uclient hui
P username huicheng
P version testing
A args 
A memjeveux 637.75
A tpmax 90000.0
F mmed ''' + cwd + '''/case3.med D  20
F comm ''' + cwd + '''/inputfiles/''' + fn2 + ''' D  1
F comm ''' + cwd + '''/inputfiles/assignF.comm D  91
F rmed ''' + cwd + '''/resufiles/paravisresults.rmed R  80
F resu ''' + cwd + '''/resufiles/reactionforce.txt R  8
F mess ''' + cwd + '''/resufiles/mess.log R  6
F mess ''' + cwd + '''/resufiles/mess.log R  6
    \n''')
    output_file.write('\n')
    output_file.close()


# F mess ''' + cwd + '''/resufiles/mess.log R  6


def CR_shscript(fn):
    output_file = open("runit.sh", 'w')
    # for the enviromentsetting
    output_file.write('''
echo "\t\t\t  Hello user!\n\t\t   This is a new terminal.\n\tDONOT CLOSE ME, OR THE CALCULATION WILL STOP!\nIt will close automatically when the calculation is finished.\nYou can minimize this terminal to make it runs in background.\n\n\nDesign for Code_Aster\nEmail: hui.cheng@uis.no" | boxes -d boy

echo -n "Press any key to continue or 'CTRL+C' to exit : \n"
read var_name
echo "Here we go!..."                                                  
sleep 2s

cd inputfiles
source /opt/aster/etc/codeaster/profile.sh
as_run ''' + fn + '''    
    \n''')
    output_file.write('\n')
    output_file.close()



