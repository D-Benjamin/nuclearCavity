#### import the simple module from the paraview
from paraview.simple import *
from math import pi
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

from pvfilters import *

from genfoam import *

########### CONFIGURATION ############################

fluxGroups = 6
precursorsGroups = 8

data = genfoamData(fluxGroups, precursorsGroups)

################## CASES #################################

path = '../'

case01 = {'path': '0.1/',
          'step': '0.1',
          'responses': [data.U],
          'tickPrecision': ['%-#6.2g']}

case02 = {'path': '0.2/',
          'step': '0.2',
          'responses': [data.oneGroupFlux],
          'tickPrecision': ['%-#6.2g']}

case03 = {'path': '0.3/',
          'step': '0.3',
          'responses': [data.T],
          'tickPrecision': ['%-#6.4g']}

case11 = {'path': '1.1/',
          'step': '1.1',
          'responses': [data.prec],
          'tickPrecision': ['%-#6.2g']}

case13 = {'path': '1.3/',
          'step': '1.3',
          'responses': [data.T, data.oneGroupFlux, data.prec, data.rhoCoolNeutro],
          'tickPrecision': ['%-#6.4g', '%-#6.2g', '%-#6.2g', '%-#6.4g']}

case15 = {'path': '1.5/',
          'step': '1.5',
          'responses': [data.U, data.T, data.oneGroupFlux, data.prec, data.rhoCoolNeutro],
          'tickPrecision': ['%-#6.2g', '%-#6.4g', '%-#6.2g', '%-#6.2g', '%-#6.4g']}

case = case01

# contour plot parameters
lower = -0.45
upper = 0.45
step = 0.05

legendPosition = 'right'
#legendPosition = 'bottom'
#output = 'tight'
output = 'center'
font = 'medium'
#font = 'big'

outputFormat = 'png'

########### PRESETS ######################

if legendPosition is 'right':
    if output is 'center':
        legend = {'fontSize': 30,
                  'horizontal': False,
                  'barLength': 0.6,
                  'barPosition': [0.80, 0.2]}
        perspective = {'position': [0, 0, 4],
                       'focalPoint': [0, 0, 0],
                       'viewUp': [0.0, 1.0, 0.0],
                       'parallelScale': 1}
        viewSize = [1200, 700]

    elif output is 'tight':
        offset = 0.3
        legend = {'fontSize': 30,
                  'horizontal': False,
                  'barLength': 0.6,
                  'barPosition': [0.78, 0.2]}
        perspective = {'position': [0 + offset, 0, 4],
                       'focalPoint': [0 + offset, 0, 0],
                       'viewUp': [0.0, 1.0, 0.0],
                       'parallelScale': 1}
        viewSize = [900, 700]

elif legendPosition is 'bottom':
    offset = 0.18
    legend = {'fontSize': 30,
              'horizontal': True,
              'barLength': 0.6,
              'barPosition': [0.2, 0.12]}
    perspective = {'position': [0, 0 - offset, 4.5],
                   'focalPoint': [0, 0 - offset, 0],
                   'viewUp': [0.0, 1.0, 0.0],
                   'parallelScale': 1}
    viewSize = [700, 800]


screenshotFactor = 2

screeshotResolution = [i * screenshotFactor for i in viewSize]

########### START OF CASE LOAD ###########

# create a new 'OpenFOAMReader'
OFcase = OpenFOAMReader(FileName=path + case['path'] + case['step'] + '.foam')
#OFcase.MeshRegions = ['fluidRegion/internalMesh', 'neutroRegion/internalMesh']
OFcase.MeshRegions = ['fluidRegion/internalMesh']
#OFcase.MeshRegions = ['neutroRegion/internalMesh']
OFcase.CellArrays = ['CRDisp', 'DFluid', 'DNeutro', 'Disp', 'E', 'Re', 'T', 'TCoolNeutro', 'TavClad', 'TavFuel',
                     'TavFuelMech', 'TcladNeutro', 'TfuelNeutro', 'TinnerClad', 'TinnerFuel', 'Tmech', 'TouterClad',
                     'TouterFuel', 'Tstructures', 'U', 'UNeutro', 'alpha', 'axExp', 'defaultFlux', 'defaultFlux2',
                     'defaultPrec', 'delayedNeutroSource', 'discFactor0', 'discFactor1', 'discFactor2', 'discFactor3',
                     'discFactor4', 'discFactor5', 'flux0', 'flux1', 'flux2', 'flux3', 'flux4', 'flux5', 'fluxStar0',
                     'fluxStar1', 'fluxStar2', 'fluxStar20', 'fluxStar21', 'fluxStar22', 'fluxStar23', 'fluxStar24',
                     'fluxStar25', 'fluxStar3', 'fluxStar4', 'fluxStar5', 'fuelDisp', 'fuelDispVector', 'meshDisp',
                     'neutroSource', 'nuMech', 'oneGroupFlux', 'p', 'p_rgh', 'porosityNeutro', 'prec0', 'prec1',
                     'prec2', 'prec3', 'prec4', 'prec5', 'prec6', 'prec7', 'radExp', 'realU', 'rho', 'rhoCoolNeutro',
                     'rhoMech', 'rhok', 'sigmaDisapp0', 'sigmaDisapp1', 'sigmaDisapp2', 'sigmaDisapp3', 'sigmaDisapp4',
                     'sigmaDisapp5', 'volFuelPower', 'volFuelPowerNeutro', 
                     'TErrorRelative', 'pErrorRelative', 'UErrorRelative', 'fluxErrorRelative']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

########### END OF OF CASE LOAD ###########

# Go to last time step
animationScene1.GoToLast()

#info = OFcase.GetDataInformation().DataInformation

########### START FIRST APPLY #############

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = viewSize

# find view
#renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

# show data in view
DataInDisplay = Show(OFcase, renderView1)
# trace defaults for the display properties.
DataInDisplay.Representation = 'Surface'
DataInDisplay.ColorArrayName = [None, '']
DataInDisplay.OSPRayScaleArray = 'CRDisp [m]'
DataInDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
DataInDisplay.SelectOrientationVectors = 'CRDisp [m]'
DataInDisplay.ScaleFactor = 0.2
DataInDisplay.SelectScaleArray = 'CRDisp [m]'
DataInDisplay.GlyphType = 'Arrow'
DataInDisplay.GlyphTableIndexArray = 'CRDisp [m]'
DataInDisplay.DataAxesGrid = 'GridAxesRepresentation'
DataInDisplay.PolarAxes = 'PolarAxesRepresentation'
DataInDisplay.ScalarOpacityUnitDistance = 0.06082201995573402
DataInDisplay.GaussianRadius = 0.1
DataInDisplay.SetScaleArray = ['POINTS', 'CRDisp [m]']
DataInDisplay.ScaleTransferFunction = 'PiecewiseFunction'
DataInDisplay.OpacityArray = ['POINTS', 'CRDisp [m]']
DataInDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
DataInDisplay.OSPRayScaleFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
DataInDisplay.ScaleTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
DataInDisplay.OpacityTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

# update the view to ensure updated data information
renderView1.Update()

################ Y-NORMAL SLICE FILTER ########################

slice1, slice1Display = createSlicePlane(OFcase, renderView1, 'Z')

# hide data in view
Hide(OFcase, renderView1)

# update the view to ensure updated data information
renderView1.Update()

################## FINISH SLICING #############################

# set active source
SetActiveSource(OFcase) # CHANGE ACTIVE SOURCE IN ORDER TO REMOVE SLICE FRAME FROM SCREENSHOT

################### PREPARE TO SAVE ##################

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

positionCamera(renderView1, perspective)

for response, tick in zip(case['responses'], case['tickPrecision']):
    for responseLabel, responseTitle in zip(response['label'], response['title']):

        HideAll(renderView1)
        HideUnusedScalarBars(renderView1)

        if response['rank'] is 0:

            # set active source
            SetActiveSource(slice1)

            # show data in view
            slice1Display = Show(slice1, renderView1)

            # show color bar/color legend
            slice1Display.SetScalarBarVisibility(renderView1, True)

            ColorBy(slice1Display, ('POINTS', responseLabel))
            
            # rescale color and/or opacity maps used to include current data range
            slice1Display.RescaleTransferFunctionToDataRange(True, False)
            
            # get color transfer function/color map for 'Ums'
            responseLUT = GetColorTransferFunction(responseLabel)
            
            # get opacity transfer function/opacity map for 'Ums'
            responsePWF = GetOpacityTransferFunction(responseLabel)
                
            # show color bar/color legend
            slice1Display.SetScalarBarVisibility(renderView1, True)
            
            responseLUT.ApplyPreset(colorPreset['positive'], True)
            
            # get color legend/bar for umsLUT in view renderView1
            responseLUTColorBar = GetScalarBar(responseLUT, renderView1)
        
            responseLUTColorBar.Title = responseTitle + response['unit']
            responseLUTColorBar.TitleColor = [0.0, 0.0, 0.0]    # change font color to Black
            responseLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
        
            # Properties modified on umsLUTColorBar
            responseLUTColorBar.RangeLabelFormat = tick
        
            # change scalar bar placement
            responseLUTColorBar.WindowLocation = 'AnyLocation'
            if legend['horizontal']:
                responseLUTColorBar.Orientation = 'Horizontal'
                responseLUTColorBar.TextPosition = 'Ticks left/bottom, annotations right/top'
            responseLUTColorBar.Position = legend['barPosition']
            responseLUTColorBar.ScalarBarLength = legend['barLength']
            responseLUTColorBar.TitleFontSize = legend['fontSize']
            responseLUTColorBar.LabelFontSize = legend['fontSize']

            # set active source
            SetActiveSource(OFcase)

            ################## SAVE #######################################

            UpdateScalarBars(renderView1)
            
            Render(renderView1)
                
            # save screenshot
            SaveScreenshot(path + case['path'] + case['step'] + responseLabel + '.png', renderView1, ImageResolution=screeshotResolution, TransparentBackground=1)

            #ExportView(path + case['path'] + responseLabel + '.pdf', renderView1)
            
            
        elif response['rank'] is 1:
            
            # pre-alocate calculators and contours for each component plus magnitude
            calculators = [None] * (3**response['rank'] + 1)
            calculatorsDisplay = [None] * (3**response['rank'] + 1)
            contours = [{'zero': None, 'notZero': None}] * (3**response['rank'] + 1)
            contoursDisplay = [{'zero': None, 'notZero': None}] * (3**response['rank'] + 1)
            
            for component, reference, calculator, calculatorDisplay, contour, contourDisplay in zip(calculatorSets['components'], calculatorSets['references'], calculators, calculatorsDisplay, contours, contoursDisplay):
            
                ################## CREATE CALCULATOR ##########################
                if component is 'Magnitude':
                    #calculator, calculatorDisplay = createCalculator(slice1, renderView1, 'sqrt(' + responseLabel + '_X^2+' + responseLabel + '_Y^2+' + responseLabel + '_Z^2)', responseLabel + '_calc_' + component)

                    #Show(slice1, renderView1)

                    # show data in view
                    slice1Display = Show(slice1, renderView1)

                    # show color bar/color legend
                    slice1Display.SetScalarBarVisibility(renderView1, True)

                    ColorBy(slice1Display, ('POINTS', responseLabel))
                    
                    # rescale color and/or opacity maps used to include current data range
                    slice1Display.RescaleTransferFunctionToDataRange(True, False)
                    
                    # get color transfer function/color map for 'Ums'
                    responseLUT = GetColorTransferFunction(responseLabel)
                    
                    # get opacity transfer function/opacity map for 'Ums'
                    responsePWF = GetOpacityTransferFunction(responseLabel)

                    #responseLUT.RescaleTransferFunction(0, 0.5)
                    #responsePWF.RescaleTransferFunction(0, 0.5)
                        
                    # show color bar/color legend
                    slice1Display.SetScalarBarVisibility(renderView1, True)
                    
                    responseLUT.ApplyPreset(colorPreset['positive'], True)
                    
                    # get color legend/bar for umsLUT in view renderView1
                    responseLUTColorBar = GetScalarBar(responseLUT, renderView1)
                
                    responseLUTColorBar.Title = responseTitle + response['unit']
                    responseLUTColorBar.TitleColor = [0.0, 0.0, 0.0]    # change font color to Black
                    responseLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
                
                    # Properties modified on umsLUTColorBar
                    responseLUTColorBar.RangeLabelFormat = tick
                
                    # change scalar bar placement
                    responseLUTColorBar.WindowLocation = 'AnyLocation'
                    if legend['horizontal']:
                        responseLUTColorBar.Orientation = 'Horizontal'
                        responseLUTColorBar.TextPosition = 'Ticks left/bottom, annotations right/top'
                    responseLUTColorBar.Position = legend['barPosition']
                    responseLUTColorBar.ScalarBarLength = legend['barLength']
                    responseLUTColorBar.TitleFontSize = legend['fontSize']
                    responseLUTColorBar.LabelFontSize = legend['fontSize']


                    # create a new 'Cell Centers'
                    cellCenters1 = CellCenters(Input=slice1)
                    # show data in view
                    cellCenters1Display = Show(cellCenters1, renderView1)
                    # trace defaults for the display properties.
                    cellCenters1Display.Representation = 'Surface'
                    cellCenters1Display.ColorArrayName = [None, '']
                    cellCenters1Display.OSPRayScaleArray = 'CRDisp'
                    cellCenters1Display.OSPRayScaleFunction = 'PiecewiseFunction'
                    cellCenters1Display.SelectOrientationVectors = 'CRDisp'
                    cellCenters1Display.ScaleFactor = 0.2
                    cellCenters1Display.SelectScaleArray = 'CRDisp'
                    cellCenters1Display.GlyphType = 'Arrow'
                    cellCenters1Display.GlyphTableIndexArray = 'CRDisp'
                    cellCenters1Display.DataAxesGrid = 'GridAxesRepresentation'
                    cellCenters1Display.PolarAxes = 'PolarAxesRepresentation'
                    cellCenters1Display.GaussianRadius = 0.1
                    cellCenters1Display.SetScaleArray = ['POINTS', 'CRDisp']
                    cellCenters1Display.ScaleTransferFunction = 'PiecewiseFunction'
                    cellCenters1Display.OpacityArray = ['POINTS', 'CRDisp']
                    cellCenters1Display.OpacityTransferFunction = 'PiecewiseFunction'

                    # init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
                    cellCenters1Display.OSPRayScaleFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

                    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
                    cellCenters1Display.ScaleTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

                    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
                    cellCenters1Display.OpacityTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

                    # show color bar/color legend
                    cellCenters1Display.SetScalarBarVisibility(renderView1, True)

                    # update the view to ensure updated data information
                    renderView1.Update()

                    # create a new 'Glyph'
                    glyph1 = Glyph(Input=cellCenters1, GlyphType='Arrow')
                    glyph1.Scalars = ['POINTS', 'None']
                    glyph1.Vectors = ['POINTS', 'U']
                    glyph1.ScaleFactor = 0.08 # TO-DO: move to config
                    glyph1.GlyphTransform = 'Transform2'

                    # show data in view
                    glyph1Display = Show(glyph1, renderView1)
                    # trace defaults for the display properties.
                    glyph1Display.Representation = 'Surface'
                    glyph1Display.ColorArrayName = [None, '']
                    glyph1Display.OSPRayScaleArray = 'CRDisp'
                    glyph1Display.OSPRayScaleFunction = 'PiecewiseFunction'
                    glyph1Display.SelectOrientationVectors = 'CRDisp'
                    glyph1Display.ScaleFactor = 0.2
                    glyph1Display.SelectScaleArray = 'CRDisp'
                    glyph1Display.GlyphType = 'Arrow'
                    glyph1Display.GlyphTableIndexArray = 'CRDisp'
                    glyph1Display.DataAxesGrid = 'GridAxesRepresentation'
                    glyph1Display.PolarAxes = 'PolarAxesRepresentation'
                    glyph1Display.GaussianRadius = 0.1
                    glyph1Display.SetScaleArray = ['POINTS', 'CRDisp']
                    glyph1Display.ScaleTransferFunction = 'PiecewiseFunction'
                    glyph1Display.OpacityArray = ['POINTS', 'CRDisp']
                    glyph1Display.OpacityTransferFunction = 'PiecewiseFunction'

                    # init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
                    glyph1Display.OSPRayScaleFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

                    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
                    glyph1Display.ScaleTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

                    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
                    glyph1Display.OpacityTransferFunction.Points = [6.548259181323878e+16, 0.0, 0.5, 0.0, 3.1789731093143355e+19, 1.0, 0.5, 0.0]

                    # TO-DO: move to config
                    #glyph1.ScaleMode = 'vector'

                    # update the view to ensure updated data information
                    renderView1.Update()

                    # Properties modified on glyph1
                    # TO-DO: move to config
                    glyph1.GlyphMode = 'Every Nth Point'
                    glyph1.Stride = 117

                    glyph1Display.DiffuseColor = [0.0, 0.0, 0.0]

                    # set active source
                    SetActiveSource(slice1)

                    ################## SAVE #######################################

                    UpdateScalarBars(renderView1)
                    
                    Render(renderView1)
                    
                    # save screenshot
                    SaveScreenshot(path + case['path'] + case['step'] + responseLabel + component + '_glyph.png', renderView1, ImageResolution=screeshotResolution, TransparentBackground=1)

                    #ExportView(path + case['path'] + responseLabel + component + '_contour.pdf', renderView1)
                    
                    Hide(glyph1, renderView1)

                else:
                    calculator, calculatorDisplay = createCalculator(slice1, renderView1, responseLabel + '_' + component, responseLabel + '_calc_' + component)
                
                    # hide data in view
                    Hide(slice1, renderView1)
                    
                    # show color bar/color legend
                    calculatorDisplay.SetScalarBarVisibility(renderView1, True)
                    
                    # update the view to ensure updated data information
                    renderView1.Update()
                    
                    ################## CREATE CONTOUR ####################
                    
                    interval = int((upper - lower)/step) + 1 # account for excluded 0.0
                    contourRange = [round(lower + step*f, 5) for f in range(interval) if round(lower + step*f, 5) != 0.0]
                    
                    contour['notZero'], contourDisplay['notZero'] = createCountour(calculator, renderView1, responseLabel + '_calc_' + component, contourRange)
                    
                    contour['zero'], contourDisplay['zero'] = createCountour(calculator, renderView1, responseLabel + '_calc_' + component, [0.0])
                    contourDisplay['zero'].DiffuseColor = [0.0, 0.0, 0.0] # set contour line color to Black
                    
                    # update the view to ensure updated data information
                    renderView1.Update()
                    
                    # set active source
                    SetActiveSource(calculator)
                    
                    # show data in view
                    calculatorDisplay = Show(calculator, renderView1)
                    
                    # show color bar/color legend
                    calculatorDisplay.SetScalarBarVisibility(renderView1, True)
                    
                    # set active source
                    SetActiveSource(contour['zero'])
                    
                    ################## COLORS AND STUFF ###########################
            
                    # set scalar coloring
                    ColorBy(calculatorDisplay, ('POINTS', responseLabel, component))
            
                    # rescale color and/or opacity maps used to include current data range
                    calculatorDisplay.RescaleTransferFunctionToDataRange(True, False)
            
                    # show color bar/color legend
                    calculatorDisplay.SetScalarBarVisibility(renderView1, True)
            
                    # get color transfer function/color map for 'Ums'
                    responseLUT = GetColorTransferFunction(responseLabel)
            
                    # get opacity transfer function/opacity map for 'Ums'
                    responsePWF = GetOpacityTransferFunction(responseLabel)
            
                    # Rescale transfer function
                    if case['step'] is '0.1':
                        if component is 'X':
                            responseLUT.RescaleTransferFunction(-0.5, 0.5)
                            responsePWF.RescaleTransferFunction(-0.5, 0.5)
            
                        if component is 'Y':
                            responseLUT.RescaleTransferFunction(-0.224595, 0.224595)
                            responsePWF.RescaleTransferFunction(-0.224595, 0.224595)
            
                    if case['step'] is '1.5':
            
                        # arrayInfo = info.GetArrayInformation(responseName, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS)
                        # valueRange = arrayInfo.GetComponentRange(reference)
                        # maxValue = max(valueRange)
            
                        if component is 'Y':
                            responseLUT.RescaleTransferFunction(-0.211705, 0.211705)
                            responsePWF.RescaleTransferFunction(-0.211705, 0.211705)
            
                    try:
                        # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
                        if component is 'Magnitude':
                            responseLUT.ApplyPreset(colorPreset['positive'], True)
                        elif component is 'X' or 'Y' or 'Z':
                            responseLUT.ApplyPreset(colorPreset['zero'], True)
                        else:
                            raise Exception("Component of vector {} is not Magnitude neither X|Y|Z".format(responseLabel))
                    except Exception as err:
                        print(err)
            
                    ################ PREPARE FOR SCREENSHOT #######################
            
                    # get color legend/bar for umsLUT in view renderView1
                    responseLUTColorBar = GetScalarBar(responseLUT, renderView1)
            
                    responseLUTColorBar.Title = responseTitle + response['unit']
                    responseLUTColorBar.TitleColor = [0.0, 0.0, 0.0]    # change font color to Black
                    responseLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

                    responseLUTColorBar.ComponentTitle = component
            
                    # Properties modified on umsLUTColorBar
                    responseLUTColorBar.RangeLabelFormat = tick
            
                    # change scalar bar placement
                    responseLUTColorBar.WindowLocation = 'AnyLocation'
                    if legend['horizontal']:
                        responseLUTColorBar.Orientation = 'Horizontal'
                        responseLUTColorBar.TextPosition = 'Ticks left/bottom, annotations right/top'
                    responseLUTColorBar.Position = legend['barPosition']
                    responseLUTColorBar.ScalarBarLength = legend['barLength']
                    responseLUTColorBar.TitleFontSize = legend['fontSize']
                    responseLUTColorBar.LabelFontSize = legend['fontSize']
        
                    ################## SAVE #######################################

                    UpdateScalarBars(renderView1)
                    
                    Render(renderView1)
                    
                    # save screenshot
                    SaveScreenshot(path + case['path'] + case['step'] + responseLabel + component + '_contour.png', renderView1, ImageResolution=screeshotResolution, TransparentBackground=1)

                    #ExportView(path + case['path'] + responseLabel + component + '_contour.pdf', renderView1)
                    
                    Hide(contour['zero'], renderView1)
                    Hide(contour['notZero'], renderView1)

