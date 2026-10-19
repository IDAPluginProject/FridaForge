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
