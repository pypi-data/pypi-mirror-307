import os

import filetype

from ..utils import get_mimes
from ..utils import solidipes_logging as logging

################################################################
logger = logging.getLogger()


################################################################
_mime_type2extensions = None


def get_mime_type2extensions():
    global _mime_type2extensions
    if _mime_type2extensions is not None:
        return _mime_type2extensions

    _mime_type2extensions = {}

    from ..plugins.discovery import loader_list

    for _cls in loader_list:
        try:
            if hasattr(_cls, "supported_extensions"):
                raise RuntimeError(f"{_cls}: should not have a member 'supported_extensions'")
            if not isinstance(_cls.supported_mime_types, dict):
                raise RuntimeError(f"need adapting class {_cls}")
            for t, exts in _cls.supported_mime_types.items():
                if isinstance(exts, str) or not isinstance(exts, list):
                    exts = [exts]

                if t not in _mime_type2extensions:
                    _mime_type2extensions[t] = []
                _mime_type2extensions[t] += exts
        except AttributeError:
            pass

    return _mime_type2extensions


################################################################
_extension2mime_types = None


def get_extension2mime_types():
    global _extension2mime_types
    if _extension2mime_types is not None:
        return _extension2mime_types

    _extension2mime_types = {}

    from ..plugins.discovery import loader_list

    for _cls in loader_list:
        try:
            for t, exts in _cls.supported_mime_types.items():
                if isinstance(exts, str) or not isinstance(exts, list):
                    exts = [exts]
                for e in exts:
                    if e not in _extension2mime_types:
                        _extension2mime_types[e] = []
                    _extension2mime_types[e].append(t)
        except AttributeError:
            pass

    return _extension2mime_types


################################################################


def get_possible_extensions(mime):
    mime = mime.split(";")[0]
    try:
        extensions = get_mime_type2extensions()[mime]
    except KeyError:
        return []
    return extensions


################################################################


def get_possible_mimes(ext):
    try:
        mimes = get_extension2mime_types()[ext]
    except KeyError:
        return []
    return mimes


################################################################


def get_extension(path):
    ext = os.path.splitext(path)[1].lower()
    if ext.startswith("."):
        ext = ext[1:]
    return ext


################################################################


def is_valid_extension(path, mime):
    mime = mime.split(";")[0]
    for possible_ext in get_possible_extensions(mime):
        # Cannot use get_extension because some possible_ext have multible
        # parts
        if path.lower().endswith(possible_ext):
            return True

    return False


################################################################


def get_mime_type(path):
    mimes_user_defined = get_mimes()
    if path in mimes_user_defined:
        return mimes_user_defined[path], ""

    ext = get_extension(path)
    if ext in get_extension2mime_types():
        return get_extension2mime_types()[ext][0], ""

    # Try to guess file type from header
    guess = filetype.guess(path)
    mime_type = guess.mime if guess is not None else None

    if mime_type is None:
        import subprocess

        p = subprocess.Popen(f"file -i -b {path}", shell=True, stdout=subprocess.PIPE)
        p.wait()
        mime_type = p.stdout.read().decode()

    try:
        mime_type, charset = mime_type.split(";")
        return mime_type, charset
    except Exception:
        pass
    return mime_type, ""


################################################################


def make_from_text(txt):
    res = {}
    for line in txt.split("\n"):
        if line == "":
            continue
        s = line.split()
        _type = s[0].strip()
        _exts = [e.strip() for e in s[1:]]
        if _type not in res:
            res[_type] = []
        res[_type] += _exts
    return res
