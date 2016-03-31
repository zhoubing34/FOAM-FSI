#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Figure dimensions
fig_width_pt = 0.5 * 345.0
inches_per_pt = 1.0/72.27
fig_width = fig_width_pt*inches_per_pt
fig_height = fig_width * 0.86
fig_size = [fig_width,fig_height]
nb_ticks = 7
params = {
    'font.size' : 7,
    'axes.labelsize' : 7,
    'font.size' : 7,
    'legend.fontsize': 7,
    'xtick.labelsize' : 7,
    'ytick.labelsize' : 7,
    'figure.figsize': fig_size
}

plt.rcParams.update(params)

markers = ["-ob", "-vg", "-<r", "-^c", "->m", "-sy", "-*k", "--ob", "--vg", "--<r", "--^c", "-->m", "--sy", "--*k", "-.db", "-ob", "-vg", "-<r", "-^c", "->m", "-sy"]
markerIndex = 0

nbComputations = 9
nbNodes = 6

timeIntegrationSchemes = ["IDC", "SDIRK"]

sdirkSchemes = ["SDIRK2", "SDIRK3", "SDIRK4"]

for i in np.arange( nbNodes + 1 ):
    for j in np.arange( nbComputations ):

        label_ref = "IDC_nbNodes_" + str( i )
        label_ref += "_nbTimeSteps_" + str( 2 ** j)

        try:
            data_fluid_u_ref = np.loadtxt( "data/" + label_ref + "_data_fluid_u.log" )
            data_fluid_a_ref = np.loadtxt( "data/" + label_ref + "_data_fluid_a.log" )
            data_fluid_p_ref = np.loadtxt( "data/" + label_ref + "_data_fluid_p.log" )
            data_solid_r_ref = np.loadtxt( "data/" + label_ref + "_data_solid_r.log" )
            data_solid_u_ref = np.loadtxt( "data/" + label_ref + "_data_solid_u.log" )
        except:
            pass

fluid_u_fig = plt.figure()
fluid_u_plot = fluid_u_fig.add_subplot(111)
fluid_a_fig = plt.figure()
fluid_a_plot = fluid_a_fig.add_subplot(111)
fluid_p_fig = plt.figure()
fluid_p_plot = fluid_p_fig.add_subplot(111)
solid_r_fig = plt.figure()
solid_r_plot = solid_r_fig.add_subplot(111)
solid_u_fig = plt.figure()
solid_u_plot = solid_u_fig.add_subplot(111)

for timeIntegrationScheme in timeIntegrationSchemes:

    nbSchemes = nbNodes
    if timeIntegrationScheme == "SDIRK":
        nbSchemes = len( sdirkSchemes )

    for iNodes in np.arange( nbSchemes ):

        timeStepList = []
        errors_fluid_u = []
        errors_fluid_a = []
        errors_fluid_p = []
        errors_solid_r = []
        errors_solid_u = []

        for iComputation in np.arange( nbComputations ):

            nbNodes = iNodes + 1
            nbTimeSteps = 2 ** iComputation

            label = timeIntegrationScheme

            if timeIntegrationScheme == "SDIRK":
                label += "_" + sdirkSchemes[iNodes]

            if timeIntegrationScheme == "IDC":
                label += "_nbNodes_" + str( nbNodes )

            label += "_nbTimeSteps_" + str( nbTimeSteps )

            try:
                data_fluid_u = np.loadtxt( "data/" + label + "_data_fluid_u.log" )
                data_fluid_a = np.loadtxt( "data/" + label + "_data_fluid_a.log" )
                data_fluid_p = np.loadtxt( "data/" + label + "_data_fluid_p.log" )
                data_solid_r = np.loadtxt( "data/" + label + "_data_solid_r.log" )
                data_solid_u = np.loadtxt( "data/" + label + "_data_solid_u.log" )
            except:
                continue

            error_fluid_u = np.linalg.norm(data_fluid_u - data_fluid_u_ref) / np.linalg.norm( data_fluid_u_ref )
            error_fluid_a = np.linalg.norm(data_fluid_a - data_fluid_a_ref) / np.linalg.norm( data_fluid_a_ref )
            error_fluid_p = np.linalg.norm(data_fluid_p - data_fluid_p_ref) / np.linalg.norm( data_fluid_p_ref )
            error_solid_r = np.linalg.norm(data_solid_r - data_solid_r_ref) / np.linalg.norm( data_solid_r_ref )
            error_solid_u = np.linalg.norm(data_solid_u - data_solid_u_ref) / np.linalg.norm( data_solid_u_ref )

            errors_fluid_u.append( error_fluid_u )
            errors_fluid_a.append( error_fluid_a )
            errors_fluid_p.append( error_fluid_p )
            errors_solid_r.append( error_solid_r )
            errors_solid_u.append( error_solid_u )
            timeStepList.append( 1.0 / float( nbTimeSteps ) )

        if timeIntegrationScheme == "SDIRK":
            legend = sdirkSchemes[iNodes]
        if timeIntegrationScheme == "IDC":
            legend = 'IDC' + str(nbNodes)

        fluid_u_plot.loglog( timeStepList, errors_fluid_u, markers[markerIndex], label = legend, markersize = 3 )
        fluid_a_plot.loglog( timeStepList, errors_fluid_a, markers[markerIndex], label = legend, markersize = 3 )
        fluid_p_plot.loglog( timeStepList, errors_fluid_p, markers[markerIndex], label = legend, markersize = 3 )
        solid_r_plot.loglog( timeStepList, errors_solid_r, markers[markerIndex], label = legend, markersize = 3 )
        solid_u_plot.loglog( timeStepList, errors_solid_u, markers[markerIndex], label = legend, markersize = 3 )

        markerIndex += 1

        try:
            print '\n' + legend
            for i in np.arange( nbComputations - 1 ):
                print ( np.log10( errors_fluid_u[i+1] ) - np.log10( errors_fluid_u[i] ) ) / ( np.log10( timeStepList[i+1] ) - np.log10( timeStepList[i] ) )

            print '\n'
            for i in np.arange( nbComputations - 1 ):
                print ( np.log10( errors_fluid_a[i+1] ) - np.log10( errors_fluid_a[i] ) ) / ( np.log10( timeStepList[i+1] ) - np.log10( timeStepList[i] ) )

            print '\n'
            for i in np.arange( nbComputations - 1 ):
                print ( np.log10( errors_fluid_p[i+1] ) - np.log10( errors_fluid_p[i] ) ) / ( np.log10( timeStepList[i+1] ) - np.log10( timeStepList[i] ) )

            print '\n'
            for i in np.arange( nbComputations - 1 ):
                print ( np.log10( errors_solid_r[i+1] ) - np.log10( errors_solid_r[i] ) ) / ( np.log10( timeStepList[i+1] ) - np.log10( timeStepList[i] ) )

            print '\n'
            for i in np.arange( nbComputations - 1 ):
                print ( np.log10( errors_solid_u[i+1] ) - np.log10( errors_solid_u[i] ) ) / ( np.log10( timeStepList[i+1] ) - np.log10( timeStepList[i] ) )
        except:
            pass

fluid_u_plot.set_xlabel( 'Time step [s]' )
fluid_u_plot.set_ylabel( 'Error in fluid velocity [-]' )
fluid_u_plot.grid( 'on' )
lgd = fluid_u_plot.legend( loc='upper center', bbox_to_anchor=(0.5, 1.38), ncol = 3, fancybox = True, shadow = False )
fluid_u_fig.savefig( 'tubeflow_fluid_u.pdf', bbox_extra_artists=(lgd,), transparent = True, bbox_inches='tight' )

fluid_a_plot.set_xlabel( 'Time step [s]' )
fluid_a_plot.set_ylabel( 'Error in fluid cross-sectional area [-]' )
fluid_a_plot.grid( 'on' )
lgd = fluid_a_plot.legend( loc='upper center', bbox_to_anchor=(0.5, 1.38), ncol = 3, fancybox = True, shadow = False )
fluid_a_fig.savefig( 'tubeflow_fluid_a.pdf', bbox_extra_artists=(lgd,), transparent = True, bbox_inches='tight' )

fluid_p_plot.set_xlabel( 'Time step [s]' )
fluid_p_plot.set_ylabel( 'Error in fluid pressure [-]' )
fluid_p_plot.grid( 'on' )
lgd = fluid_p_plot.legend( loc='upper center', bbox_to_anchor=(0.5, 1.38), ncol = 3, fancybox = True, shadow = False )
fluid_p_fig.savefig( 'tubeflow_fluid_p.pdf', bbox_extra_artists=(lgd,), transparent = True, bbox_inches='tight' )

solid_r_plot.set_xlabel( 'Time step [s]' )
solid_r_plot.set_ylabel( 'Error in solid radius [-]' )
solid_r_plot.grid( 'on' )
lgd = solid_r_plot.legend( loc='upper center', bbox_to_anchor=(0.5, 1.38), ncol = 3, fancybox = True, shadow = False )
solid_r_fig.savefig( 'tubeflow_solid_r.pdf', bbox_extra_artists=(lgd,), transparent = True, bbox_inches='tight' )

solid_u_plot.set_xlabel( 'Time step [s]' )
solid_u_plot.set_ylabel( 'Error in solid velocity [-]' )
solid_u_plot.grid( 'on' )
lgd = solid_u_plot.legend( loc='upper center', bbox_to_anchor=(0.5, 1.38), ncol = 3, fancybox = True, shadow = False )
solid_u_fig.savefig( 'tubeflow_solid_u.pdf', bbox_extra_artists=(lgd,), transparent = True, bbox_inches='tight' )
