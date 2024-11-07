import os


class FileManagement(object):
    def __init__(self, base_directory=None):
        print("Initializing File management class")
        # Use the provided base_directory or default to the current working directory
        self.base_directory = base_directory or os.path.dirname(os.path.abspath(__file__))

    def write_to_file(self, message, file_name) -> None:
        if not isinstance(file_name, str):
            file_name = str(file_name)

        print(f"Writing {message} to {file_name}")
        path = os.path.join(self.base_directory, "files", file_name)
        try:
            with open(path, 'a') as write_file:
                write_file.write(f"\n{message}")
        except FileNotFoundError as f:
            print(f"File not found: {path}, error: {f}")
            print("Now creating file")
            self.create_file(file_name)
        except PermissionError as p:
            print(f"Permission error, error: {p}")
            exit(403)
        except IOError as i:
            print(f"IO error, error: {i}")
            exit(2)
        except Exception as e:
            print(f"A General exception found, error: {e}")
            exit(1)

    @staticmethod
    def write_single_line_to_file(message, file_name) -> None:
        with open(file_name, "a") as f:
            f.write(message)

    def check_if_file_exists(self, file_name) -> bool:
        if not isinstance(file_name, str):
            file_name = str(file_name)
        path = os.path.join(self.base_directory, "files", file_name)
        return os.path.exists(path)

    def read_file_per_line(self, file_name) -> list[str]:
        if not isinstance(file_name, str):
            file_name = str(file_name)

        print(f"Reading {file_name}")
        path = os.path.join(self.base_directory, "files", file_name)
        try:
            with open(path, 'r') as read_file:
                file_lines = read_file.read().split('\n')
        except FileNotFoundError as f:
            print(f"File not found: {path}, error: {f}")
        except PermissionError as p:
            print(f"Permission error, error: {p}")
            exit(403)
        except IOError as i:
            print(f"IO error, error: {i}")
            exit(2)
        except Exception as e:
            print(f"A General exception found, error: {e}")
            exit(1)

        for line in file_lines:
            print(line)

        return file_lines

    def read_whole_file(self, file_name):
        path = os.path.join(self.base_directory, "files", file_name)
        try:
            with open(path, 'r') as read_file:
                content = read_file.read()
                print(f"Content: {content}\n")
            return content.splitlines()
        except FileNotFoundError as f:
            print(f"File not found: {path}, error: {f}")
        except PermissionError as p:
            print(f"Permission error, error: {p}")
            exit(403)
        except IOError as i:
            print(f"IO error, error: {i}")
            exit(2)
        except Exception as e:
            print(f"A General exception found, error: {e}")
            exit(1)

    def create_file(self, file_name) -> None:
        if not isinstance(file_name, str):
            file_name = str(file_name)

        print(f"Creating {file_name}")
        path = os.path.join(self.base_directory, "files", file_name)

        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        try:
            with open(path, 'w'):
                print(f"{file_name} has been created")
        except PermissionError as p:
            print(f"Permission error, error: {p}")
            exit(403)
        except IOError as i:
            print(f"IO error, error: {i}")
            exit(2)
        except Exception as e:
            print(f"A General exception found, error: {e}")
            exit(1)

    def delete_file(self, file_name) -> None:
        if not isinstance(file_name, str):
            file_name = str(file_name)

        print(f"Deleting {file_name}")
        path = os.path.join(self.base_directory, "files", file_name)

        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"{file_name} has been deleted")
            else:
                print(f"{file_name} does not exist")
        except PermissionError as p:
            print(f"Permission error, error: {p}")
            exit(403)
        except IOError as i:
            print(f"IO error, error: {i}")
            exit(2)
        except Exception as e:
            print(f"A General exception found, error: {e}")
            exit(1)

    def open_file(self, file_name, is_sdk) -> None:
        if not isinstance(file_name, str):
            file_name = str(file_name)
        print(f"Opening {file_name}")
        if not is_sdk:
            path = os.path.join(self.base_directory, "files", file_name)
        else:
            path = os.path.join("", file_name)
        os.startfile(path)

    def delete_from_file(self, file_name, what) -> None:
        if not isinstance(file_name, str):
            file_name = str(file_name)

        print(f"Removing {what} from {file_name}")
        path = os.path.join(self.base_directory, "files", file_name)
        with open(path, 'r') as file:
            lines = file.readlines()

        new_lines = [line for line in lines if what not in line]

        with open(path, 'w') as file:
            file.writelines(new_lines)