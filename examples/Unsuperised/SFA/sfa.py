# -*- coding: utf-8 -*-
# Generated by codesnippet sphinx extension on 2012-10-04

import mdp
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
p2 = np.pi*2
t = np.linspace(0, 1, 10000, endpoint=0) # time axis 1s, samplerate 10KHz
dforce = np.sin(p2*5*t) + np.cos(p2*20*t) + t
def logistic_map(x, r):
    return r*x*(1-x)

series = np.zeros((10000, 1), 'd')

series[0] = 0.6

for i in range(1,10000):
    series[i] = logistic_map(series[i-1],3.6+0.13*dforce[i])


print(series)
plt.plot(series,'o-')
plt.show()
plt.savefig("series.png")

flow = (mdp.nodes.EtaComputerNode() +
        mdp.nodes.TimeFramesNode(10) +
        mdp.nodes.PolynomialExpansionNode(3) +
        mdp.nodes.SFANode(output_dim=1) +
        mdp.nodes.EtaComputerNode() )

flow.train(series)

slow = flow(series)

resc_dforce = (dforce - np.mean(dforce, 0)) / np.std(dforce, 0)

print '%.3f' % mdp.utils.cov2(resc_dforce[:-9], slow)
# Expected:
## 1.000

print 'Eta value (time series): %d' % flow[0].get_eta(t=10000)
# Expected:
## Eta value (time series): 3004
print 'Eta value (slow feature): %.3f' % flow[-1].get_eta(t=9996)
# Expected:
## Eta value (slow feature): 10.218

plt.clf()
plt.plot(xrange(len(resc_dforce)), resc_dforce, label="real")
plt.plot(range(len(slow))[::10], slow[::10], 'o-', label="sfa")
plt.legend()
plt.savefig("sfa_comp_real.png")