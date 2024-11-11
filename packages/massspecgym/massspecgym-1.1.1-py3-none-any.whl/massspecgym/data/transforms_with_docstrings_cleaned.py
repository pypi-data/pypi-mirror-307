
import numpy as np
import torch
import matchms
import matchms.filtering as ms_filters
from rdkit.Chem import AllChem as Chem
from typing import Optional
from abc import ABC, abstractmethod
import massspecgym.utils as utils
from massspecgym.definitions import CHEM_ELEMS


class SpecTransform(ABC):
    """
    Base class for spectrum transformations. Custom transformations should inherit from this class.
    The transformation consists of two consecutive steps:
        1. Apply a series of matchms filters to the input spectrum (method `matchms_transforms`).
        2. Convert the matchms spectrum to a torch tensor (method `matchms_to_torch`).

    This class provides a structure for creating custom spectrum transformation pipelines.
    """    

    @abstractmethod
    def matchms_transforms(self, spec: matchms.Spectrum) -> matchms.Spectrum:
        """
        Apply a series of matchms filters to the input spectrum. Abstract method.

        Args:
            spec (matchms.Spectrum): Input spectrum to be filtered.

        Returns:
            matchms.Spectrum: Filtered spectrum after applying matchms filters.
        """
        pass

    @abstractmethod
    def matchms_to_torch(self, spec: matchms.Spectrum) -> torch.Tensor:
        """
        Convert a matchms spectrum to a torch tensor. Abstract method.

        Args:
            spec (matchms.Spectrum): Filtered spectrum to be converted to a torch tensor.

        Returns:
            torch.Tensor: Tensor representation of the input spectrum.
        """
        pass

    def __call__(self, spec: matchms.Spectrum) -> torch.Tensor:
        """
        Compose the matchms filters and the torch conversion.

        Args:
            spec (matchms.Spectrum): Input spectrum to be transformed.

        Returns:
            torch.Tensor: Tensor representation of the input spectrum after applying
                          the matchms filters and converting to torch tensor.
        """
        return self.matchms_to_torch(self.matchms_transforms(spec))


def default_matchms_transforms(
    spec: matchms.Spectrum,
    n_max_peaks: int = 60,
    mz_from: float = 10,
    mz_to: float = 1000,
) -> matchms.Spectrum:
    """
    Apply a default set of transformations to a spectrum using matchms filters.

    This function applies standard preprocessing steps to a spectrum, such as
    selecting peaks within a certain m/z range and limiting the number of peaks.

    Args:
        spec (matchms.Spectrum): The input spectrum to be transformed.
        n_max_peaks (int, optional): Maximum number of peaks to retain. Defaults to 60.
        mz_from (float, optional): Minimum m/z value to keep. Defaults to 10.
        mz_to (float, optional): Maximum m/z value to keep. Defaults to 1000.

    Returns:
        matchms.Spectrum: The spectrum after applying the default transformations.
    """
    spec = ms_filters.select_by_mz(spec, mz_from=mz_from, mz_to=mz_to)
ef __init__(
        self,
        max_mz: float = 1005,
        bin_width: float = 1,
        to_rel_intensities: bool = True,
    ) -> None:
        self.max_mz = max_mz
        self.bin_width = bin_width
        self.to_rel_intensities = to_rel_intensities
        if not (max_mz / bin_width).is_integer():
            raise ValueError("`max_mz` must be divisible by `bin_width`.")

    def matchms_transforms(self, spec: matchms.Spectrum) -> matchms.Spectrum:
        return default_matchms_transforms(spec, mz_to=self.max_mz, n_max_peaks=None)

    def matchms_to_torch(self, spec: matchms.Spectrum) -> torch.Tensor:
        """
        Bin the spectrum into a fixed number of bins.
        """
        binned_spec = self._bin_mass_spectrum(
            mzs=spec.peaks.mz,
            intensities=spec.peaks.intensities,
            max_mz=self.max_mz,
            bin_width=self.bin_width,
            to_rel_intensities=self.to_rel_intensities,
        )
        return torch.from_numpy(binned_spec)

    def _bin_mass_spectrum(
        self, mzs, intensities, max_mz, bin_width, to_rel_intensities=True
    ):
        # Calculate the number of bins
        num_bins = int(np.ceil(max_mz / bin_width))

        # Calculate the bin indices for each mass
        bin_indices = np.floor(mzs / bin_width).astype(int)

        # Filter out mzs that exceed max_mz
        valid_indices = bin_indices[mzs <= max_mz]
        valid_intensities = intensities[mzs <= max_mz]

        # Clip bin indices to ensure they are within the valid range
        valid_indices = np.clip(valid_indices, 0, num_bins - 1)

        # Initialize an array to store the binned intensities
        binned_intensities = np.zeros(num_bins)

        # Use np.add.at to sum intensities in the appropriate bins
        np.add.at(binned_intensities, valid_indices, valid_intensities)

        # Generate the bin edges for reference
        # bin_edges = np.arange(0, max_mz + bin_width, bin_width)

        # Normalize the intensities to relative intensities
        if to_rel_intensities:
            binned_intensities /= np.max(binned_intensities)

        return binned_intensities  # , bin_edges


class MolTransform(ABC):
    @abstractmethod
    def from_smiles(self, mol: str):
        """
        Convert a SMILES string to a tensor-like representation. Abstract method.
        """

    def __call__(self, mol: str):
        return self.from_smiles(mol)


class MolFingerprinter(MolTransform):
    def __init__(self, type: str = "morgan", fp_size: int = 2048, radius: int = 2):
        if type != "morgan":
            raise NotImplementedError(
                "Only Morgan fingerprints are implemented at the moment."
            )
        self.type = type
        self.fp_size = fp_size
        self.radius = radius

    def from_smiles(self, mol: str):
        mol = Chem.MolFromSmiles(mol)
        return utils.morgan_fp(
            mol, fp_size=self.fp_size, radius=self.radius, to_np=True
        )


class MolToInChIKey(MolTransform):
    def __init__(self, twod: bool = True) -> None:
        self.twod = twod

    def from_smiles(self, mol: str) -> str:
        mol = Chem.MolFromSmiles(mol)
        return utils.mol_to_inchi_key(mol, twod=self.twod)


class MolToFormulaVector(MolTransform):
    def __init__(self):
        self.element_index = {element: i for i, element in enumerate(CHEM_ELEMS)}

    def from_smiles(self, smiles: str):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        # Add explicit hydrogens to the molecule
        mol = Chem.AddHs(mol)

        # Initialize a vector of zeros for the 118 elements
        formula_vector = np.zeros(118, dtype=np.int32)

        # Iterate over atoms in the molecule and count occurrences of each element
        for atom in mol.GetAtoms():
            symbol = atom.GetSymbol()
            if symbol in self.element_index:
                index = self.element_index[symbol]
                formula_vector[index] += 1
            else:
                raise ValueError(f"Element '{symbol}' not found in the list of 118 elements.")

        return formula_vector

    @staticmethod
    def num_elements():
        return len(CHEM_ELEMS)
