import os
import subprocess
import tempfile
import uuid

from ..utils import solidipes_logging as logging
from .config import cloud_connection_timeout
from .utils import (
    get_cloud_dir_path,
    get_cloud_info,
    get_path_relative_to_root,
    get_path_relative_to_workdir,
    set_cloud_info,
)

print = logging.invalidPrint
logger = logging.getLogger()

key_names_per_mount_type = {
    "s3": ["access_key_id", "secret_access_key", "username", "password"],
    "smb": ["password"],
}


def check_process_return(process, fail_message):
    try:
        process.check_returncode()

    except subprocess.CalledProcessError as e:
        if e.stderr:
            raise RuntimeError(f"{fail_message}: {e.stderr.decode()}")
        else:
            raise RuntimeError(fail_message)


def get_existing_mount_info(path):
    path = get_path_relative_to_root(path)
    config = get_cloud_info()

    if path not in config:
        raise ValueError(f'Path "{path}" has not been set as mounting point.')

    mount_info = config[path]
    return mount_info


def get_mount_id(mount_info):
    """Create new unique mount_id if not already set."""

    if "mount_id" not in mount_info:
        mount_id = str(uuid.uuid4())
        mount_info["mount_id"] = mount_id
    else:
        mount_id = mount_info["mount_id"]

    return mount_id


def mount(path, mount_info, **kwargs):
    if os.path.ismount(path):
        raise RuntimeError(f'"{path}" is already mounted.')

    mount_type = mount_info["type"]

    if mount_type == "s3":
        mount_system = mount_info.get("system", "juicefs")

        if mount_system == "juicefs":
            mount_s3_juicefs(path, mount_info, **kwargs)

        elif mount_system == "s3fs":
            mount_s3fs(path, mount_info, **kwargs)

    elif mount_type == "ssh":
        mount_system = mount_info.get("system", "sshfs")

        if mount_system == "sshfs":
            mount_sshfs(path, mount_info, **kwargs)

    elif mount_type == "nfs":
        mount_system = mount_info.get("system", "mount")

        if mount_system == "mount":
            mount_nfs_with_mount_command(path, mount_info, **kwargs)

    elif mount_type == "smb":
        mount_system = mount_info.get("system", "mount")

        if mount_system == "mount":
            mount_smb_with_mount_command(path, mount_info, **kwargs)

    else:
        raise ValueError(f'Unknown cloud storage type "{mount_type}".')

    wait_mount(path)


def wait_mount(path):
    import time

    wait = 0
    while not os.path.ismount(path):
        time.sleep(1)
        wait += 1
        if wait > cloud_connection_timeout:
            raise RuntimeError(f'"{path}" may not be mounted.')


def mount_s3fs(path, mount_info=None):
    if mount_info is None:
        mount_info = get_existing_mount_info(path)

    # Check that keys are available
    if "access_key_id" not in mount_info or "secret_access_key" not in mount_info:
        raise RuntimeError("Mounting failed: access_key_id and secret_access_key are not available.")

    # Create directory if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Create temporary passwd file
    passwd_path = write_temp_passwd_file(mount_info["access_key_id"], mount_info["secret_access_key"])

    # Mount S3 bucket
    bucket_path = mount_info["bucket_name"]
    mount_id = get_mount_id(mount_info)
    remote_dir_name = mount_info.get("remote_dir_name", mount_id)
    if remote_dir_name != ".":
        bucket_path += f":/{remote_dir_name.rstrip('/')}"

    mount_process = subprocess.run(
        [
            "s3fs",
            bucket_path,
            path,
            "-o",
            f"passwd_file={passwd_path}",
            "-o",
            f"url={mount_info['endpoint_url']}",
            "-o",
            "nonempty",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=cloud_connection_timeout,
    )

    check_process_return(mount_process, "Mounting failed")

    # Remove temporary passwd file
    os.remove(passwd_path)


def write_temp_passwd_file(access_key_id, secret_access_key):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".passwd", delete=False) as f:
        f.write(f"{access_key_id}:{secret_access_key}\n")
        file_path = f.name

    return file_path


def mount_s3_juicefs(path, mount_info=None, **kwargs):
    if mount_info is None:
        mount_info = get_existing_mount_info(path)

    logger.debug(mount_info)
    # Create directory if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    if "database_url" in mount_info:
        mount_s3_juicefs_psql(path, mount_info, **kwargs)
    else:
        mount_s3_juicefs_sqlite3(path, mount_info, **kwargs)


def mount_s3_juicefs_sqlite3(path, mount_info=None, **kwargs):
    mount_id = get_mount_id(mount_info)
    database_filename = f"{mount_id}.db"
    database_path = os.path.join(get_cloud_dir_path(), database_filename)
    database_url = f"sqlite3://{database_path}"
    bucket_url = f"{mount_info['endpoint_url'].rstrip('/')}/{mount_info['bucket_name']}"

    os.environ["AWS_ACCESS_KEY"] = mount_info["access_key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = mount_info["secret_access_key"]

    # Create database file and remote directory if first time mount
    if not os.path.exists(database_path):
        remote_dir_name = mount_info.get("remote_dir_name", mount_id)
        format_process = subprocess.run(
            [
                "juicefs",
                "format",
                "--storage",
                "s3",
                "--bucket",
                bucket_url,
                database_url,
                remote_dir_name,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=cloud_connection_timeout,
        )
        check_process_return(format_process, "Formatting failed")

    # Mount S3 bucket
    mount_process = subprocess.run(
        [
            "juicefs",
            "mount",
            "--background",
            database_url,
            path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=cloud_connection_timeout,
    )
    check_process_return(mount_process, "Mounting failed")


def connect_to_postgres(psql_config):
    import psycopg2

    database_name = psql_config.database
    HOST = psql_config.host
    PORT = psql_config.port
    ADMIN_USERNAME = psql_config.username
    ADMIN_PASSWORD = psql_config.password

    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=ADMIN_USERNAME,
            password=ADMIN_PASSWORD,
            database=database_name,
        )
        connection.autocommit = True

    except Exception as e:
        message = f"Error connecting to Postgres: {e}"
        raise RuntimeError(message).with_traceback(e.__traceback__)

    return connection


def mount_s3_juicefs_psql(path, mount_info=None, allow_root=False, **kwargs):
    # Create mount_id (if necessary), used to find database file
    mount_id = get_mount_id(mount_info)

    logger.info(mount_info)
    if mount_info is None:
        mount_info = get_existing_mount_info(path)
    logger.info(mount_info)
    # Create directory if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Create mount_id (if necessary), used to find database file
    # mount_id = get_mount_id(mount_info)
    database_url = mount_info["database_url"]
    if not database_url.startswith("postgres://"):
        raise RuntimeError(f"Inconsistent database url: {database_url}")

    logger.debug(database_url)
    protocol, url = database_url.split("://")
    host = url.split("/")[0]
    # database_name = url.split("/")[1].split("?")[0]
    database_name = "dcsm"
    port = 5432

    if "username" in mount_info:
        username = mount_info["username"]
    elif "DCSM_USERNAME" in os.environ:
        username = os.environ["DCSM_USERNAME"]
    else:
        raise RuntimeError("Cannot find DCSM username")
    database_url = (
        protocol
        + "://"
        + username
        + "@"
        + url
        + "/"
        + database_name
        + f"?sslmode=disable&search_path=juicefs-{mount_id}"
    )
    logger.debug(url)
    logger.debug(host)
    logger.debug(database_name)

    if "password" in mount_info:
        psql_password = mount_info["password"]
    elif "DCSM_PASSWORD" in os.environ:
        psql_password = os.environ["DCSM_PASSWORD"]
    else:
        raise RuntimeError("Cannot find DCSM password")

    import argparse

    psql_config = argparse.Namespace(
        database=database_name, host=host, port=port, username=username, password=psql_password
    )
    conn = connect_to_postgres(psql_config)
    cursor = conn.cursor()
    from psycopg2 import sql

    if username == "admin":
        mount_info_query = sql.SQL("SELECT * from storage where mount_id = {mount_id}").format(
            mount_id=sql.Literal(f"juicefs-{mount_id}")
        )
        logger.debug(mount_info_query)
        cursor.execute(mount_info_query)
        db_mount_info = [i for i in cursor][0]
        logger.debug(db_mount_info)
        _, _, _, _, access_key, secret_key = db_mount_info
    else:
        mount_info_query = sql.SQL("SELECT * from {username}.user_mounts where mount_id = {mount_id}").format(
            username=sql.Identifier(username), mount_id=sql.Literal(f"juicefs-{mount_id}")
        )
        logger.debug(mount_info_query)
        cursor.execute(mount_info_query)
        db_mount_info = [i for i in cursor]
        logger.info(db_mount_info)
        db_mount_info = db_mount_info[0]
        logger.debug(db_mount_info)
        _, _, access_key, secret_key = db_mount_info

    env = {"META_PASSWORD": psql_password, "AWS_ACCESS_KEY": access_key, "AWS_SECRET_ACCESS_KEY": secret_key}
    logger.error(env)
    env.update(os.environ)

    cmd = ["juicefs", "mount", "--background"]

    if allow_root:
        cmd += [
            "-o",
            "allow_root",
        ]

    cmd += [
        database_url,
        path,
    ]

    logger.debug(cmd)
    # Mount S3 bucket
    mount_process = subprocess.run(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=cloud_connection_timeout,
    )
    check_process_return(mount_process, "Mounting failed")

    # Remove keys from database
    remove_keys_process = subprocess.run(
        [
            "juicefs",
            "config",
            database_url,
            "--access-key",
            "",
            "--secret-key",
            "",
            "--force",  # Skip keys validation
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=cloud_connection_timeout,
    )
    check_process_return(remove_keys_process, "Failed to remove keys from database")


def mount_sshfs(path, mount_info=None, headless=False):
    if mount_info is None:
        mount_info = get_existing_mount_info(path)

    # Create directory if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Mount SSH file system
    endpoint = mount_info["endpoint"]
    command = [
        "sshfs",
        endpoint,
        path,
    ]

    options = []
    if headless:
        options.append("password_stdin")
    if len(options) > 0:
        command += ["-o", ",".join(options)]

    mount_process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=cloud_connection_timeout,
        input=b"\n" if headless else None,
    )
    check_process_return(mount_process, "Mounting failed")


def mount_nfs_with_mount_command(path, mount_info=None, headless=False):
    mount_with_mount_command("nfs", path, mount_info, headless=headless)


def mount_smb_with_mount_command(path, mount_info=None, headless=False):
    mount_with_mount_command("cifs", path, mount_info, headless=headless)


def mount_with_mount_command(mount_command_type, path, mount_info, headless=False):
    if mount_info is None:
        mount_info = get_existing_mount_info(path)

    # Create directory if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Mount using "mount" command
    endpoint = mount_info["endpoint"]
    command = [
        "sudo",
        "mount",
        "-t",
        mount_command_type,
        endpoint,
        path,
    ]

    if headless:
        command.insert(1, "-S")  # read password from stdin

    options = []
    if "username" in mount_info:
        options.append(f"username={mount_info['username']}")
    if "password" in mount_info:
        options.append(f"password={mount_info['password']}")
    elif headless:
        options.append("password=''")
    if "domain" in mount_info:
        options.append(f"domain={mount_info['domain']}")
    if len(options) > 0:
        command.extend(["-o", ",".join(options)])

    mount_process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=cloud_connection_timeout,
        input=b"\n" if headless else None,
    )
    check_process_return(mount_process, "Mounting failed")


def unmount(path, headless=False):
    command = ["umount", path]

    # Check if mounting method requires sudo
    config = get_cloud_info()
    path_relative_to_root = get_path_relative_to_root(path)
    mount_system = config.get(path_relative_to_root, {}).get("system", "")
    sudo = mount_system in ["mount"]

    if sudo:
        command.insert(0, "sudo")
        if headless:
            command.insert(1, "-S")  # read password from stdin

    unmount_process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        input=b"\n" if headless else None,
    )
    check_process_return(unmount_process, "Unmounting failed")


def convert_local_to_cloud(local_path, mount_info):
    """Copy local content to cloud, unmount temp cloud and mount at final location"""

    temp_path = tempfile.mkdtemp()
    logger.info("Mounting to temporary location...")
    mount(temp_path, mount_info)

    logger.info("Copying local content to cloud...")
    rsync(local_path, temp_path)
    os.system(f"rm -rf {local_path}")

    logger.info("Unmounting temporary cloud...")
    unmount(temp_path)
    os.rmdir(temp_path)

    logger.info("Mounting cloud at final location...")
    mount(local_path, mount_info)


def convert_cloud_to_cloud(local_path, mount_info_prev, mount_info_new):
    raise NotImplementedError("Not implemented. Please convert to local first.")


def add_global_mount_info(mount_info):
    """Use mount_id to retrieve keys from user home's .solidipes directory.

    Keys already present in mount_info are not replaced.
    If one key is not found, no error is raised. Error should happen later when trying to mount.
    """

    if "mount_id" not in mount_info:
        return

    # Retrieve user info
    mount_id = mount_info["mount_id"]
    user_config = get_cloud_info(user=True)

    if mount_id not in user_config:  # and len(missing_keys) > 0:
        logger.warning(f'Mount information for "{mount_id}" not found in user\'s .solidipes directory.')
        return
    user_mount_info = user_config[mount_id].copy()

    user_mount_info.update(mount_info)
    mount_info.update(user_mount_info)
    logger.debug(mount_info)


def remove_keys_from_info(mount_info):
    """Remove keys from info and generate mount_id if necessary"""

    mount_type = mount_info["type"]
    key_names = key_names_per_mount_type.get(mount_type, None)
    if key_names is None:
        return

    # Retrieve user info
    mount_id = get_mount_id(mount_info)
    user_config = get_cloud_info(user=True)

    # Remove keys from current config, and add "removed_keys" entry
    removed_keys = {}

    for key_name in key_names:
        if key_name in mount_info:
            removed_keys[key_name] = mount_info.pop(key_name)
            if "removed_keys" not in mount_info:
                mount_info["removed_keys"] = []
            mount_info["removed_keys"].append(key_name)

    # Save keys in user config (if does not already exist)
    if mount_id not in user_config and len(removed_keys) > 0:
        user_config[mount_id] = removed_keys
        set_cloud_info(user_config, user=True)


def rsync(source_dir, target_dir, delete=False):
    args = [
        "rsync",
        "-rlv",  # recursive, links, verbose, cannot use -a with juicefs
        source_dir.rstrip("/") + "/",
        target_dir,
    ]

    if delete:
        args.append("--delete")

    rsync_process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    check_process_return(rsync_process, "Rsync failed")


def list_mounts(only_mounted=False):
    """Get config expressed relative to working directory, with mount status"""

    config = get_cloud_info()
    mounts = {}

    for local_path, mount_info in config.items():
        local_path_relative_to_workdir = get_path_relative_to_workdir(local_path)
        mount_info["mounted"] = os.path.ismount(local_path_relative_to_workdir)
        if only_mounted and not mount_info["mounted"]:
            continue
        mounts[local_path_relative_to_workdir] = mount_info

    return mounts


def mount_all(headless=False, allow_root=False):
    """Mount all mounts that are not already mounted"""

    mounts = list_mounts()
    for local_path, mount_info in mounts.items():
        if mount_info["mounted"]:
            continue

        logger.info(f"Mounting {local_path}...")
        try:
            add_global_mount_info(mount_info)
            mount(local_path, mount_info, headless=headless, allow_root=allow_root)
        except Exception as e:
            logger.error(f"Abort after raising {type(e)} {e}")
            raise e

    logger.info("Mount All: Done!")


def unmount_all(headless=False):
    """Unmount all mounted mounts"""

    mounts = list_mounts(only_mounted=True)
    for local_path in mounts.keys():
        logger.info(f"Unmounting {local_path}...")
        try:
            unmount(local_path, headless=headless)
        except Exception as e:
            logger.error(f"{e}")
