from bomapp.bom_api import create_bom, dfs
from bomapp.bom_requests import BoMRequests
from collections import defaultdict
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file', type=str, help='Output file name')
    args = parser.parse_args()
    if len(vars(args)) == 1:
        bom_requests = BoMRequests()
        bom, root = create_bom(bom_requests)
        if bom:
            result_map = defaultdict(int)
            dfs(bom, result_map, root, 1)
            df = pd.DataFrame()
            df['Part'] = result_map.keys()
            df['Quantity'] = result_map.values()
            df.to_excel(args.output_file, index=False)
        else:
            print("Invalid json!")
