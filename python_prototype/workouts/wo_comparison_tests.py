""" Comparing mc and qmc varying parameters """

import json
from numpy import arange, nan
from pandas import DataFrame

from qmcpy import *

distribution_pointers = [IIDStdUniform, IIDStdGaussian, Lattice, Sobol]

def abstol_comparison(abstols=arange(.1, .4, .1)):
    """
    Record solution, wall-clock time, and number of samples 
    for integrating the Keister function with 
    varying absolute tolerances
    """
    print('\nAbsolute Tolerance Comparison')
    columns = ['abs_tol'] + \
        [type(distrib()).__name__+'_solution' for distrib in distribution_pointers] + \
        [type(distrib()).__name__+'_time' for distrib in distribution_pointers] + \
        [type(distrib()).__name__+'_n' for distrib in distribution_pointers]
    df = DataFrame(columns=columns, dtype=float)
    for i,abs_tol in enumerate(abstols):
        row_i = {'abs_tol':abs_tol}
        for distrib_pointer in distribution_pointers:
            distribution = distrib_pointer(rng_seed=7)
            integrand = Keister()
            measure = Gaussian(dimension=3, variance=1 / 2)
            distrib_name = type(distribution).__name__
            if distrib_name in ['IIDStdGaussian','IIDStdUniform']:
                stopping_criterion = CLT(distribution, measure, abs_tol=abs_tol, n_max=1e10, n_init = 256)
            elif distrib_name in ['Lattice','Sobol']:
                stopping_criterion = CLTRep(distribution, measure, abs_tol=abs_tol, n_max=1e10, n_init=16)
            try:
                sol,data = integrate(integrand, measure, distribution, stopping_criterion)
                time = data.time_total
                n = data.n_total
            except:
                sol,time,n = nan,nan,nan
            row_i[distrib_name+'_solution'] = sol
            row_i[distrib_name+'_time'] = time
            row_i[distrib_name+'_n'] = n
        print(row_i)
        df.loc[i] = row_i
    df.to_csv('outputs/comparison_tests/abs_tol.csv')
    

def dimension_comparison(dimensions=arange(1, 4, 1)):
    """
    Record solution, wall-clock time, and number of samples
    for integrating the Keister function with varying dimensions
    """
    print('\nDimension Comparison')
    columns = ['dimension'] + \
        [type(distrib()).__name__+'_solution' for distrib in distribution_pointers] + \
        [type(distrib()).__name__+'_time' for distrib in distribution_pointers] + \
        [type(distrib()).__name__+'_n' for distrib in distribution_pointers]
    df = DataFrame(columns=columns, dtype=float)
    for i,dimension in enumerate(dimensions):
        row_i = {'dimension':dimension}
        for distrib_pointer in distribution_pointers:
            distribution = distrib_pointer(rng_seed=7)
            integrand = Keister()
            measure = Gaussian(dimension=[dimension], variance=1 / 2)
            distrib_name = type(distribution).__name__
            if distrib_name in ['IIDStdGaussian','IIDStdUniform']:
                stopping_criterion = CLT(distribution, measure, abs_tol=.05, n_max=1e10, n_init = 256)
            elif distrib_name in ['Lattice','Sobol']:
                stopping_criterion = CLTRep(distribution, measure, abs_tol=.05, n_max=1e10, n_init=16)
            try:
                sol,data = integrate(integrand, measure, distribution, stopping_criterion)
                time = data.time_total
                n = data.n_total
            except:
                sol,time,n = nan,nan,nan
            row_i[distrib_name+'_solution'] = sol
            row_i[distrib_name+'_time'] = time
            row_i[distrib_name+'_n'] = n
        print(row_i)
        df.loc[i] = row_i
    df.to_csv('outputs/comparison_tests/dimension.csv')

if __name__ == '__main__':
    abstols = arange(.001, .1, .003)
    dimensions = arange(1,9)

    abstol_comparison(abstols)
    dimension_comparison(dimensions)