import os
import jinja2
import jinja2.environment
import jinja2.meta
import jinja2.nodes
from pydgeot.processors import register, Processor


@register(name='jinja')
class JinjaProcessor(Processor):
    """
    Compile a Jinja (http://jinja.pocoo.org) template source file in to the build directory.

    Context variables can be set using the 'setcontext' tag. This also works as Jinja's built in 'set' tag.
    File paths that have set context variables can be retrieved with 'getcontexts("name", "value")'.
    To mark a file as only being used as a template (no file will be generated for it,) use Jinja's built in 'set'
    to set the 'template_only' variable to True.
    """

    def __init__(self, app):
        from .extensions import SetContextExtension, get_contexts

        super().__init__(app)

        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.app.source_root),
            extensions=[SetContextExtension])

        # Prepare template extensions
        for extension in self._env.extensions.values():
            extension.processor = self

        # Add template functions
        self._env.globals['getcontexts'] = get_contexts(self.app)

        # Set during prepare(), so extensions can get the processing file path
        self.current_path = None
        """:type: str | None"""
        self._generate_paths = {}
        """:type: dict[str, jinja2.nodes.Template]"""

    def can_process(self, path):
        """
        :type path: str
        :rtype: bool
        """
        from .dirconfig import DirConfig
        config = DirConfig.get(self.app, path)
        return path.endswith(config.source_ext)

    def prepare(self, path):
        """
        :type path: str
        """
        self.current_path = path
        self.app.contexts.clear_dependencies(path)
        self.app.contexts.remove_context(path)

        with open(path) as fh:
            ast = self._env.parse(fh.read())

        self.app.sources.set_targets(path, [self.target_path(path)])
        self.app.sources.set_dependencies(path, [self.app.source_path(t)
                                                 for t in jinja2.meta.find_referenced_templates(ast)])

        # Add new context dependencies (populated from get_contexts)
        for name, value in self._get_context_requests(ast):
            self.app.contexts.add_dependency(path, name, value)

        consts = self._get_const_vars(ast)
        template_only = consts.get('template_only', False)

        # Add this to the list of paths to be generated if it's not template only
        if not template_only:
            self._generate_paths[path] = ast

    def generate(self, path):
        """
        :type path: str
        """
        if path not in self._generate_paths:
            return

        target_path = self.target_path(path)
        template = jinja2.environment.Template.from_code(self._env, self._env.compile(self._generate_paths[path]),
                                                         self._env.make_globals(None))

        context_dict = {}
        source = self.app.sources.get_source(path)
        if source is not None:
            targets = self.app.sources.get_targets(path)
            if len(targets) == 1:
                context_dict['url'] = '/' + self.app.relative_path(list(targets)[0].path)
            context_dict['urls'] = ['/' + self.app.relative_path(target.path) for target in targets]
            context_dict['size'] = source.size
            context_dict['modified'] = source.modified

        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as fh:
            fh.write(template.render(**context_dict))
        del self._generate_paths[path]

    def target_path(self, path):
        """
        :type path: str
        :rtype: str
        """
        from .dirconfig import DirConfig
        config = DirConfig.get(self.app, path)
        path = path[:-len(config.source_ext)] + config.build_ext
        return self.app.target_path(path)

    @staticmethod
    def _get_const_vars(template):
        """
        :type template: jinja2.nodes.Template
        :rtype: dict[str, Any]
        """
        const_vars = {}
        for node in template.find_all((jinja2.nodes.Assign,)):
            if isinstance(node.target, jinja2.nodes.Name) and isinstance(node.node, jinja2.nodes.Const):
                # noinspection PyUnresolvedReferences
                const_vars[node.target.name] = node.node.value
        return const_vars

    @staticmethod
    def _get_context_requests(template):
        """
        :type template: jinja2.nodes.Template
        :rtype: list[tuple[str, str]]
        """
        context_requests = []
        for node in template.find_all((jinja2.nodes.Call,)):
            if isinstance(node.node, jinja2.nodes.Name) and len(node.args) == 2 and \
                    isinstance(node.args[0], jinja2.nodes.Const) and isinstance(node.args[1], jinja2.nodes.Const):
                context_requests.append((node.args[0].value, node.args[1].value))
        return context_requests
