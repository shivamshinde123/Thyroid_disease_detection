import argparse
from get_data import get_data, read_params


def load_and_save(config_path):

    """This method is used to copy the data given by the client to the local Storage

    Args: 
        config_path: Path to the parameters yaml file

    Return: None
    """

    config = read_params(config_path)

    raw_data = config['data_location']['raw_data']

    df = get_data(config_path) 

    df.to_csv(raw_data, index=False, sep=',')


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)