# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# https://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

from ramble.appkit import *


class Hpcg(SpackApplication):
    '''Define HPCG application'''
    name = 'hpcg'

    tags = ['benchmark-app', 'mini-app', 'benchmark']

    default_compiler('gcc9', base='gcc', version='9.3.0')

    mpi_library('impi2018', base='intel-mpi', version='2018.4.274')

    software_spec('hpcg', base='hpcg', version='3.1',
                  variants='+openmp',
                  compiler='gcc9', mpi='impi2018', required=True)

    executable('execute', 'xhpcg', use_mpi=True)

    executable('move-log', 'mv HPCG-Benchmark*.txt {out_file}',
               use_mpi=False)

    workload('standard', executables=['execute', 'move-log'])

    workload_variable('matrix_size', default='104 104 104',
                      description='Dimensions of the matrix to use',
                      workloads=['standard'])

    workload_variable('iterations', default='60',
                      description='Number of iterations to perform',
                      workloads=['standard'])

    workload_variable('out_file', default='{experiment_run_dir}/hpcg_result.out',
                      description='Output file for results',
                      workloads=['standard'])

    figure_of_merit('Status', log_file='{out_file}',
                    fom_regex='Final Summary::HPCG result is (?P<status>[a-zA-Z]+) with a GFLOP/s rating of=(?P<gflops>[0-9]+\.[0-9]+)',
                    group_name='status', units='')

    figure_of_merit('Gflops', log_file='{out_file}',
                    fom_regex='Final Summary::HPCG result is (?P<status>[a-zA-Z]+) with a GFLOP/s rating of=(?P<gflops>[0-9]+\.[0-9]+)',
                    group_name='gflops', units='GFLOP/s')

    figure_of_merit('Time', log_file='{out_file}',
                    fom_regex='Final Summary::Results are.* execution time.*is=(?P<exec_time>[0-9]+\.[0-9]*)',
                    group_name='exec_time', units='s')

    figure_of_merit('ComputeDotProductMsg', log_file='{out_file}',
                    fom_regex='Final Summary::Reference version of ComputeDotProduct used.*=(?P<msg>.*)',
                    group_name='msg', units='')

    figure_of_merit('ComputeSPMVMsg', log_file='{out_file}',
                    fom_regex='Final Summary::Reference version of ComputeSPMV used.*=(?P<msg>.*)',
                    group_name='msg', units='')

    figure_of_merit('ComputeMGMsg', log_file='{out_file}',
                    fom_regex='Final Summary::Reference version of ComputeMG used.*=(?P<msg>.*)',
                    group_name='msg', units='')

    figure_of_merit('ComputeWAXPBYMsg', log_file='{out_file}',
                    fom_regex='Final Summary::Reference version of ComputeWAXPBY used.*=(?P<msg>.*)',
                    group_name='msg', units='')

    figure_of_merit('HPCG 2.4 Rating', log_file='{out_file}',
                    fom_regex='Final Summary::HPCG 2\.4 rating.*=(?P<rating>[0-9]+\.*[0-9]*)',
                    group_name='rating', units='')

    def _make_experiments(self, workspace, expander):
        super()._make_experiments(workspace, expander)

        input_path = expander.expand_var('{experiment_run_dir}/hpcg.dat')

        with open(input_path, 'w+') as f:
            f.write('HPCG benchmark input file\n')
            f.write('Sandia National Laboratories; University of Tennessee, Knoxville\n')
            f.write(expander.expand_var('{matrix_size}\n'))
            f.write(expander.expand_var('{iterations}\n'))
