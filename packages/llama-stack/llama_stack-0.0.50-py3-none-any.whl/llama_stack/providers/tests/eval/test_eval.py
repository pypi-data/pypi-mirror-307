# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.


import pytest

from llama_models.llama3.api import SamplingParams

from llama_stack.apis.eval.eval import (
    AppEvalTaskConfig,
    EvalTaskDefWithProvider,
    ModelCandidate,
)
from llama_stack.distribution.datatypes import Api
from llama_stack.providers.tests.datasetio.test_datasetio import register_dataset


# How to run this test:
#
# pytest llama_stack/providers/tests/eval/test_eval.py
#   -m "meta_reference"
#   -v -s --tb=short --disable-warnings


class Testeval:
    @pytest.mark.asyncio
    async def test_eval_tasks_list(self, eval_stack):
        # NOTE: this needs you to ensure that you are starting from a clean state
        # but so far we don't have an unregister API unfortunately, so be careful
        eval_tasks_impl = eval_stack[Api.eval_tasks]
        response = await eval_tasks_impl.list_eval_tasks()
        assert isinstance(response, list)
        assert len(response) == 0

    @pytest.mark.asyncio
    async def test_eval_evaluate_rows(self, eval_stack):
        eval_impl, eval_tasks_impl, datasetio_impl, datasets_impl = (
            eval_stack[Api.eval],
            eval_stack[Api.eval_tasks],
            eval_stack[Api.datasetio],
            eval_stack[Api.datasets],
        )
        await register_dataset(
            datasets_impl, for_generation=True, dataset_id="test_dataset_for_eval"
        )
        response = await datasets_impl.list_datasets()
        assert len(response) == 1
        rows = await datasetio_impl.get_rows_paginated(
            dataset_id="test_dataset_for_eval",
            rows_in_page=3,
        )
        assert len(rows.rows) == 3

        scoring_functions = [
            "meta-reference::llm_as_judge_8b_correctness",
            "meta-reference::equality",
        ]
        task_id = "meta-reference::app_eval"
        task_def = EvalTaskDefWithProvider(
            identifier=task_id,
            dataset_id="test_dataset_for_eval",
            scoring_functions=scoring_functions,
            provider_id="meta-reference",
        )
        await eval_tasks_impl.register_eval_task(task_def)

        response = await eval_impl.evaluate_rows(
            task_id=task_id,
            input_rows=rows.rows,
            scoring_functions=scoring_functions,
            task_config=AppEvalTaskConfig(
                eval_candidate=ModelCandidate(
                    model="Llama3.2-3B-Instruct",
                    sampling_params=SamplingParams(),
                ),
            ),
        )
        assert len(response.generations) == 3
        assert "meta-reference::llm_as_judge_8b_correctness" in response.scores
        assert "meta-reference::equality" in response.scores

    @pytest.mark.asyncio
    async def test_eval_run_eval(self, eval_stack):
        eval_impl, eval_tasks_impl, datasets_impl = (
            eval_stack[Api.eval],
            eval_stack[Api.eval_tasks],
            eval_stack[Api.datasets],
        )
        await register_dataset(
            datasets_impl, for_generation=True, dataset_id="test_dataset_for_eval"
        )

        scoring_functions = [
            "meta-reference::llm_as_judge_8b_correctness",
            "meta-reference::subset_of",
        ]

        task_id = "meta-reference::app_eval-2"
        task_def = EvalTaskDefWithProvider(
            identifier=task_id,
            dataset_id="test_dataset_for_eval",
            scoring_functions=scoring_functions,
            provider_id="meta-reference",
        )
        await eval_tasks_impl.register_eval_task(task_def)
        response = await eval_impl.run_eval(
            task_id=task_id,
            task_config=AppEvalTaskConfig(
                eval_candidate=ModelCandidate(
                    model="Llama3.2-3B-Instruct",
                    sampling_params=SamplingParams(),
                ),
            ),
        )
        assert response.job_id == "0"
        job_status = await eval_impl.job_status(task_id, response.job_id)
        assert job_status and job_status.value == "completed"
        eval_response = await eval_impl.job_result(task_id, response.job_id)

        assert eval_response is not None
        assert len(eval_response.generations) == 5
        assert "meta-reference::subset_of" in eval_response.scores
        assert "meta-reference::llm_as_judge_8b_correctness" in eval_response.scores
