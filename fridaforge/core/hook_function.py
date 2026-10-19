"""Generator for Frida function hook snippets."""

from fridaforge.core import SnippetGenerator


class FunctionHookGenerator(SnippetGenerator):
    """Generate a Frida ``Interceptor.attach`` script for a function."""

    template_filename = "hook_function.js"

    def generate(
        self,
        module_name: str,
        function_relative_address: str,
        function_name: str,
    ) -> str:
        return self._render({
            "MODULE_NAME_PLACEHOLDER": module_name,
            "FUNCTION_RELATIVE_ADDRESS_PLACEHOLDER": function_relative_address,
            "FUNCTION_NAME_PLACEHOLDER": function_name,
        })
