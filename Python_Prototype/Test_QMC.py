
from numpy import arange
from matplotlib import pyplot as mpl_plot
from time import time
from copy import deepcopy
import pandas as pd

from CLTStopping import CLTStopping
from CLT_Rep import CLT_Rep
from IIDDistribution import IIDDistribution
from Lattice import Lattice
from integrate import integrate
from KeisterFun import KeisterFun 
from AsianCallFun import AsianCallFun
from measure import measure

def plot(title,xlabel,ylabel,xdata,ydata):
    mpl_plot.title(title)
    mpl_plot.xlabel(xlabel)
    mpl_plot.ylabel(ylabel)
    for name,(trend,color) in ydata.items():
        mpl_plot.plot(xdata,trend,color=color,label=name)
    mpl_plot.legend()
    # if output: mpl_plot.savefig('output/Figures/%s.png'%(title),dpi=200)
    mpl_plot.show()

def QMC_Wrapper(absTol,trueD):
    stopObj = CLTStopping(absTol=absTol)
    measureObj = measure().BrownianMotion(timeVector=[arange(1/4,5/4,1/4),arange(1/16,17/16,1/16),arange(1/64,65/64,1/64)])
    OptionObj = AsianCallFun(measureObj) # multi-level
    distribObj = IIDDistribution(trueD=trueD)
    t0 = time()
    sol,out = integrate(OptionObj,measureObj,distribObj,stopObj)
    t_delta = time()-t0
    return sol,t_delta

def comp_Clt_vs_cltRep_runtimes(fname,abstols):
    ''' Graph program-time by varying abstol '''
    # Open File and print headers
    f = open(fname,'w')
    f.write('%s,%s,%s,%s'%\
        ('CLT_stdUniform','CLT_stdGaussian','CLT_Rep_lattice','CLT_Rep_Sobol'))
    
    for absTol in abstols:
        print('Absolute Tolerance:',absTol)
        # CLT_stdUniform
        sol,tDelta = QMC_Wrapper(absTol,measure().stdUniform(dimension=[4,16,64]))
        f.write('\n'+str(tDelta)+',')
        print('\tCLT_stdUniform:',sol,tDelta)
        # CLT_stdGaussian
        sol,tDelta = QMC_Wrapper(absTol,measure().stdGaussian(dimension=[4,16,64]))
        f.write(str(tDelta)+',')
        print('\tCLT_stdGaussian:',sol,tDelta)
        # CLT_Rep_lattice
        sol,tDelta = QMC_Wrapper(absTol,measure().mesh(dimension=[4,16,64],meshType='lattice'))
        f.write(str(tDelta)+',')
        print('\tCLT_Rep_lattice:',sol,tDelta)
        # CLT_Rep_sobol
        sol,tDelta = QMC_Wrapper(absTol,measure().mesh(dimension=[4,16,64],meshType='sobol'))
        f.write(str(tDelta))
        print('\tCLT_Rep_sobol:',sol,tDelta)
    f.close()  
    
if __name__ == '__main__':
    # Generate Times CSV
    fname = 'Outputs/Compare_TrueD_and_StoppingCriterion_vs_Abstol.csv'
    absTols = arange(.004,.101,.002)
    comp_Clt_vs_cltRep_runtimes(fname,absTols)
    
    df = pd.read_csv(fname)
    plot(title = 'Multilevel AsianCallFun with Brownian Motion:  Integration Time by Absolute Tolerance',
        xlabel = 'Absolute Tolerance',
        ylabel = 'Runtime',
        xdata = absTols,
        ydata = {
            'CLT: Std Gaussian':(df.CLT_stdUniform,'r'),
            'CLT: Std Uniform ':(df.CLT_stdGaussian,'y'),
            'CLT Repeated: Lattice':(df.CLT_Rep_lattice,'b'),
            'CLT Repeated: Sobol':(df.CLT_Rep_Sobol,'g')})