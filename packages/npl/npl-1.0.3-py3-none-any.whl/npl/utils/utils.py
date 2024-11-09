from copy import deepcopy
from npl.core.nanoparticle import Nanoparticle
from npl.calculators import EMTCalculator


def get_reference_structure(particle: Nanoparticle, ase=None) -> Nanoparticle:
    if type(particle) is not Nanoparticle:
        p = Nanoparticle()
        p.add_atoms(particle)
        particle = p
    old_symbols = deepcopy(particle.atoms.atoms.symbols)
    new_symbols = ['Pt' for _ in particle.get_indices()]
    particle.transform_atoms(particle.get_indices(), new_symbols)
    EMTCalculator(relax_atoms=True).compute_energy(particle)
    particle.construct_neighbor_list()
    particle.transform_atoms(particle.get_indices(), old_symbols)
    if ase:
        return particle.get_ase_atoms()
    return particle
