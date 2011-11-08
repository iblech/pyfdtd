import numpy
import scipy.weave
from constants import constants
from material import material
from boundary import PML
import field as fi

class solver:
    """Solves FDTD equations on given field, with given materials and ports"""
    def __init__(self, field, mode='TMz', ports=None):
        # save arguments
        self.field = field
        self.mode = mode
        self.ports = ports
        self.material = material(field.xSize, field.ySize, field.deltaX, field.deltaY, mode=self.mode)
        self.pml = PML(field.xSize, fi

        # iterate
        for t in numpy.arange(starttime, starttime + time, deltaT):
            # update ports
            for port in self.ports:
                port.update(self.field, t)

            # calc oddField
            self.field.oddFieldX['flux'][1:,1:] += ky*(self.field.evenFieldY['field'][1:,1:] - self.field.evenFieldY['field'][:-1,1:])
            self.field.oddFieldY['flux'][1:,1:] -= ky*(self.field.evenFieldX['field'][1:,1:] - self.field.evenFieldX['field'][1:,:-1])
                    
            # calc field
            self.material.apply_odd(self.field, deltaT)

            # apply PML
            self.pml.apply_odd(self.field, deltaT)

            # calc even Field
            self.field.evenFieldX['flux'][:,:-1] -= ky*(self.field.oddFieldX['field'][:,1:] + self.field.oddFieldY['field'][:,1:] - self.field.oddFieldX['field'][:,:-1] - self.field.oddFieldY['field'][:,:-1])
            self.field.evenFieldY['flux'][:-1,:] += kx*(self.field.oddFieldX['field'][1:,:] + self.field.oddFieldY['field'][1:,:] - self.field.oddFieldX['field'][:-1,:] - self.field.oddFieldY['field'][:-1,:])

            # calc field
            self.material.apply_even(self.field, deltaT)

            # apply PML
            self.pml.apply_even(self.field, deltaT)

            if t/deltaT % 100 == 0:
                print "{}%".format((t-starttime)*100/time)
