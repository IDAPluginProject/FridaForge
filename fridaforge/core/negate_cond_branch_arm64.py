"""Generator for Frida ARM64 conditional branch negation snippets."""

from fridaforge.core import SnippetGenerator


class NegateArm64CondBranchGenerator(SnippetGenerator):
    """Generate a Frida script that negates an ARM64 conditional branch."""

    template_filename = "negate_cond_branch_arm64.js"

    def generate(self, module_name: str, relative_address: str) -> str:
        return self._render({
            "MODULE_NAME_PLACEHOLDER": module_name,
            "RELATIVE_ADDRESS_PLACEHOLDER": relative_address,
        })
