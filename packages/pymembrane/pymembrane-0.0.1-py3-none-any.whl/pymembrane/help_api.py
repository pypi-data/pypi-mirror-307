# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 06:52:33 2024

@author: Hedi
"""

# help_api.py

def get_help(item, attr_name=None):
    """
    Provides help for any class, method, or property within the membrane simulation module.

    Parameters:
    -----------
    item : object or class
        The object or class for which the user requires help.
    attr_name : str, optional
        The name of the attribute or property (e.g., 'Vr_out') for which help is required.
    
    Returns:
    --------
    str : The docstring associated with the requested object, class, or method.
    """
    try:
        # Si un nom d'attribut est donné, on essaie d'obtenir la propriété depuis l'objet ou la classe
        if attr_name:
            # Vérifie d'abord si l'item est une instance de classe
            if hasattr(item, '__class__'):
                # Récupérer l'attribut à partir de la classe de l'instance
                attribute = getattr(item.__class__, attr_name, None)
            else:
                # Si item est déjà une classe, obtenir directement l'attribut
                attribute = getattr(item, attr_name, None)
            
            if attribute and attribute.__doc__:
                return attribute.__doc__
            else:
                return f"No documentation available for the attribute '{attr_name}'."
        # Sinon, vérifier si l'objet a une docstring et la retourner
        else:
            if item.__doc__:
                return item.__doc__
            else:
                return f"No documentation available for the provided item."
    except AttributeError:
        return f"The provided item or attribute '{attr_name}' is not valid or does not contain a docstring."



def list_available_items():
    """
    Lists all available classes and functions in the membrane simulation module.

    Returns:
    --------
    None : Prints the list of available items.
    """
    items = {
        "Classes": ["res_membrane", "dwsim", "spiral_membrane"],
        "Functions": ["mass_layer", "get_help", "list_available_items"]
    }

    print("===== CLASSES =====")
    for cls in items["Classes"]:
        print(f"- {cls}")

    print("\n===== FUNCTIONS =====")
    for func in items["Functions"]:
        print(f"- {func}")
