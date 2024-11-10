import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self, timeout=10):
        """Establish a connection to the MySQL database."""

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin='mysql_native_password',
                connection_timeout=timeout
            )
            if self.connection.is_connected():
                print("Connection to MySQL database established successfully.")
            else:
                print("Connection to MySQL database failed.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection to MySQL database closed.")

    def execute_query(self, query, params=None):
        """Execute a SQL query."""
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error: '{e}' occurred")
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Fetch all results from a SQL query."""
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return None
        cursor = self.connection.cursor(dictionary=True)
        results = None
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
        except Error as e:
            print(f"Error: '{e}' occurred")
        finally:
            cursor.close()
        return results

    def fetch_one(self, query, params=None):
        """Fetch a single result from a SQL query."""
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return None
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
        except Error as e:
            print(f"Error: '{e}' occurred")
        finally:
            cursor.close()
        return result

    def create_table(self, create_table_query):
        """Create a table in the database."""
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute(create_table_query)
            self.connection.commit()
            print("Table created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()

    def insert_data_from_dataframe(self, dataframe, table_name):
        """Insert data from a DataFrame into the database."""
        if dataframe.empty:
            print("The DataFrame is empty. No data to insert.")
            return

        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return

        cursor = self.connection.cursor()

        # Enclose column names in backticks to handle reserved keywords
        columns = ', '.join([f'`{col}`' for col in dataframe.columns])

        # Generate the placeholders for the SQL insert statement
        placeholders = ', '.join(['%s'] * len(dataframe.columns))

        # Create the insert statement
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Convert DataFrame rows to list of tuples
        data = [tuple(row) for row in dataframe.to_numpy()]

        dup = dataframe[dataframe.duplicated(subset=['report_id', 'name', 'start_time', 'duration_in_ms','test_execution_id'], keep=False)].values.tolist()

        if len(dup) > 0:
            print(f'potential duplication error {dup}')

        try:
            cursor.executemany(sql, data)
            self.connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()

    def check_index_exists(self, table_name, index_name):
        """Check if an index exists in the table."""
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return False
        cursor = self.connection.cursor()
        check_index_query = f"""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE table_schema = '{self.database}'
              AND table_name = '{table_name}'
              AND index_name = '{index_name}';
            """
        cursor.execute(check_index_query)
        exists = cursor.fetchone()[0]
        cursor.close()
        return exists > 0

    def update_table_schema(self, table_name):
        """Update the table schema."""
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return
        cursor = self.connection.cursor()
        try:
            if not self.check_index_exists(table_name, 'unique_allure_id'):
                cursor.execute(f"ALTER TABLE `{self.database}`.`{table_name}` ADD UNIQUE INDEX `unique_allure_id` (`id`);")
                self.connection.commit()
            cursor.execute(f"""
            ALTER TABLE `{self.database}`.`{table_name}`
            DROP PRIMARY KEY,
            ADD PRIMARY KEY (`report_name`(100), `datetime`, `suite`(100), `name`(100), `start_time`);
            """)
            self.connection.commit()
            print("Table schema updated successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()


    def execute_many(self, query, params):
        
        # self.cursor.executemany(insert_query, test_cases)
        """Execute a SQL query."""
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established.")
            return
        cursor = self.connection.cursor()
        try:
            cursor.executemany(query, params)
            self.connection.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error: '{e}' occurred")
        finally:
            cursor.close()

    def execute_sql_file(self, file_path):
        """Execute SQL commands from a file."""
        if not self.connection or not self.connection.is_connected():
            print("Not connected to the database.")
            return

        try:
            with open(file_path, 'r') as file:
                sql_commands = file.read().split(';')
            
            cursor = self.connection.cursor()
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            self.connection.commit()
            print("SQL commands executed successfully.")
        except Error as e:
            print(f"Error while executing SQL commands: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        finally:
            if cursor:
                cursor.close()