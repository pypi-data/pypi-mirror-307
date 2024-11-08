import os
import re
from argparse import _SubParsersAction
from ..not_chalk import NotChalk

try:
    from simple_chalk import chalk  # type: ignore
except:
    chalk = NotChalk()


class Install:
    IGNORES = [
        "pkg_resources==0.0.0",  # This can't be installed.
    ]

    def __git1(self, line: str):
        """
        Git with credentials and commit hash.
        """
        match = re.search(
            r"^(\S+)\s+@\s+git\+https?\:\/\/([^@]+)@([^@]+)@([^@]+)$",
            line,
            re.I,
        )

        if match == None:
            return

        return f"pip install -U -e git+https://{match[2]}@{match[3]}@{match[4]}#egg={match[1]}"

    def __git2(self, line: str):
        """
        Git with credentials.
        """
        match = re.search(
            r"^(\S+)\s+@\s+git\+https?\:\/\/([^@]+)@([^@]+)$",
            line,
            re.I,
        )

        if match == None:
            return

        return f"pip install -U -e git+https://{match[2]}@{match[3]}#egg={match[1]}"

    def __git3(self, line: str):
        """
        Git with credentials.
        """
        match = re.search(
            r"^(\S+)\s+@\s+git\+https?\:\/\/([^@]+)$",
            line,
            re.I,
        )

        if match == None:
            return

        return f"pip install -U -e git+https://{match[3]}#egg={match[1]}"

    def __selector(self, line: str):
        if line in self.IGNORES:
            return

        value = self.__git1(line)

        if value:
            return value

        value = self.__git2(line)

        if value:
            return value

        value = self.__git3(line)

        if value:
            return value

        return f"pip install {line}"

    def __main(self, args):
        filepath = args.f

        with open(filepath, "r") as f:
            lines = f.readlines()

        for line in lines:
            cmd = self.__selector(line)

            if not cmd:
                continue

            print(line, chalk.gray.dim("="), chalk.green(cmd))

            os.system(cmd)

    def run(self, subparsers: _SubParsersAction):
        parser = subparsers.add_parser(
            "install",
            help="pip install",
        )

        parser.add_argument(
            "-f",
            type=str,
            help="filepath",
            default="requirements.txt",
            required=False,
        )

        parser.set_defaults(func=self.__main)
