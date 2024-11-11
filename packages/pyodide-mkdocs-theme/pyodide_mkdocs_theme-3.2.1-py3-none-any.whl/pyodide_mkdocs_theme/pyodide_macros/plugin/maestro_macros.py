"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""
# pylint: disable=invalid-name, attribute-defined-outside-init, unused-argument





import re
from typing import Dict, List, Set, Tuple, Optional, Union
from collections import defaultdict
from pathlib import Path


from jinja2 import Environment
from mkdocs.exceptions import BuildError
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.plugins import event_priority

from pyodide_mkdocs_theme.pyodide_macros.html_dependencies.deps import HtmlDependencies
from pyodide_mkdocs_theme.pyodide_macros.html_dependencies.deps_class import Block, DepKind






from ..tools_and_constants import (
    # INSERTIONS_KINDS,
    HIDDEN_MERMAID_MD,
    HtmlClass,
    IdeConstants,
    PageUrl,
)
from ..parsing import eat, compress_LZW
from ..paths_utils import PathOrStr
from ..pyodide_logger import logger
from ..tools_and_constants import Prefix

from .tools.pages_and_macros_py_configs import MacroPyConfig, PageConfiguration
from .tools.macros_data import MacroData, IdeToTest, MacroDataRun
from .tools.maestro_tools import AutoCounter
from .maestro_meta import MaestroMeta
from .maestro_indent import MaestroIndent










class MaestroMacroManager(MaestroIndent):
    """
    Holds the global logic related to generation and data tracking for Ide, terminals, ...
    """


    compteur_qcms: int = AutoCounter()
    """ Number of qcm or qcs in the docs """


    generic_count: int = AutoCounter()
    """
    Number of empty terminals (per site count. Related to the terminal() macro).
    Since there are no data associated to these in the locale storage (at least,
    no _important_ data), this counter is used for everything.
    """

    ide_count: int = AutoCounter()
    """
    Number of empty IDEs (per site count. Used for IDE without python files).
    Dedicated counter, for legacy reasons. Might break users' storage sometimes, but
    this will provide more consistency with the evolution of the redactor's documentation.
    """

    _editors_ids: Set[str]
    """
    Store the ids of all the created IDEs, to enforce their uniqueness.
    """

    _editors_paths_to_ids: Dict[str,Set[int]]
    """
    Informational purpose only: store all the ID values already used for a given "base
    path without ID".
    """


    def on_config(self, config:MkDocsConfig):

        self.compteur_qcms = 0
        self.generic_count = 0
        self.ide_count     = 0
        self._editors_ids  = set()
        self._editors_paths_to_ids = defaultdict(set)

        super().on_config(config)   # pylint: disable=no-member


    def get_qcm_id(self):
        return f"{ Prefix.py_mk_qcm_id_ }{ self.compteur_qcms :0>5}"


    def is_unique_then_register(self, id_ide:str, no_id_path:str, ID:Optional[str]) -> bool :
        """
        Check if the given id has already been used.
        If so, return False. If not, register it and return True.
        """
        if id_ide in self._editors_ids:
            return False
        self._editors_ids.add(id_ide)
        if ID is not None:
            self._editors_paths_to_ids[no_id_path].add(ID)
        return True


    def get_registered_ids_for(self, no_id_path:str):
        """
        Return a sorted list giving all the IDs already used for the given "IDE source".
        """
        return sorted(self._editors_paths_to_ids[no_id_path])



    def get_hdr_and_public_contents_from(
        self, opt_path_or_content: Union[ Optional[Path], str ],
    ) -> Tuple[str,str,str]:
        """
        Extract the header code and the public content from the given file (assuming it's a
        python file or possibly None, if @path is coming from get_sibling_of_current_page).

        @returns: (header, user_content, public_tests) where header and content may be an
                  empty string.
        """
        if isinstance(opt_path_or_content,str):
            content = opt_path_or_content
        else:
            if opt_path_or_content is None or not opt_path_or_content.is_file():
                return '','',''
            content = opt_path_or_content.read_text(encoding="utf-8")

        lst = IdeConstants.hdr_pattern.split(content)
        # NOTE: If HDR tokens are present, split will return an empty string as first element, so:
        #   - len == 1 : [content]
        #   - len == 3 : ['', hdr, content]

        if len(lst) not in (1,3):
            raise BuildError(
                f"Wrong number of HDR/ENV tokens (found { len(lst)-1 }) in:\n"
                f"{opt_path_or_content!s}"
            )

        hdr     = "" if len(lst)==1 else lst[1]
        content = lst[-1].strip()

        # Make sure the old version of the pattern separating `code` from public `tests` is
        # still accepted (...or something close... :p ):
        pm_pattern = f"# ?tests(?: ?:)?|{ self.lang.tests.as_pattern.pattern }"
        tests_cuts = re.split(pm_pattern, content, flags=re.I)

        if len(tests_cuts)>2:
            pattern = self.lang.tests.as_pattern.pattern
            raise BuildError(
                f'Found more than one time the token {pattern!r} (case insensitive) in:'
                f"\n{ opt_path_or_content }"
            )

        tests_cuts.append('')       # ensure always at least 2 elements
        user_code, public_tests, *_ = map(str.strip, tests_cuts)

        return hdr, user_code, public_tests



    def get_sibling_of_current_page(
        self, partial_path: PathOrStr, *, tail:str="", rel_to_docs:bool=False
    ):
        """
        @env: BaseMaestro
        @docs_dir
        Extract the current page from the env, then build a path name toward a file using
        the @partial_path (string name of slash separated string, or relative Path), starting
        from the same parent directory.
        If @tail is given, it is added to the name of the last segment of of the built path.
        If @rel_to_docs is False, the result will be an absolute path of the file at documentation
        building time. If @rel_to_docs is True, the returned path will be rooted at the docs_dir,
        meaning the path will also be the valid relative path of the file on the built site.

        If @partial_path is an empty string or a Path without name, return None
        """
        path: Path = self.docs_dir_path / self.page.file.src_uri
        out_path = self._get_sibling(path, partial_path, tail)
        if out_path and rel_to_docs:
            return out_path.relative_to(self.docs_dir_path)
        return out_path


    @staticmethod
    def _get_sibling(src:Path, rel:PathOrStr, tail:str="") -> Optional[Path] :
        """ Build a sibling of the given path file, replacing the current Path.name
            with the given @rel element (path or str).
            If @tail is given, it is added to the name of the built path.
            Return None if:
                - @src has no explicit parent (using '.' on the cwd will cause troubles)
                - @rel is an empty string or is a Path without name property (empty IDE)
        """
        if not src.name or not rel or isinstance(rel,Path) and not rel.name:
            return None

        possible_paths = [
            src.parent / rel,
            src.parent / 'scripts' / src.stem / rel
        ]
        for path in possible_paths:
            if tail:
                path = path.with_name( path.stem + tail )
            if path.is_file():
                return path

        return None












class MaestroMacros(MaestroMacroManager):
    """ Holds the global logic related data management for IDE-like elements. """


    _scripts_or_link_tags_to_insert: Dict[DepKind,str]
    """
    UI formatting scripts to insert only in pages containing IDEs, terminals, ...
    Note that the values are all the scripts and/or css tags needed for the key kind,
    all joined together already, as a template string expecting the variable `to_base`.

    Defined once per build, through a call to register_js_and_css_tags in on_config.
    """

    _pages_configs: Dict[PageUrl, 'PageConfiguration']
    """
    Represent the configurations of every IDE in every Page of the documentation.
    """

    _pages_with_ides_to_test: Dict[PageUrl, List[IdeToTest]]
    """
    Holds all the pages url of pages containing IDE that will be tested, with the related
    test config.
    """                     # (note: used on CodEx)

    all_macros_data: List[MacroData]
    """
    Contains all the objects tracking the various states of the PMT macros calls.
    """


    def on_config(self, config:MkDocsConfig):

        self.all_macros_data = []
        self._pages_configs  = defaultdict(lambda: PageConfiguration(self))
        self._scripts_or_link_tags_to_insert = {}
        self._pages_with_ides_to_test = defaultdict(list)

        super().on_config(config)   # pylint: disable=no-member



    @MaestroMeta.meta_config_swap
    def on_page_markdown(
        self,
        markdown:str,
        page:Page,
        config:MkDocsConfig,
        site_navigation=None,
        **kwargs
    ):
        """
        Automatically add the mermaid code (hidden figure) at the end of the page, if it got
        marked as needing some.
        """
        markdown_out = super().on_page_markdown(
            markdown, page, config, site_navigation=site_navigation, **kwargs
        )
        if self.does_current_page_need(DepKind.mermaid):
            markdown_out += HIDDEN_MERMAID_MD
            # WARNING: The check above actually ensure that ALL the pages of the documentation
            #      will end up being present in self._pages_config, even if they don't contain
            #      any macro call. If ever this part of the logic gets removed, the implementation
            #      in `HtmlDependencies` of `build_templates` and `render_tags_for` will become
            #      wrong... (KeyError raised in `render_tags_for`).

        return markdown_out




    def on_env(self, env:Environment, config:MkDocsConfig, files:Files):
        from ..macros.ide_run_macro import AutoRun      # pylint: disable=C0415

        logger.debug("Build the mapping {page.url: list of MacroData}.")
        self._pages_with_run_macro: Dict[str,List[MacroDataRun]] = defaultdict(list)
        for m in self.all_macros_data:
            if m.macro == AutoRun.MACRO_NAME:
                self._pages_with_run_macro[m.page_url].append(m)




    @MaestroMeta.meta_config_swap
    @event_priority(9001)
    def on_page_context(self, _ctx, page:Page, *, config:MkDocsConfig, nav:Navigation):
        """
        Spot pages in which corrections and remarks have been inserted, and encrypt them.

        This hook uses high priority because the html content must be modified before the
        search plugin starts indexing stuff in the related plugin (which precisely happens
        in the on_page_context hook).
        """
        # pylint: disable=pointless-string-statement

        if self.is_page_with_something_to_insert(page):

            # `self._page` update needed so that self.page reflects the correct page through this
            # event (the original MacrosPlugin isn't managing it for us anymore, at this point).
            self._page = page       # Before logging because self.file_location() uses it...)

            logger.debug(f"Add scripts + encrypt solutions and remarks in { self.file_location() }")

            page_config = self.get_page_config_and_set_base_url()
            chunks      = []

            if page_config.has_need(DepKind.ides_test):
                from ..macros.ide_tester import IdeTester   # pylint: disable=import-outside-toplevel

                logger.info("Create the tests for all the IDEs in the test page.")
                tests_content = IdeTester.build_html_for_tester(self, self._pages_with_ides_to_test)
                chunks = [page.content, tests_content]

            elif page_config.has_need(DepKind.pyodide):
                self.chunk_and_encrypt_solutions_and_rems(page.content, chunks)

            else:
                chunks.append(page.content)

            chunks.extend(
                f'<span id="{ run_macro.storage_id }" class="{ HtmlClass.py_mk_hidden }"></span>'
                for run_macro in self._pages_with_run_macro[page.url]
            )

            script_tag = page_config.build_page_script_tag_with_ides_configs_and_mermaid_status()
            chunks.append(script_tag)

            content_tags = HtmlDependencies.render_tags_for(Block.content, page, self)
            chunks.append(content_tags)

            page.content = ''.join(chunks)


        # If ever the MacrosPlugin gets the super method implemented:
        if hasattr(super(), 'on_page_context'):
            super().on_page_context(_ctx, page, config=config, nav=nav)






    #-----------------------------------------------------------------------
    #     Manage scripts and css to include only in some specific pages
    #-----------------------------------------------------------------------



    def set_current_page_insertion_needs(self, *kind:DepKind):
        """ Mark a page url as needing some specific kinds of scripts (depending on the macro
            triggering the call). """
        self._pages_configs[self.page.url].needs.update(kind)



    def does_current_page_need(self, kind:DepKind):
        """ Check if the current page needs this kind of data. """
        return kind in self._pages_configs[self.page.url].needs



    def archive_ide_to_tests(self, conf:IdeToTest):
        """
        Store data for an IDE in the current Page. @prop must be a property of the
        MacroPyConfig class.
        """
        self._pages_with_ides_to_test[self.page.url].append(conf)



    def set_current_page_js_macro_config(self, editor_name:str, conf:MacroPyConfig):
        """
        Store data for an IDE in the current Page. @prop must be a property of the
        MacroPyConfig class.
        """
        self._pages_configs[self.page.url][editor_name] = conf


    def is_page_with_something_to_insert(self, page:Optional[Page]=None):
        """
        Check if the current page is marked as holding at least one thing needing a script,
        insertion or ide content.
        If @page is given, use this instance instead of the one from self.page (useful for hooks)
        """
        url = page.url if page else self.page.url
        return url in self._pages_configs


    def get_page_config_and_set_base_url(self, page:Optional[Page]=None):

        page = page or self.page
        url  = page.url

        self.base_url = self.level_up_from_current_page(url)
        page_config   = self._pages_configs[url]
        return page_config




    #--------------------------------------------------------------------
    #                    Solution & remarks encryption
    #--------------------------------------------------------------------



    def chunk_and_encrypt_solutions_and_rems(self, html:str, chunks:List[str]):
        """
        Assuming it's known that the @page holds corrections and/or remarks:
            - Search for the encryption tokens
            - Encrypt the content in between two consecutive tokens in the page html content.
            - Once done for the whole page, replace the page content with the updated version.
        Encryption tokens are removed on the way.
        """
        if not self.encrypt_corrections_and_rems:
            chunks.append(html)
            return

        entering = 0
        while entering < len(html):
            i,j = eat(html, IdeConstants.encryption_token, start=entering, skip_error=True)
            i,j = self._cleanup_p_tags_around_encryption_tokens(html, i, j)

            chunks.append( html[entering:i] )

            if i==len(html):
                break

            ii,entering = eat(html, IdeConstants.encryption_token, start=j)     # raise if not found
            ii,entering = self._cleanup_p_tags_around_encryption_tokens(html, ii, entering)

            solution_and_rem = html[j:ii].strip()
            encrypted_content = compress_LZW(solution_and_rem, self)
            chunks.append(encrypted_content)



    def _cleanup_p_tags_around_encryption_tokens(self, html:str, i:int, j:int):
        """
        mkdocs automatically surrounds the encryption token with <p> tag, so they must be removed.
        Note: Including the tags in the ENCRYPTION_TOKEN doesn't change the problem: you'd just
              get another <p> tag surrounding the token... sometimes... x/
        """
        while html[i-3:i]=='<p>' and html[j:j+4]=='</p>':
            i -= 3
            j += 4
        return i,j
