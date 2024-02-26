import psycopg2
import csv
import json
import subprocess 
from datetime import date
import argparse
# import os

def connect_to_database(database, user, password, host, port):
    """
    Connects to the PostgreSQL database.

    Args:
        database (str): Name of the database.
        user (str): Username.
        password (str): Password.
        host (str): Hostname or IP address of the database server.
        port (str): Port number of the database server.

    Returns:
        psycopg2.extensions.connection: A connection object if successful, None otherwise.
    """
    try:
        conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_data(conn, sql_query):
    """
    Fetches data from the database using the provided SQL query.

    Args:
        conn (psycopg2.extensions.connection): Connection object to the database.
        sql_query (str): SQL query to fetch the data.

    Returns:
        list: A list of tuples containing the fetched data.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def write_to_csv(rows, today):
    """
    Writes data to a CSV file.

    Args:
        rows (list): A list of tuples containing the data to be written.
        today (datetime.date): The current date.

    Returns:
        str: The file path of the created CSV file.
    """
    try:
        csv_file_path = f"data-{today}.csv"
        with open(csv_file_path, 'w', newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_NONE, escapechar='\\')
            csv_writer.writerows(rows)
        return csv_file_path
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return None

def create_json_files(csv_file_path, output_path):
    """
    Creates JSON files based on data from a CSV file.

    Args:
        csv_file_path (str): The file path of the CSV file containing the data.
        output_path (str): The directory where JSON files will be created.
    """
    try:
        out_json_per_repo = {}
        with open(csv_file_path, 'r') as list_file:
            for path in list_file:
                path_list = path.split(",")
                repo_name = path_list[0]
                if repo_name[0].isdigit():
                    repo_name = "m-" + repo_name
                path = path_list[0] + path_list[1]
                path = path.rstrip()
                data = {"source": path, "fileblobRef": ""}
                if repo_name in out_json_per_repo:
                    out_json_per_repo[repo_name]["assets"].append(data)
                else:
                    out_json_per_repo[repo_name] = {"assets": [data]}
        for repo in out_json_per_repo:
            output_file = f"{output_path}/{repo}_assetmap.json"
            with open(output_file, 'w') as fp:
                json.dump(out_json_per_repo[repo], fp)
    except Exception as e:
        print(f"Error creating JSON files: {e}")

def run_migration(output_path, migrator_script):
    """
    Runs migration tasks.

    Args:
        output_path (str): The directory containing JSON files.
        migrator_script (str): Full path to the migrator script.
    """
    try:
        out_flag = '--repos="'
        # alist = []
        for repo in out_json_per_repo:
            out_flag += "^" + repo + "$,"
        out_flag = out_flag[:-1] + '"'
        cmd_run = f'{migrator_script} ma {out_flag} --use-existing-asset-file="true"'
        subprocess.Popen(cmd_run, shell=True)
    except Exception as e:
        print(f"Error running migration: {e}")

def main(database, user, password, host, port, sql_date, output_path, migrator_script):
    """
    Main function to execute the script.

    Args:
        database (str): Name of the database.
        user (str): Username.
        password (str): Password.
        host (str): Hostname or IP address of the database server.
        port (str): Port number of the database server.
        sql_date (str): Date parameter for the SQL query.
        output_path (str): The directory where JSON files will be created.
        migrator_script (str): Full path to the migrator script.
    """
    conn = connect_to_database(database, user, password, host, port)
    if conn:
        # ensure that the sql_date value is correctly substituted into the SQL query without redundancy.
        # https://stackoverflow.com/questions/52975112/efficient-way-to-pass-this-variable-multiple-times
        sql_query = f"""
            SELECT r.name as Repo_Name, a.path
            FROM repository r
            JOIN yum_content_repository cr ON cr.config_repository_id = r.id
            LEFT OUTER JOIN yum_component c ON c.repository_id = cr.repository_id
            LEFT OUTER JOIN yum_asset a ON c.component_id = a.component_id
            WHERE recipe_name LIKE '%hosted' AND a.last_updated > '{sql_date}'
            
            UNION ALL
            
            SELECT r.name AS Repo_Name, a.path
            FROM repository r
            JOIN raw_content_repository cr ON cr.config_repository_id = r.id
            LEFT OUTER JOIN raw_component c ON c.repository_id = cr.repository_id
            LEFT OUTER JOIN raw_asset a ON c.component_id = a.component_id
            WHERE recipe_name LIKE '%hosted' AND a.last_updated > '{sql_date}'

            UNION ALL

            SELECT r.name AS Repo_Name, a.path
            FROM repository r
            JOIN go_content_repository cr ON cr.config_repository_id = r.id
            LEFT OUTER JOIN go_component c ON c.repository_id = cr.repository_id
            LEFT OUTER JOIN go_asset a ON c.component_id = a.component_id
            WHERE recipe_name LIKE '%hosted' AND a.last_updated > '{sql_date}'
            """
        rows = fetch_data(conn, sql_query)
        if rows:
            csv_file_path = write_to_csv(rows, today)
            if csv_file_path:
                create_json_files(csv_file_path, output_path)
                run_migration(output_path, migrator_script)
        conn.close()

def validate_sql_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Date should be in YYYY-MM-DD format.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetch data from PostgreSQL database, write to CSV, create JSON files, and run migration.")
    parser.add_argument("--database", help="Database name")
    parser.add_argument("--user", help="Username")
    parser.add_argument("--password", help="Password")
    parser.add_argument("--host", help="Host")
    parser.add_argument("--port", help="Port")
    parser.add_argument("--sql_date", help="SQL date (format: YYYY-MM-DD)", type=validate_sql_date)
    # output_path = 'C:/Workenv/nexus-audit-events/abc'
    # output_path = '/opt/app/workload/jfrog/migration/nexus-migrator'
    parser.add_argument("--output_path", help="Output path for JSON files")
    parser.add_argument("--migrator_script", help="Full path to the migrator script")
    args = parser.parse_args()
    
    today = date.today()
    main(args.database, args.user, args.password, args.host, args.port, args.sql_date, args.output_path, args.migrator_script)
