import augmentor
import os

OUTPUT_PATH = os.path.join("..", "output")

if __name__ == "__main__":
    """ """

    ua_augmentor = augmentor.UserAgentAugmentor()
    ua_augmentor.run()
