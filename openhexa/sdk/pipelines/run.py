class CurrentRun:
    def add_file_output(self, path: str, *, name: str = None):
        print(f"Sending output with path {path} and name: {name}")

    def add_database_output(self, table_name: str, *, name: str = None):
        print(f"Sending output with table_name {table_name} and name: {name}")


current_run = CurrentRun()
