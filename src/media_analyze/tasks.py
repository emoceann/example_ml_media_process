import asyncio

import cv2
import numpy as np
from aiofiles import os as asyncos
from onnxruntime import InferenceSession
from taskiq import TaskiqDepends, Context

from src.core.process_model.config import get_model, get_labels
from src.core.tasks.broker import get_broker
from src.core.utils.prepare_image import pre_process_edgetpu
from src.core.utils.video_to_frames import get_video_frames
from src.media_analyze.repositories.media_data import MediaDataRepo
from src.media_analyze.serializers.processed_media_serializer import MediaSerializer

broker = get_broker()


@broker.task
async def process_image(
        image_path: str,
        session_model: InferenceSession = TaskiqDepends(get_model),
        labels: dict = TaskiqDepends(get_labels),
        repo: MediaDataRepo = TaskiqDepends(),
        serializer: MediaSerializer = TaskiqDepends(),
        context: Context = TaskiqDepends()
) -> None:
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = pre_process_edgetpu(img, (224, 224, 3))
    img_batch = np.expand_dims(img, axis=0)
    results = session_model.run(["Softmax:0"], {"images:0": img_batch})[0]
    result = [{"accuracy": results[0][i], "top_class": labels[str(i)]} for i in results[0].argsort() if
              results[0][i] >= 0.8]
    top_res = None
    if result:
        top_res = result.pop(0)
        top_res["top_list"] = result
    schema_result = serializer.serialize(
        {
            "result_id": context.message.task_id,
            "data": top_res
        }
    )
    await asyncio.gather(
        repo.create_result_record(schema_result),
        asyncos.remove(image_path)
    )


@broker.task
async def process_video(
        video_path: str,
        repo: MediaDataRepo = TaskiqDepends(),
        serializer: MediaSerializer = TaskiqDepends(),
        session_model: InferenceSession = TaskiqDepends(get_model),
        labels: dict = TaskiqDepends(get_labels),
        context: Context = TaskiqDepends()
) -> None:
    frames = get_video_frames(path=video_path)
    pre_processed_images = []
    for i in frames:
        img = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
        img = pre_process_edgetpu(img, (224, 224, 3))
        img_batch = np.expand_dims(img, axis=0)
        pre_processed_images.append(img_batch)
    analysis_result = []
    unique_label_keys = set()
    for i in pre_processed_images:
        results = session_model.run(["Softmax:0"], {"images:0": i})[0]
        sorted_args = [i for i in results[0].argsort() if results[0][i] >= 0.8]
        analysis_result.extend(
            [{"label_id": i, "accuracy": results[0][i]} for i in sorted_args]
        )
        unique_label_keys.update(sorted_args)
    combined_analysis_result = []
    for i in unique_label_keys:
        results = [v for v in analysis_result if v.get("label_id") == i]
        combined_accuracy = [j.get("accuracy") for j in results]
        combined_analysis_result.append(
            {
                "accuracy": sum(combined_accuracy) / len(combined_accuracy),
                "top_class": labels[str(i)]
            }
        )
    top_res = None
    if combined_analysis_result:
        top_res = combined_analysis_result.pop(0)
        top_res["top_list"] = combined_analysis_result
    schema_result = serializer.serialize(
        {
            "result_id": context.message.task_id,
            "data": top_res
        }
    )
    await asyncio.gather(
        repo.create_result_record(schema_result),
        asyncos.remove(video_path)
    )
