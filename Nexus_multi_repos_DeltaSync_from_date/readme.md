### Nexus Multi Repos Delta Sync from Date

This Python script facilitates syncing data from multiple repositories in Nexus, converting it into JSON files, and executing migration tasks. It's particularly useful for managing assets in Nexus repositories efficiently.

### Prerequisites
- PostgreSQL database access with necessary permissions.
- Python 3.x installed.
- Proper configuration and access to the Nexus repository manager.
- A migrator script compatible with your Nexus environment.

### Usage
1. **Setup PostgreSQL Database**:
   Ensure the PostgreSQL database with necessary schema and permissions is set up properly.

2. **Configuration**:
   Modify the script variables according to your environment:
   - `--database`: Name of the PostgreSQL database.
   - `--user`: Username for database access.
   - `--password`: Password for database access.
   - `--host`: Hostname or IP address of the PostgreSQL server.
   - `--port`: Port number of the PostgreSQL server.
   - `--sql_date`: Date parameter for the SQL query in the format YYYY-MM-DD.
   - `--output_path`: Path where JSON files will be saved.
   - `--migrator_script`: Full path to the migrator script `jfrog-nexus-migrator-<version>.sh` for executing migration tasks.

Note: The   `output_path` is usually the same folder where the  `migrator_script` i.e `./jfrog-nexus-migrator-<version>.sh` mentioned in the `migrateArtifact` option in JFrog Installation & Setup Documentation > Migrating from Sonatype Nexus Repository Manager to Artifactory > [Run the migration tool in multiple stages](https://jfrog.com/help/r/jfrog-installation-setup-documentation/run-the-migration-tool-in-multiple-stages)

3. **Execution**:
   Execute the script using Python in the terminal or command prompt.

   Example:
   ```
   python Nexus_multi_repos_DeltaSync_from_date.py --database <database_name> --user <username> --password <password> --host <hostname> --port <port_number> --sql_date <YYYY-MM-DD> --output_path <output_path> --migrator_script <migrator_script_path>
   ```

### Functionality
- **Data Retrieval**: Fetches data from PostgreSQL database regarding repositories and assets based on the provided date parameter.
- **CSV Export**: Writes the fetched data into a CSV file.
- **JSON File Creation**: Converts CSV data into JSON files structured for Nexus repository asset mapping.
- **Migration Execution**: Executes migration tasks using the provided migrator script, utilizing the JSON files created.

### Note
- Ensure the migrator script provided is compatible with your Nexus version and environment.
- Make sure to provide correct database credentials and Nexus configurations.
- Verify the SQL query logic for fetching relevant data based on your Nexus repository structure.


### Disclaimer
Your use of this code is governed by the following license:

JFrog hereby grants you a non-exclusive, non-transferable, non-distributable right to use this code solely in connection with
your use of a JFrog product or service. This code is provided 'as-is' and without any warranties or
conditions, either express or implied including, without limitation, any warranties or conditions
of title, non-infringement, merchantability or fitness for a particular cause. Nothing herein shall
convey to you any right or title in the code, other than for the limited use right set forth
herein. For the purposes hereof "you" shall mean you as an individual as well as the organization
on behalf of which you are using the software and the JFrog product or service.
