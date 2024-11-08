from django.conf import settings


def create_copied_files_message(file_path_pairs: list[tuple[str, str]]) -> str:
    if not file_path_pairs:
        return 'No media files were copied'

    copied_files_display = [
        f'{index + 1}. {relative_src} -> {relative_dest}\n'
        for index, (relative_src, relative_dest)
        in enumerate([
            (_get_relative_path(src), _get_relative_path(dest))
            for src, dest in file_path_pairs
        ])
    ]
    return f'Copied files:\n{"".join(copied_files_display)}'


def _get_relative_path(absolute_path: str) -> str:
    if not absolute_path.startswith(str(settings.BASE_DIR)):
        return absolute_path

    relative_path = absolute_path.replace(str(settings.BASE_DIR), '')
    return (
        relative_path[1:]
        if relative_path.startswith('/')
        else relative_path
    )
