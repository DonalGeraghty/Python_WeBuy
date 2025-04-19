from datetime import date, timedelta

import os, csv
import pandas as pd


def get_today_filename():
    today_date = date.today()
    filetype = '.csv'
    return str(today_date) + filetype


def get_yesterday_filename():
    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    filetype = '.csv'
    return str(yesterday_date) + filetype


def return_diff_yesterday_today():
    column = "name"

    yesterday_list = get_list_from_csv_column(get_yesterday_filename(), column)
    today_list = get_list_from_csv_column(get_today_filename(), column)

    # Elements in today but not in yesterday
    difference = list(set(today_list) - set(yesterday_list))
    return difference


def get_prices_from_list(filter_list):
    df = pd.read_csv(get_today_filename())
    filtered_df = df[df['name'].isin(filter_list)]
    result_df = filtered_df[['name', 'price']]
    return result_df


def check_file_exists(file_path):
    return os.path.exists(file_path)


def get_list_from_csv_column(filename: str, column: str):
    exists = check_file_exists(filename)
    if exists:
        df = pd.read_csv(filename)
        return df[column].tolist()
    else:
        headers = {'id': [], 'name': [], 'price': []}
        df = pd.DataFrame(headers)
        df.to_csv(filename, index=False)
        return df[column].tolist()


def output_blu_rays(blu_ray_all):
    filename = get_today_filename()
    headers = ["id", "name", "price"]
    print(filename)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for index, blu_ray in enumerate(blu_ray_all):
            writer.writerow([index, blu_ray.title, blu_ray.price])


def get_repo_path_from_script():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return parent_dir


def cleanup_files():
    file_today = get_today_filename()
    file_yesterday = get_yesterday_filename()
    delete_other_csvs(file_today, file_yesterday)


def delete_other_csvs(file1: str, file2: str):
    folder_path = get_repo_path_from_script()
    print(folder_path)
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv") and filename not in [file1, file2]:
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("Finished checking and deleting CSV files.")
    except FileNotFoundError:
        print(f"Error: Folder not found at '{folder_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")
