# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Protocol, runtime_checkable

from llama_models.schema_utils import json_schema_type, webmethod

from llama_stack.apis.resource import Resource, ResourceType


@json_schema_type
class ShieldType(Enum):
    generic_content_shield = "generic_content_shield"
    llama_guard = "llama_guard"
    code_scanner = "code_scanner"
    prompt_guard = "prompt_guard"


@json_schema_type
class Shield(Resource):
    """A safety shield resource that can be used to check content"""

    type: Literal[ResourceType.shield.value] = ResourceType.shield.value
    shield_type: ShieldType
    params: Dict[str, Any] = {}


@runtime_checkable
class Shields(Protocol):
    @webmethod(route="/shields/list", method="GET")
    async def list_shields(self) -> List[Shield]: ...

    @webmethod(route="/shields/get", method="GET")
    async def get_shield(self, identifier: str) -> Optional[Shield]: ...

    @webmethod(route="/shields/register", method="POST")
    async def register_shield(
        self,
        shield_id: str,
        shield_type: ShieldType,
        provider_shield_id: Optional[str] = None,
        provider_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Shield: ...
