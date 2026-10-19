"""Base class for host-agnostic FridaForge commands."""

from abc import ABC, abstractmethod

from fridaforge.backend import Backend, ContextKind


class Command(ABC):
    """A single user-facing feature, independent of the host.

    Subclasses set the metadata class attributes and implement
    :meth:`run`, which pulls data from the *backend* and copies the
    generated snippet to the clipboard.
    """

    id: str
    description: str
    category: str
    hotkey: str | None = None
    context: ContextKind

    @abstractmethod
    def run(self, backend: Backend) -> None:
        """Execute the command against the given backend."""

    def _deliver(self, backend: Backend, snippet: str) -> None:
        """Copy the snippet to the clipboard and report the outcome."""
        if backend.copy_to_clipboard(snippet):
            backend.log_info("Frida snippet copied to clipboard.")
        else:
            backend.log_warn("Failed to copy snippet to clipboard.")
