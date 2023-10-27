import os, glob
from generator.synthetic_data import SyntheticData

if __name__ == '__main__':

    path=os.path.join(os.getcwd(), "01-model", "02-feature-set")
    generator=SyntheticData(path, label="50 items", count=50, bulk_max=10, compress=True)

    generator.generate()

    print("")


