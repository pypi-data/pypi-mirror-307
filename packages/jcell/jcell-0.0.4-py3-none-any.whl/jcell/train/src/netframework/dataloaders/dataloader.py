import torch

try:
    from ffcv.writer import DatasetWriter
    from ffcv.loader import Loader, OrderOption
    from ffcv.transforms import *
    from ffcv.fields.decoders import *
    from ffcv.fields import FloatField, IntField, NDArrayField
    from ffcv.fields.decoders import FloatDecoder, IntDecoder, NDArrayDecoder
    from ffcv.transforms import ToTensor, Squeeze

    FCCV_AVAILABLE = True
except ImportError:
    FCCV_AVAILABLE = False
import os
import numpy as np


def datawriter(dataset, file_name=None, force_write=False, offline_augmentation=1):
    if file_name is None:
        file_name = "{:}/.{:}.beton".format("data", str(dataset))
    assert offline_augmentation > 0, "`offline_augmentation` must be greater than 0."

    if force_write or not os.path.exists(file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        writer = DatasetWriter(
            file_name,
            dataset.ffcv_writer(dataset),
            num_workers=16,
        )
        for i in range(offline_augmentation):
            writer.from_indexed_dataset(dataset)

    return file_name


def dataloader(file_name, load_pipeline, shuffle=True, batch_size=1, **opts):
    order = OrderOption.RANDOM if shuffle else OrderOption.SEQUENTIAL

    loader = Loader(
        file_name,
        order=order,
        pipelines=load_pipeline,
        batch_size=batch_size,
        **opts,
    )
    return loader


class WrapDataset(torch.utils.data.Dataset):
    def __init__(self, dataset, times=10):
        self.dataset = dataset
        self.times = times

    def __getitem__(self, idx):
        data = self.dataset[idx % len(self.dataset)]
        data["image"] = data["image"].numpy()
        data["label"] = data["label"].numpy()
        if "weight" not in data:
            data["weight"] = np.array([1.0], dtype=np.float32)

        return data["idx"], data["image"], data["label"], data["weight"]

    def __len__(self):
        return len(self.dataset) * self.times

    def ffcv_writer(self):
        if FCCV_AVAILABLE:
            x = self.__getitem__(0)
            image, label, weight = x[1], x[2], x[3]

            ret_dict = {
                "idx": IntField(),
                "image": NDArrayField(dtype=np.dtype("float32"), shape=image.shape),
                "label": NDArrayField(dtype=np.dtype("int64"), shape=label.shape),
                "weight": NDArrayField(dtype=np.dtype("float32"), shape=weight.shape),
            }

            return ret_dict
        return {}

    def ffcv_loader(self):
        if FCCV_AVAILABLE:
            ret_dict = {
                "idx": [IntDecoder(), ToTensor()],
                "image": [NDArrayDecoder(), ToTensor()],
                "label": [NDArrayDecoder(), ToTensor()],
                "weight": [NDArrayDecoder(), ToTensor()],
            }
            return ret_dict
        return {}


def DataLoader(dataset=None, loader="ffcv", **opts):
    """dataloader

    Args:
        dataset (torch.utils.data.Dataset, optional): PyTorch dataset. Defaults to None.
        loader (str, optional): Loader type ['ffcv', 'torch']. Defaults to "ffcv".
        file_name (str, optional): File name for ffcv format. Ignored for torch. Defaults to data/dataset_str.beton.
        force_write (bool, optional): Force writing for ffcv format. Ignored for torch. Defaults to False.
        shuffle (bool, optional): Shuffle data. Defaults to False.
        num_workers (int, optional): Number of workers.
        batch_size (int, optional): Batch size.

    Returns:
        [torch.utils.data.DataLoader, ffcv.loader.Loader]: Data loader, either torch or ffcv.
    """
    assert loader in ["ffcv", "torch"]

    if not FCCV_AVAILABLE:
        loader = "torch"

    if loader == "ffcv":
        file_name = "data/.tmp.beton"
        if "file_name" in opts:
            file_name = opts.pop("file_name")

        force = True
        if "force_write" in opts:
            force = opts.pop("force_write")

        if dataset is not None and (force or not os.path.exists(file_name)):
            dataset = WrapDataset(dataset)
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            writer = DatasetWriter(
                file_name,
                dataset.ffcv_writer(),
                num_workers=16,
            )
            writer.from_indexed_dataset(dataset)

        order = OrderOption.SEQUENTIAL
        if "shuffle" in opts:
            shuffle = opts.pop("shuffle")
            order = OrderOption.RANDOM if shuffle else OrderOption.SEQUENTIAL

        if "batch_size" not in opts:
            opts["batch_size"] = 1

        if "load_pipeline" in opts:
            load_pipeline = opts.pop("load_pipeline")
        elif dataset is not None:
            load_pipeline = dataset.ffcv_loader()
        else:
            raise ValueError("No load pipeline specified")

        if "sampler" in opts:
            sampler = opts.pop("sampler")
            #opts["indices"] = sampler.indices

        opts.pop("pin_memory", None)

        loader = Loader(file_name, order=order, pipelines=load_pipeline, **opts)
        return loader

    elif loader == "torch":
        if "file_name" in opts:
            file_name = opts.pop("file_name")
        if "force_write" in opts:
            force = opts.pop("force_write")
        dataset = WrapDataset(dataset)
        dl = torch.utils.data.DataLoader(dataset, **opts)
        dl.indices = torch.arange(0, len(dataset))
        return dl
