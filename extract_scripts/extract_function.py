from MyPack2.Utilities import truncDecimal

def extract_stallSpeed(blkx_path):
    """
    Extrait les données d'un fichier .blkx.
    Args:
        blkx_path (str): Chemin vers le fichier .blkx.
    Returns:
        dict: Données extraites.
    """
    stall_speed = 150

    with open(blkx_path, 'r', encoding='utf-8') as blkx_file:
        lines = blkx_file.readlines()

    for i, line in enumerate(lines):
        if "\"stallSpeed\"" in line:
                stall_speed = float(lines[i + 2].strip().strip('[],'))
        elif "\"MinimalSpeed\"" in line:
                stall_speed = float(line.split(":")[1].strip().strip(","))
        stall_speed = truncDecimal(stall_speed,0)
    return {
        "stallSpeed": stall_speed
    }