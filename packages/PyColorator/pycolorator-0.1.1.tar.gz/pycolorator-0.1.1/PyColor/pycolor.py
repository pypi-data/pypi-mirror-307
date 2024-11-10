import os
import shutil
import sys
import platform
from enum import Enum
from typing import List, Tuple
import math
import atexit


class TerminalSupport:
    """Handles terminal compatibility and initialization across platforms."""

    @staticmethod
    def init_windows():
        """Initialize Windows terminal for ANSI support."""
        if platform.system() == "Windows":
            # Enable ANSI escape sequences on Windows
            from ctypes import windll, c_int, byref
            kernel32 = windll.kernel32

            # Get the current console mode
            mode = c_int(0)
            stdout_handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            kernel32.GetConsoleMode(stdout_handle, byref(mode))

            # Enable VIRTUAL_TERMINAL_PROCESSING
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(stdout_handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

            return True
        return False

    @staticmethod
    def init_unix():
        """Check and setup Unix-like terminal support."""
        if platform.system() in ["Linux", "Darwin"]:
            # Check if terminal supports colors
            if os.getenv('TERM') and 'color' in os.getenv('TERM'):
                return True

            # Try to force color support
            os.environ['TERM'] = 'xterm-256color'
            return True
        return False

    @staticmethod
    def get_terminal_size():
        """Get terminal size across platforms."""
        try:
            columns, rows = os.get_terminal_size()
        except (AttributeError, OSError):
            columns, rows = 80, 24  # Default fallback
        return columns, rows


class ColorGradients(Enum):
    # Basic Colors
    RED_GRADIENTS = [
        "\033[38;2;156;0;0m",
        "\033[38;2;208;0;0m",
        "\033[38;2;255;0;0m"
    ]

    ORANGE_GRADIENTS = [
        "\033[38;2;204;82;0m",
        "\033[38;2;255;102;0m",
        "\033[38;2;255;153;0m"
    ]

    YELLOW_GRADIENTS = [
        "\033[38;2;204;204;0m",
        "\033[38;2;255;255;0m",
        "\033[38;2;255;255;102m"
    ]

    GREEN_GRADIENTS = [
        "\033[38;2;0;156;0m",
        "\033[38;2;0;208;0m",
        "\033[38;2;0;255;0m"
    ]

    BLUE_GRADIENTS = [
        "\033[38;2;0;0;156m",
        "\033[38;2;0;0;208m",
        "\033[38;2;0;0;255m"
    ]

    PURPLE_GRADIENTS = [
        "\033[38;2;156;0;156m",
        "\033[38;2;208;0;208m",
        "\033[38;2;255;0;255m"
    ]

    CYAN_GRADIENTS = [
        "\033[38;2;0;156;156m",
        "\033[38;2;0;208;208m",
        "\033[38;2;0;255;255m"
    ]

    # Extended Colors
    PINK_GRADIENTS = [
        "\033[38;2;255;105;180m",
        "\033[38;2;255;130;200m",
        "\033[38;2;255;155;220m"
    ]

    MAGENTA_GRADIENTS = [
        "\033[38;2;208;0;128m",
        "\033[38;2;255;0;155m",
        "\033[38;2;255;0;180m"
    ]

    CORAL_GRADIENTS = [
        "\033[38;2;240;128;128m",
        "\033[38;2;255;160;160m",
        "\033[38;2;255;192;192m"
    ]

    SALMON_GRADIENTS = [
        "\033[38;2;250;128;114m",
        "\033[38;2;255;160;144m",
        "\033[38;2;255;192;174m"
    ]

    GOLD_GRADIENTS = [
        "\033[38;2;218;165;32m",
        "\033[38;2;238;185;52m",
        "\033[38;2;255;205;72m"
    ]

    LIME_GRADIENTS = [
        "\033[38;2;50;205;50m",
        "\033[38;2;70;225;70m",
        "\033[38;2;90;255;90m"
    ]

    EMERALD_GRADIENTS = [
        "\033[38;2;0;168;107m",
        "\033[38;2;0;198;127m",
        "\033[38;2;0;228;147m"
    ]

    TEAL_GRADIENTS = [
        "\033[38;2;0;156;156m",
        "\033[38;2;0;186;186m",
        "\033[38;2;0;216;216m"
    ]

    SKY_GRADIENTS = [
        "\033[38;2;135;206;235m",
        "\033[38;2;155;226;255m",
        "\033[38;2;175;246;255m"
    ]

    ROYAL_BLUE_GRADIENTS = [
        "\033[38;2;65;105;225m",
        "\033[38;2;85;125;245m",
        "\033[38;2;105;145;255m"
    ]

    INDIGO_GRADIENTS = [
        "\033[38;2;75;0;130m",
        "\033[38;2;95;20;150m",
        "\033[38;2;115;40;170m"
    ]

    VIOLET_GRADIENTS = [
        "\033[38;2;138;43;226m",
        "\033[38;2;158;63;246m",
        "\033[38;2;178;83;255m"
    ]

    LAVENDER_GRADIENTS = [
        "\033[38;2;230;230;250m",
        "\033[38;2;240;240;255m",
        "\033[38;2;250;250;255m"
    ]

    TURQUOISE_GRADIENTS = [
        "\033[38;2;64;224;208m",
        "\033[38;2;84;244;228m",
        "\033[38;2;104;255;248m"
    ]

    BRONZE_GRADIENTS = [
        "\033[38;2;205;127;50m",
        "\033[38;2;225;147;70m",
        "\033[38;2;245;167;90m"
    ]

    SILVER_GRADIENTS = [
        "\033[38;2;192;192;192m",
        "\033[38;2;212;212;212m",
        "\033[38;2;232;232;232m"
    ]

    # Neon Colors
    NEON_PINK_GRADIENTS = [
        "\033[38;2;255;0;102m",
        "\033[38;2;255;20;122m",
        "\033[38;2;255;40;142m"
    ]

    NEON_GREEN_GRADIENTS = [
        "\033[38;2;57;255;20m",
        "\033[38;2;77;255;40m",
        "\033[38;2;97;255;60m"
    ]

    NEON_BLUE_GRADIENTS = [
        "\033[38;2;0;146;255m",
        "\033[38;2;20;166;255m",
        "\033[38;2;40;186;255m"
    ]

    NEON_ORANGE_GRADIENTS = [
        "\033[38;2;255;128;0m",
        "\033[38;2;255;148;20m",
        "\033[38;2;255;168;40m"
    ]

    # Pastel Colors
    PASTEL_PINK_GRADIENTS = [
        "\033[38;2;255;182;193m",
        "\033[38;2;255;202;213m",
        "\033[38;2;255;222;233m"
    ]

    PASTEL_BLUE_GRADIENTS = [
        "\033[38;2;173;216;230m",
        "\033[38;2;193;236;250m",
        "\033[38;2;213;255;255m"
    ]

    PASTEL_GREEN_GRADIENTS = [
        "\033[38;2;176;224;176m",
        "\033[38;2;196;244;196m",
        "\033[38;2;216;255;216m"
    ]

    PASTEL_YELLOW_GRADIENTS = [
        "\033[38;2;255;239;213m",
        "\033[38;2;255;249;233m",
        "\033[38;2;255;255;253m"
    ]

    # Special Colors
    RAINBOW_GRADIENTS = [
        "\033[38;2;255;0;0m",  # Red
        "\033[38;2;255;127;0m",  # Orange
        "\033[38;2;255;255;0m",  # Yellow
        "\033[38;2;0;255;0m",  # Green
        "\033[38;2;0;0;255m",  # Blue
        "\033[38;2;139;0;255m"  # Violet
    ]

    SUNSET_GRADIENTS = [
        "\033[38;2;255;128;0m",  # Orange
        "\033[38;2;255;64;64m",  # Red-Orange
        "\033[38;2;255;0;128m"  # Pink
    ]

    OCEAN_GRADIENTS = [
        "\033[38;2;0;119;190m",  # Deep Blue
        "\033[38;2;0;150;220m",  # Medium Blue
        "\033[38;2;0;180;255m"  # Light Blue
    ]

    FOREST_GRADIENTS = [
        "\033[38;2;34;139;34m",  # Forest Green
        "\033[38;2;0;160;0m",  # Medium Green
        "\033[38;2;50;205;50m"  # Light Green
    ]


class Direction(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL = "diagonal"
    REVERSE_DIAGONAL = "reverse_diagonal"
    RADIAL = "radial"
    WAVE = "wave"  # New wave pattern


class ColorateSystem:
    """Singleton class to manage global coloring system state."""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ColorateSystem, cls).__new__(cls)
        return cls._instance

    def get_terminal_size(self):
        try:
            cols, rows = shutil.get_terminal_size((80, 20))
        except AttributeError:
            # Impostazione di default
            cols, rows = 80, 20
        return cols, rows

    @classmethod
    def init(cls, force_color: bool = False, wave_amplitude: float = 1.0,
             wave_frequency: float = 0.1, restore_on_exit: bool = True):
        """Initialize the coloring system with custom settings."""
        if cls._initialized:
            return

        instance = cls()
        instance.force_color = force_color
        instance.wave_amplitude = wave_amplitude
        instance.wave_frequency = wave_frequency
        instance.original_term = os.getenv('TERM')

        # Platform-specific initialization
        if platform.system() == "Windows":
            TerminalSupport.init_windows()
        else:
            TerminalSupport.init_unix()

        # Setup terminal restoration on exit if requested
        if restore_on_exit:
            def restore_terminal():
                if instance.original_term:
                    os.environ['TERM'] = instance.original_term
                sys.stdout.write('\033[0m')  # Reset all attributes
                sys.stdout.flush()

            atexit.register(restore_terminal)

        # Store terminal capabilities
        instance.supports_color = (
                force_color or
                sys.stdout.isatty() and
                (platform.system() != "Windows" or TerminalSupport.init_windows())
        )

        cls._initialized = True
        return instance

    @property
    def initialized(self):
        return self._initialized


class Colorate:
    RESET = "\033[0m"

    def __init__(self):
        self.width = 0
        self.height = 0
        self.system = ColorateSystem()
        self.system.init()

        # Ensure the system is initialized with defaults if not done already
        if not ColorateSystem.initialized:
            ColorateSystem.init()

    @staticmethod
    def _interpolate_colors(color1: List[int], color2: List[int], ratio: float) -> Tuple[int, int, int]:
        """Interpolate between two RGB colors."""
        return tuple(int(color1[i] + (color2[i] - color1[i]) * ratio) for i in range(3))  # type: ignore

    @staticmethod
    def _parse_ansi_color(ansi_code: str) -> Tuple[int, int, int]:
        """Extract RGB values from ANSI color code."""
        rgb = ansi_code.split('[38;2;')[1].split('m')[0].split(';')
        return tuple(map(int, rgb))  # type: ignore

    def gradient_text(self, text: str, gradient1: ColorGradients, gradient2: ColorGradients = None,
                      direction: Direction = Direction.HORIZONTAL) -> str:
        """
        Apply gradient coloring to text.

        Parameters:
            text (str): The text to be colored with gradients.
            gradient1 (ColorGradients): The first gradient color to apply.
            gradient2 (ColorGradients, optional): The second gradient color to apply.
                If None, gradient1 will be used for both ends.
            direction (Direction): The direction of the gradient. Can be one of
                Direction.HORIZONTAL, Direction.VERTICAL, Direction.DIAGONAL,
                Direction.REVERSE_DIAGONAL, Direction.RADIAL, or Direction.WAVE.

        Returns:
            str: The text with applied gradient colors. If the text is empty or
                 color support is not enabled, returns the original text.

        Raises:
            ValueError: If gradient1 or gradient2 is not of type ColorGradients or
                        list, or if direction is not a valid Direction.
        """
        if not text:
            return text

        if not isinstance(gradient1, (ColorGradients, list)):
            raise ValueError("Invalid gradient1 type. Must be ColorGradients or list of RGB tuples.")

        if gradient2 is not None and not isinstance(gradient2, (ColorGradients, list)):
            raise ValueError("Invalid gradient2 type. Must be ColorGradients or list of RGB tuples.")

        if direction not in Direction:
            raise ValueError("Invalid direction. Must be one of the Direction enum values.")

        self.width = max(map(len, text.split('\n')))
        self.height = text.count('\n') + 1

        if gradient2 is None:
            gradient2 = gradient1

        grad1_colors = [self._parse_ansi_color(c) for c in gradient1.value]
        grad2_colors = [self._parse_ansi_color(c) for c in gradient2.value]

        result = []
        lines = text.split('\n')

        for y, line in enumerate(lines):
            colored_line = ""
            for x, char in enumerate(line):
                if char.strip():
                    color = self._get_color_at_position(x, y, direction, grad1_colors, grad2_colors)
                    colored_line += f"\033[38;2;{color[0]};{color[1]};{color[2]}m{char}"
                else:
                    colored_line += char
            result.append(colored_line)

        return f"{self.RESET}\n".join(result) + self.RESET

    def _get_color_at_position(self, x: int, y: int, direction: Direction,
                               grad1_colors: List[Tuple[int, int, int]],
                               grad2_colors: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
        """Calculate color at specific position based on direction."""
        ratio = int()
        if direction == Direction.HORIZONTAL:
            ratio = x / max(1, self.width - 1)
        elif direction == Direction.VERTICAL:
            ratio = y / max(1, self.height - 1)
        elif direction == Direction.DIAGONAL:
            ratio = (x + y) / max(1, self.width + self.height - 2)
        elif direction == Direction.REVERSE_DIAGONAL:
            ratio = (x + (self.height - 1 - y)) / max(1, self.width + self.height - 2)
        elif direction == Direction.RADIAL:
            center_x = self.width / 2
            center_y = self.height / 2
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            max_distance = math.sqrt(center_x ** 2 + center_y ** 2)
            ratio = distance / max_distance
        elif direction == Direction.WAVE:
            # Create a wave effect using sine function
            wave = math.sin(x * self.system.wave_frequency) * self.system.wave_amplitude
            ratio = (y + wave) / max(1, self.height - 1)
            ratio = max(0, min(1, ratio))  # Clamp between 0 and 1

        # Interpolate between the gradient colors
        grad1_pos = ratio * (len(grad1_colors) - 1)
        grad2_pos = ratio * (len(grad2_colors) - 1)

        grad1_idx = int(grad1_pos)
        grad2_idx = int(grad2_pos)

        grad1_ratio = grad1_pos - grad1_idx
        grad2_ratio = grad2_pos - grad2_idx

        if grad1_idx >= len(grad1_colors) - 1:
            color1 = grad1_colors[-1]
        else:
            color1 = self._interpolate_colors(
                grad1_colors[grad1_idx],  # type: ignore
                grad1_colors[grad1_idx + 1],  # type: ignore
                grad1_ratio
            )

        if grad2_idx >= len(grad2_colors) - 1:
            color2 = grad2_colors[-1]
        else:
            color2 = self._interpolate_colors(
                grad2_colors[grad2_idx],  # type: ignore
                grad2_colors[grad2_idx + 1],  # type: ignore
                grad2_ratio
            )

        return self._interpolate_colors(color1, color2, ratio)  # type: ignore


