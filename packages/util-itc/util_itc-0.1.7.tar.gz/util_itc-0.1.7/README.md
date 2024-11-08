A package for fitting intertemporal choice data to models. 

Available models for fitting are exponential, hyperbolic, generalized hyperbolic, and quasi-hyperbolic. 

The constructor takes a model type and data (choices, payoffs, and delays) for two options and instantiates a util-itc object, fitting the data during instantiation. 

The resulting object stores the fitted parameters (k, inverse temperature, and an extra parameter s or b for generalized hyperbolic or quasi-hyperbolic models, respectively) in an instance variable, output.

Dependencies: numpy version >= 1.26.4, scipy version >= 1.12.0