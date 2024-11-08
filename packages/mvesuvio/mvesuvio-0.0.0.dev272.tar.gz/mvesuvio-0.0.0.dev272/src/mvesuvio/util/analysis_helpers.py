
from mantid.simpleapi import Load, Rebin, Scale, SumSpectra, Minus, CropWorkspace, \
                            CloneWorkspace, MaskDetectors, CreateWorkspace, CreateEmptyTableWorkspace, \
                            mtd, RenameWorkspace
import numpy as np
import numbers

from mvesuvio.analysis_fitting import passDataIntoWS

from dataclasses import dataclass

@dataclass(frozen=False)
class NeutronComptonProfile:
    label: str
    mass: float

    intensity: float
    width: float
    center: float

    intensity_bounds: list[float, float]
    width_bounds: list[float, float]
    center_bounds: list[float, float]

    mean_intensity: float = None
    mean_width: float = None
    mean_center: float = None



def loadRawAndEmptyWsFromUserPath(userWsRawPath, userWsEmptyPath, 
                                  tofBinning, name, scaleRaw, scaleEmpty, subEmptyFromRaw):
    print("\nLoading local workspaces ...\n")
    Load(Filename=str(userWsRawPath), OutputWorkspace=name + "_raw")
    Rebin(
        InputWorkspace=name + "_raw",
        Params=tofBinning,
        OutputWorkspace=name + "_raw",
    )

    assert (isinstance(scaleRaw, numbers.Real)), "Scaling factor of raw ws needs to be float or int."
    Scale(
        InputWorkspace=name + "_raw",
        OutputWorkspace=name + "_raw",
        Factor=str(scaleRaw),
    )

    SumSpectra(InputWorkspace=name + "_raw", OutputWorkspace=name + "_raw" + "_sum")
    wsToBeFitted = mtd[name+"_raw"]

    if subEmptyFromRaw:
        Load(Filename=str(userWsEmptyPath), OutputWorkspace=name + "_empty")
        Rebin(
            InputWorkspace=name + "_empty",
            Params=tofBinning,
            OutputWorkspace=name + "_empty",
        )

        assert (isinstance(scaleEmpty, float)) | (
            isinstance(scaleEmpty, int)
        ), "Scaling factor of empty ws needs to be float or int"
        Scale(
            InputWorkspace=name + "_empty",
            OutputWorkspace=name + "_empty",
            Factor=str(scaleEmpty),
        )

        SumSpectra(
            InputWorkspace=name + "_empty", OutputWorkspace=name + "_empty" + "_sum"
        )

        wsToBeFitted = Minus(
            LHSWorkspace=name + "_raw",
            RHSWorkspace=name + "_empty",
            OutputWorkspace=name + "_raw_minus_empty",
        )
    return wsToBeFitted


def cropAndMaskWorkspace(ws, firstSpec, lastSpec, maskedDetectors, maskTOFRange):
    """Returns cloned and cropped workspace with modified name"""
    # Read initial Spectrum number
    wsFirstSpec = ws.getSpectrumNumbers()[0]
    assert (
        firstSpec >= wsFirstSpec
    ), "Can't crop workspace, firstSpec < first spectrum in workspace."

    initialIdx = firstSpec - wsFirstSpec
    lastIdx = lastSpec - wsFirstSpec

    newWsName = ws.name().split("_raw")[0]  # Retrieve original name
    wsCrop = CropWorkspace(
        InputWorkspace=ws,
        StartWorkspaceIndex=initialIdx,
        EndWorkspaceIndex=lastIdx,
        OutputWorkspace=newWsName,
    )

    maskBinsWithZeros(wsCrop, maskTOFRange)  # Used to mask resonance peaks

    MaskDetectors(Workspace=wsCrop, SpectraList=maskedDetectors)
    return wsCrop


def maskBinsWithZeros(ws, maskTOFRange):
    """
    Masks a given TOF range on ws with zeros on dataY.
    Leaves errors dataE unchanged, as they are used by later treatments.
    Used to mask resonance peaks.
    """

    if maskTOFRange is None:
        return

    dataX, dataY, dataE = extractWS(ws)
    start, end = [int(s) for s in maskTOFRange.split(",")]
    assert (
        start <= end
    ), "Start value for masking needs to be smaller or equal than end."
    mask = (dataX >= start) & (dataX <= end)  # TOF region to mask

    dataY[mask] = 0

    passDataIntoWS(dataX, dataY, dataE, ws)
    return


def extractWS(ws):
    """Directly extracts data from workspace into arrays"""
    return ws.extractX(), ws.extractY(), ws.extractE()


def loadConstants():
    """Output: the mass of the neutron, final energy of neutrons (selected by gold foil),
    factor to change energies into velocities, final velocity of neutron and hbar"""
    mN = 1.008  # a.m.u.
    Ef = 4906.0  # meV
    en_to_vel = 4.3737 * 1.0e-4
    vf = np.sqrt(Ef) * en_to_vel  # m/us
    hbar = 2.0445
    constants = (mN, Ef, en_to_vel, vf, hbar)
    return constants


def numericalThirdDerivative(x, y):
    k6 = (- y[:, 12:] + y[:, :-12]) * 1
    k5 = (+ y[:, 11:-1] - y[:, 1:-11]) * 24
    k4 = (- y[:, 10:-2] + y[:, 2:-10]) * 192
    k3 = (+ y[:, 9:-3] - y[:, 3:-9]) * 488
    k2 = (+ y[:, 8:-4] - y[:, 4:-8]) * 387
    k1 = (- y[:, 7:-5] + y[:, 5:-7]) * 1584

    dev = k1 + k2 + k3 + k4 + k5 + k6
    dev /= np.power(x[:, 7:-5] - x[:, 6:-6], 3)
    dev /= 12**3

    derivative = np.zeros_like(y)
    # Padded with zeros left and right to return array with same shape
    derivative[:, 6:-6] = dev
    return derivative


def createWS(dataX, dataY, dataE, wsName, parentWorkspace=None):
    ws = CreateWorkspace(
        DataX=dataX.flatten(),
        DataY=dataY.flatten(),
        DataE=dataE.flatten(),
        Nspec=len(dataY),
        OutputWorkspace=wsName,
        ParentWorkspace=parentWorkspace
    )
    return ws


def fix_profile_parameters(incoming_means_table, receiving_profiles_table, h_ratio):
    means_dict = _convert_table_to_dict(incoming_means_table)
    profiles_dict = _convert_table_to_dict(receiving_profiles_table)

    # Set intensities
    for p in profiles_dict.values():
        if np.isclose(p['mass'], 1, atol=0.1):    # Hydrogen present
            p['intensity'] = h_ratio * _get_lightest_profile(means_dict)['mean_intensity']
            continue
        p['intensity'] = means_dict[p['label']]['mean_intensity']

    # Normalise intensities
    sum_intensities = sum([p['intensity'] for p in profiles_dict.values()])
    for p in profiles_dict.values():
        p['intensity'] /= sum_intensities
        
    # Set widths
    for p in profiles_dict.values():
        try:
            p['width'] = means_dict[p['label']]['mean_width']
        except KeyError:
            continue

    # Fix all widths except lightest mass
    for p in profiles_dict.values():
        if p == _get_lightest_profile(profiles_dict):
            continue
        p['width_bounds'] = str([p['width'] , p['width']])

    result_profiles_table = _convert_dict_to_table(profiles_dict)
    return result_profiles_table


def _convert_table_to_dict(table):
    result_dict = {}
    for i in range(table.rowCount()):
        row_dict = table.row(i) 
        result_dict[row_dict['label']] = row_dict
    return result_dict


def _convert_dict_to_table(m_dict):
    table = CreateEmptyTableWorkspace()
    for p in m_dict.values():
        if table.columnCount() == 0:
            for key, value in p.items():
                value_type = 'str' if isinstance(value, str) else 'float'
                table.addColumn(value_type, key)

        table.addRow(p)
    return table


def _get_lightest_profile(p_dict):
    profiles = [p for p in p_dict.values()]
    masses = [p['mass'] for p in p_dict.values()]
    return profiles[np.argmin(masses)]


def calculate_h_ratio(means_table):

    masses = means_table.column("mass")
    intensities = np.array(means_table.column("mean_intensity"))

    if not np.isclose(min(masses), 1, atol=0.1):    # Hydrogen not present
        return None
    
    # Hydrogen present 
    sorted_intensities = intensities[np.argsort(masses)]

    return sorted_intensities[0] / sorted_intensities[1] 

