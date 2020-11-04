﻿# Dataset Loading

<!-- TOC -->

- [Dataset Loading](#dataset-loading)
    - [Overview](#overview)
    - [Common Dataset Loading](#common-dataset-loading)
        - [CIFAR-10 and CIFAR-100 Datasets](#cifar-10-and-cifar-100-datasets)
        - [VOC Dataset](#voc-dataset)
        - [COCO Dataset](#coco-dataset)
    - [Loading Datasets in Specific Formats](#loading-datasets-in-specific-formats)
        - [MindRecord](#mindrecord)
        - [Manifest](#manifest)
        - [TFRecord](#tfrecord)
        - [NumPy](#numpy)
        - [CSV](#csv)
    - [Loading a User-defined Dataset](#loading-a-user-defined-dataset)
        - [Constructing a Dataset Generator Function](#constructing-a-dataset-generator-function)
        - [Constructing an Iterable Dataset Class](#constructing-an-iterable-dataset-class)
        - [Constructing a Dataset Class that Can Be Randomly Accessed](#constructing-a-dataset-class-that-can-be-randomly-accessed)

<!-- /TOC -->

<a href="https://gitee.com/mindspore/docs/blob/master/docs/programming_guide/source_en/dataset_loading.md" target="_blank"><img src="./_static/logo_source.png"></a>

## Overview

MindSpore can load common image datasets. You can directly use the corresponding class in `mindspore.dataset` to load datasets. The following table lists the supported common dataset classes and datasets.

| Image Dataset | Dataset Class | Description |
|  ----                    | ----  | ----           |
| MNIST | MnistDataset | MNIST is a large handwritten digital image dataset. It has 60,000 training images and 10,000 test images and is often used to train various image processing systems. |
| CIFAR-10 | Cifar10Dataset | CIFAR-10 is a small image dataset that contains 60,000 32 x 32 color images of 10 categories. On average, each category contains 6,000 images, of which 5,000 images are training images and 1,000 images are test images. |
| CIFAR-100 | Cifar100Dataset | CIFAR-100 is similar to CIFAR-10, but it has 100 categories. On average, there are 600 images in each category, among which 500 images are training images and 100 images are test images. |
| CelebA | CelebADataset | CelebA is a large face image dataset that contains more than 200,000 face images of celebrities. Each image has 40 feature labels. |
| PASCAL-VOC | VOCDataset | PASCAL-VOC is a commonly used image dataset, which is widely used in computer vision fields such as object detection and image segmentation. |
| COCO | CocoDataset | COCO is a large dataset for object detection, image segmentation, and pose estimation. |
| CLUE | CLUEDataset | CLUE is a large Chinese semantic comprehension dataset. |

MindSpore also can load datasets in different data storage formats. You can directly use the corresponding class in `mindspore.dataset` to load data files in the disk. The following table lists the supported data formats and loading modes.

| Data Format | Dataset Class | Description |
|  ----                    | ----  | ----           |
| MindRecord | MindDataset | MindRecord is a self-developed data format of MindSpore. It features efficient read/write and easy distributed processing. |
| Manifest | ManifestDataset | Manifest is a data format supported by Huawei ModelArts. It describes the original files and labeling information and can be used for labeling, training, and inference. |
| TFRecord | TFRecordDataset | TFRecord is a binary data file format defined by TensorFlow. |
The | NumPy | NumpySlicesDataset | NumPy data source refers to the NumPy array dataset that has been read into the memory. |
| Text File | TextFileDataset | Text File refers to common data in text format. |
| CSV File | CSVDataset | CSV refers to comma-separated values. Files in this format store tabular data in plain text. |

MindSpore also can load datasets constructed using `GeneratorDataset`. You can implement your own dataset classes as required.

For details about the dataset loading API, see [MindSpore API](https://www.mindspore.cn/doc/api_python/en/master/mindspore/mindspore.dataset.html).

## Common Dataset Loading

The following describes how to load common datasets.

### CIFAR-10 and CIFAR-100 Datasets

Download [CIFAR-10 dataset](https://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz) and unzip it, the directory structure is as follows:

```text
└─cifar-10-batches-bin
    ├── batches.meta.txt
    ├── data_batch_1.bin
    ├── data_batch_2.bin
    ├── data_batch_3.bin
    ├── data_batch_4.bin
    ├── data_batch_5.bin
    ├── readme.html
    └── test_batch.bin
```

The following example uses the `Cifar10Dataset` API to load the CIFAR-10 dataset, uses the sequential sampler to obtain five samples, and displays the shape and label of the corresponding image.

The methods for loading the CIFAR-100 and MNIST datasets are similar.

```python
import mindspore.dataset as ds

DATA_DIR = "cifar-10-batches-bin/"

sampler = ds.SequentialSampler(num_samples=5)
dataset = ds.Cifar10Dataset(DATA_DIR, sampler=sampler)

for data in dataset.create_dict_iterator():
    print("Image shape:", data['image'].shape, ", Label:", data['label'])
```

The output is as follows:

```text
Image shape: (32, 32, 3) , Label: 6
Image shape: (32, 32, 3) , Label: 9
Image shape: (32, 32, 3) , Label: 9
Image shape: (32, 32, 3) , Label: 4
Image shape: (32, 32, 3) , Label: 1
```

### VOC Dataset

There are multiple versions of the VOC dataset, here is VOC2012 as an example. Download [VOC2012 dataset](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar) and unzip it, The directory structure is as follows:

```text
└─ VOCtrainval_11-May-2012
    └── VOCdevkit
        └── VOC2012
            ├── Annotations
            ├── ImageSets
            ├── JPEGImages
            ├── SegmentationClass
            └── SegmentationObject
```

The following example uses the `VOCDataset` API to load the VOC2012 dataset to display the original image shape and target image shape when segmentation and detection tasks are specified.

```python
import mindspore.dataset as ds

DATA_DIR = "VOCtrainval_11-May-2012/VOCdevkit/VOC2012/"

dataset = ds.VOCDataset(DATA_DIR, task="Segmentation", usage="train", num_samples=2, decode=True, shuffle=False)

print("[Segmentation]:")
for data in dataset.create_dict_iterator():
    print("image shape:", data["image"].shape)
    print("target shape:", data["target"].shape)

dataset = ds.VOCDataset(DATA_DIR, task="Detection", usage="train", num_samples=1, decode=True, shuffle=False)

print("[Detection]:")
for data in dataset.create_dict_iterator():
    print("image shape:", data["image"].shape)
    print("bbox shape:", data["bbox"].shape)
```

The output is as follows:

```text
[Segmentation]:
image shape: (281, 500, 3)
target shape: (281, 500, 3)
image shape: (375, 500, 3)
target shape: (375, 500, 3)
[Detection]:
image shape: (442, 500, 3)
bbox shape: (2, 4)
```

### COCO Dataset

There are multiple versions of the COCO dataset. Here, the verification dataset of COCO2017 is taken as an example.Download COCO2017 [verification dataset](http://images.cocodataset.org/zips/val2017.zip), [detection task annotation](http://images.cocodataset.org/annotations/annotations_trainval2017.zip) and [panorama segmentation task annotation](http://images.cocodataset.org/annotations/panoptic_annotations_trainval2017.zip) and unzip them, take only the part of the verification dataset and store it in the following directory structure:

```text
└─ COCO
    ├── val2017
    └── annotations
        ├── instances_val2017.json
        ├── panoptic_val2017.json
        └── person_keypoints_val2017.json
```

The following example uses the `CocoDataset` API to load the COCO dataset, and displays the data when object detection, stuff segmentation, keypoint detection, and panoptic segmentation tasks are specified.

```python
import mindspore.dataset as ds

DATA_DIR = "COCO/val2017/"
ANNOTATION_FILE = "COCO/annotations/instances_val2017.json"
KEYPOINT_FILE = "COCO/annotations/person_keypoints_val2017.json"
PANOPTIC_FILE = "COCO/annotations/panoptic_val2017.json"

dataset = ds.CocoDataset(DATA_DIR, annotation_file=ANNOTATION_FILE, task="Detection", num_samples=1)
for data in dataset.create_dict_iterator():
    print("Detection:", data.keys())

dataset = ds.CocoDataset(DATA_DIR, annotation_file=ANNOTATION_FILE, task="Stuff", num_samples=1)
for data in dataset.create_dict_iterator():
    print("Stuff:", data.keys())

dataset = ds.CocoDataset(DATA_DIR, annotation_file=KEYPOINT_FILE, task="Keypoint", num_samples=1)
for data in dataset.create_dict_iterator():
    print("Keypoint:", data.keys())

dataset = ds.CocoDataset(DATA_DIR, annotation_file=PANOPTIC_FILE, task="Panoptic", num_samples=1)
for data in dataset.create_dict_iterator():
    print("Panoptic:", data.keys())
```

The output is as follows:

```text
Detection: dict_keys(['image', 'bbox', 'category_id', 'iscrowd'])
Stuff: dict_keys(['image', 'segmentation', 'iscrowd'])
Keypoint: dict_keys(['image', 'keypoints', 'num_keypoints'])
Panoptic: dict_keys(['image', 'bbox', 'category_id', 'iscrowd', 'area'])
```

## Loading Datasets in Specific Formats

The following describes how to load dataset files in specific formats.

### MindRecord

MindRecord is a data format defined by MindSpore. Using MindRecord can improve performance.

> For details about how to convert a dataset into the MindRecord data format, see [Data Format Conversion](https://www.mindspore.cn/doc/programming_guide/en/master/dataset_conversion.html).

The following example uses the `MindDataset` API to load a MindRecord file, and displays labels of the loaded data.

```python
import mindspore.dataset as ds

DATA_FILE = ["mindrecord_file_0", "mindrecord_file_1", "mindrecord_file_2"]
mindrecord_dataset = ds.MindDataset(DATA_FILE)

for data in mindrecord_dataset.create_dict_iterator(output_numpy=True):
    print(data["label"])
```

### Manifest

Manifest is a data format file supported by Huawei ModelArts. For details, see [Specifications for Importing the Manifest File](https://support.huaweicloud.com/en-us/engineers-modelarts/modelarts_23_0009.html).

The following example uses the `ManifestDataset` API to load a Manifest file, and displays labels of the loaded data.

```python
import mindspore.dataset as ds

DATA_FILE = "manifest_file"
manifest_dataset = ds.ManifestDataset(DATA_FILE)

for data in manifest_dataset.create_dict_iterator():
    print(data["label"])
```

### TFRecord

TFRecord is a binary data file format defined by TensorFlow.

The following example uses the `TFRecordDataset` API to load a TFRecord file and introduces two methods for setting the format of datasets.

1. Specify the dataset path or TFRecord file list to create a `TFRecordDataset` object.

    ```python
    import mindspore.dataset as ds

    DATA_FILE = ["tfrecord_file_0", "tfrecord_file_1", "tfrecord_file_2"]
    tfrecord_dataset = ds.TFRecordDataset(DATA_FILE)
    ```

2. Compile a schema file or create a schema object to set the dataset format and features.

    - Compile a schema file.

        Write the dataset format and features to the schema file in JSON format. The following is an example:

        ```text
        {
         "columns": {
             "image": {
                 "type": "uint8",
                 "rank": 1
                 },
             "label" : {
                 "type": "string",
                 "rank": 1
                 }
             "id" : {
                 "type": "int64",
                 "rank": 0
                 }
             }
         }
        ```

        - `columns`: column information field, which needs to be defined based on the actual column name of the dataset. In the preceding example, the dataset columns are `image`, `label`, and `id`.

        When creating `TFRecordDataset`, transfer the path of the schema file.

        ```python
        SCHEMA_DIR = "dataset_schema_path/schema.json"
        tfrecord_dataset = ds.TFRecordDataset(DATA_FILE, schema=SCHEMA_DIR)
        ```

    - Create a schema object.

        Create a schema object, add user-defined fields to the schema object, and import the fields when creating a dataset object.

        ```python
        import mindspore.common.dtype as mstype
        schema = ds.Schema()
        schema.add_column('image', de_type=mstype.uint8)
        schema.add_column('label', de_type=mstype.int32)
        tfrecord_dataset = ds.TFRecordDataset(DATA_FILE, schema=schema)
        ```

### NumPy

If all data has been read into the memory, you can directly use the `NumpySlicesDataset` class to load the data.

The following examples describe how to use `NumpySlicesDataset` to load array, list, and dict data.

- Load NumPy array data.

    ```python
    import numpy as np
    import mindspore.dataset as ds

    np.random.seed(58)
    features, labels = np.random.sample((5, 2)), np.random.sample((5, 1))

    data = (features, labels)
    dataset = ds.NumpySlicesDataset(data, column_names=["col1", "col2"], shuffle=False)

    for data in dataset:
        print(data[0], data[1])
    ```

    The output is as follows:

    ```text
    [0.36510558 0.45120592] [0.78888122]
    [0.49606035 0.07562207] [0.38068183]
    [0.57176158 0.28963401] [0.16271622]
    [0.30880446 0.37487617] [0.54738768]
    [0.81585667 0.96883469] [0.77994068]
    ```

- Load Python list data.

    ```python

    import mindspore.dataset as ds

    data1 = [[1, 2], [3, 4]]

    dataset = ds.NumpySlicesDataset(data1, column_names=["col1"], shuffle=False)

    for data in dataset:
        print(data[0])
    ```

    The output is as follows:

    ```text
    [1 2]
    [3 4]
    ```

- Load Python dict data.

    ```python
    import mindspore.dataset as ds

    data1 = {"a": [1, 2], "b": [3, 4]}

    dataset = ds.NumpySlicesDataset(data1, column_names=["col1", "col2"], shuffle=False)

    for data in dataset.create_dict_iterator():
        print(data)
    ```

    The output is as follows:

    ```text
    {'col1': Tensor(shape=[], dtype=Int64, value= 1), 'col2': Tensor(shape=[], dtype=Int64, value= 3)}
    {'col1': Tensor(shape=[], dtype=Int64, value= 2), 'col2': Tensor(shape=[], dtype=Int64, value= 4)}
    ```

### CSV

The following example uses `CSVDataset` to load the CSV dataset file, and displays labels of the loaded data.

The method of loading a text dataset file is similar to that of loading a CSV file.

```python
import mindspore.dataset as ds

DATA_FILE = ["csv_file_0", "csv_file_1", "csv_file_2"]
csv_dataset = ds.CSVDataset(DATA_FILE)

for data in csv_dataset.create_dict_iterator(output_numpy=True):
    print(data["1"])
```

## Loading a User-defined Dataset

For the datasets that cannot be directly loaded by MindSpore, you can construct the `GeneratorDataset` object to load them in customized mode or convert them into the MindRecord data format. Currently, user-defined datasets can be loaded in the following modes:

### Constructing a Dataset Generator Function

Construct a generator function that defines the data return mode, and then use this function to construct the user-defined dataset object.

```python
import numpy as np
import mindspore.dataset as ds

np.random.seed(58)
data = np.random.sample((5, 2))
label = np.random.sample((5, 1))

def GeneratorFunc():
    for i in range(5):
        yield (data[i], label[i])

dataset = ds.GeneratorDataset(GeneratorFunc, ["data", "label"])

for sample in dataset.create_dict_iterator():
    print(sample["data"], sample["label"])
```

The output is as follows:

```text
[0.36510558 0.45120592] [0.78888122]
[0.49606035 0.07562207] [0.38068183]
[0.57176158 0.28963401] [0.16271622]
[0.30880446 0.37487617] [0.54738768]
[0.81585667 0.96883469] [0.77994068]
```

### Constructing an Iterable Dataset Class

Construct a dataset class to implement the `__iter__` and `__next__` methods, and then use the objects of this class to construct the user-defined dataset object.

```python
import numpy as np
import mindspore.dataset as ds

class IterDatasetGenerator:
    def __init__(self):
        np.random.seed(58)
        self.__index = 0
        self.__data = np.random.sample((5, 2))
        self.__label = np.random.sample((5, 1))

    def __next__(self):
        if self.__index >= len(self.__data):
            raise StopIteration
        else:
            item = (self.__data[self.__index], self.__label[self.__index])
            self.__index += 1
            return item

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.__data)

dataset_generator = IterDatasetGenerator()
dataset = ds.GeneratorDataset(dataset_generator, ["data", "label"], shuffle=False)

for data in dataset.create_dict_iterator():
    print(data["data"], data["label"])
```

The output is as follows:

```text
[0.36510558 0.45120592] [0.78888122]
[0.49606035 0.07562207] [0.38068183]
[0.57176158 0.28963401] [0.16271622]
[0.30880446 0.37487617] [0.54738768]
[0.81585667 0.96883469] [0.77994068]
```

### Constructing a Dataset Class that Can Be Randomly Accessed

Construct a dataset class to implement the `__getitem__` method, and then use the objects of this class to construct a user-defined dataset object.

```python
import numpy as np
import mindspore.dataset as ds

class GetDatasetGenerator:
    def __init__(self):
        np.random.seed(58)
        self.__data = np.random.sample((5, 2))
        self.__label = np.random.sample((5, 1))

    def __getitem__(self, index):
        return (self.__data[index], self.__label[index])

    def __len__(self):
        return len(self.__data)

dataset_generator = GetDatasetGenerator()
dataset = ds.GeneratorDataset(dataset_generator, ["data", "label"], shuffle=False)

for data in dataset.create_dict_iterator():
    print(data["data"], data["label"])
```

The output is as follows:

```text
[0.36510558 0.45120592] [0.78888122]
[0.49606035 0.07562207] [0.38068183]
[0.57176158 0.28963401] [0.16271622]
[0.30880446 0.37487617] [0.54738768]
[0.81585667 0.96883469] [0.77994068]
```

If you want to use distributed training, you need to implement the `__iter__` method in the sampler class based on this mode. The index of the sampled data is returned each time.

```python
import math

class MySampler():
    def __init__(self, dataset, local_rank, world_size):
        self.__num_data = len(dataset)
        self.__local_rank = local_rank
        self.__world_size = world_size
        self.samples_per_rank = int(math.ceil(self.__num_data / float(self.__world_size)))
        self.total_num_samples = self.samples_per_rank * self.__world_size

    def __iter__(self):
        indices = list(range(self.__num_data))
        indices.extend(indices[:self.total_num_samples-len(indices)])
        indices = indices[self.__local_rank:self.total_num_samples:self.__world_size]
        return iter(indices)

    def __len__(self):
        return self.samples_per_rank

dataset_generator = GetDatasetGenerator()
sampler = MySampler(dataset_generator, local_rank=0, world_size=2)
dataset = ds.GeneratorDataset(dataset_generator, ["data", "label"], shuffle=False, sampler=sampler)

for data in dataset.create_dict_iterator():
    print(data["data"], data["label"])
```

The output is as follows:

```text
[0.36510558 0.45120592] [0.78888122]
[0.57176158 0.28963401] [0.16271622]
[0.81585667 0.96883469] [0.77994068]
```