from netpyne import specs, sim

cfg = specs.SimConfig()
cfg.label = 'trial'
cfg.x0 = 0
cfg.x1 = 1

cfg.update()

results = {'x0': cfg.x0, 'x1': cfg.x1, 'results': cfg.x0**2 + cfg.x1**2}
print(results)

sim.send(results)