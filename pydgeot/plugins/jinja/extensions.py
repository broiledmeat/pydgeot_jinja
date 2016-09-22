import jinja2
import jinja2.nodes
import jinja2.parser
from jinja2.ext import Extension


class SetContextExtension(Extension):
    tags = {'setcontext'}

    def __init__(self, environment):
        """
        :type environment: jinja2.Environment
        """
        super().__init__(environment)
        self.processor = None
        """:type: pydgeot.plugins.jinja.processor.JinjaProcessor | None"""

    def parse(self, parser):
        """
        :type parser: jinja2.parser.Parser
        :rtype: jinja2.nodes.Node | list[jinja2.nodes.Node]
        """
        line_no = next(parser.stream).lineno
        name = parser.stream.expect('name')

        if parser.stream.current.type != 'assign':
            return []

        next(parser.stream)
        value = parser.parse_expression()
        self.processor.app.contexts.set_context(self.processor.current_path, name.value, value.value)
        name_node = jinja2.nodes.Name(name.value, 'store', lineno=line_no)
        value_node = jinja2.nodes.Const(value.value, lineno=line_no)
        return jinja2.nodes.Assign(name_node, value_node, lineno=line_no)


def get_contexts(app):
    """
    :type: pydgeot.app.App
    :rtype: callable[str, str]
    """
    def get_contexts_(name, value):
        """
        :type name: str
        :type value: str
        :rtype: list[dict[str, Any]]
        """
        context_dicts = []
        results = app.contexts.get_contexts(name, value)
        for result in results:
            context_dict = {}
            source = app.sources.get_source(result.source)
            if source is not None:
                targets = app.sources.get_targets(result.source)
                if len(targets) == 1:
                    context_dict['url'] = '/' + app.relative_path(list(targets)[0].path)
                context_dict['urls'] = ['/' + app.relative_path(target.path) for target in targets]
                context_dict['size'] = source.size
                context_dict['modified'] = source.modified
            for context_var in app.contexts.get_contexts(source=result.source):
                context_dict[context_var.name] = context_var.value
            context_dicts.append(context_dict)
        return context_dicts
    return get_contexts_
