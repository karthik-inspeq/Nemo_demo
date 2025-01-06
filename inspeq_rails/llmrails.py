
import asyncio
import importlib.util
import logging
import os
import re
import threading
import time
import warnings
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple, Type, Union, cast

from langchain_core.language_models import BaseLanguageModel
from langchain_core.language_models.llms import BaseLLM

from nemoguardrails.actions.llm.generation import LLMGenerationActions
from nemoguardrails.actions.llm.utils import get_colang_history
from nemoguardrails.actions.v2_x.generation import LLMGenerationActionsV2dotx
from nemoguardrails.colang import parse_colang_file
from nemoguardrails.colang.v1_0.runtime.flows import compute_context
from nemoguardrails.colang.v1_0.runtime.runtime import Runtime, RuntimeV1_0
from nemoguardrails.colang.v2_x.runtime.flows import Action, State
from nemoguardrails.colang.v2_x.runtime.runtime import RuntimeV2_x
from nemoguardrails.colang.v2_x.runtime.serialization import (
    json_to_state,
    state_to_json,
)
from nemoguardrails.context import (
    explain_info_var,
    generation_options_var,
    llm_stats_var,
    raw_llm_request,
    streaming_handler_var,
)
from nemoguardrails.embeddings.index import EmbeddingsIndex
from nemoguardrails.embeddings.providers import register_embedding_provider
from nemoguardrails.embeddings.providers.base import EmbeddingModel
from nemoguardrails.kb.kb import KnowledgeBase
from nemoguardrails.llm.providers import get_llm_provider, get_llm_provider_names
from nemoguardrails.logging.explain import ExplainInfo
from nemoguardrails.logging.processing_log import compute_generation_log
from nemoguardrails.logging.stats import LLMStats
from nemoguardrails.logging.verbose import set_verbose
from nemoguardrails.patch_asyncio import check_sync_call_from_async_loop
from nemoguardrails.rails.llm.config import EmbeddingSearchProvider, Model, RailsConfig
from nemoguardrails.rails.llm.options import (
    GenerationLog,
    GenerationOptions,
    GenerationResponse,
)
from nemoguardrails.rails.llm.utils import get_history_cache_key
from nemoguardrails.streaming import StreamingHandler
from nemoguardrails.utils import get_or_create_event_loop, new_event_dict, new_uuid
