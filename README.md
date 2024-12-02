# SAL PROJECT

## Paper title: SD-HuBERT: Sentence-Level Self-Distillation Induces Syllabic Organization In HuBERT

## Environment

1. Set up a conda environment. We trained/tested the model on Python 3.9.
```
conda create -n sdhubert python=3.9
conda activate sdhubert
```
2. Please install a working version of PyTorch which fits your computing resources (tested on torch=1.13.1, CUDA==11.7, Linux).
3. Then install dependency packages through `pip install -r requirements.txt`.
4. Run the following code after installing requirements for segmentation purpuse given as per the paper
```
cd ./mincut
python setup.py build_ext --inplace
```

### Extract segments

To extract segments from audio files, please run the following command with your own input and output directory.

```
python segment.py --input_dir=INPUT_DIR --output_dir=OUTPUT_DIR
```

The audio files in a specified directory `INPUT_DIR` will be processed. Currently, the script only works on one of `wav`, `flac`, and `ogg` formats.
The results will be saved in `OUTPUT_DIR` with following format for each `AUDIO_FILE_NAME.wav`.

```
AUDIO_FILE_NAME_segments.txt # Each line has a comma separated start end end of each syllable segment in second.
AUDIO_FILE_NAME_feature.npy  # An array of features in 50 hz frame before segmented, resulting (Length of audio frames, 768) array.
AUDIO_FILE_NAME_segmentfeature.npy # An array of segment-averaged featues after segmentation, resulting (Number of segments, 768) array.
```


## Training SD-HuBERT

First, download the [LibriSpeech](https://www.openslr.org/12) data under some data directory, let's say `LIBRISPEECH_ROOT`. The directory should look like 
```
LIBRISPEECH_ROOT
├── train-clean-100
├── train-clean-360
├── train-other-500
├── dev-clean
├── dev-other
├── test-clean
└── test-other
```

The trainer is implemented using [PyTorch Lightning](https://lightning.ai/docs/pytorch/stable/), so please download the package through `pip install lightning` (we used lightning==2.1.2).

You can train with the following command. Also please check `configs/sdhubert_base` for detailed configurations.
```
python train.py --config-name=sdhubert_base data.root_dir=LIBRISPEECH_ROOT
```

After the model training is finished, export model to more handy checkpoint file. The `ckpt_path` should be pointed to the path that is created by running the training script.
```
python export_model.py --ckpt_path=outputs/DATE/TIME/NAME
```

## Conversion of obtained files into single file

Run the `segmentation_mine.py` to merge all the different files containing segments, features and segment features (AUDIO_FILE_NAME_segments.txt, AUDIO_FILE_NAME_feature.npy , AUDIO_FILE_NAME_segmentfeature.npy') into one file for each of the audio files.

## Dividing the files into directories 

This is done based on speaker number -> chapter number -> audio file number for evaluation
Run the `split_folders.py` to split them respectively

## Evaluation

Please run through the following commands to extract segments and evaluate syllable boundary detection, purity, and SSABX task. Also, please check the arguments in the scripts to get full control of experiment.

### Extract segments for LibriSpeech

This will extract segments under `OUTPUT_DIR`. The `NAME` is `sdhubert_base` by default.

```
python segment.py --input_dir=INPUT_DIR_LIBRISPEECH --output_dir=OUTPUT_DIR
```
Keep OUTPUT_DIR as `SEGMENT_PATH=LIBRISPEECH_ROOT/segments/NAME` for evaluation purpose. The `NAME` is sdhubert_base by default.


### Evaluate syllable boundary detection

```
python evaluate_boundary.py --segment_path=SEGMENT_PATH
```

### Train clustering model

```
python train_km.py --segment_path=SEGMENT_PATH --n_clusters=16384 --n_clusters_agglomerative=4096
```

### Evaluate syllable clustering quality

```
python evaluate_purity.py --segment_path=SEGMENT_PATH --km_path=km/sdhubert_base_16384.pt --reducer_path=km/sdhubert_base_16384to4096.npy
```
