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
rhsinker=2000
E = 40000000
refa = 0.886
nod_num=186
StruMeshLen=3


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
U=np.array([1.0,0.0,0.0])              # current velocity[0.12 0.26 0.39 0.50 0.65 0.76 0.93]
Sn=''' + str(Sn) + '''            # solidity ratio, 
dw=''' + str(dw) + '''            # [mm]
hml=''' + str(a) +'''             # [mm] half mesh length of the physical net
L=''' + str(StruMeshLen) +'''                  # used to check the length of line element
hy.dwhydro = dw             # define to check the cd-re relation
hy.dwmesh = dw*L/hml      # define to calculate the hydro forces
hy.refa=''' + str(refa) +'''                # constant reduction factor
areaF=L*L/2               # used to check the area of a net plane
dwmg=dw*np.sqrt(L/hml)    # structural diameter for weight 
ta=0.25*pi*pow(dwmg,2)    # structural diameter
Fbuoy=L*L*Sn/dw*0.25*pi*pow(dw,2)*9.81*1025
Fbuoy2=55*pi/30*pi*pow(0.15,2)*9.81*1025

DEBUT(PAR_LOT='NON',
IGNORE_ALARM=("SUPERVIS_25","DISCRETE_26") )
mesh = LIRE_MAILLAGE(UNITE=20)
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'), 
                             MODELISATION=('CABLE'), 
                             PHENOMENE='MECANIQUE'), 
                          _F(GROUP_MA=('bottomring','topring'), 
                             MODELISATION=('POU_D_E'), 
                             PHENOMENE='MECANIQUE')
                          ), 
                    MAILLAGE=mesh)
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=ta),
                          POUTRE=(_F(GROUP_MA=('bottomring', ), 
                                    SECTION='CERCLE', 
                                    CARA=('R', 'EP'), 
                                    VALE=(0.15, 0.011)),
                                  _F(GROUP_MA=('topring', ), 
                                    SECTION='CERCLE', 
                                    CARA=('R', 'EP'), 
                                    VALE=(0.15, 0.009)),
                                ),                          
                          MODELE=model)
mater = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                          ELAS=_F(E=''' + str(E) +''',NU=0.2,RHO=1140.0))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0)) 
fe = DEFI_MATERIAU(ELAS=_F(E=2e+11, 
                           NU=0.3,
                           RHO=''' + str(rhsinker) +''' ))  
hdpe = DEFI_MATERIAU(ELAS=_F(E=1e+9,
                           NU=0.3,
                           RHO=200 ))                          
fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(mater)),
                               _F(GROUP_MA=('bottomring'),
                                 MATER=(fe)),
                               _F(GROUP_MA=('topring'),
                                 MATER=(fe)),
                               ),
                         MODELE=model)

fix = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_NO=('fixed'),
                                 LIAISON='ENCASTRE'),
                     MODELE=model)


selfwigh = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                       GRAVITE=9.81,
                                       GROUP_MA=('twines')),
                      MODELE=model)
buoyF= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('allnodes'),
                                      FZ=Fbuoy), 
                      MODELE=model)
buoyF2= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=('topnodes','bottomnodes'),
                                      FZ=Fbuoy2), 
                      MODELE=model)

itimes=1100    
dt=0.1       # Physically it simulates 110s
tend=itimes*dt

listr = DEFI_LIST_REEL(DEBUT=0.0,
                       INTERVALLE=_F(JUSQU_A=tend,PAS=dt))

times = DEFI_LIST_INST(DEFI_LIST=_F(LIST_INST=listr,PAS_MINI=1e-8),
                       METHODE='AUTO')
NODEnumber=''' + str(nod_num) + ''' 
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
reac = POST_RELEVE_T(ACTION=_F(GROUP_NO=('fixed' ),
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
loadr.append( _F(CHARGE=buoyF), )
loadr.append( _F(CHARGE=buoyF2), )
for i in range (1,len(Fnh)+1):    
    loadr.append( _F(CHARGE=l[i],),)
    
if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                    CHAM_MATER=fieldmat,
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                  _F(#DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('bottomring', 'topring'),
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
                                  _F(#DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('bottomring', 'topring'),
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
if k%10==0:
    np.savetxt(cwd+'resufiles/posi'+str((k)*dt)+'.txt', posi)
if k==0:
    con=np.loadtxt(cwd+'/initialcondition/lineconnections.txt' )
    refl=hy.Cal_shie_line_elem(posi, con, U)
    np.savetxt(cwd+'/initialcondition/initialpositions.txt', posi)
    np.savetxt(cwd+'/initialcondition/flowreductionlines.txt', refl)
   
    # refs=hy.Cal_shie_screen_elem(posi, sur, U)
    # sur=hy.Cal_screen(posi,con,areaF)
    # np.savetxt(cwd+'/initialcondition/flowreductionscreens.txt', refs)
    # np.savetxt(cwd+'/initialcondition/screenconnections.txt', sur)
U=np.array([np.fix(k*dt/10.0)/10.0+0.1,0.0,0.0])''')

    if hm[1] == "M":
        output_file.write('''
Fnh=hy.Cal_''' + hm + '''(posi,con,U,Sn,refl)   ''')
    elif hm[1] == "S":
        output_file.write('''
Fnh=hy.Cal_''' + hm + '''(posi,sur,U,Sn,refs)   ''')
    else: 
        return
    output_file.write('''
# np.savetxt(cwd+'Fh1'+str((1+k)*dt)+'.txt', Fnh)    
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
if k < itimes-1:
    for i in range (1,len(Fnh)+1):
        DETRUIRE(CONCEPT=_F( NOM=(l[i])))

    \n''')
    output_file.write('\n')
    output_file.close()


def CR_export(filename1, fn2, MeshName,cwd):
    suffix = rd.randint(1, 10000)
    output_file = open('./inputfiles/' + filename1, 'w')
    # for the enviromentsetting
    output_file.write('''
P actions make_etude
P aster_root /opt/aster144
P consbtc oui
P corefilesize unlimited
P cpresok RESNOOK
P debug nodebug
P display UiS.D202.D202:0
P facmtps 1
P lang en
P mclient UiS.D202
P memjob 5224448
P memory_limit 5102.0
P mode interactif
P mpi_nbcpu 1
P mpi_nbnoeud 1
P nbmaxnook 5
P ncpus 10
P noeud localhost
P nomjob astkrun
P origine ASTK 2019.0.final
P platform LINUX64
P profastk hui@UiS.D202:''' + cwd + '''/run.astk
P protocol_copyfrom asrun.plugins.server.SCPServer
P protocol_copyto asrun.plugins.server.SCPServer
P protocol_exec asrun.plugins.server.SSHServer
P proxy_dir /tmp
P rep_trav /tmp/hui-UiS-interactif_1''' + str(suffix) + '''
P serveur localhost
P soumbtc oui
P time_limit 90000.0
P tpsjob 151
P uclient hui
P username hui
P version stable
A args 
A memjeveux 640.0
A tpmax 90000.0
F mmed ''' + cwd + '''/''' + MeshName + ''' D  20
F comm ''' + cwd + '''/inputfiles/''' + fn2 + ''' D  1
F comm ''' + cwd + '''/inputfiles/assignF.comm D  91
F rmed ''' + cwd + '''/resufiles/paravisresults.rmed R  80
F resu ''' + cwd + '''/resufiles/reactionforce.txt R  8
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
source /opt/aster144/etc/codeaster/profile.sh
as_run ''' + fn + '''    
    \n''')
    output_file.write('\n')
    output_file.close()


def CR_post(cw):
    output_file = open("post.py", 'w')
    # for the enviromentsetting
    output_file.write('''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('/home/hui/GitCode/allcodesinbitbucket/coderepository/CodeAsterModule/postprocessing')
import FunPostAster as Ffa
cwd="''' + cw + '''/"

bl=Ffa.bottomlist(cwd+"initialcondition/initialpositions.txt")
sur=Ffa.readsur(cwd+"initialcondition/screenconnections.txt")

# read the reaction force from the resutls files
force=Ffa.readforce(cwd+"resufiles/reactionforce.txt") 


# read all the results files to get the prositions.
namelist=[]
Estvol=np.zeros((110,1))
for i in range(110):
    namelist.append("resufiles/posi%s.0.txt" % i)
    posi=Ffa.readnodes(cwd+namelist[i])
    Estvol[i]=Ffa.volumeEst(posi,bl,sur)
# Estvol is the estimated volume according to different time.
    
    
VeloVolu=Ffa.EstiVoluRe(Estvol) # the matric Velo-vloume-volume coefficient
VeloForc=Ffa.meanf(force) # the matrix Velo-Forces


# >>>>>>>>>>the below is to check the origianl resutls
## check the forces
#plt.figure()
#x=np.linspace(0,1.1,110)
#plt.title('fish cage volume')
#plt.plot(x,Estvol)
#plt.xlabel('velocity')
#plt.show()
#
#
## check the velocity
#plt.figure()
#plt.plot(force[:,0],-force[:,1])
#plt.title('fish cage drag force')
#plt.xlabel('time (s)')
#plt.show()

 
    \n''')
    output_file.write('\n')
    output_file.close()

