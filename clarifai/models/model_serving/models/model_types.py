# Copyright 2023 Clarifai, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Parse inference model predictions to triton inference responses
per model type.
"""

from functools import wraps
from typing import Callable, List

import numpy as np

try:
  import triton_python_backend_utils as pb_utils
except ModuleNotFoundError:
  pass


def visual_detector(func: Callable):
  """
  Visual detector type output parser.
  """

  @wraps(func)
  def parse_predictions(input_data: List[List], model: Callable):
    """
    Format predictions and return clarifai compatible output.
    """
    out_bboxes = []
    out_labels = []
    out_scores = []
    for item in input_data:
      preds = func(item, model)
      out_bboxes.append(preds.predicted_bboxes)
      out_labels.append(preds.predicted_labels)
      out_scores.append(preds.predicted_scores)

    if len(out_bboxes) < 1 or len(out_labels) < 1:
      out_tensor_bboxes = pb_utils.Tensor("predicted_bboxes", np.zeros((0, 4), dtype=np.float32))
      out_tensor_labels = pb_utils.Tensor("predicted_labels", np.zeros((0, 1), dtype=np.int32))
      out_tensor_scores = pb_utils.Tensor("predicted_scores", np.zeros((0, 1), dtype=np.float32))
    else:
      out_tensor_bboxes = pb_utils.Tensor("predicted_bboxes",
                                          np.asarray(out_bboxes, dtype=np.float32))
      out_tensor_labels = pb_utils.Tensor("predicted_labels",
                                          np.asarray(out_labels, dtype=np.int32))
      out_tensor_scores = pb_utils.Tensor("predicted_scores",
                                          np.asarray(out_scores, dtype=np.float32))

    inference_response = pb_utils.InferenceResponse(
        output_tensors=[out_tensor_bboxes, out_tensor_labels, out_tensor_scores])

    return inference_response

  return parse_predictions


def visual_classifier(func: Callable):
  """
  Visual classifier type output parser.
  """

  @wraps(func)
  def parse_predictions(input_data: List[List], model: Callable):
    """
    Format predictions and return clarifai compatible output.
    """
    raise NotImplementedError()


def text_classifier(func: Callable):
  """
  Text classifier type output parser.
  """

  @wraps(func)
  def parse_predictions(input_data: List[List], model: Callable):
    """
    Format predictions and return clarifai compatible output.
    """
    raise NotImplementedError()
