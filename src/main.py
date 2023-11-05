import augmentor
import os

OUTPUT_PATH = os.path.join("..", "output")

if __name__ == "__main__":
    """ """

    # clear the folder output from previous runs
    files = os.listdir(OUTPUT_PATH)
    for file in files:
        file_path = os.path.join(OUTPUT_PATH, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    script = augmentor.UserAgentAugmentor()
    script.run()
