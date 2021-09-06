import argparse

import pandas as pd
from urlclassifier.model import (
    create_pipeline,
    save_model,
    encode_target,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='path to data')
    parser.add_argument('--model', required=True, help='path to model')
    args = parser.parse_args()
    
    df = pd.read_csv(args.data, encoding='latin-1')
    pipeline = create_pipeline()
    target = encode_target(df['label'])
    pipeline.fit(df['url'].tolist(), target)
    save_model(pipeline, args.model)

if __name__ == "__main__":
    main()
    