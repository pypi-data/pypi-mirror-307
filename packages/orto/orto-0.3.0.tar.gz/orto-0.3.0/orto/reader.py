def read_uvvis(file_name: str, intensity_type: str = 'velocity'):
    '''
    Reads Absorption Spectrum (UVVIS) data from CI calculation

    Parameters
    ----------
    file_name: str
        Name of ORCA output file
    intensity_type: str, {'velocity', 'electric'}
        Intensities to use in plot
    '''

    wnumbers, fosc, p2 = [], [], []

    with open(file_name, 'r') as f:
        for line in f:
            if f'ABSORPTION SPECTRUM VIA TRANSITION {intensity_type.upper()} DIPOLE' in line: # noqa
                for _ in range(5):
                    line = next(f)
                while len(line.split()):
                    wnumbers.append(float(line.split()[4]))
                    fosc.append(float(line.split()[6]))
                    p2.append(float(line.split()[7]))
                    line = next(f)
                break

    if not all([len(wnumbers), len(fosc), len(p2)]):
        raise ValueError('Cannot find data in file')

    return wnumbers, fosc, p2


def read_infrared(file_name: str):
    '''
    Reads infrared spectroscopy information from ORCA output file
    '''
    raise NotImplementedError


def read_raman(file_name: str):
    '''
    Reads Raman spectroscopy information from ORCA output file
    '''
    raise NotImplementedError
