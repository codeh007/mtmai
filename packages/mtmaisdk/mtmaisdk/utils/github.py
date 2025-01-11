import json
import logging
import os
import random
import re
import shutil
import subprocess
from os import path
from pathlib import Path
from urllib.parse import urlparse

import httpx
import requests

from mtmlib.mtutils import bash

logger = logging.getLogger()


def gitParseOwnerRepo(giturl: str):
    """再git url 中识别出owner 和 repo 名称"""
    parsed = urlparse(giturl)
    path = parsed.path
    m = re.match(r"/(.*)/(.*).git(.*)", path, flags=0)
    if m:
        owner = m.groups()[0]
        repo = m.groups()[1]
        file = m.groups()[2]
        return (owner, repo, file)
    return None


def gitup(giturl: str):
    """
    给定git 网址，下载到指定路径并根据规则运行相关代码。
    """
    parsed = urlparse(giturl)
    owner, repo, file = gitParseOwnerRepo(giturl)

    clone_to = path.join(GITCLONE_BASEDIR, repo)
    gitclone(owner, repo, parsed.username, clone_to)
    if not file:
        logger.info("no entry script,skip launch")
    if file:
        file = file.lstrip("/")
        scriptFile = path.join(clone_to, file)
        if not Path(scriptFile).exists():
            logger.warning(f"入口文件不存在{scriptFile}")

        logpath = path.join(clone_to, GITUP_LOGFILE)
        Path(scriptFile).chmod(0o700)
        logger.info(f"""========================================
[ ✅ gitup]
entry script\t: {scriptFile}
logs\t: tail -f {logpath}
========================================
""")
        logfile = open(logpath, "w")
        subprocess.Popen(
            [scriptFile],
            stdout=logfile,  # 输出重定向到文件。
            stderr=logfile,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            cwd=clone_to,
            shell=False,
        )
    return logpath


def gitCopy(giturl: str, dest_dir: str):
    """
    以类似cp命令的方式，复制仓库中的文件到指定目录，
    为什么不直接用git clone? 因为如果目前文件夹非空，会运行失败
    """
    parsed = urlparse(giturl)
    owner, repo, file = gitParseOwnerRepo(giturl)
    tmp_dir = "/tmp/gitclone_" + str(random.randint(0, 999999999))
    clone_to = path.join(tmp_dir, repo)
    gitclone(owner, repo, parsed.username, clone_to)
    logger.info(f"copytree from `{clone_to}` to `{dest_dir}` ")
    shutil.copytree(clone_to, dest_dir, dirs_exist_ok=True)


def dockerdev_git(giturl: str):
    """在容器内clone 源码并启动为基于容器的开发环境"""
    parsed = urlparse(giturl)
    owner, repo, file = gitParseOwnerRepo(giturl)
    clone_to = path.join(repo)
    logger.info(f"clone 到 {clone_to}")
    gitclone(owner, repo, parsed.username, clone_to)


def gitclone(owner, repo, token, dest_dir):
    """克隆一个github仓库"""
    _token = token or os.environ.get("GITTOKEN")

    bash(f"rm -rdf {dest_dir}")
    cmd = (
        f"git clone --depth=1 https://{_token}@github.com/{owner}/{repo}.git {dest_dir}"
    )
    logger.info(f"cmd {cmd}")
    cp = bash(cmd)
    if cp.returncode != 0:
        logger.info(f"clone 失败 {owner}, {repo},{dest_dir}")
        logger.info(cp.stderr)
    else:
        logger.info("clone 成功")


def deploy_repo(repo_url):
    """更新源码，目前配合github hook 的功能，暂时写死
    TODO: 目前仅支持ssh的方式拉取源码。要更新到支持github token
    """
    # os.system('curl -q --insecure https://116.202.120.181/api/ip')
    # os.system('curl -q http://google.com')
    url = urlparse(repo_url)
    owner = url.path.split("/")[1]
    repo_name = url.path.split("/")[2].rstrip(".git")

    targetdir = "/deploy/" + owner + "/" + repo_name
    if os.path.exists(targetdir):
        logger.info("文件夹 %s 存在，拉取github" % targetdir)
        os.system("cd %s && git reset --hard origin/main && git pull" % targetdir)
    else:
        parent_dir = Path(targetdir).parent
        Path(parent_dir).mkdir(mode=0o777, parents=True, exist_ok=True)
        logger.info("部署路径 %s" % targetdir)
        os.system(f"git clone {repo_url} {targetdir}")
    # 运行
    is_entry_exists = False
    for entry_file in DEFAULT_ENTRY_SCRIPTS.split(" "):
        fullpath = os.path.join(targetdir, entry_file)
        logger.info(f"搜索入口脚本；{fullpath}")
        if os.path.exists(fullpath):
            is_entry_exists = True
            logger.info("执行脚本 %s " % targetdir)
            proc = subprocess.Popen(["sh", "-c", fullpath], cwd=targetdir)
            break
    if not is_entry_exists:
        logger.warning(f"仓库入库脚本文件'{DEFAULT_ENTRY_SCRIPTS}'不存在，跳过启动")


class GHRepo:
    """对一个github repo进行操作"""

    def __init__(
        self, url: str = None, token: str = None, owner: str = None, repo: str = None
    ):
        if url:
            repourl = urlparse(url)
            self.token = repourl.password
            self.owner = repourl.username
            pathitems = repourl.path.split("/")
            self.repo = pathitems[1]
            print("REPO")
            print(
                f"根据网址否则ghrepo， token {self.token}, owner:{self.owner}, repo:{self.repo}"
            )
        else:
            self.token = token
            self.owner = owner
            self.repo = repo

        self.http_headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
        }

    def repoInfo(self):
        """获取当前仓库的信息"""
        r = requests.get(
            f"https://api.github.com/orgs/{self.owner}/repos",
            data=payload,
            headers=self.http_headers,
        )
        # text = r.text
        print("DEBUG 当前仓库信息", json.loads(r.text))

    def _put(apiurl, payload):
        """发出put请求"""
        return requests.put(
            f"https://api.github.com/orgs/{self.owner}/repos",
            data=payload,
            headers=self.http_headers,
        )

    # 将文件转换为base64编码，上传文件必须将文件以base64格式上传

    def delete_file(self, file_path, sha, message="api delete"):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}"
        headers = {"Authorization": "token " + self.token}
        payload = json.dumps(
            {
                "sha": sha,
                "message": message,
            }
        )
        resp = requests.delete(url=url, data=payload, headers=headers)
        json_data = resp.json()
        # print("删除结果：")
        # print(json_data)
        message = json_data.get("message")
        if message == "Not Found":
            return None
        return json_data

    def get_file_content(self, file_path: str):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}"
        headers = {"Authorization": "token " + self.token}
        resp = requests.get(url=url, data=None, headers=headers)
        return resp.json()

    def _write_content(self, file_path: str, file_data: bytes):
        req = requests.put(
            url=f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}",
            data=json.dumps(
                {
                    "message": "message",
                    "committer": {"name": "[user]", "email": "user@163.com"},
                    "content": file_base64(file_data),
                }
            ),
            headers={"Authorization": "token " + self.token},
        )
        req.encoding = "utf-8"
        return json.loads(req.text)

    # 上传文件（单个）
    def write_file_content(self, file_path: str, file_data: bytes, skipExists=False):
        """以覆盖的方式写入文件到github仓库"""
        contentJson = self.get_file_content(file_path)
        sha = contentJson.get("sha")
        if sha and not skipExists:
            print(f"删除旧文件：{file_path}")
            self.delete_file(file_path, sha=sha)
            self._write_content(file_path, file_data)
        elif sha and skipExists:
            print(f"跳过{file_path}")
        else:
            self._write_content(file_path, file_data)

    def write_file_content_mutil(self, files=[]):
        """以覆盖的方式写入文件到github仓库"""
        for file in files:
            print(f"上传：{file}")
            self.write_file_content(file["path"], file["content"])

        # print(json.dumps(re_data))
        # print(f"https://cdn.jsdelivr.net/gh/{self.owner}/{self.repo}/{file_path}")


def git_commit_push(commit_msg: str = "auto-commit"):
    bash(f"""git add -A
	git commit -m "{commit_msg}" --allow-empty
	# git push origin main --force
    git push --follow-tags
""")


##########################################################################################################
# 新版代码开始
async def get_github_user_data(access_token: str):
    # 使用 access token 获取用户信息
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()
        return user_data


async def git_clone_repos(*, base_dir: str, repo_urls: list[str], force: bool = False):
    # 将多个指定的 git 开源项目 clone 到指定的目类下
    # all_git_srcs = ["https://github.com/Skyvern-AI/skyvern"]
    for gitsrc in repo_urls:
        uri = urlparse(gitsrc)
        sub_dir = uri.path.split("/")[-1]
        target_dir = Path(base_dir).joinpath(sub_dir)
        if Path(target_dir).exists() and not force:
            logger.info("⚠ %s 已存在", target_dir)
        else:
            if Path(target_dir).exists():
                logger.info("⚠ %s 已存在，删除", target_dir)
                shutil.rmtree(target_dir)
            cmd = f"git clone --depth=1 {gitsrc} {target_dir}"
            bash(cmd)
