import numpy as np
import pytest
from openff.toolkit.topology import Molecule, Topology
from openff.units import unit

from openff.interchange import Interchange
from openff.interchange.drivers import get_lammps_energies, get_openmm_energies
from openff.interchange.drivers.lammps import _write_lammps_input
from openff.interchange.tests import _BaseTest, needs_lmp


@needs_lmp
class TestLammps(_BaseTest):
    @pytest.mark.slow()
    @pytest.mark.parametrize("n_mols", [1, 2])
    @pytest.mark.parametrize(
        "mol",
        [
            "C",
            "CC",  # Adds a proper torsion term(s)
            pytest.param(
                "C=O",
                marks=pytest.mark.xfail,
            ),  # Simplest molecule with any improper torsion
            pytest.param(
                "OC=O",
                marks=pytest.mark.xfail,
            ),  # Simplest molecule with a multi-term torsion
            "CCOC",  # This hits t86, which has a non-1.0 idivf
            pytest.param(
                "C1COC(=O)O1", marks=pytest.mark.xfail
            ),  # This adds an improper, i2
        ],
    )
    def test_to_lammps_single_mols(self, mol, parsley_unconstrained, n_mols):
        """
        Test that Interchange.to_openmm Interchange.to_lammps report sufficiently similar energies.

        TODO: Tighten tolerances
        TODO: Test periodic and non-periodic
        """
        mol = Molecule.from_smiles(mol)
        mol.generate_conformers(n_conformers=1)
        top = Topology.from_molecules(n_mols * [mol])
        mol.conformers[0] -= np.min(mol.conformers[0], axis=0)

        top.box_vectors = 10 * np.eye(3) * unit.nanometer

        if n_mols == 1:
            positions = mol.conformers[0]
        elif n_mols == 2:
            positions = np.concatenate(
                [mol.conformers[0], mol.conformers[0] + 3 * unit.nanometer]
            )

        openff_sys = Interchange.from_smirnoff(parsley_unconstrained, top)
        openff_sys.positions = positions
        openff_sys.box = top.box_vectors

        reference = get_openmm_energies(
            off_sys=openff_sys,
            round_positions=3,
        )

        lmp_energies = get_lammps_energies(
            off_sys=openff_sys,
            round_positions=3,
        )

        _write_lammps_input(
            off_sys=openff_sys,
            file_name="tmp.in",
        )

        lmp_energies.compare(
            reference,
            custom_tolerances={
                "Nonbonded": 100 * unit.kilojoule_per_mole,
                "Electrostatics": 100 * unit.kilojoule_per_mole,
                "vdW": 100 * unit.kilojoule_per_mole,
            },
        )