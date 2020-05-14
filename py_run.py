#!/usr/bin/env python
# coding: utf-8

# In[26]:


import random
import re
import sys
import math
import numpy as np


# In[1]:


name = 'run' # Name der run-Dateien. NameZahl
#run_n = snakemake.params.run_n # Anzahl der Dateien

Teilchenzahl = snakemake.params.Teilchenzahl
#Teilchenzahl = 100
#ordner = 'Applikator-CCB'
ordner = '/Users/smller/Simulationen/ccb-plaque'
pfad = ordner+'-build'
#run = 1
run = int(snakemake.wildcards.zahl)

offset_y = 0.0
offset_z = 0.0
radius_target = 12.1
offset_ges = 0.35


# In[29]:


random.seed(run)
zahl_1 = 2
zahl_2 = 1
while zahl_1 > zahl_2 or zahl_1 == zahl_2: # Randomisierte Zahlen fuer Set Seeds
    zahl_1 = random.randint(1,100000000)
    zahl_2 = random.randint(1,100000000)



dok_neu_name = pfad + '/makros/' + str(name)+'_'+str(run)+'.mac'
dok_neu = open(dok_neu_name, 'w')
################################## Uebliche Einstellungen #######################################
#print('hiho')
dok_neu.write('#/mycommands/addPhysics emstandard_opt4\n')
dok_neu.write('/random/setSeeds '+ str(zahl_1) + ' ' + str(zahl_2) + '\n')
dok_neu.write('/run/setCut 0.01 mm\n')
dok_neu.write('/run/initialize\n')
dok_neu.write('/control/verbose 0 \n')
dok_neu.write('/run/verbose 0 \n')
dok_neu.write('/event/verbose 0 \n')
dok_neu.write('/tracking/verbose 0 \n')
dok_neu.write('\n\n')
dok_neu.write('/mycommands/setFileName Daten/daten_' + str(run) +'\n')
###################################### Partikel Definition #######################################
dok_neu.write('/gps/particle ion \n')
dok_neu.write('/gps/ion 44 106 0 0.0\n')
dok_neu.write('/gps/energy 0. keV\n')
dok_neu.write('/gps/pos/type Surface\n')
dok_neu.write('/gps/pos/shape Sphere\n')
dok_neu.write('/gps/pos/radius ' + str(radius_target) + ' mm\n')
dok_neu.write('/gps/pos/centre 0. 0. 0.1 mm \n')        #gucken, ob z= 0.1 bei mir auch richtig ist
dok_neu.write('/gps/ang/type iso\n')
dok_neu.write('/gps/pos/confine Target_silver_PV\n')
dok_neu.write('\n\n')
############################## Scorer Definition TDK #######################################
#dok_neu.write('#### 0. Zylinder-Mesh ####\n')
#dok_neu.write('/score/create/cylinderMesh cylMesh_0\n')
#dok_neu.write('/score/mesh/cylinderSize 0.5 12. mm #Radius, Länge, Einheit\n')
#dok_neu.write('/score/mesh/nBin 1 48 1 #R, Z, Phi\n')
#dok_neu.write('/score/mesh/translate/xyz 0.0 0.0 ' + str(offset_ges) + ' mm\n')
#dok_neu.write('/score/quantity/doseDeposit dDep0\n')
#dok_neu.write('/score/close\n')
#dok_neu.write('#/score/drawProjection cylMesh_0 dDep0\n\n')
dok_neu.write('/run/beamOn ' + str(Teilchenzahl) + '\n')
#dok_neu.write('/score/dumpQuantityToFile cylMesh_0 dDep0 TDKapplikator_' + str(run) + '.txt\n')
dok_neu.close()
