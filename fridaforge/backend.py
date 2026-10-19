"""Host-agnostic backend interface for FridaForge commands."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class ContextKind(Enum):
    """The host context a command needs to run."""

    GLOBAL = auto()    # only the module is needed
    ADDRESS = auto()   # the current address is needed
    FUNCTION = auto()  # the current function is needed


@dataclass(frozen=True)
class FunctionRef:
    """A resolved reference to a function in the loaded binary."""

    start: int
    name: str


class Backend(ABC):
    """The port each host (Binary Ninja, IDA) must implement."""

    @abstractmethod
    def get_module_name(self) -> str:
        """Return the loaded module's base file name."""

    @abstractmethod
    def get_image_base(self) -> int:
        """Return the image base address of the loaded binary."""

    @abstractmethod
    def get_current_address(self) -> int | None:
        """Return the currently selected address, or ``None``."""

    @abstractmethod
    def get_current_function(self) -> FunctionRef | None:
        """Return the currently selected function, or ``None``."""

    @abstractmethod
    def get_section_name_at(self, addr: int) -> str | None:
        """Return the name of the section/segment containing *addr*."""

    @abstractmethod
    def get_instruction_mnemonic(self, addr: int) -> str | None:
        """Return the mnemonic of the instruction at *addr*, or ``None``."""

    @abstractmethod
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy *text* to the system clipboard. Return success."""

    @abstractmethod
    def log_info(self, msg: str) -> None:
        """Emit an informational message in the host's idiom."""

    @abstractmethod
    def log_warn(self, msg: str) -> None:
        """Emit a warning message in the host's idiom."""

    # --- concrete helpers shared by all hosts ---

    def get_relative_address(self, addr: int) -> str:
        """Return *addr*'s offset from the image base as a hex string."""
        return hex(addr - self.get_image_base())

    def _resolve_function_name(self, start: int, raw_name: str) -> str:
        """Return *raw_name*, or a ``sub_<offset>`` fallback when empty."""
        if raw_name:
            return raw_name
        relative_address = self.get_relative_address(start)
        return f"sub_{relative_address.removeprefix('0x')}"
