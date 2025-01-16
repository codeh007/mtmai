import logging
import os
import re
from pathlib import Path

from mtmai.core import coreutils
from mtmai.core.config import settings
from mtmai.mtlibs import mtutils
from mtmai.mtlibs.mtutils import command_exists, is_in_gitpod, npm_patch_version
from mtmai.mtlibs.temboio import run_tmpbo_instance1
from mtmlib.github import git_commit_push
from mtmlib.mtutils import bash

logger = logging.getLogger()


async def init_project():
    is_in_docker_build = os.getenv("X_DOCKER_BUILD")
    if is_in_docker_build:
        pass
    if not coreutils.is_in_gitpod():
        return
    docker_config = Path.home().joinpath(".docker/config.json")
    # if settings.DOCKERHUB_PASSWORD and not docker_config.exists():
    #     bash(
    #         f"(command -v docker && echo {settings.DOCKERHUB_PASSWORD} | docker login --username {
    #             settings.DOCKERHUB_USER} --password-stdin) || true"
    #     )
    # if settings.NPM_TOKEN:
    #     if is_in_gitpod():
    #         Path.home().joinpath(".npmrc").write_text(
    #             f"//registry.npmjs.org/:_authToken={settings.NPM_TOKEN}\n"
    #         )

    # from mtmlib import tunnel
    # threading.Thread(target=lambda: asyncio.run(
    #     tunnel.start_cloudflared())).start()
    # from mtmai.mtlibs.server.kasmvnc import run_kasmvnc
    # threading.Thread(target=run_kasmvnc).start()
    # 拉取第三方项目
    # await git_clone_repos(
    #     base_dir=settings.storage_dir,
    #     repo_urls=["https://github.com/Skyvern-AI/skyvern"],
    # )
    # bash("command -v playwright || ( python -m pip install playwright)")
    # bash("playwright install-deps")
    # bash("playwright install")
    # bash("vnc")


def hf_trans1_commit():
    target_dir = (
        Path(settings.storage_dir)
        .joinpath(settings.gitsrc_dir)
        .joinpath(settings.HUGGINGFACEHUB_DEFAULT_WORKSPACE)
    )
    rnd_str = mtutils.gen_orm_id_key()
    Path(target_dir).joinpath("Dockerfile").write_text(f"""
# {rnd_str}
FROM docker.io/gitgit188/tmpboai
ENV DATABASE_URL={settings.MTMAI_DATABASE_URL}
ENV LOKI_USER={settings.LOKI_USER}
ENV GRAFANA_TOKEN={settings.GRAFANA_TOKEN}
ENV LOKI_ENDPOINT={settings.LOKI_ENDPOINT}
RUN sudo apt update

""")
    Path(target_dir).joinpath("README.md").write_text(f"""---
title: Trans1
emoji: 🏢
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: other
app_port:  {settings.FRONT_PORT}
---""")
    bash(f"cd {target_dir} && git commit -am abccommit && git push")
    return {"ok": True}


def run_clean():
    bun_cache_dir = Path.home().joinpath(".bun/install/cache")
    bash(f"rm -rdf {bun_cache_dir}")

    if command_exists("pip"):
        logging.info("正在清理 pip 缓存")
        bash("pip cache dir && pip cache purge")
    if command_exists("docker"):
        logging.info("正在清理 docker 缓存")
        bash("docker system prune -f")

    if command_exists("pyenv"):
        bash("pyenv rehash")  # 可能不正确
    if is_in_gitpod():
        logger.info("删除 ~/.rustup")
        bash("rm -rdf ~/.rustup")
        logger.info("删除 ~/.rvm")
        dotrvm = Path.home().joinpath(".rvm")
        if dotrvm.exists():
            bash("rm -rdf ~/.rvm")


def docker_build_base():
    logger.info("🚀 build docker image_base")
    image_tag = f"{settings.DOCKERHUB_USER}/base"
    bash(
        f"docker build --progress=plain -t {
            image_tag} -f Dockerfile.base . && docker push {image_tag}"
    )
    logger.info("✅ build docker image_base")


async def run_deploy():
    await dp_vercel_mtmaiadmin()
    # await dp_vercel_mtmaifront()
    await run_tmpbo_instance1()
    logger.info("✅ tembo io pushed")
    hf_trans1_commit()
    logger.info("✅ hf_space_commit")
    git_commit_push()
    logger.info("✅ git_commit_push")


py_projects = [
    "mtmai",
    "mtmlib",
    "mtmtrain",
    "mtmaisdk",
]


def run_testing():
    for project in py_projects:
        if Path(f"{project}/{project}/tests").exists():
            bash(f"cd {project} && coverage run -m pytest ")
            logger.info("✅ testing ok!")


def release_py():
    # version_tag = read_tag()
    # logger.info("version tag: %s", version_tag)
    # run_testing()
    # for project in py_projects:
    #     dist_dir = Path(f"{project}/dist")
    #     if dist_dir.exists():
    #         bash(f"rm -rdf {dist_dir}")
    #     bash(f"cd pyprojects/{project} && poetry build")

    # for project in py_projects:
    #     try:
    #         bash(f"cd pyprojects/{project} && poetry publish")
    #     except Exception as e:  # noqa: BLE001
    #         logger.info("⚠ pypi %s 发布失败 %s", project, e)

    for project in py_projects:
        py_project_dir = f"pyprojects/{project}"
        mtutils.pyproject_patch_version(Path(py_project_dir).joinpath("pyproject.toml"))

    release_npm()
    # next_version = patch_git_tag_version()
    # logger.info("✅ patch_git_tag_version ok!,next version tag: %s", next_version)


def release_npm():
    npm_packages = [
        # "apps/mtmaiweb",
        "apps/mtmaiadmin",
        # "apps/mtmaifront",
        # "packages/mtmscreentocode",
        "packages/mtxuilib",
        "packages/mtmaiapi",
    ]

    bash("bun run turbo build")

    for package in npm_packages:
        npm_patch_version(package)
    NPM_TOKEN = os.getenv("NPM_TOKEN")
    print("NPM_TOKEN", NPM_TOKEN)
    if NPM_TOKEN:
        bash(
            f"export NPM_TOKEN={NPM_TOKEN} && bun run changeset publish --token {NPM_TOKEN} --no-git-tag"
        )
    else:
        raise Exception("NPM_TOKEN 未设置")

    logger.info("✅ release_npm ok!")


async def dp_cfpage():
    logger.info("🚀 正在部署 cfpage")
    from mtmlib import vercel

    pages = ["apps/mtmaiweb/src/app/(web)/layout.tsx"]
    pre_content = Path(pages[0]).read_text()
    # Check if the current runtime is nodejs before replacing
    if re.search(r'runtime\s*=\s*["\']nodejs["\']', pre_content):
        new_content = re.sub(r'runtime\s*=\s*"nodejs"', r'runtime="edge"', pre_content)
        Path(pages[0]).write_text(new_content)
        logger.info("✅ 替换layout 源码中的 runtime 为 edge")
    else:
        new_content = pre_content

    vercel.deploy_vercel(
        project_dir="apps/mtmaiweb",
        is_cfpage=True,
        project_name="mtmaiweb",
        vercel_token=settings.vercel_token,
    )

    # 恢复
    Path(pages[0]).write_text(pre_content)
    logger.info("✅ 恢复layout 源码中的 runtime 为原来的值")
    git_commit_push()


async def dp_vercel_mtmaiadmin():
    logger.info("🚀 正在部署到 vercel")
    from mtmlib import vercel

    vercel.deploy_vercel(
        project_dir="apps/mtmaiadmin",
        is_cfpage=False,
        project_name="mtmaiadmin",
        vercel_token=settings.vercel_token,
        deploy_to_vercel=True,
        build_local=False,
    )
    git_commit_push()


async def dp_vercel_mtmaifront():
    logger.info("🚀 正在部署到 vercel")
    from mtmlib import vercel

    vercel.deploy_vercel(
        project_dir="apps/mtmaifront",
        is_cfpage=False,
        project_name="mtmaifront",
        vercel_token=settings.vercel_token,
        deploy_to_vercel=True,
        build_local=False,
    )
    git_commit_push()
