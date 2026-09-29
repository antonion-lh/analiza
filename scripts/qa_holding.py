#!/usr/bin/env python3
"""QA Holding feature flag + panels."""
from __future__ import annotations

import os
import sys

from streamlit.testing.v1 import AppTest


def main() -> int:
    os.environ["HOLDING_DEV"] = "0"
    at = AppTest.from_file("streamlit_app.py", default_timeout=45)
    at.run()
    if at.exception:
        print("FAIL off", at.exception)
        return 1
    if at.segmented_control[0].options != ["Javni dosje", "Uz štrajk", "Alati"]:
        print("FAIL unexpected seg", at.segmented_control[0].options)
        return 1
    print("OK HOLDING_DEV=0 → samo ZET")

    os.environ["HOLDING_DEV"] = "1"
    at2 = AppTest.from_file("streamlit_app.py", default_timeout=45)
    at2.run()
    if at2.exception:
        print("FAIL on", at2.exception)
        return 1
    if at2.segmented_control[0].options != ["ZET", "Holding", "Grad"]:
        print("FAIL realm", at2.segmented_control[0].options)
        return 1
    print("OK HOLDING_DEV=1 → realm picker")

    at2.segmented_control[0].set_value("Holding").run()
    if at2.exception:
        print("FAIL Holding", at2.exception)
        return 1
    for p in list(at2.pills[0].options):
        at2.pills[0].set_value(p).run()
        if at2.exception:
            print("FAIL", p, at2.exception)
            return 1
        print("OK Holding", p)

    at2.segmented_control[0].set_value("Grad").run()
    for p in list(at2.pills[0].options):
        at2.pills[0].set_value(p).run()
        if at2.exception:
            print("FAIL Grad", p, at2.exception)
            return 1
        print("OK Grad", p)

    at2.segmented_control[0].set_value("ZET").run()
    if at2.exception:
        print("FAIL back ZET", at2.exception)
        return 1
    print("ALL GREEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
