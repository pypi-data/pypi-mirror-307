from typing import Type

import pytest
import torch

from lightning_ir.base.model import LightningIROutput
from lightning_ir.bi_encoder.model import BiEncoderEmbedding, BiEncoderOutput
from lightning_ir.loss.loss import (
    ApproxMRR,
    ApproxNDCG,
    ApproxRankMSE,
    ConstantMarginMSE,
    FLOPSRegularization,
    InBatchCrossEntropy,
    InBatchLossFunction,
    KLDivergence,
    L1Regularization,
    L2Regularization,
    LocalizedContrastiveEstimation,
    RankNet,
    RegularizationLossFunction,
    ScoringLossFunction,
    SupervisedMarginMSE,
)

torch.manual_seed(42)


@pytest.fixture(scope="module")
def batch_size() -> int:
    return 4


@pytest.fixture(scope="module")
def sequence_length() -> int:
    return 8


@pytest.fixture(scope="module")
def depth() -> int:
    return 10


@pytest.fixture(scope="module")
def embedding_dim() -> int:
    return 4


@pytest.fixture(scope="module")
def output(batch_size: int, depth: int) -> LightningIROutput:
    return LightningIROutput(torch.randn((batch_size, depth), requires_grad=True))


@pytest.fixture(scope="module")
def labels(batch_size: int, depth: int) -> torch.Tensor:
    tensor = torch.randint(0, 5, (batch_size, depth))
    return tensor


@pytest.fixture(scope="module")
def embeddings(batch_size: int, sequence_length: int, embedding_dim: int) -> torch.Tensor:
    tensor = torch.randn((batch_size, sequence_length, embedding_dim), requires_grad=True)
    return tensor


@pytest.mark.parametrize(
    "LossFunc",
    [
        ApproxMRR,
        ApproxNDCG,
        ApproxRankMSE,
        ConstantMarginMSE,
        KLDivergence,
        LocalizedContrastiveEstimation,
        RankNet,
        SupervisedMarginMSE,
    ],
)
def test_loss_func(output: LightningIROutput, labels: torch.Tensor, LossFunc: Type[ScoringLossFunction]):
    loss_func = LossFunc()
    loss = loss_func.compute_loss(output, labels)
    assert loss >= 0
    assert loss.requires_grad


@pytest.mark.parametrize("InBatchLossFunc", [InBatchCrossEntropy])
def test_in_batch_loss_func(InBatchLossFunc: Type[InBatchLossFunction], output: LightningIROutput):
    loss_func = InBatchLossFunc()
    loss = loss_func.compute_loss(output)
    assert loss >= 0
    assert loss.requires_grad


@pytest.mark.parametrize("RegularizationLossFunc", [L1Regularization, L2Regularization, FLOPSRegularization])
def test_regularization_loss_func(RegularizationLossFunc: Type[RegularizationLossFunction], embeddings: torch.Tensor):
    loss_func = RegularizationLossFunc()
    loss = loss_func.compute_loss(
        BiEncoderOutput(
            None, BiEncoderEmbedding(embeddings, torch.empty(0)), BiEncoderEmbedding(embeddings, torch.empty(0))
        )
    )
    assert loss >= 0
    assert loss.requires_grad
