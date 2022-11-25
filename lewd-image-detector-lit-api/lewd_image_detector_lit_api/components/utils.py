from datetime import datetime
import tensorflow as tf
from typing import Tuple


def pad_resize_image(image: tf.Tensor, dims: Tuple[int, int]):
        """
        Resize image with padding
        Parameters
        ----------
        image : tf.Tensor
            Image to resize
        dims : Tuple[int, int]
            Dimensions of resized image
        Returns
        -------
        image : tf.Tensor
            Resized image
        """
        image = tf.image.resize(
            image,
            dims,
            preserve_aspect_ratio=True
        )

        shape = tf.shape(image)

        sxd = dims[1] - shape[1]
        syd = dims[0] - shape[0]

        sx = tf.cast(
            sxd / 2,
            dtype=tf.int32
        )
        sy = tf.cast(
            syd / 2,
            dtype=tf.int32
        )

        paddings = tf.convert_to_tensor([
            [sy, syd - sy],
            [sx, sxd - sx],
            [0, 0]
        ])

        image = tf.pad(
            image,
            paddings,
            mode='CONSTANT',
            constant_values=128
        )

        return image


def preprocess_for_evaluation(image: tf.Tensor,
                              image_size: int,
                              dtype: tf.dtypes.DType) -> tf.Tensor:
    """
    Preprocess image for evaluation
    Parameters
    ----------
    image : tf.Tensor
        Image to be preprocessed
    image_size : int
        Height/Width of image to be resized to
    dtype : tf.dtypes.DType
        Dtype of image to be used
    Returns
    -------
    image : tf.Tensor
        Image ready for evaluation
    """
    image = pad_resize_image(
        image,
        [image_size, image_size]
    )

    image = tf.cast(image, dtype)

    image -= 128
    image /= 128

    return image


def read_image(filename: str) -> tf.Tensor:
    """
    Load and preprocess image for inference with the Private Detector
    Parameters
    ----------
    filename : str
        Filename of image
    Returns
    -------
    image : tf.Tensor
        Image ready for inference
    """
    image = tf.io.read_file(filename)
    image = tf.io.decode_jpeg(image, channels=3)

    image = preprocess_for_evaluation(
        image,
        480,
        tf.float16
    )

    image = tf.reshape(image, -1)

    return image


def get_current_time():
    time = datetime.now()
    ist_time = time.strftime('%Y-%m-%d_%H-%M-%S')
    return ist_time