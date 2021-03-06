"""
Python wrapper for the `evm b11r` tool.
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Optional, Tuple


class BlockBuilder:
    """
    Block builder frontend.
    """

    binary: Path = Path("evm")

    def build(
        self,
        header: Any,
        txs: Any,
        ommers: Any,
        clique: Optional[Any] = None,
        ethash: bool = False,
        ethashMode: str = "normal",
    ) -> Tuple[str, str]:
        """
        Executes `evm b11r` with the specified arguments.
        """
        args = [
            str(self.binary),
            "b11r",
            "--input.header=stdin",
            "--input.txs=stdin",
            "--input.ommers=stdin",
            "--seal.clique=stdin",
            "--output.block=stdout",
        ]

        if ethash:
            args.append("--seal.ethash")
            args.append("--seal.ethash.mode=" + ethashMode)

        stdin = {
            "header": header,
            "txs": txs,
            "uncles": ommers,
            "clique": clique,
        }

        result = subprocess.run(
            args,
            input=str.encode(json.dumps(stdin)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0:
            raise Exception("failed to build")

        output = json.loads(result.stdout)

        if "rlp" not in output or "hash" not in output:
            Exception("malformed result")

        return (output["rlp"], output["hash"])
