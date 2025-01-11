import logging
import subprocess

logger = logging.getLogger()


class TagVersionError(Exception):
    """自定义异常类, 用于处理版本号错误"""


def exec_shell_command(*args):
    try:
        result = (
            subprocess.check_output(args, stderr=subprocess.STDOUT).decode().strip()  # noqa: S603
        )
        return result, None  # noqa: TRY300
    except subprocess.CalledProcessError as e:
        return None, e


def read_tag():
    current_tag, err = exec_shell_command("git", "describe", "--tags")
    if err:
        return current_tag, err

    current_tag_rev, _ = exec_shell_command("git", "describe", "--tags", "--abbrev=0")
    if current_tag_rev == current_tag:
        return current_tag[1:], None

    short_commit, _ = exec_shell_command("git", "rev-parse", "--short", "HEAD")
    version = parse_version(current_tag_rev[1:])
    return f"{version}-{short_commit}", None


# def patch_git_tag_version():
#     """版本号的补丁版本加1"""
#     version = read_tag_version_next()
#     new_patch_version = f"v{version['major']}.{version['minor']}.{version['patch']}"

#     # 必须 先 commit 再 create tag。 因为tag 直接跟当前状态相关。
#     bash(f"""git add -A
#         git commit -m "{new_patch_version}" --allow-empty
#         git push --follow-tags
#     """)

#     _, tag_creation_err = exec_shell_command("git", "tag", new_patch_version)
#     if tag_creation_err:
#         msg = f"创建标签失败: {tag_creation_err}"
#         raise TagVersionError(msg)

#     return new_patch_version


def parse_version(version_str):
    parts = version_str.split(".")
    return {"major": int(parts[0]), "minor": int(parts[1]), "patch": int(parts[2])}


# def read_tag_version_next():
#     """读取下一个版本号"""
#     current_tag, err = exec_shell_command("git", "describe", "--tags")

#     if err:
#         msg = f"无法读取当前标签: {err}"
#         raise TagVersionError(msg)

#     current_tag_rev, _ = exec_shell_command("git", "describe", "--tags", "--abbrev=0")
#     version = parse_version(current_tag_rev.lstrip("v"))
#     version["patch"] += 1
#     logger.info(
#         "当前tag %s, next tag: %s, current_tag_rev: %s",
#         current_tag,
#         version,
#         current_tag_rev,
#     )
#     return version
