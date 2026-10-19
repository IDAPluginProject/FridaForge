"""Generator for Frida dlopen hook snippets."""

from fridaforge.core import SnippetGenerator


class DlopenHookGenerator(SnippetGenerator):
    """Generate a Frida script that hooks dlopen-family functions."""

    template_filename = "hook_dlopen_functions.js"

    def generate(self, module_name: str) -> str:
        return self._render({
            "MODULE_NAME_PLACEHOLDER": module_name,
        })
