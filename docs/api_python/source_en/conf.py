# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import re
# import sys
# sys.path.append('..')
# sys.path.insert(0, os.path.abspath('.'))

import mindspore
# If you don't want to generate MindArmour APIs, comment this line.
import mindarmour
# If you don't want to generate MindSpore_Hub APIs, comment this line.
import mindspore_hub

# -- Project information -----------------------------------------------------

project = 'MindSpore'
copyright = '2020, MindSpore'
author = 'MindSpore'

# The full version, including alpha/beta/rc tags
release = 'master'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_markdown_tables',
    'recommonmark',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

pygments_style = 'sphinx'

autodoc_inherit_docstrings = False

autosummary_generate = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

# -- Options for Texinfo output -------------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/', '../python_objects.inv'),
    'numpy': ('https://docs.scipy.org/doc/numpy/', '../numpy_objects.inv'),
}

from typing import List, Tuple
from docutils.parsers.rst import directives
from docutils.nodes import Node

from sphinx.locale import __
from sphinx.ext.autosummary import Autosummary, posixpath, addnodes, logger, Matcher, autosummary_toc, get_import_prefixes_from_env
from sphinx.ext.autosummary import mock, StringList, ModuleType, get_documenter, ModuleAnalyzer, PycodeError, mangle_signature
from sphinx.ext.autosummary import import_by_name, extract_summary, autosummary_table, nodes, switch_source_input, rst
from sphinx.ext.autodoc.directive import DocumenterBridge, Options


class MsAutoSummary(Autosummary):
    """
    Inherited from sphinx's autosummary, added titles and a column for the generated table.
    """
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True
    option_spec = {
        'toctree': directives.unchanged,
        'nosignatures': directives.flag,
        'template': directives.unchanged,
    }

    @staticmethod
    def extract_env_summary(doc: List[str]) -> str:
        """Extract env summary from docstring."""
        env_sum = "To Be Developed"
        for i, piece in enumerate(doc):
            if piece.startswith("Supported Platforms:"):
                env_sum = doc[i+1][4:]
        return env_sum

    def run(self):
        """
        run method
        """
        self.bridge = DocumenterBridge(self.env, self.state.document.reporter,
                                       Options(), self.lineno, self.state)

        names = [x.strip().split()[0] for x in self.content
                 if x.strip() and re.search(r'^[~a-zA-Z_]', x.strip()[0])]
        items = self.get_items(names)
        teble_nodes = self.get_table(items)

        if 'toctree' in self.options:
            dirname = posixpath.dirname(self.env.docname)

            tree_prefix = self.options['toctree'].strip()
            docnames = []
            excluded = Matcher(self.config.exclude_patterns)
            for item in items:
                docname = posixpath.join(tree_prefix, item[3])
                docname = posixpath.normpath(posixpath.join(dirname, docname))
                if docname not in self.env.found_docs:
                    location = self.state_machine.get_source_and_line(self.lineno)
                    if excluded(self.env.doc2path(docname, None)):
                        msg = __('autosummary references excluded document %r. Ignored.')
                    else:
                        msg = __('autosummary: stub file not found %r. '
                                 'Check your autosummary_generate setting.')
                    logger.warning(msg, item[3], location=location)
                    continue
                docnames.append(docname)

            if docnames:
                tocnode = addnodes.toctree()
                tocnode['includefiles'] = docnames
                tocnode['entries'] = [(None, docn) for docn in docnames]
                tocnode['maxdepth'] = -1
                tocnode['glob'] = None
                teble_nodes.append(autosummary_toc('', '', tocnode))
        return teble_nodes

    def get_items(self, names: List[str]) -> List[Tuple[str, str, str, str, str]]:
        """Try to import the given names, and return a list of
        ``[(name, signature, summary_string, real_name, env_summary), ...]``.
        """
        prefixes = get_import_prefixes_from_env(self.env)
        items = []  # type: List[Tuple[str, str, str, str, str]]
        max_item_chars = 50

        for name in names:
            display_name = name
            if name.startswith('~'):
                name = name[1:]
                display_name = name.split('.')[-1]
            try:
                with mock(self.config.autosummary_mock_imports):
                    real_name, obj, parent, modname = import_by_name(name, prefixes=prefixes)
            except ImportError:
                logger.warning(__('failed to import %s'), name)
                items.append((name, '', '', name, ''))
                continue

            self.bridge.result = StringList()  # initialize for each documenter
            full_name = real_name
            if not isinstance(obj, ModuleType):
                # give explicitly separated module name, so that members
                # of inner classes can be documented
                full_name = modname + '::' + full_name[len(modname) + 1:]
            # NB. using full_name here is important, since Documenters
            #     handle module prefixes slightly differently
            doccls = get_documenter(self.env.app, obj, parent)
            documenter = doccls(self.bridge, full_name)

            if not documenter.parse_name():
                logger.warning(__('failed to parse name %s'), real_name)
                items.append((display_name, '', '', real_name, ''))
                continue
            if not documenter.import_object():
                logger.warning(__('failed to import object %s'), real_name)
                items.append((display_name, '', '', real_name, ''))
                continue
            if documenter.options.members and not documenter.check_module():
                continue

            # try to also get a source code analyzer for attribute docs
            try:
                documenter.analyzer = ModuleAnalyzer.for_module(
                    documenter.get_real_modname())
                # parse right now, to get PycodeErrors on parsing (results will
                # be cached anyway)
                documenter.analyzer.find_attr_docs()
            except PycodeError as err:
                logger.debug('[autodoc] module analyzer failed: %s', err)
                # no source file -- e.g. for builtin and C modules
                documenter.analyzer = None

            # -- Grab the signature

            try:
                sig = documenter.format_signature(show_annotation=False)
            except TypeError:
                # the documenter does not support ``show_annotation`` option
                sig = documenter.format_signature()

            if not sig:
                sig = ''
            else:
                max_chars = max(10, max_item_chars - len(display_name))
                sig = mangle_signature(sig, max_chars=max_chars)

            # -- Grab the summary

            documenter.add_content(None)
            summary = extract_summary(self.bridge.result.data[:], self.state.document)
            env_sum = self.extract_env_summary(self.bridge.result.data[:])

            items.append((display_name, sig, summary, real_name, env_sum))

        return items

    def get_table(self, items: List[Tuple[str, str, str, str, str]]) -> List[Node]:
        """Generate a proper list of table nodes for autosummary:: directive.

        *items* is a list produced by :meth:`get_items`.
        """
        table_spec = addnodes.tabular_col_spec()
        table_spec['spec'] = r'\X{1}{2}\X{1}{2}'

        table = autosummary_table('')
        real_table = nodes.table('', classes=['longtable'])
        table.append(real_table)
        group = nodes.tgroup('', cols=3)
        real_table.append(group)
        group.append(nodes.colspec('', colwidth=10))
        group.append(nodes.colspec('', colwidth=50))
        group.append(nodes.colspec('', colwidth=50))
        body = nodes.tbody('')
        group.append(body)

        def append_row(*column_texts: str) -> None:
            row = nodes.row('', color="red")
            source, line = self.state_machine.get_source_and_line()
            for text in column_texts:
                node = nodes.paragraph('')
                vl = StringList()
                vl.append(text, '%s:%d:<autosummary>' % (source, line))
                with switch_source_input(self.state, vl):
                    self.state.nested_parse(vl, 0, node)
                    try:
                        if isinstance(node[0], nodes.paragraph):
                            node = node[0]
                    except IndexError:
                        pass
                    row.append(nodes.entry('', node))
            body.append(row)

        # add table's title
        append_row("**Operator Name**", "**Description**", "**Supported Platforms**")
        for name, sig, summary, real_name, env_sum in items:
            qualifier = 'obj'
            if 'nosignatures' not in self.options:
                col1 = ':%s:`%s <%s>`\\ %s' % (qualifier, name, real_name, rst.escape(sig))
            else:
                col1 = ':%s:`%s <%s>`' % (qualifier, name, real_name)
            col2 = summary
            col3 = env_sum
            append_row(col1, col2, col3)

        return [table_spec, table]

def setup(app):
    app.add_directive('msautosummary', MsAutoSummary)
