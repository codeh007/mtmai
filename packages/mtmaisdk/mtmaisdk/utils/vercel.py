import logging

from mtmlib import mtutils
from mtmlib.mtutils import bash

logger = logging.getLogger()


def deploy_vercel(
    *,
    project_dir: str,
    is_cfpage: bool = False,
    build_local: bool = True,
    # with_gomtm: bool,
    project_name: str,
    vercel_token: str,
    deploy_to_vercel: bool = False,
):
    logger.info("deploy_verce %s, %s", project_dir, project_name)
    if not mtutils.command_exists("vercel"):
        bash("npm install -g vercel@latest")
    bash(
        f'cd {project_dir} && vercel link --project={project_name} --yes --token="{vercel_token}" '
    )
    bash(f'cd {project_dir} && vercel pull --yes --token="{vercel_token}"')
    if build_local:
        bash(f"cd {project_dir} && vercel build --prod --local-config vercel.json")
    if is_cfpage:
        bash(f"cd {project_dir} && bunx @cloudflare/next-on-pages -s")
        bash(
            f'cd {project_dir} && bunx wrangler pages deploy .vercel/output/static --project-name="{project_name}"'
        )
    if deploy_to_vercel:
        bash(
            f'cd {project_dir} && vercel deploy --yes --local-config vercel.json --prod --token="{vercel_token}"'
        )
