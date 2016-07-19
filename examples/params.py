from netpyne import specs, sim

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

netParams.sizeX = 100 # x-dimension (horizontal length) size in um
netParams.sizeY = 1000 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 100 # z-dimension (horizontal length) size in um
netParams.propVelocity = 100.0 # propagation velocity (um/ms)
netParams.probLengthConst = 150.0 # length constant for conn probability (um)


## Population parameters
netParams.addPopParams('E2', {'cellType': 'E', 'numCells': 50, 'yRange': [100,300], 'cellModel': 'HH'}) 
netParams.addPopParams('I2', {'cellType': 'I', 'numCells': 50, 'yRange': [100,300], 'cellModel': 'HH'}) 
netParams.addPopParams('E4', {'cellType': 'E', 'numCells': 50, 'yRange': [300,600], 'cellModel': 'HH'}) 
netParams.addPopParams('I4', {'cellType': 'I', 'numCells': 50, 'yRange': [300,600], 'cellModel': 'HH'}) 
netParams.addPopParams('E5', {'cellType': 'E', 'numCells': 50, 'ynormRange': [0.6,1.0], 'cellModel': 'HH'}) 
netParams.addPopParams('I5', {'cellType': 'I', 'numCells': 50, 'ynormRange': [0.6,1.0], 'cellModel': 'HH'}) 
netParams.addPopParams('background', {'rate': 20, 'noise': 0.3, 'cellModel': 'NetStim'})


## Cell property rules
cellRule = {'conds': {'cellType': 'E'},  'secs': {}}  # cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                              # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 15, 'L': 14, 'Ra': 120.0}                   # soma geometry
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.13, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}      # soma hh mechanism
netParams.addCellParams('Erule', cellRule)                          # add dict to list of cell params

cellRule = {'conds': {'cellType': 'I'},  'secs': {}}  # cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                              # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 10.0, 'L': 9.0, 'Ra': 110.0}                  # soma geometry
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.11, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}      # soma hh mechanism
netParams.addCellParams('Irule', cellRule)                          # add dict to list of cell params


## Synaptic mechanism parameters
netParams.addSynMechParams('exc', {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0})  # NMDA synaptic mechanism
netParams.addSynMechParams('inh', {'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 8.5, 'e': -75})  # GABA synaptic mechanism
 

## Cell connectivity rules
netParams.addConnParams('bg->all',
{'preConds': {'popLabel': 'background'}, 'postConds': {'cellType': ['E', 'I']}, # background -> all
  'weight': 0.01,                     # synaptic weight 
  'delay': 'max(1, gauss(5,2))',      # transmission delay (ms) 
  'synMech': 'exc'})                  # synaptic mechanism 

netParams.addConnParams('E->all',
{'preConds': {'cellType': 'E'}, 'postConds': {'y': [100,1000]},  #  E -> all (100-1000 um)
  'probability': 0.1 ,                  # probability of connection
  'weight': '0.005*post_ynorm',         # synaptic weight 
  'delay': 'dist_3D/propVelocity',      # transmission delay (ms) 
  'synMech': 'exc'})                    # synaptic mechanism 

netParams.addConnParams('I->E',
{'preConds': {'cellType': 'I'}, 'postConds': {'popLabel': ['E2','E4','E5']},       #  I -> E
  'probability': '0.4*exp(-dist_3D/probLengthConst)',   # probability of connection
  'weight': 0.001,                                     # synaptic weight 
  'delay': 'dist_3D/propVelocity',                    # transmission delay (ms) 
  'synMech': 'inh'})                                  # synaptic mechanism 


# Simulation options
simConfig = specs.SimConfig()        # object of class SimConfig to store simulation configuration
simConfig.duration = 1*1e3           # Duration of the simulation, in ms
simConfig.dt = 0.05                 # Internal integration timestep to use
simConfig.verbose = False            # Show detailed messages 
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.recordStep = 1             # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'model_output'  # Set file output name
simConfig.savePickle = False         # Save params, network and sim output to pickle file

simConfig.addAnalysis('plotRaster', {'orderBy': 'y', 'orderInverse': True})      # Plot a raster
simConfig.addAnalysis('plotTraces', {'include': [('E2',0), ('E4', 0), ('E5', 5)]})      # Plot recorded traces for this list of cells
simConfig.addAnalysis('plot2Dnet', True)           # plot 2D visualization of cell positions and connections
simConfig.addAnalysis('plotConn', True)           # plot connectivity matrix

# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)    
   
# import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty