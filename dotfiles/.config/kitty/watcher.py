from os import environ, getpid, makedirs, path
from contextlib import suppress
from kitty.fast_data_types import get_boss
from kitty.config import atomic_save

public_keys_dir = path.join(environ["XDG_RUNTIME_DIR"], "kitty/public-keys")
with suppress(FileExistsError):
    makedirs(public_keys_dir)
public_key_file_path = path.join(public_keys_dir, str(getpid()))
atomic_save(get_boss().encryption_public_key.encode("utf-8"), public_key_file_path)
