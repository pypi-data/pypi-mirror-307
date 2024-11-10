import json5
from chinu9653s.src.decorator.warning.not_used_return_value import use_return


@use_return
def load_json(file_path: str, encoding='utf-8') -> dict:
    with open(file_path, 'r', encoding=encoding) as f:
        return json5.load(f)


@use_return
def dump_json(
        file_path: str,
        data: dict,
        encoding='utf-8',
        ensure_ascii=False,
        indent=4
) -> None:
    with open(file_path, 'w', encoding=encoding) as f:
        json5.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)