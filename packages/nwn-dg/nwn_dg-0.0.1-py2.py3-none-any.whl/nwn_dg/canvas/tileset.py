import copy
import json
import random
import sys

from ..classes import Directions, get_new_coordinates

TILESET_BASEDATA = {
    "ChanceLightning": {"type": "int", "value": 0},
    "ChanceRain": {"type": "int", "value": 0},
    "ChanceSnow": {"type": "int", "value": 0},
    "Comments": {"type": "cexostring", "value": ""},
    "Creator_ID": {"type": "int", "value": -1},
    "DayNightCycle": {"type": "byte", "value": 0},
    "Expansion_List": {"type": "list", "value": []},
    "Flags": {"type": "dword", "value": 3},
    "FogClipDist": {"type": "float", "value": 45},
    "Height": {"type": "int", "value": 15},
    "ID": {"type": "int", "value": -1},
    "IsNight": {"type": "byte", "value": 1},
    "LightingScheme": {"type": "byte", "value": 13},
    "LoadScreenID": {"type": "word", "value": 0},
    "ModListenCheck": {"type": "int", "value": 0},
    "ModSpotCheck": {"type": "int", "value": 0},
    "MoonAmbientColor": {"type": "dword", "value": 2960685},
    "MoonDiffuseColor": {"type": "dword", "value": 6457991},
    "MoonFogAmount": {"type": "byte", "value": 5},
    "MoonFogColor": {"type": "dword", "value": 0},
    "MoonShadows": {"type": "byte", "value": 0},
    "Name": {
        "type": "cexolocstring",
        "value": {"0": "Unnamed"},
    },
    "NoRest": {"type": "byte", "value": 0},
    "OnEnter": {"type": "resref", "value": ""},
    "OnExit": {"type": "resref", "value": ""},
    "OnHeartbeat": {"type": "resref", "value": ""},
    "OnUserDefined": {"type": "resref", "value": ""},
    "PlayerVsPlayer": {"type": "byte", "value": 3},
    "ResRef": {"type": "resref", "value": "new_resref"},
    "ShadowOpacity": {"type": "byte", "value": 60},
    "SkyBox": {"type": "byte", "value": 0},
    "SunAmbientColor": {"type": "dword", "value": 0},
    "SunDiffuseColor": {"type": "dword", "value": 0},
    "SunFogAmount": {"type": "byte", "value": 0},
    "SunFogColor": {"type": "dword", "value": 0},
    "SunShadows": {"type": "byte", "value": 0},
    "Tag": {"type": "cexostring", "value": "NewTag"},
    "TileBrdrDisabled": {"type": "byte", "value": 0},
    "Tile_List": {
        "type": "list",
        "value": [],
    },
    "Tileset": {"type": "resref", "value": "tdc01"},
    "Version": {"type": "dword", "value": 3},
    "Width": {"type": "int", "value": 15},
    "WindPower": {"type": "int", "value": 0},
    "__data_type": "ARE ",
}

# The orientation of the tile, 0-3.
#     0 = Normal orientation
#     1 = 90 degrees counterclockwise
#     2 = 180 degrees counterclockwise
#     3 = 270 degrees counterclockwise

# Center, N, E, S, W
# Terminating corridor, North
# Corridors: 41, 119
#
G_CELL_PATTERNS = {
    "tdc01": {
        "W": {"Tile_ID": [5]},
        # Corridor
        "CCWWW": {"Tile_ID": [41]},  # , 119]},
        "CWWCC": {"Tile_ID": [127]},  # , 37, 128]},
        "CCWCC": {"Tile_ID": [130]},  # , 39]},
        "CCWCW": {"Tile_ID": [118]},
        "CCCCC": {"Tile_ID": [40]},
        # ---
        # Corridor next to rooms
        "CRWCW": {"Tile_ID": [129]},
        "CRWRW": {"Tile_ID": [118]},
        # ---
        # Rooms
        "RWWRR": {"Tile_ID": [0]},
        "RRWRR": {"Tile_ID": [117]},
        "RRRRR": {"Tile_ID": [101]},
        # ---
        # Rooms + Corridor exits
        "RCWRR": {"Tile_ID": [125]},
        "RRCCR": {"Tile_ID": [19]},
        "RRWCR": {"Tile_ID": [126]},
        "RRCRR": {"Tile_ID": [18]},
    },
}

G_TILESET_TILES = {
    # fmt: off
  "tdc01": {
      0: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 0}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
      4: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 4}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
      5: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 5}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
     18: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 18}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     19: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 19}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 0}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
     21: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 21}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
     30: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 117}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     38: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 38}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     65: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 65}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     40: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 40}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
     41: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 41}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     71: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 71}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    101: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 101}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    102: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 102}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 0}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
    109: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 109}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
    114: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 114}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    115: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 115}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    116: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 116}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    117: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 117}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    118: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 118}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 0}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    119: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 119}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    125: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 125}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    126: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 126}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    127: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 127}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    129: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 129}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    130: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 130}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},

  },
    # fmt: on
}


# TODO: Parse tdc01.set.txt to combine tiles together
#
class Tileset:
    def __init__(self, dungeon):
        self._dungeon = dungeon
        self._cells = dungeon.cells
        self._tileset = copy.deepcopy(TILESET_BASEDATA)
        self._cell_patterns = copy.deepcopy(G_CELL_PATTERNS["tdc01"])
        self._tileset_tiles = copy.deepcopy(G_TILESET_TILES["tdc01"])

        # TODO: ResRef, Tag, OnExit, OnEnter, ... merge from input
        # TODO: Tileset
        self._tileset["Height"]["value"] = self._dungeon.height
        self._tileset["Width"]["value"] = self._dungeon.width

        self._calculate_cells()
        # pprint(self._cell_patterns)

    def _calculate_cells(self):
        def get_orientations(c0, pattern):
            # Rotate with C.1234 becomes C.4123
            retval = []
            for i in range(1, 4):
                pattern = pattern[1:] + pattern[0]
                # pattern = pattern[-1:] + pattern[:-1]
                retval += [(i, c0 + pattern)]
            return retval

        # Do all permutations
        patterns = copy.deepcopy(self._cell_patterns)
        for pattern, pattern_data in patterns.items():
            c0 = pattern[0]
            pattern = pattern[1:]
            if not len(pattern):
                continue

            orientations = get_orientations(c0, pattern)
            for orientation, key in orientations:
                # if it already exists, skip it
                if key in self._cell_patterns.keys():
                    continue
                pattern_data = copy.deepcopy(pattern_data)
                pattern_data["Tile_Orientation"] = orientation
                self._cell_patterns[key] = pattern_data

    def draw(self):
        def get_new_cell(x, y, direction):
            x, y = get_new_coordinates(x, y, direction)
            if x < 0 or y < 0:
                return None
            if x >= self._dungeon.width or y >= self._dungeon.height:
                return None
            return self._cells[x][y]

        def get_key(cells):
            retval = ""
            for cell in cells:
                if cell is None:
                    retval += "W"
                elif cell.is_corridor():
                    retval += "C"
                elif cell.is_room():
                    retval += "R"
                else:
                    retval += "W"
            return retval

        def set_tile(keys):
            for key in keys:
                if key not in self._cell_patterns.keys():
                    continue

                cell_pattern = self._cell_patterns[key]
                tileids = cell_pattern["Tile_ID"]
                random.shuffle(tileids)
                tileid = tileids[0]

                if tileid not in self._tileset_tiles:
                    sys.exit(f"tileid {tileid} does not exist in tileset tiles")

                tile = copy.deepcopy(self._tileset_tiles[tileid])
                tile["Tile_Orientation"]["value"] = cell_pattern.get("Tile_Orientation", 0)
                self._tileset["Tile_List"]["value"] += [tile]
                return True
            return False

        # dungeon map is (0,0) at the top, but it's bottom left to right, to top
        # in the are file list
        for y in range(self._dungeon.height, 0, -1):
            y -= 1
            for x in range(self._dungeon.width):
                cell = self._cells[x][y]
                n_cell = get_new_cell(x, y, Directions.NORTH)
                e_cell = get_new_cell(x, y, Directions.EAST)
                s_cell = get_new_cell(x, y, Directions.SOUTH)
                w_cell = get_new_cell(x, y, Directions.WEST)

                k1 = get_key([cell])
                k5 = k1 + get_key([n_cell, e_cell, s_cell, w_cell])

                # TODO: temporary fix
                if not set_tile([k1, k5, "W"]):
                    set_tile(["W"])
                    sys.exit(f"key not found: {k1},{k5} for {cell}")

        with open("output.json", "w") as fd:
            fd.write(json.dumps(self._tileset, indent=2))
