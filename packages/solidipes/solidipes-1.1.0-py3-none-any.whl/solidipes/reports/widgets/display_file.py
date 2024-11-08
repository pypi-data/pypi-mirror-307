import os
import urllib.parse

import streamlit as st

################################################################
from datasize import DataSize
from solidipes_solid_mech_plugin.loaders.pyvista_mesh import PyvistaMesh
from streamlit.components.v1 import html

from solidipes.loaders.file_sequence import FileSequence
from solidipes.loaders.group import loader_list as group_loader_list
from solidipes.loaders.mime_types import get_extension2mime_types, get_mime_type2extensions, is_valid_extension
from solidipes.loaders.sequence import Sequence
from solidipes.reports.widgets.utils import FileWrapper
from solidipes.utils import get_mimes, logging, set_mimes

from .solidipes_widget import SolidipesWidget as SPW

################################################################

print = logging.invalidPrint
logger = logging.getLogger()
################################################################


class DisplayFile(SPW):
    def __init__(self, filename: str, loader_name: str, paths_str: str, options_layout=None, **kwargs):
        super().__init__(**kwargs)

        self.fname = filename
        self.f = FileWrapper(self._load(filename, loader_name, paths_str))
        self.f.state.valid = self.f.valid_loading
        title = self.get_file_title(self.f)

        st.markdown("<br>", unsafe_allow_html=True)
        with self.layout:
            st.markdown(title)
            self.show_file()

    def _load(self, filename: str, loader_name: str, paths_str: str):
        from solidipes.loaders.file import load_file

        group_loader_dict = {loader.__name__: loader for loader in group_loader_list}

        if loader_name in group_loader_dict:
            dir_path = os.path.dirname(filename)
            encoded_paths = paths_str.split(",")
            paths = [urllib.parse.unquote(p) for p in encoded_paths]
            paths = [os.path.join(dir_path, p) for p in paths]
            loader = group_loader_dict[loader_name]
            return loader(pattern=filename, paths=paths)

        else:
            return load_file(filename)

    def _get_jupyter_link(self):
        try:
            session = os.environ["SESSION_URL"]
            dir_path = os.getcwd()
            rel_path = os.path.relpath(dir_path, self.git_infos.root)
            if rel_path == ".":
                _link = f"{session}/lab/"
            else:
                _link = f"{session}/lab/tree/{rel_path}"
            return _link
        except Exception:
            raise RuntimeError("Not in a renku session")

    def show_file(self):
        e = self.f
        if not e.state.valid and e.errors:
            for err in e.errors:
                st.error(err)

        st.sidebar.button(
            "&#8629; Back to file list",
            on_click=lambda: html("<script>window.parent.history.back();</script>"),
            use_container_width=True,
            type="primary",
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        self.show_discussions(e)

        if e.state.adding_comment:
            from streamlit_ace import st_ace

            content = st_ace(
                theme="textmate",
                show_gutter=False,
                key=f"chat_input_{e.unique_identifier}",
            )
            if content:
                import re

                m = re.match(r"(\w+):(.*)", content)
                if m:
                    e.add_message(m[1], m[2].strip())
                else:
                    e.add_message("Unknown", content)
                e.state.adding_comment = False
                st.rerun()

        if isinstance(e.f, Sequence) and not (isinstance(e.f, FileSequence) and e.sequence_type == PyvistaMesh):
            sequence_switcher = st.container()
            with sequence_switcher:
                st.write(f"Sequence of {e._element_count} elements.")

                selected_element = st.slider(
                    "Current element",
                    min_value=1,
                    max_value=e._element_count,
                    step=1,
                    key="sequence_switcher_" + e.unique_identifier,
                )
                e.select_element(selected_element - 1)

        file_size = e.file_info.size

        col4.download_button(
            f"Download {os.path.basename(e.file_info.path)} ({DataSize(file_size):.2a})",
            data=open(e.file_info.path, "rb"),
            file_name=os.path.basename(e.file_info.path),
            key="download_" + e.unique_identifier,
        )
        try:
            _link = self._get_jupyter_link()
            _link += "/" + os.path.dirname(e.file_info.path)
            col2.markdown(
                f"[Edit in Jupyterlab]({_link}/)",
                unsafe_allow_html=True,
            )
            _link = self._get_filebrowser_link()
            _link += "/" + os.path.dirname(e.file_info.path)
            col2.markdown(
                f"[Edit in Filebrowser]({_link}/)",
                unsafe_allow_html=True,
            )
        except RuntimeError:
            pass

        col3.button(
            ":speech_balloon: add a comment",
            on_click=lambda: setattr(e.state, "adding_comment", True),
            key=f"add_comment_button_{e.unique_identifier}",
        )

        self.mime_type_information(e, col1, st.container())
        container_error = st.container()
        with st.container():
            try:
                with st.spinner(f"Loading {e.file_info.path}..."):
                    e.view()
            except Exception as err:
                with container_error.expander(":warning: Error trying to display file"):
                    st.exception(err)
                    logger.error("Error trying to display file")
                    logger.error(err)
                # raise err

    def show_discussions(self, e):
        from solidipes.reports.widgets.custom_widgets import SpeechBubble

        if not e.discussions:
            return

        title = "Discussions"
        if e.archived_discussions:
            title += " (archived)"

        with st.expander("Discussions", expanded=not e.archived_discussions):
            st.markdown("### :speech_balloon: Discussions")
            for author, message in e.discussions:
                SpeechBubble(author, message)
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(2)

            cols[0].button(
                "Respond",
                on_click=lambda: setattr(e.state, "adding_comment", True),
                key=f"respond_button_{e.unique_identifier}",
            )

            if e.archived_discussions:
                cols[1].button("Unarchive messages", on_click=lambda: e.archive_discussions(False))
            else:
                cols[1].button("Mark as resolved", on_click=lambda: e.archive_discussions(True))
        st.markdown("---")

    def mime_type_information(self, e, layout, main_layout):
        def format_types(x):
            if x == "Select type":
                return x
            extensions = ", ".join(get_mime_type2extensions()[x])
            x = x.strip()
            if x.endswith("/"):
                x = x[:-1]
            if extensions:
                extensions = "(" + extensions + ")"
            return f"{x} {extensions}"

        valid_ext = is_valid_extension(e.file_info.path, e.file_info.type)
        type_choice_box = layout.empty()
        type_choice = type_choice_box.container()

        if e.state.valid and valid_ext:
            ext = e.file_info.extension
            possible_types = get_extension2mime_types()[ext]
            allow_mismatch = type_choice.checkbox("Allow mismatching type/extension")
            if allow_mismatch:
                possible_types = [e for e in get_mime_type2extensions().keys()]
        else:
            possible_types = ["Select type"] + [e for e in get_mime_type2extensions().keys()]

        if e.file_info.type in possible_types:
            current_index = e.file_info.type
        else:
            current_index = "Select type"

        index = possible_types.index(current_index)
        choice = type_choice.selectbox(
            "type",
            possible_types,
            format_func=format_types,
            index=index,
            key="mime_" + e.unique_identifier,
            label_visibility="collapsed",
        )

        possible_types = [e for e in get_extension2mime_types().keys()]

        if choice != current_index:
            mimes = get_mimes()
            mimes[e.file_info.path] = choice
            set_mimes(mimes)
            e.clear_cached_metadata(["file_info", "valid_loading"])
            st.rerun()

    def get_file_title(self, e):
        path = e.file_info.path
        if isinstance(e.f, FileSequence):
            path = e.f.path

        file_title = f"{path}"

        if isinstance(e.f, FileSequence):
            file_size = e.total_size
        else:
            file_size = e.file_info.size

        file_title += f"&nbsp; &nbsp; **{e.file_info.type.strip()}/{DataSize(file_size):.2a}** "
        title = file_title

        if e.state.valid and (not e.discussions or e.archived_discussions):
            title = ":white_check_mark: &nbsp; &nbsp;" + file_title
        else:
            title = ":no_entry_sign: &nbsp; &nbsp; " + file_title

        # if e.discussions or e.state.view:
        #    title += "&nbsp; :arrow_forward: &nbsp; &nbsp; "

        if e.state.view:
            title += "&nbsp; :open_book:"

        if e.discussions:
            title += "&nbsp;:e-mail: &nbsp; :arrow_forward: **You have a message**"

        return title
