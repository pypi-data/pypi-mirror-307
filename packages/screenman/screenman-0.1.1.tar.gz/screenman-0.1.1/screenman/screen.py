"""Screen abstractions for screenman."""

import re
from dataclasses import dataclass

from loguru import logger

from screenman import toml_config
from screenman.edid import Edid
from screenman.utils import ScreenSettings, exec_cmd, rot_to_str, str_to_rot

LAYOUTS: dict[str, dict[str, ScreenSettings]] = toml_config.layouts


@dataclass
class Mode:
    width: int
    height: int
    freq: float
    current: bool
    preferred: bool

    def resolution(self):
        return self.width, self.height

    def __str__(self):
        return f"<{self.width}x{self.height}, {self.freq}, curr: {self.current}, pref: {self.preferred}>"

    def cmd_str(self):
        return f"{self.width}x{self.height}"


class Screen:
    """
    Represents a screen with various settings and capabilities.
    Taken and modified from pyrandr:
    https://github.com/cakturk/pyrandr/tree/master

    Attributes:
        name (str): The name of the screen.
        uid (str): The unique identifier for the screen, derived from EDID.
        curr_mode (Mode): The current mode of the screen.
        supported_modes (list): List of supported modes for the screen.
        __set (ScreenSettings): The settings for the screen.

    Methods:
        name: Returns the name of the screen.
        is_connected: Returns whether the screen is connected.
        is_enabled: Gets or sets whether the screen is enabled.
        is_primary: Gets or sets whether the screen is the primary screen.
        resolution: Gets or sets the resolution of the screen.
        rotation: Gets or sets the rotation of the screen.
        position: Gets or sets the position of the screen.
        available_resolutions: Returns a list of available resolutions.
        check_resolution: Checks if a given resolution is supported.
        build_cmd: Builds the command to apply the screen settings.
    """

    def __init__(self, name, primary, rot, modes, edid_hex):
        self.__name = name
        self.__set = ScreenSettings()
        self.uid = None

        if edid_hex:
            edid = Edid.from_edid_hex(edid_hex)
            self.uid = edid.serial or edid.fallback_uid

        self.curr_mode = (
            next((item for item in modes if item.current), None) if modes else None
        )
        self.supported_modes = modes
        self._initialize_settings(primary, rot)

    def _initialize_settings(self, primary, rot):
        self.__set.rotation = rot
        self.__set.is_primary = primary
        self.__set.is_enabled = bool(
            [mode for mode in self.supported_modes if mode.current]
        )
        self.__set.is_connected = bool(self.supported_modes)
        if self.curr_mode:
            self.__set.resolution = self.curr_mode.resolution()

    @property
    def name(self):
        return self.__name

    @property
    def is_connected(self):
        return self.__set.is_connected

    @property
    def is_enabled(self):
        return self.__set.is_enabled

    @is_enabled.setter
    def is_enabled(self, enable):
        if enable != self.__set.is_enabled:
            self.__set.is_enabled = enable
            self.__set.change_table["is_enabled"] = True

    @property
    def is_primary(self):
        return self.__set.is_primary

    @is_primary.setter
    def is_primary(self, is_primary):
        if is_primary != self.__set.is_primary:
            self.__set.is_primary = is_primary
            self.__set.change_table["is_primary"] = True

    @property
    def resolution(self):
        return self.__set.resolution

    @resolution.setter
    def resolution(self, newres):
        if not self.is_enabled and not self.__set.change_table["is_enabled"]:
            return
        if newres != self.__set.resolution:
            self.check_resolution(newres)
            self.__set.resolution = newres
            self.__set.change_table["resolution"] = True

    @property
    def rotation(self):
        return self.__set.rotation

    @rotation.setter
    def rotation(self, direction):
        if direction != self.__set.rotation:
            self.__set.rotation = direction
            self.__set.change_table["rotation"] = True

    @property
    def position(self):
        return self.__set.position

    @position.setter
    def position(self, args):
        if args != self.__set.position:
            self.__set.position = args
            self.__set.change_table["position"] = True

    def available_resolutions(self):
        return [(r.width, r.height) for r in self.supported_modes]

    def check_resolution(self, newres):
        if newres not in self.available_resolutions():
            raise ValueError("Requested resolution is not supported", newres)

    def build_cmd(self):
        if any(self.__set.change_table.values()):
            if not self.name:
                raise ValueError("Cannot apply settings without screen name", self.name)
            cmd = ["xrandr", "--output", self.name]

            if self.is_enabled:
                cmd.append("--auto")
                self._add_resolution(cmd)
                self._add_primary(cmd)
                self._add_rotation(cmd)
                self._add_position(cmd)
            else:
                cmd.append("--off")

            return cmd
        return None

    def _add_resolution(self, cmd):
        if self.__set.change_table["resolution"]:
            cmd.extend(
                ["--mode", f"{self.__set.resolution[0]}x{self.__set.resolution[1]}"]
            )

    def _add_primary(self, cmd):
        if self.__set.change_table["is_primary"]:
            cmd.append("--primary")

    def _add_rotation(self, cmd):
        if self.__set.change_table["rotation"]:
            rot = rot_to_str(self.__set.rotation)
            if not rot:
                raise ValueError("Invalid rotation value", rot, self.__set.rotation)
            cmd.extend(["--rotate", rot])

    def _add_position(self, cmd):
        if self.__set.change_table["position"]:
            rel, pos = self.__set.position
            cmd.extend([rel, pos])

    def __str__(self):
        return (
            f"<{self.name}, UID: {self.uid}, primary: {self.is_primary}, modes: {len(self.supported_modes)}, "
            f"conn: {self.is_connected}, rot: {rot_to_str(self.rotation)}, enabled: {self.is_enabled}, res: {self.resolution}>"
        )

    __repr__ = __str__


def create_screen(name_str, modes, edid):
    """
    Create a Screen object from the given parameters.

    Args:
        name_str (str): The name string containing screen information.
        modes (list): A list of supported modes for the screen.
        edid (str): The EDID data for the screen.

    Returns:
        Screen: A Screen object initialized with the given parameters.
    """
    sc_name = name_str.split()[0]
    rot = str_to_rot(name_str.split()[3]) if len(name_str.split()) > 2 else None
    return Screen(sc_name, "primary" in name_str, rot, modes, edid)


def parse_screen_connection(line):
    """
    Parse a line to determine if it indicates a connected or disconnected screen.

    Args:
        line (str): The line to parse.

    Returns:
        str: "connected" if the screen is connected, "disconnected" if the screen is disconnected, None otherwise.
    """
    rx_conn = re.compile(r"\bconnected\b")
    rx_disconn = re.compile(r"\bdisconnected\b")
    if re.search(rx_conn, line):
        return "connected"
    elif re.search(rx_disconn, line):
        return "disconnected"
    return None


def parse_edid_data(line, parsing_edid, edid):
    """
    Extract EDID data from the line if currently parsing EDID information.

    Args:
        line (str): The line to parse.
        parsing_edid (bool): Whether EDID parsing is currently active.
        edid (str): The accumulated EDID data.

    Returns:
        tuple: A tuple containing a boolean indicating if EDID parsing is active and the accumulated EDID data.
    """
    rx_edid_start = re.compile(r"\s+EDID:")
    rx_edid_data = re.compile(r"\s+([0-9a-fA-F]{32})")

    if re.search(rx_edid_start, line):
        return True, edid
    if parsing_edid:
        match = re.match(rx_edid_data, line)
        if match:
            edid += match.group(1)
            return parsing_edid, edid
        return False, edid
    return parsing_edid, edid


def parse_screen_modes(line, modes):
    """
    Parse a line to extract mode information.

    Args:
        line (str): The line to parse.
        modes (list): The list of modes to append the parsed mode to.

    Returns:
        list: The updated list of modes.
    """
    rx_mode = re.compile(r"^\s+(\d+)x(\d+)\s+((?:\d+\.)?\d+)([* ]?)([+ ]?)")
    match = re.search(rx_mode, line)
    if match:
        width, height = int(match.group(1)), int(match.group(2))
        freq = float(match.group(3))
        current = match.group(4).strip() == "*"
        preferred = match.group(5).strip() == "+"
        modes.append(Mode(width, height, freq, current, preferred))
    return modes


def parse_xrandr(lines):
    """
    Parse the output of the xrandr command to extract screen information.

    Args:
        lines (list): The lines of output from the xrandr command.

    Returns:
        list: A list of Screen objects representing the connected screens.
    """
    sc_name_line = None
    edid = ""
    parsing_edid = False
    screens = []
    modes = []

    for line in lines:
        connection_status = parse_screen_connection(line)
        if connection_status:
            if sc_name_line:
                newscreen = create_screen(sc_name_line, modes, edid)
                screens.append(newscreen)
                modes = []
                edid = ""
                parsing_edid = False
            sc_name_line = line
        else:
            parsing_edid, edid = parse_edid_data(line, parsing_edid, edid)
            modes = parse_screen_modes(line, modes)

    if sc_name_line:
        newscreen = create_screen(sc_name_line, modes, edid)
        screens.append(newscreen)

    return screens


def connected_screens():
    """
    Get a list of connected screens.

    Returns:
        list: A list of connected Screen objects.
    """
    return [s for s in parse_xrandr(exec_cmd(["xrandr", "--props"])) if s.is_connected]


def determine_layout(screens):
    """
    Determine the layout name based on the connected screens.

    Args:
        screens (list): A list of connected Screen objects.

    Returns:
        str: The name of the determined layout, or "auto" if no matching layout is found.
    """
    layouts = sorted(LAYOUTS.items(), key=lambda x: len(x[1]), reverse=True)
    for layout_name, layout in layouts:
        if all(
            screen_uid in {screen.uid for screen in screens} for screen_uid in layout
        ):
            return layout_name
    return "auto"


def apply_layout(screens, layout_name):
    """
    Apply the specified layout to the connected screens.

    Args:
        screens (list): A list of connected Screen objects.
        layout_name (str): The name of the layout to apply.

    Returns:
        None
    """
    xrandr_auto = exec_cmd(["xrandr", "--auto", "-v"])
    logger.debug(f"Output of xrandr --auto: {xrandr_auto}")

    if layout_name == "auto":
        return

    xrandr_cmd = ["xrandr"]

    layout = LAYOUTS.get(layout_name, {})
    for screen in screens:
        settings: ScreenSettings | None = layout.get(screen.uid)
        if settings:
            for key, value in settings.__dict__.items():
                if key not in ["change_table", "is_connected"]:
                    logger.debug(f"Setting {key} to {value} for screen {screen.uid}")
                    setattr(screen, key, value)
        else:
            screen.is_enabled = False
        xrandr_cmd.append(screen.build_cmd()[1:])

    logger.debug(f"Applying settings: {xrandr_cmd}")
    exec_cmd(xrandr_cmd)


###
# Run the script standalone, useful for debugging
###
if __name__ == "__main__":
    screens = connected_screens()
    for s in screens:
        print(s)
    layout_name = determine_layout(screens)
    if layout_name:
        print(f"Applying layout: {layout_name}")
        apply_layout(screens, layout_name)
    else:
        print("No matching layout found.")
