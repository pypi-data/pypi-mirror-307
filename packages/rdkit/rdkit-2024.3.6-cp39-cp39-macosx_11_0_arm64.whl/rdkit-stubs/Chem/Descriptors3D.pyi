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
descList: list  # value = [('PMI1', <function <lambda> at 0x1032461f0>), ('PMI2', <function <lambda> at 0x105d51040>), ('PMI3', <function <lambda> at 0x105d510d0>), ('NPR1', <function <lambda> at 0x105d51160>), ('NPR2', <function <lambda> at 0x105d511f0>), ('RadiusOfGyration', <function <lambda> at 0x105d51280>), ('InertialShapeFactor', <function <lambda> at 0x105d51310>), ('Eccentricity', <function <lambda> at 0x105d513a0>), ('Asphericity', <function <lambda> at 0x105d51430>), ('SpherocityIndex', <function <lambda> at 0x105d514c0>), ('PBF', <function <lambda> at 0x105d51550>)]
