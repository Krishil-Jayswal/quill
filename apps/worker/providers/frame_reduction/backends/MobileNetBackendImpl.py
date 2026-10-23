import torch
from PIL import Image
from ..base import FrameReductionBackend
import torchvision.transforms as T
from concurrent.futures import ThreadPoolExecutor
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
from typing import cast
from pathlib import Path

class MobileNetBackendImpl(FrameReductionBackend):
    def __init__(
        self,
        batch_size: int = 300,
        threshold: float = 0.9,
        max_worker: int = 15
    ) -> None:

        self._batch_size = batch_size
        self._threshold = threshold
        self._max_worker = max_worker

        self._device = "cuda" if torch.cuda.is_available() else "cpu"

        self._model = (
            torch.nn.Sequential(
                *list(
                    mobilenet_v3_small(
                        weights=MobileNet_V3_Small_Weights.IMAGENET1K_V1
                    ).children()
                )[:-1]
            )
            .to(self._device)
            .eval()
        )
        self._preprocess = T.Compose(
            [
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

    def _load_and_preprocess(
        self, 
        frame_path: Path
    ) -> torch.Tensor:
        image = Image.open(frame_path).convert("RGB")

        return cast(
            torch.Tensor,
            image
        )

    def reduce(
        self, 
        frames: list[Path]
    ) -> list[str]:
        selected_frames: list[str] = []
        previous_embedding = None

        with ThreadPoolExecutor(max_workers=self._max_worker) as executor:
            for i in range(0, len(frames), self._batch_size):

                batch_frames = frames[i: i+self._batch_size]                
                imgs = list(executor.map(self._load_and_preprocess, batch_frames))
                batch = torch.stack(imgs).to(self._device)

                with torch.no_grad():
                    embeddings = self._model(batch)

                    embeddings = torch.nn.functional.normalize(
                        embeddings.view(embeddings.size(0), -1), dim=-1
                    )

                if previous_embedding is not None:
                    score = torch.sum(previous_embedding * embeddings[0]).item()
                    if score < self._threshold:
                        selected_frames.append(
                            frames[i-1].name
                        )
                scores = torch.sum(
                    embeddings[:-1] * embeddings[1:],
                    dim=-1
                ).cpu()

                for j, score in enumerate(scores):
                    if score.item() < self._threshold:
                        selected_frames.append(
                            frames[i+j].name
                        )
                previous_embedding = embeddings[-1]

        selected_frames.append(frames[-1].name)
        
        return selected_frames