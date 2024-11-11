#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/9/10
# @Author  : zhangzhijun
# @File    : download_artifact.py
"""
import os
from argparse import ArgumentParser

from windmillclient.client.windmill_client import WindmillClient
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--artifact_name", required=False, type=str, default="")

    args, _ = parser.parse_known_args()

    return args


def run():
    """
    download artifact.
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    artifact = parse_artifact_name(args.artifact_name)
    windmill_client.download_artifact(object_name=artifact.object_name, version=artifact.version)


if __name__ == "__main__":
    run()
