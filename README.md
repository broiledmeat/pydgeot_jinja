# Jinja2 Support for Pydgeot
Add support for [Jinja2](https://github.com/mitsuhiko/jinja2) templates to
[Pydgeot](http://www.github.com/broiledmeat/pydgeot). Any changes to extended or included templates will propagate
regeneration to the file that used those templates. Templates may set context variables that are accessible from
other templates, which will also affect the regeneration.

### Features
- Standard [Jinja2](https://github.com/mitsuhiko/jinja2) templating.
- Globally available context variables.
- Regenerate files dependent on other templates or context variables.

### Requirements
- Python 3.*
- [Pydgeot](http://www.github.com/broiledmeat/pydgeot)
- [Jinja2](https://github.com/mitsuhiko/jinja2)

### Installation
Via pip:
```bash
pip install pydgeot_jinja
```

Or via source:
```bash
git clone https://github.com/broiledmeat/pydgeot_jinja.git pydgeot_jinja
cd pydgeot_jinja
python setup.py install
```

### Configuration
Add `jinja` to your pydgeot.conf `plugins` list to enable the plugin. Then add `jinja` to the `processors` list in
pydgeot.conf, or nested .pydgeot.conf's, to use the file processor. Options are, also, placed under a `jinja` key.
- `source_ext` Extension of source files to build. _Default: .html_
- `build_ext` Extension of built files. _Default: .html_
```json
{
  "plugins": ["jinja"],
  "processors": ["jinja"],
  "jinja" {
    "source_ext": ".jinja"
  }
}
```

### Usage
The Jinja2 plugin will process any `.html` (or `source_ext` extension specified in pydgeot.conf) file as a Jinja2
template.

A page may be marked as template only by setting the `template_only` variable to `True`. This will cause the file to not
be generated, but any changes will still cause dependent files to be generated.

#### Context Variables
Setting a context variable makes it available to the file it was created in, and to any other template file.
`{% setcontext name="value" }%`

Context variables can be accessed in the setting file (or extended and included files,) in the same way as if it had
been created with the standard Jinja `set`.

Context variables may be created with the same names across multiple sources, so global access is done iteratively.
`getcontexts(name, "value")` will retrieve a list of files that have set a context variable matching the name and value.
The value may be a [glob pattern](https://github.com/broiledmeat/pydgeot#glob-patterns).

For example, `{% for page in getcontexts("fullname", "test.*") %}` would find any file with context variables named
"fullname" with values starting with "test.", then grab all of that files context variables and set them as properties
of `page`.
