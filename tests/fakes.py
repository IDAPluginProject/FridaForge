"""Test doubles for FridaForge backends."""

from fridaforge.backend import Backend, FunctionRef


class FakeBackend(Backend):
    """An in-memory Backend for unit tests."""

    def __init__(
        self,
        module_name: str = "libtest.so",
        image_base: int = 0x1000,
        current_address: int | None = None,
        current_function: FunctionRef | None = None,
        section_at: dict[int, str] | None = None,
        mnemonic_at: dict[int, str] | None = None,
    ):
        self._module_name = module_name
        self._image_base = image_base
        self._current_address = current_address
        self._current_function = current_function
        self._section_at = section_at or {}
        self._mnemonic_at = mnemonic_at or {}
        self.clipboard: str | None = None
        self.infos: list[str] = []
        self.warnings: list[str] = []

    def get_module_name(self) -> str:
        return self._module_name

    def get_image_base(self) -> int:
        return self._image_base

    def get_current_address(self) -> int | None:
        return self._current_address

    def get_current_function(self) -> FunctionRef | None:
        return self._current_function

    def get_section_name_at(self, addr: int) -> str | None:
        return self._section_at.get(addr)

    def get_instruction_mnemonic(self, addr: int) -> str | None:
        return self._mnemonic_at.get(addr)

    def copy_to_clipboard(self, text: str) -> bool:
        self.clipboard = text
        return True

    def log_info(self, msg: str) -> None:
        self.infos.append(msg)

    def log_warn(self, msg: str) -> None:
        self.warnings.append(msg)
