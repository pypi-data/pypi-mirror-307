from WITecSDK import WITecSDKClass

def iterateObj(testobj, prefix: str):
    attributes = [attr for attr in dir(testobj)
            if not attr.startswith('_')]
    for item in attributes:
        itemobj = testobj.__getattribute__(item)
        if not callable(itemobj):
            if itemobj is None or isinstance(itemobj, (bool, int, float, str, tuple, list)):
                print(prefix + item + ': ' + str(itemobj))
            else:
                print(prefix + item + ': ' + str(type(itemobj)))
                iterateObj(itemobj, prefix + item + '.')

def testmodule(methodpointer):
    print('')
    print('Testing: ' + str(methodpointer))
    try:
        testmod = methodpointer()
        print(type(testmod))
        iterateObj(testmod, '')

    except Exception as exc:
        print(methodpointer)
        print(type(exc))
        print(exc)

WITec = WITecSDKClass()

testmodule(WITec.CreateActiveSequencer)
testmodule(WITec.CreateAFM)
testmodule(WITec.CreateApertureFieldStop)
testmodule(WITec.CreateApplicationControl)
testmodule(WITec.CreateAutoFocus)
testmodule(WITec.CreateBeamPath)
testmodule(WITec.CreateBottomIllumination)
testmodule(WITec.CreateConfigurationLoader)
testmodule(WITec.CreateDetectorOutput)
testmodule(WITec.CreateDistanceCurve)
testmodule(WITec.CreateFastTimeSeries)
testmodule(WITec.CreateHeating)
testmodule(WITec.CreateImageScan)
testmodule(WITec.CreateImageScanMultipass)
testmodule(WITec.CreateLargeAreaScan)
testmodule(WITec.CreateLaserManager)
testmodule(WITec.CreateLaserPowerSeries)
testmodule(WITec.CreateLineScan)
testmodule(WITec.CreateManualTopography)
testmodule(WITec.CreateObjectiveTurret)
testmodule(WITec.CreateParameterNameGetter)
testmodule(WITec.CreatePolarization)
testmodule(WITec.CreateProjectCreatorSaver)
testmodule(WITec.CreateSampleName)
testmodule(WITec.CreateScanTable)
testmodule(WITec.CreateSingleSpectrum)
testmodule(WITec.CreateSilentSpectrum)
testmodule(WITec.CreateSlowTimeSeriesManual)
testmodule(WITec.CreateSlowTimeSeriesTimed)
testmodule(WITec.CreateSpectralAutofocus)
testmodule(WITec.CreateSpectralStitching)
testmodule(WITec.CreateSpectrograph1)
testmodule(WITec.CreateSpectrograph2)
testmodule(WITec.CreateSpectrograph3)
testmodule(WITec.CreateStateManager)
testmodule(WITec.CreateTopIllumination)
testmodule(WITec.CreateTrueSurface)
testmodule(WITec.CreateVideoControl)
testmodule(WITec.CreateWITecControlVersionTester)
testmodule(WITec.CreateXYAxes)
testmodule(WITec.CreateZAxis)
