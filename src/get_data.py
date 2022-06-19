import argparse
import yaml
import pandas as pd

config_path = "params.yaml"

def read_params(config_path):

    """This method is used to read the parameters yaml file and returns the loaded file object.

    Args:
        config_path: Path to the parameters yaml file
    
    Returns:
        Loaded yaml file object: Returns the yaml file object.
    """

    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)
        return config


def get_data(config_path):

    """This method is used to read the data from the location where client has put it and return the variable for the dataframe.

    Args:
        config_path: Path to the parameters yaml file

    Returns:
        Dataframe variable: Returns the dataframe variable
    """
    config = read_params(config_path)

    data_given_by_client = config['data_location']['data_given_by_client']

    df = pd.read_csv(data_given_by_client)

    return df


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    get_data(config_path=parsed_args.config)