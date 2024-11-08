"""LightningModule for Lightning IR.

This module contains the main module class deriving from a LightningModule_.

.. _LightningModule: https://lightning.ai/docs/pytorch/stable/common/lightning_module.html
"""

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Type

import torch
from lightning import LightningModule
from transformers import BatchEncoding

from ..data import RankBatch, SearchBatch, TrainBatch
from ..loss.loss import InBatchLossFunction, LossFunction
from .config import LightningIRConfig
from .model import LightningIRModel, LightningIROutput
from .tokenizer import LightningIRTokenizer
from .validation_utils import create_qrels_from_dicts, create_run_from_scores, evaluate_run


class LightningIRModule(LightningModule):
    """LightningIRModule base class. It dervies from a LightningModule_. LightningIRModules contain a
    LightningIRModel and a LightningIRTokenizer and implements the training, validation, and testing steps for the
    model. Derived classes must implement the forward method for the model.

    .. _LightningModule: https://lightning.ai/docs/pytorch/stable/common/lightning_module.html
    """

    def __init__(
        self,
        model_name_or_path: str | None = None,
        config: LightningIRConfig | None = None,
        model: LightningIRModel | None = None,
        loss_functions: Sequence[LossFunction | Tuple[LossFunction, float]] | None = None,
        evaluation_metrics: Sequence[str] | None = None,
    ):
        """Initializes the LightningIRModule.

        .. _ir-measures: https://ir-measur.es/en/latest/index.html

        :param model_name_or_path: Name or path of backbone model or fine-tuned Lightning IR model, defaults to None
        :type model_name_or_path: str | None, optional
        :param config: LightningIRConfig to apply when loading from backbone model, defaults to None
        :type config: LightningIRConfig | None, optional
        :param model: Already instantiated Lightning IR model, defaults to None
        :type model: LightningIRModel | None, optional
        :param loss_functions: Loss functions to apply during fine-tuning, optional loss weights can be provided per
            loss function, defaults to None
        :type loss_functions: Sequence[LossFunction | Tuple[LossFunction, float]] | None, optional
        :param evaluation_metrics: Metrics corresponding to ir-measures_ measure strings to apply during validation or
            testing, defaults to None
        :type evaluation_metrics: Sequence[str] | None, optional
        :raises ValueError: If both model and model_name_or_path are provided
        :raises ValueError: If neither model nor model_name_or_path are provided
        """
        super().__init__()
        self.save_hyperparameters()
        if model is not None and model_name_or_path is not None:
            raise ValueError("Only one of model or model_name_or_path must be provided.")
        if model is None:
            if model_name_or_path is None:
                raise ValueError("Either model or model_name_or_path must be provided.")
            model = LightningIRModel.from_pretrained(model_name_or_path, config=config)

        self.model: LightningIRModel = model
        self.config = self.model.config
        self.loss_functions: List[Tuple[LossFunction, float]] | None = None
        if loss_functions is not None:
            self.loss_functions = []
            for loss_function in loss_functions:
                if isinstance(loss_function, LossFunction):
                    self.loss_functions.append((loss_function, 1.0))
                else:
                    self.loss_functions.append(loss_function)
        self.evaluation_metrics = evaluation_metrics
        self._optimizer: torch.optim.Optimizer | None = None
        self.tokenizer = LightningIRTokenizer.from_pretrained(self.config.name_or_path, config=self.config)

    def on_train_start(self) -> None:
        """Called at the beginning of training after sanity check."""
        super().on_train_start()
        # NOTE huggingface models are in eval mode by default
        self.model = self.model.train()

    def configure_optimizers(self) -> torch.optim.Optimizer:
        """Configures the optizmizer for fine-tuning. This method is ignored when using the CLI. When using Lightning IR
        programmatically, the optimizer must be set using :meth:`set_optimizer`.

        :raises ValueError: If optimizer is not set
        :return: Optimizer
        :rtype: torch.optim.Optimizer
        """
        if self._optimizer is None:
            raise ValueError("Optimizer is not set. Call `set_optimizer`.")
        return self._optimizer

    def set_optimizer(
        self, optimizer: Type[torch.optim.Optimizer], **optimizer_kwargs: Dict[str, Any]
    ) -> "LightningIRModule":
        """Sets the optimizer for the model. Necessary for fine-tuning when not using the CLI.

        :param optimizer: Torch optimizer class
        :type optimizer: Type[torch.optim.Optimizer]
        :param optimizer_kwargs: Arguments to initialize the optimizer
        :type optimizer_kwargs: Dict[str, Any]
        :return: self
        :rtype: LightningIRModule
        """
        self._optimizer = optimizer(self.parameters(), **optimizer_kwargs)
        return self

    def score(self, queries: Sequence[str] | str, docs: Sequence[Sequence[str]] | Sequence[str]) -> LightningIROutput:
        """Computes relevance scores for queries and documents.

        :param queries: Queries to score
        :type queries: Sequence[str]
        :param docs: Documents to score
        :type docs: Sequence[Sequence[str]]
        :return: Model output
        :rtype: LightningIROutput
        """
        if isinstance(queries, str):
            queries = (queries,)
        if isinstance(docs[0], str):
            docs = (docs,)
        batch = RankBatch(queries, docs, None, None)
        with torch.no_grad():
            return self.forward(batch)

    def forward(self, batch: TrainBatch | RankBatch | SearchBatch) -> LightningIROutput:
        """Handles the forward pass of the model.

        :param batch: Batch of training or ranking data
        :type batch: TrainBatch | RankBatch
        :raises NotImplementedError: Must be implemented by derived class
        :return: Model output
        :rtype: LightningIROutput
        """
        raise NotImplementedError

    def prepare_input(
        self, queries: Sequence[str] | None, docs: Sequence[str] | None, num_docs: Sequence[int] | int | None
    ) -> Dict[str, BatchEncoding]:
        """Tokenizes queries and documents and returns the tokenized BatchEncoding_.

        :: _BatchEncoding: https://huggingface.co/transformers/main_classes/tokenizer#transformers.BatchEncoding

        :param queries: Queries to tokenize
        :type queries: Sequence[str] | None
        :param docs: Documents to tokenize
        :type docs: Sequence[str] | None
        :param num_docs: Number of documents per query, if None num_docs is inferred by `len(docs) // len(queries)`,
            defaults to None
        :type num_docs: Sequence[int] | int | None
        :return: Tokenized queries and documents, format depends on the tokenizer
        :rtype: Dict[str, BatchEncoding]
        """
        encodings = self.tokenizer.tokenize(
            queries, docs, return_tensors="pt", padding=True, truncation=True, num_docs=num_docs
        )
        for key in encodings:
            encodings[key] = encodings[key].to(self.device)
        return encodings

    def _compute_losses(self, batch: TrainBatch, output: LightningIROutput) -> List[torch.Tensor]:
        """Computes the losses for a training batch."""
        raise NotImplementedError

    def training_step(self, batch: TrainBatch, batch_idx: int) -> torch.Tensor:
        """Handles the training step for the model.

        :param batch: Batch of training data
        :type batch: TrainBatch
        :param batch_idx: Index of the batch
        :type batch_idx: int
        :raises ValueError: If no loss functions are set
        :return: Sum of the losses weighted by the loss weights
        :rtype: torch.Tensor
        """
        if self.loss_functions is None:
            raise ValueError("Loss functions are not set")
        output = self.forward(batch)
        losses = self._compute_losses(batch, output)
        total_loss = torch.tensor(0)
        assert len(losses) == len(self.loss_functions)
        for (loss_function, loss_weight), loss in zip(self.loss_functions, losses):
            self.log(loss_function.__class__.__name__, loss)
            total_loss = total_loss + loss * loss_weight
        self.log("loss", total_loss, prog_bar=True)
        return total_loss

    def validation_step(
        self, batch: TrainBatch | RankBatch | SearchBatch, batch_idx: int, dataloader_idx: int = 0
    ) -> LightningIROutput:
        """Handles the validation step for the model.

        :param batch: Batch of validation or testing data
        :type batch: TrainBatch | RankBatch | SearchBatch
        :param batch_idx: Index of the batch
        :type batch_idx: int
        :param dataloader_idx: Index of the dataloader, defaults to 0
        :type dataloader_idx: int, optional
        :return: Model output
        :rtype: LightningIROutput
        """
        output = self.forward(batch)

        if self.evaluation_metrics is None:
            return output

        dataset_id = self.get_dataset_id(dataloader_idx)
        metrics = self.validate(
            output=output,
            query_ids=batch.query_ids,
            doc_ids=batch.doc_ids,
            qrels=batch.qrels,
            targets=getattr(batch, "targets", None),
        )
        for key, value in metrics.items():
            key = f"{dataset_id}/{key}"
            self.log(key, value, batch_size=len(batch.queries))
        return output

    def test_step(
        self,
        batch: TrainBatch | RankBatch,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> LightningIROutput:
        """Handles the testing step for the model. Passes the batch to the validation step.

        :param batch: Batch of testing data
        :type batch: TrainBatch | RankBatch
        :param batch_idx: Index of the batch
        :type batch_idx: int
        :param dataloader_idx: Index of the dataloader, defaults to 0
        :type dataloader_idx: int, optional
        :return: Model output
        :rtype: LightningIROutput
        """
        return self.validation_step(batch, batch_idx, dataloader_idx)

    def get_dataset_id(self, dataloader_idx: int) -> str:
        """Gets the dataset id from the dataloader index for logging.

        .. _ir-datasets: https://ir-datasets.com/

        :param dataloader_idx: Index of the dataloader
        :type dataloader_idx: int
        :return: ir-datasets_ dataset id or dataloader index
        :rtype: str
        """
        dataset_id = str(dataloader_idx)
        datamodule = None
        try:
            datamodule = getattr(self.trainer, "datamodule", None)
            dataset_id = datamodule.inference_datasets[dataloader_idx].dataset_id
        except Exception:
            pass
        return dataset_id

    def validate(
        self,
        output: LightningIROutput,
        query_ids: Sequence[str] | None = None,
        doc_ids: Sequence[Sequence[str]] | None = None,
        qrels: Sequence[Dict[str, int]] | None = None,
        targets: torch.Tensor | None = None,
        num_docs: Sequence[int] | int | None = None,
    ) -> Dict[str, float]:
        """Validates the model output with the evaluation metrics and loss functions.

        :param output: Model output
        :type output: LightningIROutput
        :param query_ids: ids of the queries, defaults to None
        :type query_ids: Sequence[str] | None, optional
        :param doc_ids: ids of the documents, defaults to None
        :type doc_ids: Sequence[Sequence[str]] | None, optional
        :param qrels: Mappings of doc_id -> relevance for each query, defaults to None
        :type qrels: Sequence[Dict[str, int]] | None, optional
        :param targets: Target tensor used during fine-tuning, defaults to None
        :type targets: torch.Tensor | None, optional
        :param num_docs: Specifies how many documents are passed per query. If a sequence of integers, `len(num_doc)`
            should be equal to the number of queries and `sum(num_docs)` equal to the number of documents, i.e., the
            sequence contains one value per query specifying the number of documents for that query. If an integer,
            assumes an equal number of documents per query. If None, tries to infer the number of documents by dividing
            the number of documents by the number of queries, defaults to None
        :raises ValueError: If num_docs can not be parsed and query_ids are not set
        :raises ValueError: If num_docs can not be parsed and doc_ids are not set
        :return: _description_
        :rtype: Dict[str, float]
        """
        metrics: Dict[str, float] = {}
        if self.evaluation_metrics is None or output.scores is None:
            return metrics
        if query_ids is None:
            if num_docs is None:
                raise ValueError("num_docs must be set if query_ids is not set")
            query_ids = tuple(str(i) for i in range(len(num_docs)))
        if doc_ids is None:
            if num_docs is None:
                raise ValueError("num_docs must be set if doc_ids is not set")
            doc_ids = tuple(tuple(f"{i}-{j}" for j in range(docs)) for i, docs in enumerate(num_docs))
        metrics.update(self.validate_metrics(output, query_ids, doc_ids, qrels))
        metrics.update(self.validate_loss(output, query_ids, targets))
        return metrics

    def validate_metrics(
        self,
        output: LightningIROutput,
        query_ids: Sequence[str],
        doc_ids: Sequence[Sequence[str]],
        qrels: Sequence[Dict[str, int]] | None,
    ) -> Dict[str, float]:
        """Validates the model output with the evaluation metrics.

        :param output: Model output
        :type output: LightningIROutput
        :param query_ids: ids of the queries
        :type query_ids: Sequence[str]
        :param doc_ids: ids of the documents
        :type doc_ids: Sequence[Sequence[str]]
        :param qrels: Mappings of doc_id -> relevance for each query, defaults to None
        :type qrels: Sequence[Dict[str, int]] | None
        :return: Evaluation metrics
        :rtype: Dict[str, float]
        """
        metrics: Dict[str, float] = {}
        if self.evaluation_metrics is None or qrels is None:
            return metrics
        evaluation_metrics = [metric for metric in self.evaluation_metrics if metric != "loss"]
        ir_measures_qrels = create_qrels_from_dicts(qrels)
        if evaluation_metrics and qrels is not None and output.scores is not None:
            run = create_run_from_scores(query_ids, doc_ids, output.scores)
            metrics.update(evaluate_run(run, ir_measures_qrels, evaluation_metrics))
        return metrics

    def validate_loss(
        self, output: LightningIROutput, query_ids: Sequence[str], targets: torch.Tensor | None
    ) -> Dict[str, float]:
        """Validates the model output with the loss functions.

        :param output: Model output
        :type output: LightningIROutput
        :param query_ids: ids of the queries
        :type query_ids: Sequence[str]
        :param targets: Target tensor used during fine-tuning
        :type targets: torch.Tensor | None
        :return: Loss metrics
        :rtype: Dict[str, float]
        """
        metrics: Dict[str, float] = {}
        if (
            self.evaluation_metrics is None
            or "loss" not in self.evaluation_metrics
            or targets is None
            or self.loss_functions is None
            or output.scores is None
        ):
            return metrics
        output.scores = output.scores.view(len(query_ids), -1)
        for loss_function, _ in self.loss_functions:
            # NOTE skip in-batch losses because they can use a lot of memory
            if isinstance(loss_function, InBatchLossFunction):
                continue
            metrics[f"validation-{loss_function.__class__.__name__}"] = loss_function.compute_loss(
                output, targets
            ).item()
        return metrics

    def on_validation_epoch_end(self) -> None:
        """Logs the accumulated metrics for each dataloader."""
        try:
            trainer = self.trainer
        except RuntimeError:
            trainer = None
        if trainer is not None:
            metrics = trainer.callback_metrics
            accum_metrics = defaultdict(list)
            for key, value in metrics.items():
                split = key.split("/")
                if "dataloader_idx" in split[-1]:
                    accum_metrics[split[-2]].append(value)
            for key, value in accum_metrics.items():
                self.log(key, torch.stack(value).mean(), logger=False)

    def on_test_epoch_end(self) -> None:
        """Logs the accumulated metrics for each dataloader."""
        self.on_validation_epoch_end()

    def save_pretrained(self, save_path: str | Path) -> None:
        """Saves the model and tokenizer to the save path.

        :param save_path: Path to save the model and tokenizer
        :type save_path: str | Path
        """
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)

    def on_save_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """Saves the model and tokenizer to the trainer's log directory."""
        if self.trainer is not None and self.trainer.log_dir is not None:
            if self.trainer.global_rank != 0:
                return
            _step = self.trainer.global_step
            self.config.save_step = _step
            log_dir = Path(self.trainer.log_dir)
            save_path = log_dir / "huggingface_checkpoint"
            self.save_pretrained(save_path)
