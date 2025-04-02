# Auto Deployment Logic Description

## Open
- Read the last saved configuration file information and write it to the page

## Close
- Ask whether to confirm exit
  - Yes → Exit
    - Ask whether to save the current configuration
      - Yes → Save and exit
        - Save the page fields to the config file
      - No → Exit without saving
  - No → Ignore

## t2

### Database Initialization

#### MySQL
- Unzip (user specifies extraction path)
- Initialize MySQL (via .bat)
  - Add MySQL user environment variable
  - Copy `.ini` file to installation directory
  - `mysqld --initialize --console`
    - Parse output file to get initial password
  - `mysqld --install`
  - `net start mysql`
- Create users (via `pymysql`)
  - Login with root and initial password
  - Change root password and log it
  - Create users using input from the page:
    ```sql
    create user 'alex'@'%' identified by '123';
    create user 't_user_20220517_uheh'@'%' identified by 't_user_20220517_uheh';
    grant all privileges on *.* to 'alex'@'%';
    ```
- Create database
  - Use name entered on the page
  - `create database \`bytter\` character set utf8;`
- Execute initialization SQL scripts
  - Connect using new user/database
  - Run all initialization SQL scripts
- Validation
  - Check if service is started: `sc query mysql`
    - If yes
      - Skip unzip/init/install
      - Check if user/database can connect
        - If yes
          - Run a SQL to check if DB is already initialized
            - If initialized → show popup and stop
            - If not → execute init scripts
        - If no → show error popup
    - If no → try to start MySQL service

#### Oracle
- First test connection
  - If passed, run initialization scripts via `.bat`:
    ```sh
    sqlplus [<option>] [{logon | /nolog}] [<start>]
    ```

### Test Database Connection
- Check if DB type, host/port, DB name, username, and password are entered
  - If yes → regex check host/port
  - If no → popup: fields required
- Perform DB connection test
  - If cursor created
    - Save DB config
    - Set `is_tested` = True
  - If cursor creation fails → show error popup

### Environment Configuration
- Must pass DB connection test first
- Check if DB config changed
  - If changed
    - Set `is_tested` = False
    - Show popup to retest DB connection
  - If unchanged
    - Check paths
      - Ensure paths entered
        - If JDK env is set, auto-fill path
      - Validate paths
        - Program: contains `WEB-INF`, `static`
        - Tomcat: contains `bin`, `conf`
        - Update tool: contains `tomcat`, `autoupdate`, `patches`
        - JDK: contains `bin`, `jre`, `lib`
        - If any check fails → show error
      - Modify config files
        - `t2.xml` → program path
        - `server.xml` → update tool DB config (TODO)
        - `dbconfig.properties` → t2 DB config

## Update Build Package (TODO)
- Check if paths for build and program are entered
  - If yes
    - Unzip package
      - If includes SQL
        - Run DB test and execute SQL
        - Copy files to program path (non-reversible)
      - If no SQL
        - Copy files to program path
    - Log update success
  - If not → show popup

## Update Patch Package (TODO)
- Check if patch and update tool paths are entered
  - If yes
    - Validate patch file is `.patch`
    - Copy patch to `patches\patch_now`
    - Start Tomcat
    - Open IE → upgrade tool → user manual upgrade
  - If not → show popup

## Bank Interface (TODO)
- Test DB connection (same as t2)
- Run upgrade script
  - If test passed → run `run_sql.py` to execute all `.sql`
- Path config

## Unresolved Issues
- Duplicate `pyqtSignal` when running child threads multiple times
- Move to new machine should clear config:
  - Check machine info → generate ID
  - On mismatch → clear `yml`
- Combine: unzip + init MySQL + create DB/user + run SQL
- Debug: run all `.sql` files in a folder

## Resolved
- Multithread signal-slot binding
- After DB test, recheck config changes before environment setup
- Missing port → validation error
- Tomcat startup failure via CLI