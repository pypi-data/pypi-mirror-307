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
descList: list  # value = [('PMI1', <function <lambda> at 0x000001DB425FF420>), ('PMI2', <function <lambda> at 0x000001DB425FFA60>), ('PMI3', <function <lambda> at 0x000001DB425FFBA0>), ('NPR1', <function <lambda> at 0x000001DB425FFC40>), ('NPR2', <function <lambda> at 0x000001DB425FFCE0>), ('RadiusOfGyration', <function <lambda> at 0x000001DB425FFD80>), ('InertialShapeFactor', <function <lambda> at 0x000001DB425FFE20>), ('Eccentricity', <function <lambda> at 0x000001DB425FFEC0>), ('Asphericity', <function <lambda> at 0x000001DB425FFF60>), ('SpherocityIndex', <function <lambda> at 0x000001DB4266C040>), ('PBF', <function <lambda> at 0x000001DB4266C0E0>)]
