import os
import math
import yaml
import numpy as np
### define, how many simulations will run to evaulate the uncertainty and mean

with open('Anzahl_Simulationen.yaml') as file:
	 Anzahl_Simulationen = yaml.load(file, Loader=yaml.FullLoader)['Anzahl_Simulationen']
nummerierung =  range(Anzahl_Simulationen)

### geant4 singularity container
#aktuelles_Geant4_image = '/ceph/Singularity/Geant4-10.6.simg'

# all paths will be relative to this one, snakemake will put the output here
#workdir: '/ceph/users/hmanke/Bebig_Benchmark'
MyConfigFile = 'Parameter_allgemein.yaml'
configfile: MyConfigFile


### define the scr and include files of the simulations (rotational symmetry)
src_dateien = 'B3aActionInitialization.cc B3aEventAction.cc B3aRunAction.cc B3DetectorConstruction.cc B3PrimaryGeneratorAction.cc B3StackingAction.cc PhysicsList.cc PhysicsListMessenger.cc RunActionMessenger.cc'.split()
include_dateien = 'B3aActionInitialization.hh B3aEventAction.hh B3aRunAction.hh B3DetectorConstruction.hh B3PrimaryGeneratorAction.hh B3StackingAction.hh PhysicsList.hh PhysicsListMessenger.hh RunActionMessenger.hh CADMesh.hh meine_globalen_Variablen.hh'.split()

#localrules: targets, create_run, build, TDK

### output der simulationen
rule targets:
	input:
		#input0 = 'Ergebnisse/Plots/Hase.png',
		#input1 = 'ccb-plaque-build/daten.dat'
		#war voher drin vor dat_0#input2 = 'Ergebnisse/TDK-Werte'
		input2 = 'ccb-plaque-build/Daten/daten_0'
		#input1 = 'Ergebnisse/TDK.pdf',
		#input2 = 'Ergebnisse/TDK-Werte.txt',


### erstellt die run-files mit hilfe des Pythonskriptes.
rule create_run:
	input: 'py_run.py', MyConfigFile
	output:'ccb-plaque-build/makros/run_{zahl}.mac'
	params:
		Teilchenzahl = config['Teilchenzahl'],
	script: 'py_run.py'

### erstellt einen gleichnamigen build ordner, und führt dort cmake und make aus. dafür wird das singularity image mit Geant4 benötigt.
rule build:
	input:
		input1 = ('ccb-plaque/ccbPlaque.cc'),#'ccb-plaque/ccbPlaque.in','ccb-plaque/ccbPlaque.out'),
		input2 = 'ccb-plaque/CMakeLists.txt',
		input3 = expand('ccb-plaque/src/{src_datei}', src_datei = src_dateien),
		input4 = expand('ccb-plaque/include/{include_datei}', include_datei = include_dateien),
	output:
		output1 = ('ccb-plaque-build/ccbPlaque'),#'ccb-plaque-build/ccbPlaque.in','ccb-plaque-build/ccbPlaque.out'),
		output2 = ('ccb-plaque-build/cmake_install.cmake', 'ccb-plaque-build/CMakeCache.txt', 'ccb-plaque-build/init_vis.mac', 'ccb-plaque-build/Makefile', 'ccb-plaque-build/vis.mac'),
	#singularity: aktuelles_Geant4_image
	threads: 1
	shell: 'mkdir -p ccb-plaque-build && cd ccb-plaque-build && cmake -DGeant4_DIR=/Users/smller/geant4.10.06-install/lib/Geant4-10.6.1 ../ccb-plaque && make '


rule simulate:
	input:
		input0 = ('ccb-plaque/models'),
		input1 = ('ccb-plaque-build/ccbPlaque'),#'ccb-plaque-build/ccbPlaque.in','ccb-plaque-build/ccbPlaque.out'),
		input2 = ('ccb-plaque-build/cmake_install.cmake', 'ccb-plaque-build/CMakeCache.txt', 'ccb-plaque-build/init_vis.mac', 'ccb-plaque-build/Makefile', 'ccb-plaque-build/vis.mac'),
		input3 = 'ccb-plaque-build/makros/run_{zahl}.mac'
		#input3 = 'ccb-plaque-build/run_4.mac'
	output:
		#output1 = 'ccb-plaque-build/TDK_{zahl}.txt'
		output2 = 'ccb-plaque-build/Daten/daten_{zahl}'
	threads: 1
	#singularity: aktuelles_Geant4_image
	shell: 'cd ccb-plaque-build && ./ccbPlaque makros/run_{wildcards.zahl}.mac'
	#shell: 'cd ccb-plaque-build && ./ccbPlaque run_4.mac'


rule TDK:	# die TDK kann in jeder Simulation abgerufen werden
	input:
		#input1 = expand('ccb-plaque-build/TDK_{zahl}.txt', zahl=nummerierung),
		input1 = expand('ccb-plaque-build/Daten/daten_{zahl}', zahl=nummerierung),
		#input2 = 'py_TDK.ipynb',
		input2 = 'python/TDK.py',
		input4 = 'Anzahl_Simulationen.yaml'
	output:
		output1 = ('Ergebnisse/TDK-Werte') #'Ergebnisse/TDK.pdf',,
	params:
		run_n = Anzahl_Simulationen,
				Teilchenzahl = config['Teilchenzahl'],
	shell: 'python python/TDK.py'
	#notebook: 'py_TDK.ipynb'

rule plot:
	input:
		#input1 = ('ccb-plaque-build/daten.dat'),
		#input2 = ('python/test/box.stl'),
		input3 = ('python/test'),
		input4 = ('python/inside-3d-mesh-master/Haseisinside.py')
	output:
		output1 = ('Ergebnisse/Plots/Auge_z_1.png')
	shell: ' python3 python/inside-3d-mesh-master/Haseisinside.py'
