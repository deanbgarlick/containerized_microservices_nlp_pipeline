import argparse
import requests
import pandas as pd


def run_service_on_email_csv(input_filename, output_filename):
    """ Run service on a csv containing emails.

    Args
    ----
    input_filename: str
        Input csv filename. The the csv must contain a header row with an index and a 'message' column containing
        the string representation of an email for parsing.
    output_filename: str
        Location for saving the service output json to.
    """
    emails_df = pd.read_csv(input_filename, index_col=0)
    json_response_list = []
    for i in range(emails_df.shape[0]):
        email_record = emails_df.iloc[i]
        res = requests.post('http://localhost:80/email', json={"email_string": email_record.message})
        result = res.json()
        result['id'] = email_record.name
        json_response_list.append(result)
    results_df = pd.DataFrame.from_records(json_response_list)
    results_df = results_df.set_index('id')
    results_df.to_csv(output_filename)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input_filename', type=str)
    parser.add_argument('--output_filename', type=str)

    args, _ = parser.parse_known_args()

    run_service_on_email_csv(args.input_filename, args.output_filename)
