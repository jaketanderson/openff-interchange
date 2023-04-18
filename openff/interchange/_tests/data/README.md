# Data files

A collection of files used for testing Interchange.

Disclaimer: Not intended for public consumption and no guarantees related to usage are made.

Below documents how some of these files were generated

`10_ar.pdb`:

```python3
import mbuild as mb
ar = mb.Compound(name='Ar')
mol = mb.fill_box(ar, 10, box=[2, 2, 2])
mol.to_parmed().save('10_ar.pdb')
```

`water-dimer.pdb`:

- Taken from the `openmm-tests` [repo:](https://github.com/choderalab/openmm-tests/blob/5a7d3b7bee753a384c98f4b6f8bb1460c371935c/energy-continuity/water-dimer.pdb)

`tip3p.offxml`:

- Taken from the toolkit, but with a default-looking `<Electrostatics>` tag added.
  - [Source](https://github.com/openforcefield/openff-toolkit/blob/d0b768a6d2cd0297b34aab3618197604b81d6e03/openff/toolkit/data/test_forcefields/tip3p.offxml)
  - [Source](https://github.com/openforcefield/openff-toolkit/issues/716)

`ALA_GLY/ALA_GLY.*`

- The SDF and PDB files files were prepared by Jeff Wagner
- The .gro and .top files were prepared by internal exporters 3/26/21

`packed-argon.pdb`

- Generated via mBuild and ParmEd

```python
import mbuild as mb
argon = mb.Compound(name='Ar')
packed_box = mb.fill_box(
    compound=[argon],
    box=mb.Box(lengths=[3, 3, 3]),  # nm
    density=1417,  # kg/m3
)
struct = packed_box.to_parmed(residues=['Ar'])
struct.save('packed-argon.pdb')
```

`benzene.sdf`

`molecules.sdf`

- Meant to serve as a rough coverage test, likely to be replaced by a more curated set
- Taken from below link and converted to SDF with smi_to_sdf.py in order to bypass repeated charge assignment
- [Source](https://github.com/openforcefield/open-forcefield-data/blob/8622f00860c507102a4c8ac9088d9e73bc76857e/Utilize-All-Parameters/selected/chosen.smi)

`MiniDrugBank.sdf`

- Meant to serve as a minimal, but not tiny, coverage set
- Generated by `trim_drug_bank.py`
- Uses most molecules from [here](https://github.com/openforcefield/cheminformatics-toolkit-equivalence/pull/2)
  - At least one fails an RDKit round-trip, and was skipped in generating this set

`CB8.sdf`

- [Source](https://github.com/samplchallenges/SAMPL6/blob/c661d3985af7fa0ba8c64a1774cfb2363cd31bda/host_guest/CB8AndGuests/CB8.mol2)

`complex.top`

- [Source](https://raw.githubusercontent.com/samplchallenges/SAMPL6/master/host_guest/SAMPLing/CB8-G3-0/GROMACS/complex.top)

`complex.gro`

- [Source](https://raw.githubusercontent.com/samplchallenges/SAMPL6/master/host_guest/SAMPLing/CB8-G3-0/GROMACS/complex.gro)