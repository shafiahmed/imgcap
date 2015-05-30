import numpy as np
import random

class SGD:

    def __init__(self,model,alpha=1e-2,dh=None,
                 optimizer='sgd'):
        # dh = instance of data handler
        self.model1 = model
        self.model2 = model.topLayer
        self.dh = dh
        print "initializing SGD"
        assert self.model is not None, "Must define a function to optimize"
        self.it = 0
        self.alpha = alpha # learning rate
        self.optimizer = optimizer
        if self.optimizer == 'sgd':
            print "Using sgd.."
        elif self.optimizer == 'adagrad':
            print "Using adagrad..."
            epsilon = 1e-8
            self.gradt1 = [epsilon + np.zeros(W.shape) for W in self.model1.stack]
            self.gradt2 = [epsilon + np.zeros(W.shape) for W in self.model2.stack]
        else:
            raise ValueError("Invalid optimizer")

        self.costt = []
        self.expcost = []

    def run(self):
        """
        Runs stochastic gradient descent with model as objective.
        """
        print "running SGD"
        mbdata = self.dh.nextBatch
        while mbdata != None:
            self.it = self.dh.cur_iteration
            cost = self.model1.costAndGrad(mbdata)
            grad1 = self.model1.grads
            grad2 = self.model2.grads
            if np.isfinite(cost):
                if self.it > 1:
                    self.expcost.append(.01*cost + .99*self.expcost[-1])
                else:
                    self.expcost.append(cost)
            if self.optimizer == 'sgd':
                update = grad
                scale = -self.alpha

            elif self.optimizer == 'adagrad':
                # trace = trace+grad.^2
                self.gradt[1:] = [gt+g**2
                        for gt,g in zip(self.gradt[1:],grad[1:])]
                # update = grad.*trace.^(-1/2)
                update =  [g*(1./np.sqrt(gt))
                        for gt,g in zip(self.gradt[1:],grad[1:])]
                # handle dictionary separately
                dL = grad[0]
                dLt = self.gradt[0]
                for j in dL.iterkeys():
                    dLt[:,j] = dLt[:,j] + dL[j]**2
                    dL[j] = dL[j] * (1./np.sqrt(dLt[:,j]))
                update = [dL] + update
                scale = -self.alpha


            # update params
            self.model.updateParams(scale,update,log=False)

            self.costt.append(cost)
            if self.it%1 == 0:
                print "Iter %d : Cost=%.4f, ExpCost=%.4f."%(self.it,cost,self.expcost[-1])

