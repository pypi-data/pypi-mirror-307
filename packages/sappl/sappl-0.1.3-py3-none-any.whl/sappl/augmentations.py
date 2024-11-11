# sappl/augmentations.py
# TODO: it is work in progress!

import torch
from torch_audiomentations import (
    Compose, AddBackgroundNoise, AddColoredNoise, ApplyImpulseResponse, Gain, PolarityInversion,
    PitchShift, Shift, TimeInversion, LowPassFilter, HighPassFilter
)
import numpy as np

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

def add_background_noise(audio, sample_rate=16000, noise_paths=None, min_snr_db=10, max_snr_db=20, p=0.5):
    """
    Adds background noise to the audio signal.

    Args:
        audio (Union[np.ndarray, torch.Tensor]): Input audio array.
        sample_rate (int): Sample rate of the audio. Default is 16000.
        noise_paths (list): List of paths to noise audio files.
        min_snr_db (int): Minimum signal-to-noise ratio in dB. Default is 10.
        max_snr_db (int): Maximum signal-to-noise ratio in dB. Default is 20.
        p (float): Probability of applying the transformation. Default is 0.5.

    Returns:
        torch.Tensor: Augmented audio signal.
    """
    augmenter = AddBackgroundNoise(noise_paths=noise_paths, min_snr_in_db=min_snr_db, max_snr_in_db=max_snr_db, p=p)
    audio = _convert_to_torch(audio)
    return augmenter(audio, sample_rate=sample_rate)

def add_colored_noise(audio, sample_rate=16000, min_snr_db=10, max_snr_db=20, p=0.5):
    """
    Adds colored noise to the audio signal.

    Args:
        audio (Union[np.ndarray, torch.Tensor]): Input audio array.
        sample_rate (int): Sample rate of the audio. Default is 16000.
        min_snr_db (int): Minimum signal-to-noise ratio in dB. Default is 10.
        max_snr_db (int): Maximum signal-to-noise ratio in dB. Default is 20.
        p (float): Probability of applying the transformation. Default is 0.5.

    Returns:
        torch.Tensor: Augmented audio signal.
    """
    augmenter = AddColoredNoise(min_snr_in_db=min_snr_db, max_snr_in_db=max_snr_db, p=p)
    audio = _convert_to_torch(audio)
    return augmenter(audio, sample_rate=sample_rate)

def apply_reverb(audio, ir_paths=None, p=0.5):
    """
    Convolve the given audio with impulse responses to apply reverb.

    Args:
        audio (Union[np.ndarray, torch.Tensor]): Input audio array.
        ir_paths (list): List of paths to impulse response audio files.
        p (float): Probability of applying the transformation. Default is 0.5.

    Returns:
        torch.Tensor: Augmented audio signal.
    """
    augmenter = ApplyImpulseResponse(ir_paths=ir_paths, p=p)
    audio = _convert_to_torch(audio)
    return augmenter(audio)

def gain(audio, min_gain_db=-15.0, max_gain_db=5.0, p=0.5):
    """
    Apply random gain to the audio signal.

    Args:
        audio (Union[np.ndarray, torch.Tensor]): Input audio array.
        min_gain_db (float): Minimum gain in dB. Default is -15.0.
        max_gain_db (float): Maximum gain in dB. Default is 5.0.
        p (float): Probability of applying the transformation. Default is 0.5.

    Returns:
        torch.Tensor: Augmented audio signal.
    """
    augmenter = Gain(min_gain_in_db=min_gain_db, max_gain_in_db=max_gain_db, p=p)
    audio = _convert_to_torch(audio)
    return augmenter(audio)

def pitch_shift(audio, sample_rate=16000, min_semitones=-4, max_semitones=4, p=0.5):
    """
    Shifts the pitch of the audio signal.

    Args:
        audio (Union[np.ndarray, torch.Tensor]): Input audio array.
        sample_rate (int): Sample rate of the audio. Default is 16000.
        min_semitones (int): Minimum number of semitones to shift. Default is -4.
        max_semitones (int): Maximum number of semitones to shift. Default is 4.
        p (float): Probability of applying the transformation. Default is 0.5.

    Returns:
        torch.Tensor: Augmented audio signal.
    """
    augmenter = PitchShift(min_transpose_semitones=min_semitones, max_transpose_semitones=max_semitones, p=p)
    audio = _convert_to_torch(audio)
    return augmenter(audio, sample_rate=sample_rate)

def time_invert(audio, p=0.5):
    """
    Reverses the audio along the time axis.

    Args:
        audio (Union[np.ndarray, torch.Tensor]): Input audio array.
        p (float): Probability of applying the transformation. Default is 0.5.

    Returns:
        torch.Tensor: Augmented audio signal.
    """
    augmenter = TimeInversion(p=p)
    audio = _convert_to_torch(audio)
    return augmenter(audio)

def _convert_to_torch(audio):
    """
    Converts input audio to a torch.Tensor if it is not already.

    Args:
        audio (Union[np.ndarray, torch.Tensor]): Input audio array.

    Returns:
        torch.Tensor: Audio as a torch tensor.
    """
    if isinstance(audio, np.ndarray):
        audio = torch.from_numpy(audio)
    elif not isinstance(audio, torch.Tensor):
        raise TypeError("Input audio must be a NumPy array or a torch.Tensor")
    return audio

if __name__ == "__main__":
    # Example usage for testing purposes
    from sappl.io import load_audio

    # Load an example audio file
    test_audio_path = "../samples/music_sample.wav"  # Replace with a valid path
    audio_data = load_audio(test_audio_path, sample_rate=16000, mono=True)

    # Apply background noise
    augmented_audio = add_background_noise(audio_data, noise_paths=["../samples/noise_sample.wav"])
    print("Augmented audio shape (Background Noise):", augmented_audio.shape)

    # Apply pitch shift
    pitch_shifted_audio = pitch_shift(audio_data, sample_rate=16000)
    print("Pitch shifted audio shape:", pitch_shifted_audio.shape)

    # Apply time inversion
    inverted_audio = time_invert(audio_data)
    print("Time inverted audio shape:", inverted_audio.shape)
