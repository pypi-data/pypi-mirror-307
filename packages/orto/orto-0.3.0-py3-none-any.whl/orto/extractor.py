import numpy as np
from numpy.typing import NDArray
import xyz_py as xyzp
import extto
import re
import pandas as pd
from io import StringIO


def get_coords(file_name: str, coord_type: str = 'init',
               index_style: str = 'per_element') -> tuple[list, NDArray]:
    '''
    Extracts cartesian coordinates and atom labels from Orca output file

    Parameters
    ----------
    file_name: str
        Name of Orca output file to parse
    coord_type: str, {'init', 'opt'}
        Specifies which set of coordinates to extract\n
        Options are:\n
        "init" = Initial coordinates\n
        "opt" = Final optimised coordinates
    index_style: str {'per_element', 'sequential', 'sequential_orca', 'none'}
        Specifies what type of atom label indexing used for final atom labels\n
        Options are:\n
        'per_element' = Index by element e.g. Dy1, Dy2, N1, N2, etc.\n
        'sequential' = Index the atoms 1->N regardless of element\n
        'sequential_orca' = Index the atoms 0->N-1 regardless of element\n
        'none' = No label indexing

    Returns
    -------
    list
        Atomic labels
    ndarray of floats
        (n_atoms,3) array containing xyz coordinates of each atom
    '''

    labels, coords = [], []

    with open(file_name, 'r') as f:
        for line in f:
            if 'CARTESIAN COORDINATES (ANGSTROEM)' in line:
                labels, coords = [], []
                line = next(f)
                line = next(f)
                while len(line.lstrip().rstrip()):
                    labels.append(line.split()[0])
                    coords.append([float(val) for val in line.split()[1:4]])
                    line = next(f)
                if coord_type.lower() == 'init':
                    break

    if not len(labels):
        raise ValueError(f'Cannot find coordinates in {file_name}')

    if index_style in ['per_element', 'sequential']:
        labels = xyzp.add_label_indices(labels, style=index_style)
    elif index_style == 'sequential_orca':
        labels = xyzp.add_label_indices(
            labels, style='sequential', start_index=0
        )
    else:
        labels = xyzp.remove_label_indices(labels)

    return labels, np.asarray(coords)


class SusceptibilityExtractor(extto.BetweenExtractor):
    '''
    Extracts Magnetic Susceptibility as a function of temperature
    '''

    # Modifiers for line/block extraction
    MODIFIERS = [re.MULTILINE]

    # Regex Start Pattern
    START_PATTERN = rb'(?<=-{59}$\s{8}TEMPERATURE DEPENDENT MAGNETIC SUSCEPTIBILITY\s{8}-{59}[\S\s]{182})' # noqa

    # Regex End Pattern
    END_PATTERN = rb'(?=-{59}$)'

    @property
    def data(self) -> list[pd.DataFrame]:
        '''
        Processed susceptibility data, one dataframe per extracted block.\n
        For each entry, column titles are \n
         - Static Field (Gauss)\n
         - Temperature (K)\n
         - M/B: chi*T (cm3*K/mol)\n
         - chi*T (cm3*K/mol)\n
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> pd.DataFrame:
        '''
        Converts single block into array of susceptibility as a function of
        temperature

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        pd.DataFrame
            Susceptibility dataframe with columns described in self.data
        '''

        _ext = re.compile(
            r'\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(----|\d+\.\d+)\s+(\d+\.\d+)\s*'
        )

        data = pd.DataFrame(_ext.findall(block), index=None)
        data.columns = [
            'Static Field (Gauss)',
            'Temperature (K)',
            'M/B: chi*T (cm3*K/mol)',
            'chi*T (cm3*K/mol)'
        ]
        data['M/B: chi*T (cm3*K/mol)'] = pd.to_numeric(
            data['M/B: chi*T (cm3*K/mol)'],
            errors='coerce'
        )
        data = data.astype(float)

        return data

    @classmethod
    def extract(cls, file_name: str) -> list[pd.DataFrame]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[pd.DataFrame]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        _ext(file_name, process=True)
        return _ext.data


class ExchangeCouplingExtractor(extto.BetweenExtractor):
    '''
    Extracts Exchange Coupling Constants and information (J)
    '''

    # Regex Start Pattern
    START_PATTERN = rb'(?<=BROKEN SYMMETRY MAGNETIC COUPLING ANALYSIS\s-{42})' # noqa

    # Regex End Pattern
    END_PATTERN = rb'(?=Ginsberg)'

    @property
    def data(self) -> list[dict[str, float]]:
        '''
        Processed Exchange coupling analysis, one dict per block
        For each list entry, keys are \n
         - S(High-Spin)\n
         - <S**2>(High-Spin)\n
         - <S**2>(BrokenSym)\n
         - E(High-Spin) (Eh)\n
         - E(BrokenSym) (Eh)\n
         - E(High-Spin)-E(BrokenSym) (cm^-1)
         - J(1) (cm^-1)
         - J(2) (cm^-1)
         - J(3) (cm^-1)
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> dict[str, float]:
        '''
        Converts single block into array of susceptibility as a function of
        temperature

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        dict[str, float]
            Keys described in self.data
        '''

        data = {
            'S(High-Spin)': float(re.findall(
                r'S\(High-Spin\) *= *(\d*\.\d*)',
                block
            )[0]),
            '<S**2>(High-Spin)': float(re.findall(
                r'<S\*\*2>\(High-Spin\) *= *(\d*\.\d*)',
                block
            )[0]),
            '<S**2>(BrokenSym)': float(re.findall(
                r'<S\*\*2>\(BrokenSym\) *= *(\d*\.\d*)',
                block
            )[0]),
            'E(High-Spin) (Eh)': float(re.findall(
                r'E\(High-Spin\) *= *(-\d*\.\d*) Eh',
                block
            )[0]),
            'E(BrokenSym) (Eh)': float(re.findall(
                r'E\(BrokenSym\) *= *(-\d*\.\d*) Eh',
                block
            )[0]),
            'E(High-Spin)-E(BrokenSym) (cm^-1)': float(re.findall(
                r'E\(High-Spin\)-E\(BrokenSym\)= *-?\d*.\d* eV *(-?\d*\.\d*) *cm\*\*-1', # noqa
                block
            )[0]),
            'J(1) (cm^-1)': float(re.findall(
                r'J\(1\) *= *(-?\d*\.\d*)', # noqa
                block
            )[0]),
            'J(2) (cm^-1)': float(re.findall(
                r'J\(2\) *= *(-?\d*\.\d*)', # noqa
                block
            )[0]),
            'J(3) (cm^-1)': float(re.findall(
                r'J\(3\) *= *(-?\d*\.\d*)', # noqa
                block
            )[0])
        }

        return data

    @classmethod
    def extract(cls, file_name: str) -> list[dict[str, float]]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[dict[str, float]]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        _ext(file_name, process=True)
        return _ext.data


class AILFTOrbEnergyExtractor(extto.BetweenExtractor):
    '''
    Extracts AI-LFT orbital energies from output file
    '''
    # Regex Start Pattern
    START_PATTERN = rb'(?<=The ligand field one electron eigenfunctions:\s-{41})' # noqa

    # Regex End Pattern
    END_PATTERN = rb'(?=Ligand field orbitals were stored in)'

    MODIFIERS = [re.MULTILINE]

    @property
    def data(self) -> list[dict[str, NDArray]]:
        '''
        AI-LFT one electron eigenvalues and eigenfunctions, one dict per block
        For each dict, keys are \n
         - energy (cm-1)\n
         - eigenvectors\n
         - orbitals
        and all values are numpy arrays of shape (n_orbs, n_orbs)\n
        or just n_orbs\n
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> dict[str, NDArray]:
        '''
        Converts single block into data entries described in self.data

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        dict[str, NDArray]
            Keys described in self.data
        '''

        energies = re.findall(
            r'\s+\d\s+\d\.\d{3}\s+(\d+\.\d)',
            block
        )
        energies = np.array([float(energy) for energy in energies])

        n_orbs = len(energies)

        vectors = re.findall(
            rf'\s+\d\s+\d\.\d{{3}}\s+\d+\.\d((?:\s+\-?\d\.\d{{6}}){{{n_orbs:d}}})', # noqa
            block
        )

        vectors = np.array([
            [float(ve) for ve in vector.split()]
            for vector in vectors
        ]).T

        names = re.findall(
            rf'Orbital\s+Energy\s+\(eV\)\s+Energy\s?\(cm-1\)((?:\s+[A-Za-z\d-]*){{{n_orbs:d}}})', # noqa
            block
        )
        names = np.array([na.rstrip().lstrip() for na in names[0].split()])

        data = {
            'energies (cm-1)': energies,
            'eigenvectors': vectors,
            'orbitals': names
        }

        return data


class FrequencyExtractor(extto.BetweenExtractor):
    '''
    Extracts Vibrational mode energies, eigenvectors, and intensity information
    '''

    # Regex Start Pattern
    START_PATTERN = rb'(?<=VIBRATIONAL FREQUENCIES\s-{23})' # noqa

    # Regex End Pattern
    END_PATTERN = rb'(?=The first frequency considered to be a vibration)'

    MODIFIERS = [re.MULTILINE]

    @property
    def data(self) -> list[dict[str, NDArray]]:
        '''
        Processed Exchange coupling analysis, one dict per block
        For each dict, keys are \n
         - frequency (cm^-1)\n
         - displacements - shape: (n_atoms, 3 * n_atoms, 3)\n
         - epsilon (L mol^-1 cm^-1)\n
         - txX\n
         - ty\n
         - tz\n
        and all values are numpy arrays.\n
        Dimensions are n_atoms*3, 1 for all arrays other than displacements.
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> dict[str, NDArray]:
        '''
        Converts single block into data entries described in self.data

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        dict[str, NDArray]
            Keys described in self.data
        '''

        # Extract Frequencies
        freq_pattern = re.compile(
            r' *\d*: *(-?\d*\.\d*) cm\*\*-1'
        )
        frequencies = np.array(
            [float(val) for val in freq_pattern.findall(block)]
        )

        n_atoms = len(frequencies) // 3

        # Extract Displacements
        disp_table = re.findall(
            r'((?: +\d+){6} +\s(?: +\d+ +(?: +-?\d\.\d{6}){6}\s)*)',
            block
        )

        # and combine in a single dataframe
        master = pd.read_csv(
                StringIO(disp_table[0]),
                sep=r'\s{2,}',
                engine='python',
                index_col=0
            )

        for chunk in disp_table[1:]:
            _df = pd.read_csv(
                StringIO(chunk),
                sep=r'\s{2,}',
                engine='python',
                index_col=0
            )
            master = master.join(_df)

        # convert to numpy array
        disp_table = master.to_numpy()
        # and reshape
        disp_x = disp_table[0::3, :]
        disp_y = disp_table[1::3, :]
        disp_z = disp_table[2::3, :]
        disp = np.zeros((n_atoms, n_atoms * 3, 3))
        disp[:, :, 0] = disp_x
        disp[:, :, 1] = disp_y
        disp[:, :, 2] = disp_z

        # Extract TX, TY, and TZ and calculate epsilon
        tx_pattern = re.compile(
            r'\((-?\d\.\d{6}) *-?\d\.\d{6} *-?\d\.\d{6}\)'
        )
        ty_pattern = re.compile(
            r'\(-?\d\.\d{6} *(-?\d\.\d{6}) *-?\d\.\d{6}\)'
        )
        tz_pattern = re.compile(
            r'\(-?\d\.\d{6} *-?\d\.\d{6} *(-?\d\.\d{6})\)'
        )
        tx = np.asarray(
            [0] * 6 + [float(val) for val in tx_pattern.findall(block)]
        )
        ty = np.asarray(
            [0] * 6 + [float(val) for val in ty_pattern.findall(block)]
        )
        tz = np.asarray(
            [0] * 6 + [float(val) for val in tz_pattern.findall(block)]
        )

        data = {
            'frequency (cm^-1)': frequencies,
            'displacements': disp,
            'tx': tx,
            'ty': ty,
            'tz': tz
        }

        return data

    @classmethod
    def extract(cls, file_name: str) -> list[dict[str, NDArray]]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[dict[str, NDArray]]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        _ext(file_name, process=True)
        return _ext.data


class LoewdinCompositionExtractor(extto.BetweenExtractor):
    '''
    Extracts Loewdin Orbital-Compositions Section
    '''

    # Regex Start Pattern
    START_PATTERN = rb'(?<=LOEWDIN ORBITAL-COMPOSITIONS\s-{28}\s)'

    # Regex End Pattern
    END_PATTERN = rb'(?=-{28})'

    @property
    def data(self) -> list[tuple[list[dict[str, float]], list[float]]]:
        '''
        Processed Loewdin Natural orbital data
        Each data entry is a tuple containing:\n
        First entry - a list of dicts, one dict per Natural orbital\n
            Keys:\n
                ATOM_NUMBER ATOM_SYMBOL ORBITAL_NAME\n
            Values\n
                % Contribution to orbital\n
        Second entry - a list of occupation numbers, one float per orbital\n
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> tuple[list[dict[str, float]], list[float]]: # noqa
        '''
        Converts single block into data entries described in self.data

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        tuple[list[dict[str, float]], list[float]]
            First entry - a list of dicts, one dict per Natural orbital\n
                Keys:\n
                    ATOM_NUMBER ATOM_SYMBOL ORBITAL_NAME\n
                Values\n
                    % Contribution to orbital\n
            Second entry - a list of occupation numbers, one float per orbital\n # noqa
        '''

        # Extract each <=5 orbital sub block
        patt = re.compile(
            r'\n{2,}'
        )
        _sub_blocks = patt.split(block)
        _sub_blocks = [
            sb.lstrip().rstrip()
            for sb in _sub_blocks
            if len(sb.lstrip().rstrip())
        ]

        # and process into lists

        occupations = []
        contributions = []

        for _sub_block in _sub_blocks:
            [_header, _, _table] = re.split(r'\s(:?--------\s+)+', _sub_block)

            _orb_nos = [
                int(val)
                for val in _header.split('\n')[0].split()
            ]

            _occs = [
                float(val)
                for val in _header.split('\n')[2].split()
            ]

            for _occ in _occs:
                occupations.append(_occ)

            _df = pd.read_csv(
                StringIO(_table), sep=r'\s+',
                header=None,
                engine='python',
                index_col=None
            )
            _df.set_index([0, 1, 2], inplace=True)
            _df.columns = _orb_nos

            for _on in _orb_nos:
                _contrib = {}
                for name, pc in zip(_df.index, _df[_on]):
                    if pc > 1.:
                        _contrib[f'{name[0]:3} {name[1]:2} {name[2]:5}'] = pc
                contributions.append(_contrib)

        return (contributions, occupations)

    @classmethod
    def extract(cls, file_name: str) -> list[tuple[list[dict[str, float]], list[float]]]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[tuple[list[dict[str, float]], list[float]]]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        _ext(file_name, process=True)
        return _ext.data


class NProcsInputExtractor(extto.LineExtractor):
    '''
    Extracts Number of processors from input file
    '''

    # Regex Start Pattern
    PATTERN = rb'%PAL\s+NPROCS\s+\d+\s+END'

    MODIFIERS = [re.IGNORECASE]

    @property
    def data(self) -> list[int]:
        '''
        Number of cores. One entry per match
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> int:
        '''
        Converts single block into data entries described in self.data

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        int
            Number of cores
        '''

        n_cores = re.findall(r'(\d+)', block)[0]

        n_cores = int(n_cores)

        return n_cores

    @classmethod
    def extract(cls, file_name: str) -> list[int]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[int]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        _ext(file_name, process=True)
        return _ext.data


class XYZFileInputExtractor(extto.LineExtractor):
    '''
    Extracts .xyz file name from the following line of an input file

    *xyzfile charge multiplicity file_name
    '''

    # Regex Start Pattern
    PATTERN = rb'\* *xyzfile *\d+ *\d+ *.*'

    MODIFIERS = [re.IGNORECASE]

    @property
    def data(self) -> list[str]:
        '''
        xyz file, one entry per match
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> int:
        '''
        Converts single block into data entries described in self.data

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        str
            xyz file name
        '''

        file = block.split()[-1]

        return file

    @classmethod
    def extract(cls, file_name: str) -> list[int]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[int]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        try:
            _ext(file_name, process=True)
        except extto.DataNotFoundError:
            pass
        return _ext.data


class XYZInputExtractor(extto.LineExtractor):
    '''
    Extracts .xyz line of an input file

    *xyz charge multiplicity
    '''

    # Regex Start Pattern
    PATTERN = rb'\* *xyz *\d+ *\d'

    MODIFIERS = [re.IGNORECASE]

    @property
    def data(self) -> list[str]:
        '''
        *xyz line, one entry per match
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> int:
        '''
        Converts single block into data entries described in self.data

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        str
            String block extracted from file
        '''

        return block

    @classmethod
    def extract(cls, file_name: str) -> list[int]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[int]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        try:
            _ext(file_name, process=True)
        except extto.DataNotFoundError:
            pass
        return _ext.data


class MaxCoreInputExtractor(extto.LineExtractor):
    '''
    Extracts maxcore from input file\n
    i.e. the amount of memory allocated per core
    '''

    # Regex Start Pattern
    PATTERN = rb'%maxcore +\d+'

    MODIFIERS = [re.IGNORECASE]

    @property
    def data(self) -> list[int]:
        '''
        Maxcore. One entry per match
        '''
        return self._data

    @staticmethod
    def _process_block(block: str) -> int:
        '''
        Converts single block into data entries described in self.data

        Parameters
        ----------
        block: str
            String block extracted from file

        Returns
        -------
        int
            Maxcore
        '''

        maxcore = re.findall(r'(\d+)', block)[0]

        maxcore = int(maxcore)

        return maxcore

    @classmethod
    def extract(cls, file_name: str) -> list[int]: # noqa
        '''
        Convenience method which instantiates class, extracts blocks, and
        returns processed datasets

        Parameters
        ----------
        file_name: str
            Name of file to parse

        Returns
        -------
        list[int]
            Each entry contains processed data, as defined in cls.data
        '''
        _ext = cls()
        _ext(file_name, process=True)
        return _ext.data
