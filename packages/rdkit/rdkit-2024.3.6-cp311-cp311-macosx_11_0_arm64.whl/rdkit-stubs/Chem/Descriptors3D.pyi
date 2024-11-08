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
descList: list  # value = [('PMI1', <function <lambda> at 0x104df19e0>), ('PMI2', <function <lambda> at 0x107e1c4a0>), ('PMI3', <function <lambda> at 0x107e1c5e0>), ('NPR1', <function <lambda> at 0x107e1c680>), ('NPR2', <function <lambda> at 0x107e1c720>), ('RadiusOfGyration', <function <lambda> at 0x107e1c7c0>), ('InertialShapeFactor', <function <lambda> at 0x107e1c860>), ('Eccentricity', <function <lambda> at 0x107e1c900>), ('Asphericity', <function <lambda> at 0x107e1c9a0>), ('SpherocityIndex', <function <lambda> at 0x107e1ca40>), ('PBF', <function <lambda> at 0x107e1cae0>)]
