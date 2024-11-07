import os


class Filemanagement(object):
    def __init__(self):
        print("initializing File management class")

    def write_to_file(self, message, file_name) -> None:
        if file_name is not str:
            file_name = str(file_name)

        print(f"writing {message} to {file_name}")
        root = os.path.dirname(os.path.abspath(__file__))
        real_root = root.replace("classes", "")
        path = os.path.join("files/", file_name)
        file_path = os.path.join(real_root, path)
        try:
            with open(file_path, 'a') as write_file:
                write_file.write(f"\n{message}")
        except FileNotFoundError as f:
            print(f"File not found: {file_path}, error: {f}")
            print("now creating file")
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
        f = open(file_name, "a")
        f.write(message)
        f.close()

    @staticmethod
    def check_if_file_exists(file_name) -> bool:
        root = os.path.dirname(os.path.abspath(__file__))
        real_root = root.replace("classes", "")
        path = os.path.join("files/", file_name)
        file_path = os.path.join(real_root, path)
        return os.path.exists(file_path)

    @staticmethod
    def read_file_per_line(file_name) -> list[str]:
        if file_name is not str:
            file_name = str(file_name)

        print(f"reading {file_name}")
        root = os.path.dirname(os.path.abspath(__file__))
        real_root = root.replace("classes", "")
        path = os.path.join("files/", file_name)
        file_path = os.path.join(real_root, path)
        try:
            with open(file_path, 'r') as read_file:
                file_lines = read_file.read().split('\n')
        except FileNotFoundError as f:
            print(f"File not found: {file_path}, error: {f}")
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

    @staticmethod
    def read_whole_file(file_name):
        root = os.path.dirname(os.path.abspath(__file__))
        real_root = root.replace("classes", "")
        path = os.path.join("files/", file_name)
        file_path = os.path.join(real_root, path)
        try:
            with open(file_path, 'r') as read_file:
                park = read_file.read()
                park = park.splitlines()
                print(f" {park}  \n")
            return park
        except FileNotFoundError as f:
            print(f"File not found: {file_path}, error: {f}")
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
    def create_file(file_name) -> None:
        if file_name is not str:
            file_name = str(file_name)

        print(f"creating {file_name}")
        root = os.path.dirname(os.path.abspath(__file__))
        real_root = root.replace("classes", "")
        path = os.path.join("files/", file_name)
        file_path = os.path.join(real_root, path)

        dir_path = file_path.replace(file_name, "")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        try:
            with open(file_path, 'w'):
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

    @staticmethod
    def delete_file(file_name) -> None:
        if file_name is not str:
            file_name = str(file_name)

        print(f"deleting {file_name}")
        root = os.path.dirname(os.path.abspath(__file__))
        real_root = root.replace("classes", "")
        path = os.path.join("files/", file_name)
        file_path = os.path.join(real_root, path)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file_name} has been deleted")
            else:
                print(f"{file_name} has not been there at all")
        except PermissionError as p:
            print(f"Permission error, error: {p}")
            exit(403)
        except IOError as i:
            print(f"IO error, error: {i}")
            exit(2)
        except Exception as e:
            print(f"An General exception found, error: {e}")
            exit(1)

    @staticmethod
    def open_file(file_name, is_sdk) -> None:
        if file_name is not str:
            file_name = str(file_name)
            print(f"opening {file_name}")
            root = os.path.dirname(os.path.abspath(__file__))
            real_root = root.replace("classes", "")
            if not is_sdk:
                path = os.path.join("files/", file_name)
            else:
                path = os.path.join("", file_name)
            file_path = os.path.join(real_root, path)
            os.startfile(file_path)

    @staticmethod
    def delete_from_file(file_name, what) -> None:
        if file_name is not str:
            file_name = str(file_name)

        print(f"removing {what} from {file_name}")
        root = os.path.dirname(os.path.abspath(__file__))
        real_root = root.replace("classes", "")
        path = os.path.join("files/", file_name)
        file_path = os.path.join(real_root, path)
        # Open the file in read mode
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove lines containing the specified string
        new_lines = [line for line in lines if what not in line]

        # Open the file in write mode
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
