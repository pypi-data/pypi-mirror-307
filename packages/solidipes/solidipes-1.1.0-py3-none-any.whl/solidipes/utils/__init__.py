import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submod_attrs={
        "cloud": [
            "get_cloud_info",
            "list_mounts",
            "mount_all",
            "mount_s3fs",
            "set_cloud_info",
            "unmount",
        ],
        "config": [
            "cached_metadata_filename",
            "default_ignore_patterns",
            "solidipes_dirname",
            "study_medatada_mandatory_fields",
            "study_medatada_removed_fields_upload",
            "study_metadata_filename",
            "zenodo_infos_filename",
        ],
        "utils": [
            "bcolors",
            "generate_readme",
            "get_git_repository",
            "get_git_root",
            "get_ignore",
            "get_mimes",
            "get_path_relative_to_root",
            "get_readme_path",
            "get_study_description_path",
            "get_study_log_path",
            "get_study_metadata",
            "get_study_metadata_path",
            "get_study_root_path",
            "include_metadata_description",
            "rename_file",
            "set_ignore",
            "set_mimes",
            "set_study_metadata",
            "add_completed_stage",
            "remove_completed_stage",
            "is_stage_completed",
            "get_completed_stages",
        ],
        "zenodo_utils": [
            "ZenodoException",
            "check_response",
            "download_files",
            "get_host_and_id",
        ],
    },
)

from . import solidipes_logging as logging  # noqa: E402,F401

__all__.extend(["logging"])
