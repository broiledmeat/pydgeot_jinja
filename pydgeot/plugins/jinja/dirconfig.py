from pydgeot.app.dirconfig import BaseDirConfig


class DirConfig(BaseDirConfig):
    _config_key = 'jinja'
    _default_config = {
        'source_ext': '.html',
        'build_ext': '.html'
    }

    def __init__(self, app, path):
        """
        :type app: pydgeot.app.App
        :type path: str
        """
        self.source_ext = None
        """:type: str | None"""
        self.build_ext = None
        """:type: str | None"""

        super().__init__(app, path)

    def _parse(self, config_path, config, parent):
        """
        :type config_path: str
        :type config: dict[str, Any]
        :type parent: DirConfig | None
        """
        config = config.get(DirConfig._config_key, {})

        for name in ('source_ext', 'build_ext'):
            value = config.pop(name, None)
            if value is None:
                value = self._default_config.get(name) if parent is None else getattr(parent, name)
            setattr(self, name, value)
