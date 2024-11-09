import typing, enum


def key_migrate(
    instance: dict[str, object], current: str, goal: str, deleting=True
) -> bool:
    if current not in instance:
        return False
    instance[goal] = instance[current]
    if deleting:
        del instance[current]
    return True


class ReplaceMode(enum.Enum):
    REPLACING = 1
    FIRST_ONLY = 2
    MERGING = 4


_merge_sentinel = object()


def key_merge(
    o: dict[str, object], *keys: str, repl_mode: ReplaceMode = ReplaceMode.FIRST_ONLY
):
    if repl_mode == ReplaceMode.FIRST_ONLY or repl_mode == ReplaceMode.REPLACING:
        result = _merge_sentinel
    elif repl_mode == ReplaceMode.MERGING:
        result = []

    last_key = _merge_sentinel
    for k in keys:
        if k in o:
            last_key = k
            value = o[k]
            if (
                repl_mode == ReplaceMode.FIRST_ONLY and result is _merge_sentinel
            ) or repl_mode == ReplaceMode.REPLACING:
                result = value
            elif repl_mode == ReplaceMode.MERGING:
                typing.cast(list[object], result).append(value)

    if repl_mode == ReplaceMode.FIRST_ONLY or repl_mode == ReplaceMode.MERGING:
        k = keys[0]
        o[k] = result
        return o
    if repl_mode == ReplaceMode.REPLACING:
        if last_key is not _merge_sentinel:
            last_key = typing.cast(str, last_key)
            o[last_key] = result
        return o
    assert False, "Missing ENUM case {}".format(repl_mode)
