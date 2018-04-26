#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 22:02:29 2018

@author: rodrigo
"""

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

colorPreset = {'positive': 'Cool to Warm',
               'zero': 'Cool to Warm (Extended)'}

calculatorSets = {'components': ['Magnitude', 'X', 'Y', 'Z'],
                  'references': [-1, 1, 2, 3]}

def viewCreateAndActive(layoutName, viewName, viewSize=[1200, 1000]):
    CreateLayout('layoutName')

    # set active view
    SetActiveView(None)

    # Create a new 'Render View'
    view = CreateView('RenderView')
    view.ViewSize = viewSize
    view.AxesGrid = 'GridAxes3DActor'
    view.StereoType = 0
    view.Background = [0.32, 0.34, 0.43]

    # get layout
    layout = GetLayout()

    # place view in the layout
    layout.AssignView(0, view)

    # close an empty frame
    layout.Collapse(2)

    # set active view
    SetActiveView(view)

    return layout, view

def createSlicePlane(dataToFilter, view, normalToPlane):
    # create a new 'Slice'
    sliced = Slice(Input=dataToFilter)
    sliced.SliceType = 'Plane'
    sliced.SliceOffsetValues = [0.0]

    # Properties modified on sliced.SliceType
    try:
        # if normalToPlane.lower() is 'x':
        if normalToPlane is 'X':
            sliced.SliceType.Normal = [1.0, 0.0, 0.0]
        # elif normalToPlane.lower() is 'y':
        elif normalToPlane is 'Y':
            sliced.SliceType.Normal = [0.0, 1.0, 0.0]
        #elif normalToPlane.lower() is 'z':
        elif normalToPlane is 'Z':
            sliced.SliceType.Normal = [0.0, 0.0, 1.0]
        else:
            raise Exception("slice not normal to xyz")
    except Exception as err:
        print(err)

    # show data in view
    slicedDisplay = Show(sliced, view)
    # trace defaults for the display properties.
    slicedDisplay.Representation = 'Surface'
    slicedDisplay.ColorArrayName = [None, '']
    slicedDisplay.OSPRayScaleArray = 'CRDisp [m]'
    slicedDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    slicedDisplay.SelectOrientationVectors = 'CRDisp [m]'
    slicedDisplay.ScaleFactor = 0.2
    slicedDisplay.SelectScaleArray = 'CRDisp [m]'
    slicedDisplay.GlyphType = 'Arrow'
    slicedDisplay.GlyphTableIndexArray = 'CRDisp [m]'
    slicedDisplay.DataAxesGrid = 'GridAxesRepresentation'
    slicedDisplay.PolarAxes = 'PolarAxesRepresentation'
    slicedDisplay.GaussianRadius = 0.1
    slicedDisplay.SetScaleArray = ['POINTS', 'CRDisp [m]']
    slicedDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    slicedDisplay.OpacityArray = ['POINTS', 'CRDisp [m]']
    slicedDisplay.OpacityTransferFunction = 'PiecewiseFunction'

    # init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
    slicedDisplay.OSPRayScaleFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    slicedDisplay.ScaleTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    slicedDisplay.OpacityTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

    return sliced, slicedDisplay

def createCalculator(dataToFilter, view, variableOfInterest, resultName):
    
    # create a new 'Calculator'
    calculated = Calculator(Input=dataToFilter)
    calculated.Function = ''
    
    # Properties modified on calculator1
    calculated.Function = variableOfInterest
    calculated.ResultArrayName = resultName
    
    # get color transfer function/color map for 'Vel_X'
    # vel_XLUT = GetColorTransferFunction('Vel_X')
    
    # show data in view
    calculatedDisplay = Show(calculated, view)
    # trace defaults for the display properties.
    calculatedDisplay.Representation = 'Surface'
    calculatedDisplay.ColorArrayName = [None, '']
    calculatedDisplay.OSPRayScaleArray = 'CRDisp [m]'
    calculatedDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    calculatedDisplay.SelectOrientationVectors = 'CRDisp [m]'
    calculatedDisplay.ScaleFactor = 0.2
    calculatedDisplay.SelectScaleArray = 'CRDisp [m]'
    calculatedDisplay.GlyphType = 'Arrow'
    calculatedDisplay.GlyphTableIndexArray = 'CRDisp [m]'
    calculatedDisplay.DataAxesGrid = 'GridAxesRepresentation'
    calculatedDisplay.PolarAxes = 'PolarAxesRepresentation'
    calculatedDisplay.GaussianRadius = 0.1
    calculatedDisplay.SetScaleArray = ['POINTS', 'CRDisp [m]']
    calculatedDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    calculatedDisplay.OpacityArray = ['POINTS', 'CRDisp [m]']
    calculatedDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    
    return calculated, calculatedDisplay

def createCountour(dataToFilter, view, variableOfInterest, contours):
    # create a new 'Contour'
    contoured = Contour(Input=dataToFilter)
    contoured.ContourBy = ['POINTS', variableOfInterest]
    contoured.Isosurfaces = contours
    contoured.PointMergeMethod = 'Uniform Binning'
    
    # show data in view
    contouredDisplay = Show(contoured, view)
    # trace defaults for the display properties.
    contouredDisplay.Representation = 'Surface'
    contouredDisplay.ColorArrayName = [None, '']
    contouredDisplay.OSPRayScaleArray = 'CRDisp [m]'
    contouredDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    contouredDisplay.SelectOrientationVectors = 'CRDisp [m]'
    contouredDisplay.ScaleFactor = 0.2
    contouredDisplay.SelectScaleArray = 'CRDisp [m]'
    contouredDisplay.GlyphType = 'Arrow'
    contouredDisplay.GlyphTableIndexArray = 'CRDisp [m]'
    contouredDisplay.DataAxesGrid = 'GridAxesRepresentation'
    contouredDisplay.PolarAxes = 'PolarAxesRepresentation'
    contouredDisplay.GaussianRadius = 0.1
    contouredDisplay.SetScaleArray = ['POINTS', 'CRDisp [m]']
    contouredDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    contouredDisplay.OpacityArray = ['POINTS', 'CRDisp [m]']
    contouredDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    
    return contoured, contouredDisplay

def positionCamera(view, perspective):
    #view.CameraPosition = [0.17, -4, 0]
    #view.CameraFocalPoint = [0.17, 0, 0]
    view.CameraPosition = perspective['position']
    view.CameraFocalPoint = perspective['focalPoint']
    view.CameraViewUp = perspective['viewUp']
    view.CameraParallelScale = perspective['parallelScale']

