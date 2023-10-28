import os, glob
from generator.synthetic_data import SyntheticData

if __name__ == '__main__':

#    generator=SyntheticData(os.path.join(os.getcwd(), "01-model", "02-feature-set"))
    generator = SyntheticData()

    generator.generate(label="0-size-100", count=100, bulk_max=100, compress=True)
    generator.generate(label="1-size-1K", count=1000, bulk_max=1000, compress=True)

    print("")


