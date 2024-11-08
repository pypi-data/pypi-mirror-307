from typing import Any, Callable, Dict, List, Optional
import json

from jinja2 import (
    Environment,
    BaseLoader,
    TemplateError,
    UndefinedError,
    StrictUndefined,
)

from .types import DocumentData, MessageData, PromptMetadata
from .messages import MessageProcessor


class DotPrompt:
    """Main dot prompt template engine implementation"""

    def __init__(self):
        self.message_processor = MessageProcessor()
        # Use StrictUndefined to force exceptions for undefined variables
        self.env = Environment(loader=BaseLoader(), undefined=StrictUndefined)
        self._register_default_filters()

    def _register_default_filters(self):
        """Register default filters and globals for the Jinja2 environment"""

        def json_filter(serializable: Any, indent: Optional[int] = None) -> str:
            return json.dumps(
                serializable,
                separators=(",", ":") if indent is None else None,
                indent=indent,
            )

        def role(role_name: str) -> str:
            return f"<<<dotprompt:role:{role_name}>>>"

        def history() -> str:
            return "<<<dotprompt:history>>>"

        def section(name: str) -> str:
            return f"<<<dotprompt:section {name}>>>"

        def media(url: str, content_type: Optional[str] = None) -> str:
            result = f"<<<dotprompt:media:url {url}"
            if content_type:
                result += f" {content_type}"
            result += ">>>"
            return result

        self.env.filters["json"] = json_filter
        self.env.globals["role"] = role
        self.env.globals["history"] = history
        self.env.globals["section"] = section
        self.env.globals["media"] = media

    def compile(self, source: str, metadata: PromptMetadata):
        """Compile template string into a render function"""
        try:
            template = self.env.from_string(source)
        except TemplateError as e:
            raise ValueError(f"Invalid template: {str(e)}")

        def render(
            input_vars: Dict[str, Any],
            context: Optional[List[DocumentData]] = None,
            history: Optional[List[MessageData]] = None,
        ) -> List[MessageData]:
            try:
                context_data = {
                    "_metadata": {"prompt": metadata, "context": context or None}
                }
                input_vars_with_context = {**input_vars, **context_data}
                rendered = template.render(**input_vars_with_context)
                return self.message_processor.to_messages(rendered, context, history)
            except UndefinedError as e:
                raise ValueError(f"Undefined variable in template: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Error rendering template: {str(e)}")

        return render

    def define_filter(self, name: str, fn: Callable):
        """Define a custom filter"""
        self.env.filters[name] = fn

    def define_global(self, name: str, value: Any):
        """Define a custom global variable"""
        self.env.globals[name] = value
