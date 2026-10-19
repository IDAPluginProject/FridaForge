"""Base class for Frida snippet generators.

Every generator **must** subclass :class:`SnippetGenerator` and:

1. Set the ``template_filename`` class attribute to the name of a
   JavaScript template file located in the ``templates/`` directory.
2. Implement a ``generate()`` method with explicit, typed parameters
   that builds a placeholder mapping and delegates to :meth:`_render`.

Both constraints are validated at class-creation time; forgetting
either one raises :class:`TypeError` immediately.
"""

from collections.abc import Mapping

from fridaforge.core.utils import fill_template, read_template


class SnippetGenerator:
    """Abstract base for all Frida snippet generators."""

    template_filename: str

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)

        if not getattr(cls, "template_filename", None):
            raise TypeError(
                f"{cls.__name__} must define 'template_filename' "
                f"as a non-empty class attribute."
            )

        if "generate" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} must implement a 'generate()' method."
            )

    def _render(self, placeholders: Mapping[str, str | int]) -> str:
        """Read the template, substitute placeholders, and return the result."""
        template = read_template(self.template_filename)
        return fill_template(template, placeholders)


from fridaforge.core.hook_dlopen_functions import DlopenHookGenerator
from fridaforge.core.hook_function import FunctionHookGenerator
from fridaforge.core.modify_section_protection import (
    ModifySectionProtectionGenerator,
)
from fridaforge.core.negate_cond_branch_arm64 import (
    NegateArm64CondBranchGenerator,
)
from fridaforge.core.negate_cond_branch_x86 import (
    NegateX86CondBranchGenerator,
)

__all__ = [
    "SnippetGenerator",
    "DlopenHookGenerator",
    "FunctionHookGenerator",
    "ModifySectionProtectionGenerator",
    "NegateArm64CondBranchGenerator",
    "NegateX86CondBranchGenerator",
]
