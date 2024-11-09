__version__="0.2.2"

major_changes = [
    "Major code changes to initial lipid placement algorithm. Lipids are now sorted into size (radius) groups and inserted progressively from largest to smallest.",
    [
        "This prevents former issues that could occur when creating membranes containing lipids with different radii.",
    ],
    "Code changes to lipid position optimization algorithm.",
    [
        "Improved performance (speed) without loss of accuracy by reducing the number of times the neighbor list is updated.",
        "The neighbor list update frequency was previously based on the distance travelled by lipids since the last neighbor list update, without taking into account the direction travelled at each step.",
        "The neighbor list update frequency is now based on the distance travelled from the initial position (after the last neighbor list update) to the current position.",
    ],
    "'stacked_membranes' argument:",
    [
        "Added 'pbc' subargument which determines how the position 1 solvent box should be placed:",
        [
            "'split' (default) - Same as before. The solvent box is split across the pbc",
            "'bottom'/'bot' - The solvent box is placed on the bottom",
            "'top' - The solvent box is placed on the top",
        ],
        "Multiple 'membrane' and 'solvation' arguments can now be given to each 'position' for both membranes and solvations.",
        "Removed the 'mean_surface' option for 'distance_type' subargument.",
        "Multiple checks are now made to ensure that the system complies with certain inter-membrane distance criteria (lipids from membranes in different positions are not allowed to overlap).",
    ],
]

minor_changes = [
    "'molecule_import' argument:",
    [
        "Added 'density', 'molar_mass' and 'mapping_ratio' subarguments to 'molecule_import' argument allowing one to set those values for imported solvents.",
        "Added 'scale' subargument to 'molecule_import' argument allowing for one to scale the x/y/z coordinates of imported molecules.",
        "Added 'refname' subargument to 'molecule_import' argument which can only be used when 'moleculetype' is used.",
        [
            "Molecules imported using 'moleculetype' will by default use 'moleculetype' as their reference name in membrane/solvation/flooding argumetns. If 'refname' is given then it will be used instead.",
        ],
    ],
    "Added 'rotate' subargument to 'protein' argument",
    [
        "Allows for multiple sets of rotations to be performed.",
    ],
    "Added 'solvate_hydrophobic_volume' subargument for membrane and solvation arguments",
    [
        "Membrane argument: Leaflet-specific subargument that sets whether or not the leaflet should allow solvent being placed within it. Default is 'False' (prevents solvent placement inside leaflet).",
        "Solvation argument: Sets whether or not the solvation will place molecules inside leaflets that have enabled it. Default is 'False' (prevents solvent placement inside leaflets).",
        "'solvate_hydrophobic_volume' must be used in at least one membrane AND one solvation argument to have any effect.",
    ],
    "Added 'solv_per_lipid_cutoff' allowing one to set the percentage cutoff (of number of beads contained in solvent box) for when a lipid should be counted for solvations using 'solv_per_lipid'. Default is '0.5' (half of a lipid)."
    "Re-added out-of-solvent-box checks, that moves molecules inside the solvent box if they have somehow ended up outside."
    "Added about 20 subarguments to the documentation that were previously available for use but not documented anywhere."
]

bug_fixes = [
    "Fixed error caused by using solvents that do not have 'molar_mass' and 'density' values set.",
    "Fixed improper dictionary keys for certain subarguments previously moved from the protein argument to the membrane argument.",
    "Fixed a few bugs with designating 'upbead'/'downbead' with 'molecule_import'.",
    "Fixed a bug regarding the z position of beads in multi-residue lipids.",
    "Protein placer now correctly checks if beads are placed outside the box and moves them inside (on the opposite side of the box).",
    "Molecules present in the ion libraries are now properly added to the solvent library with the parameter names 'pos_ions_[ParameterLibraryName]' / 'neg_ions_[ParameterLibraryName]' for each parameter library in the 'pos_ions' and 'neg_ions' libraries.",
    "Fixed problem with backup functionality when using full paths instead of relative paths",
]

tutorial_changes = [
    "Added new tutorials to the 'Tutorial_paper' notebook."
]

def version_change_writer(iterable, recursion_depth = 0):
    list_of_strings = []
    for i in iterable:
        if type(i) == str:
            if recursion_depth == 0:
                list_of_strings.append("    " * recursion_depth + i)
            else:
                list_of_strings.append("    " * recursion_depth + "-" + " " + i)

        elif type(i) in [list, tuple]:
            list_of_strings.extend(version_change_writer(i, recursion_depth + 1))
    return list_of_strings

### Extra empty "" is to add a blank line between sections
all_changes = []
if len(major_changes) > 0:
    all_changes += ["Major changes:", major_changes, ""]

if len(minor_changes) > 0:
    all_changes += ["Minor changes:", minor_changes, ""]

if len(bug_fixes) > 0:
    all_changes += ["Bug fixing:", bug_fixes, ""]

if len(tutorial_changes) > 0:
    all_changes += ["Tutorial changes:", tutorial_changes]

version_changes_list = version_change_writer(all_changes)
version_changes_str = "\n".join(version_changes_list)

def version_changes():
    print(version_changes_str)

### Abbreviation
changes = version_changes

