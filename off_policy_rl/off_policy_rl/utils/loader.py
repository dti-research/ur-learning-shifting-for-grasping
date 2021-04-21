
from off_policy_rl.config.config import Config

import tensorflow as tf

class Loader:

    @classmethod
    def get_model(
            cls,
            name: str,
        ):
        #for device in tf.config.experimental.list_physical_devices('GPU'):
        #    tf.config.experimental.set_memory_growth(device, True)

        model_path = Config.get_model_path(name)
        return tf.keras.models.load_model(str(model_path), compile=False)
