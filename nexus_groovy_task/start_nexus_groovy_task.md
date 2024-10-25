
# Start Nexus Groovy Task Script

This [start_nexus_groovy_task.sh](start_nexus_groovy_task.sh) triggers the execution of a specified Groovy script in a Nexus 3 instance by accepting parameters for URL, username, and script name. The password is read from the `$USER_PASSWORD` environment variable.

 It's useful for automating Nexus maintenance tasks or custom operations created in Groovy.


## Prerequisites

- **Nexus 3 Instance**: Ensure that Nexus 3 is installed and accessible.
- **Groovy Script**: The target Groovy script should already be uploaded in Nexus under **Administration -> System -> API -> Scripts**.
- **Environment Variable**: Set the `USER_PASSWORD` environment variable with your Nexus password.
- **Permissions**: Admin credentials or user permissions to execute scripts in Nexus are required.

## Setup

1. **Set the environment variable for the password**:
    ```bash
    export USER_PASSWORD='your_password'
    ```

## Usage

2. **Make the script executable**:
    ```bash
    chmod +x start_nexus_groovy_task.sh
    ```

3. **Run the script**:
    ```bash
    ./start_nexus_groovy_task.sh <NEXUS_URL> <USERNAME> <SCRIPT_NAME>
    ```

    - `<NEXUS_URL>`: URL of your Nexus instance (e.g., `http://nexus-url:8081`).
    - `<USERNAME>`: Nexus username with permissions to run tasks.
    - `<SCRIPT_NAME>`: Name of the Groovy script in Nexus you want to execute.

   If successful, you should see a message indicating the Groovy script executed successfully.

## Example

```bash
export USER_PASSWORD='your_password'
./start_nexus_groovy_task.sh http://nexus-url:8081 admin your-script-name
```

## Troubleshooting

- Ensure the **SCRIPT_NAME** matches exactly with the name of the script in Nexus.
- If `USER_PASSWORD` is not set, the script will not run. Ensure it’s set with `export USER_PASSWORD='your_password'`.
- Verify Nexus and network accessibility by testing the **NEXUS_URL** in a browser or with `curl`.

