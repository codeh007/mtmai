import subprocess

from setuptools import Command, setup

print(
    "setup1233333====================================================================================="
)


class PostInstallCommand(Command):
    """Post-installation for installation mode."""

    description = "Run custom post-installation tasks"
    user_options = []

    def initialize_options(self):
        print("11111111111111111111111Running post-install tasks...", flush=True)

    def finalize_options(self):
        print(
            "111111333333333333333333311111111111111111Running post-install tasks...",
            flush=True,
        )

    def run(self):
        print("Running post-install tasks...", flush=True)
        subprocess.call(["python", "mtmtrain/scripts/post_install.py"])


setup(
    name="mtmtrain",
    version="0.3.292",
    packages=["mtmtrain"],
    cmdclass={
        "install": PostInstallCommand,
    },
)
