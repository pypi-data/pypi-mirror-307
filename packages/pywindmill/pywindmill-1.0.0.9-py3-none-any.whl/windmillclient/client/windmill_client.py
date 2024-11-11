# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/2/27 16:16
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : windmill_client.py
# @Software: PyCharm
"""
from windmillartifactv1.client.artifact_client import ArtifactClient
from windmillcomputev1.client.compute_client import ComputeClient
from windmillendpointv1.client.endpoint_monitor_client import EndpointMonitorClient
from windmillendpointv1.client.endpoint_client import EndpointClient
from windmillmodelv1.client.model_client import ModelClient
from windmilltrainingv1.client.training_client import TrainingClient
from windmillcategoryv1.client.category_client import CategoryClient
from windmillworkspacev1.client.workspace_client import WorkspaceClient
from windmillusersettingv1.client.internal_usersetting_client import InternalUsersettingClient


class WindmillClient(WorkspaceClient,
                     ArtifactClient,
                     ModelClient,
                     TrainingClient,
                     ComputeClient,
                     EndpointClient,
                     EndpointMonitorClient,
                     CategoryClient,
                     InternalUsersettingClient):
    """
    A client class for interacting with the windmill service. Initializes with default configuration.

    This client provides an interface to send requests to the BceService.
    """