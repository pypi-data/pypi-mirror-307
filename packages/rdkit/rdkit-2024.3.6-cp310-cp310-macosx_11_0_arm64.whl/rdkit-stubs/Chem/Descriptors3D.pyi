"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x104b82cb0>), ('PMI2', <function <lambda> at 0x10785a290>), ('PMI3', <function <lambda> at 0x10785a320>), ('NPR1', <function <lambda> at 0x10785a3b0>), ('NPR2', <function <lambda> at 0x10785a440>), ('RadiusOfGyration', <function <lambda> at 0x10785a4d0>), ('InertialShapeFactor', <function <lambda> at 0x10785a560>), ('Eccentricity', <function <lambda> at 0x10785a5f0>), ('Asphericity', <function <lambda> at 0x10785a680>), ('SpherocityIndex', <function <lambda> at 0x10785a710>), ('PBF', <function <lambda> at 0x10785a7a0>)]
