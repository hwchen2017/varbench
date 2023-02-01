| Energy             | Sigma   | Energy Variance | DOF | Einf | Method                                                  | Data Repository |
|--------------------|---------|-----------------|-----|------|---------------------------------------------------------|-----------------|
| -33.83169340557936 |         |                 | 16  | 0    | Exact diagonalization                                   |                 |
| -33.8315064        |         | 7e-3            | 16  | 0    | VQE + symm. circuit (64 pars., exact grad, statevector) |                 |
| -33.83169340557946 |         | 1e-15           | 16  | 0    | DMRG (bond dimension = 256)                             |                 |
| -33.0219           | 0.0036  | 12.9877         | 16  | 0    | RBM (alpha = 1)                                         |                 |
| -32.5106           | 0.0015  | 2.20818         | 16  | 0    | Jastrow baseline                                        |                 |
| -33.831039193      | 0.00031 | 0.01741932679   | 16  | 0    | ClebschTree (10.1103/PhysRevB.104.045123)               |                 |