import tensorflow as tf
import numpy as np
import re
from dataclasses import dataclass 
from rdkit import Chem 
import functools 

from molgraph import GraphTensor
from molgraph.chemistry import MolecularGraphEncoder

from .definitions import NUM_RESIDUE_TYPES
from .definitions import SUPER_NODE_INDICATOR
from .definitions import RESIDUE_INDEX



@dataclass
class PeptideGraphEncoder(MolecularGraphEncoder):

    def call(self, sequence: str, index_dtype: str = 'int32') -> GraphTensor:
        
        peptide = _Peptide(sequence)
        
        x = super().call(peptide.smiles)
        
        residue_sizes = peptide.residue_sizes
        num_nodes = x.node_feature.shape[0]
        num_super_nodes = len(sequence)
        num_super_edges = len(sequence) + sum(residue_sizes)
        
        data = {
            SUPER_NODE_INDICATOR: np.concatenate([[0] * num_nodes, [1] * num_super_nodes])
        }
        
        residue_index = np.arange(num_nodes, num_nodes + num_super_nodes)
        super_target_index = np.repeat(residue_index, residue_sizes)
        super_source_index = np.arange(num_nodes)

        data['node_feature'] = np.pad(x.node_feature, [(0, num_super_nodes), (0, NUM_RESIDUE_TYPES)])
        data['node_feature'][-num_super_nodes:, -NUM_RESIDUE_TYPES:] = np.eye(NUM_RESIDUE_TYPES)[sequence.residue_indices]
        data['edge_src'] = np.concatenate([x.edge_src, super_source_index, residue_index]).astype(index_dtype)
        data['edge_dst'] = np.concatenate([x.edge_dst, super_target_index, residue_index]).astype(index_dtype)
        data['edge_feature'] = np.pad(x.edge_feature, [(0, num_super_edges), (0, 2)])
        data['edge_feature'][-num_super_edges:, -2:] = np.eye(2)[np.concatenate([[0] * sum(residue_sizes), [1] * num_super_nodes])]
        return GraphTensor(**data)
    

@dataclass
class BondlessPeptideGraphEncoder(MolecularGraphEncoder):

    """For experimental purposes"""

    def call(self, sequence: str, index_dtype: str = 'int32') -> GraphTensor:
        
        peptide = _Peptide(sequence)
        
        x = super().call(peptide.smiles)
        
        residue_sizes = peptide.residue_sizes
        num_nodes = x.node_feature.shape[0]
        num_super_nodes = len(sequence)
        
        data = {
            SUPER_NODE_INDICATOR: np.concatenate([[0] * num_nodes, [1] * num_super_nodes])
        }

        residue_index = np.arange(num_nodes, num_nodes + num_super_nodes)
        super_target_index = np.repeat(residue_index, residue_sizes)
        super_source_index = np.arange(num_nodes)

        data['node_feature'] = np.pad(x.node_feature, [(0, num_super_nodes), (0, NUM_RESIDUE_TYPES)])
        data['node_feature'][-num_super_nodes:, -NUM_RESIDUE_TYPES:] = np.eye(NUM_RESIDUE_TYPES)[sequence.residue_indices]
        data['edge_src'] = np.concatenate([super_source_index, residue_index]).astype(index_dtype)
        data['edge_dst'] = np.concatenate([super_target_index, residue_index]).astype(index_dtype)
        data['edge_feature'] = np.eye(2)[np.concatenate([[0] * sum(residue_sizes), [1] * num_super_nodes])].astype(np.float32)

        return GraphTensor(**data)


RESIDUE_SMILES = {
    "A": "N[C@@H](C)C(=O)O",
    "C": "N[C@@H](CS)C(=O)O",
    "D": "N[C@@H](CC(=O)O)C(=O)O",
    "E": "N[C@@H](CCC(=O)O)C(=O)O",
    "F": "N[C@@H](Cc1ccccc1)C(=O)O",
    "G": "NCC(=O)O",
    "H": "N[C@@H](CC1=CN=C-N1)C(=O)O",
    "I": "N[C@@H](C(CC)C)C(=O)O",
    "K": "N[C@@H](CCCCN)C(=O)O",
    "L": "N[C@@H](CC(C)C)C(=O)O",
    "M": "N[C@@H](CCSC)C(=O)O",
    "N": "N[C@@H](CC(=O)N)C(=O)O",
    "P": "N1[C@@H](CCC1)C(=O)O",
    "Q": "N[C@@H](CCC(=O)N)C(=O)O",
    "R": "N[C@@H](CCCNC(=N)N)C(=O)O",
    "S": "N[C@@H](CO)C(=O)O",
    "T": "N[C@@H](C(O)C)C(=O)O",
    "V": "N[C@@H](C(C)C)C(=O)O",
    "W": "N[C@@H](CC(=CN2)C1=C2C=CC=C1)C(=O)O",
    "Y": "N[C@@H](Cc1ccc(O)cc1)C(=O)O",
    "M[Oxidation]": "N[C@@H](CCS(=O)C)C(=O)O",
    "P[Oxidation]": "N1CC(O)C[C@H]1C(=O)O",
    "K[Propionyl]": "N[C@@H](CCCCNC(=O)CC)C(=O)O",
    "R[Deamidated]": "N[C@@H](CCCNC(N)=O)C(=O)O",
    "K[Methyl]": "N[C@@H](CCCCNC)C(=O)O",
    "R[Methyl]": "N[C@@H](CCCNC(=N)NC)C(=O)O",
    "K[Succinyl]": "N[C@@H](CCCCNC(CCC(O)=O)=O)C(=O)O",
    "K[Formyl]": "N[C@@H](CCCCNC=O)C(=O)O",
    "K[Dimethyl]": "N[C@@H](CCCCN(C)C)C(=O)O",
    "R[Dimethyl]": "N[C@@H](CCCNC(N(C)C)=N)C(=O)O",
    "K[Acetyl]": "N[C@@H](CCCCNC(=O)C)C(=O)O",
    "K[Crotonyl]": "N[C@@H](CCCCNC(C=CC)=O)C(=O)O",
    "K[Trimethyl]": "N[C@@H](CCCC[N+](C)(C)C)C(=O)O",
    "Y[Phospho]": "N[C@@H](Cc1ccc(OP(O)(=O)O)cc1)C(=O)O",
    "K[Malonyl]": "N[C@@H](CCCCNC(=O)CC(O)=O)C(=O)O",
    "C[Carbamidomethyl]": "N[C@@H](CSCC(=O)N)C(=O)O",
    "Y[Nitro]": "N[C@@H](Cc1ccc(O)c(N(=O)=O)c1)C(=O)O",
    "[Acetyl]-A": "N(C(C)=O)[C@@H](C)C(=O)O",
    "[Acetyl]-C": "N(C(C)=O)[C@@H](CS)C(=O)O",
    "[Acetyl]-D": "N(C(=O)C)[C@H](C(=O)O)CC(=O)O",
    "[Acetyl]-E": "N(C(=O)C)[C@@H](CCC(O)=O)C(=O)O",
    "[Acetyl]-F": "N(C(C)=O)[C@@H](Cc1ccccc1)C(=O)O",
    "[Acetyl]-G": "N(C(=O)C)CC(=O)O",
    "[Acetyl]-H": "N(C(=O)C)[C@@H](Cc1[nH]cnc1)C(=O)O",
    "[Acetyl]-I": "N(C(=O)C)[C@@H]([C@H](CC)C)C(=O)O",
    "[Acetyl]-K": "N(C(C)=O)[C@@H](CCCCN)C(=O)O",
    "[Acetyl]-L": "N(C(=O)C)[C@@H](CC(C)C)C(=O)O",
    "[Acetyl]-M": "N(C(=O)C)[C@@H](CCSC)C(=O)O",
    "[Acetyl]-N": "N(C(C)=O)[C@@H](CC(=O)N)C(=O)O",
    "[Acetyl]-P": "N1(C(=O)C)CCC[C@H]1C(=O)O",
    "[Acetyl]-Q": "N(C(=O)C)[C@@H](CCC(=O)N)C(=O)O",
    "[Acetyl]-R": "N(C(C)=O)[C@@H](CCCN=C(N)N)C(=O)O",
    "[Acetyl]-S": "N(C(C)=O)[C@@H](CO)C(=O)O",
    "[Acetyl]-T": "N(C(=O)C)[C@@H]([C@H](O)C)C(=O)O",
    "[Acetyl]-V": "N(C(=O)C)[C@@H](C(C)C)C(=O)O",
    "[Acetyl]-W": "N(C(C)=O)[C@@H](Cc1c2ccccc2[nH]c1)C(=O)O",
    "[Acetyl]-Y": "N(C(C)=O)[C@@H](Cc1ccc(O)cc1)C(=O)O"
}


class _Peptide:

    def __init__(self, sequence):
        self._sequence = sequence
        self._split_sequence = _sequence_split(self._sequence) 
        self._num_residues = len(self._split_sequence)
    
    def __repr__(self):
        return f"<Peptide: {self._sequence} at {hex(id(self))}>"
    
    def __len__(self):
        return self._num_residues
    
    def __iter__(self):
        self._i = 0
        return self
    
    def __next__(self):
        if self._i < self._num_residues:
            residue = self._split_sequence[self._i]
            self._i += 1 
            return residue 
        else:
            raise StopIteration

    @property
    def smiles(self):
        smiles_list = [RESIDUE_SMILES[residue] for residue in self]
        return _concatenate_smiles(smiles_list)

    @property
    def residue_sizes(self):
        sizes = []
        for i, residue in enumerate(self):
            size = _num_atoms(RESIDUE_SMILES[residue])
            last_residue = i == (len(self) - 1)
            if not last_residue:
                size -= 1
            sizes.append(size)
        return sizes
    
    @property
    def residue_indices(self):
        return [_extract_residue_index(residue) for residue in self]


@functools.lru_cache(maxsize=4096)
def _num_atoms(smiles):
    return Chem.MolFromSmiles(smiles).GetNumAtoms()

def _sequence_split(sequence):
    patterns = [
        r'(\[[A-Za-z0-9]+\]-[A-Z]\[[A-Za-z0-9]+\])', # N-term mod + mod
        r'([A-Z]\[[A-Za-z0-9]+\]-\[[A-Za-z0-9]+\])', # C-term mod + mod
        r'([A-Z]-\[[A-Za-z0-9]+\])', # C-term mod
        r'(\[[A-Za-z0-9]+\]-[A-Z])', # N-term mod
        r'([A-Z]\[[A-Za-z0-9]+\])', # Mod
        r'([A-Z])', # No mod
    ]
    return [match.group(0) for match in re.finditer("|".join(patterns), sequence)]

def _concatenate_smiles(smiles_list: list[str], sep='') -> str:
    # ['NCC(=O)O', 'NCC(=O)O', ...] -> 'NCC(=O)NCC(=O)...'
    smiles_list = [
        smiles.rstrip("O") if i < len(smiles_list) - 1 else smiles
        for (i, smiles) in enumerate(smiles_list)
    ]
    return sep.join(smiles_list)

def _extract_residue_type(residue_tag):
    pattern = r"(?<!\[)[A-Z](?![\w-])"
    return [match.group(0) for match in re.finditer(pattern, residue_tag)][0]

def _extract_residue_index(residue_tag):
    return RESIDUE_INDEX[_extract_residue_type(residue_tag)]
