"""Basic tests for blueprint metadata completeness."""

import importlib
import inspect

from covalent_blueprints_ai.database import SnowflakeConfig


class TestSummaries:
    """Tests for blueprints summaries."""

    @classmethod
    def setup_class(cls):
        module = importlib.import_module("covalent_blueprints_ai")
        cls.blueprint_initializers = {
            attr: getattr(module, attr) for attr in module.__all__
        }
        cls.blueprint_objs = {}
        for name, bp in cls.blueprint_initializers.items():
            cls.blueprint_objs[name] = bp()

    def test_name_not_empty(self):
        """Check that the name is not empty."""
        for bp_name, bp in self.blueprint_objs.items():
            assert bp.name, f"Empty name in blueprint {bp_name}"

    def test_title_not_empty(self):
        """Check that the title is not empty."""
        for bp_name, bp in self.blueprint_objs.items():
            assert bp.title, f"Empty title in blueprint {bp_name}"

    def test_description_not_empty(self):
        """Check that the description is not empty."""
        for bp_name, bp in self.blueprint_objs.items():
            assert bp.description, f"Empty description in blueprint {bp_name}"

    def test_at_least_one_executor(self):
        """Check that there is at least one executor."""
        for bp_name, bp in self.blueprint_objs.items():
            assert bp.executors, f"No executors in blueprint {bp_name}"

    def test_at_least_one_environment(self):
        """Check that there is at least one environment."""
        for bp_name, bp in self.blueprint_objs.items():
            assert bp.environments, f"No environments in blueprint {bp_name}"

    def test_example_not_empty(self):
        """Check that the example string is not empty."""
        for bp_name, bp in self.blueprint_objs.items():
            assert bp.example, f"Empty usage example for '{bp_name}'"

    def test_args_tuple_is_empty(self):
        """Check that the current arguments tuple is empty."""
        for bp_name, bp in self.blueprint_objs.items():
            msg = f"Blueprint '{bp_name}' has a non-empty args tuple."
            assert bp.inputs._core_args == (), msg

    def test_every_kwarg_documented(self):
        """Check that every keyword input has a matching docs entry."""
        for bp_name, bp in self.blueprint_objs.items():
            for kwarg in bp.inputs.kwargs:
                assert (
                    kwarg in bp.inputs.docs
                ), f"Missing doc for '{kwarg}' in '{bp_name}'"

    def test_every_doc_matches_kwarg(self):
        """Check that every documented input has a matching keyword."""
        for bp_name, bp in self.blueprint_objs.items():
            docs_ = bp.inputs.docs.copy()
            missing = []
            for kwarg_name in docs_:
                if kwarg_name not in bp.inputs.kwargs:
                    missing.append(kwarg_name)

            for kwarg in missing:
                if not kwarg.startswith("*"):
                    msg = (
                        f"Documented kwarg '{kwarg}' for '{bp_name}' does "
                        "not exist in `.inputs.kwargs`"
                    )
                    assert kwarg in bp.inputs.kwargs, msg

    def test_doc_keys_match_argument_type(self):
        """Check that every input is documented with '*' or '**' in
        name if required."""
        for bp_name, bp in self.blueprint_objs.items():
            bp_initializer = self.blueprint_initializers[bp_name]
            bp_initializer_params = inspect.signature(bp_initializer).parameters

            for param in bp_initializer_params.values():
                if param.kind == inspect.Parameter.VAR_POSITIONAL:
                    start_str = "*"
                elif param.kind == inspect.Parameter.VAR_KEYWORD:
                    start_str = "**"
                else:
                    start_str = ""

                _param = start_str + param.name
                assert (
                    _param in bp.inputs.docs
                ), f"Missing doc for '{_param}' in '{bp_name}'"
