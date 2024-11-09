import numpy as np
from pipecat_ai_krisp.krisp_python import KrispAudioProcessorPcmFloat
from pipecat_ai_krisp.krisp_python import KrispAudioProcessorPcm16

class KrispAudioProcessor:
    """
    A class for processing audio frames using Krisp's audio processing library.

    Attributes:
        sample_rate (int): The sample rate of the audio.
        sample_type (str): The type of sample data, either "FLOAT" or "PCM_16".
        channels (int): The number of audio channels.
    """

    FRAME_SIZE_MS = 10  # Krisp requires audio frames of 10ms duration for processing.

    def __init__(self, sample_rate: int, sample_type: str, channels: int, model_path: str):
        """
        Initializes the KrispAudioProcessor with a specific sample rate, sample type,
        number of channels, and model path.

        Args:
            sample_rate (int): Sample rate for the audio processor.
            sample_type (str): Type of the samples, either "FLOAT" or "PCM_16".
            channels (int): Number of channels in the audio.
            model_path (str): Path to the model file.

        Raises:
            ValueError: If an unsupported sample type is provided.
        """
        if sample_type == "FLOAT":
            self.__data_type = np.float32
            self.processor = KrispAudioProcessorPcmFloat(sample_rate, model_path)
        elif sample_type == "PCM_16":
            self.__data_type = np.int16
            self.processor = KrispAudioProcessorPcm16(sample_rate, model_path)
        else:
            raise ValueError(f"Unsupported sample type: {sample_type}")

        self.sample_rate = sample_rate
        self.__channels = channels

    def __store_frames(self, audio_frames: np.ndarray):
        """Stores audio frames in the Krisp processor for later processing."""
        self.processor.add_audio_frames(audio_frames)

    def __get_processed_frames(self) -> np.ndarray:
        """
        Retrieves processed audio frames.

        Returns:
            np.ndarray: The processed audio frames.
        """
        samples_per_frame = (self.sample_rate * self.FRAME_SIZE_MS) // 1000
        frame_count = self.processor.get_samples_count() // (samples_per_frame * self.__channels)
        output_shape = (frame_count, samples_per_frame, self.__channels)

        output_frames = np.zeros(output_shape, dtype=self.__data_type)
        processed_frames_count = self.processor.get_processed_frames(output_frames)

        return output_frames[:processed_frames_count]

    def process(self, audio_frames: np.ndarray) -> np.ndarray:
        """
        Processes input audio frames and returns the denoised frames.

        Args:
            audio_frames (np.ndarray): The input audio frames.

        Returns:
            np.ndarray: The denoised and processed audio frames.
        """
        self.__store_frames(audio_frames)
        return self.__get_processed_frames()
