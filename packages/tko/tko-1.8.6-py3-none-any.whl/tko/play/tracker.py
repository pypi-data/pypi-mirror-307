import datetime
import os
import shutil
import argparse
import csv

class Track:
    def __init__(self):
        self.timestamp = ""
        self.files: list[str] = []
        self.result: str = ""

    def set_timestamp(self, timestamp: str):
        self.timestamp = timestamp
        return self
    
    def set_files(self, files: list[str]):
        self.files = [os.path.basename(f) for f in files]
        return self
    
    def set_result(self, result: str):
        self.result = result
        return self
    
    def track_to_column(self):
        return [self.timestamp, self.result, ";".join(self.files)]


class Tracker:

    def __init__(self):
        self._files: list[str] = []
        self._folder: str = ""
        self._result: str = "None"
        self.log_file = "track.csv"
        self.track_folder = ".track"
        self.extension = ".log"
        self.posfix = ":"
        self.timestamp_size = len(self.get_timestamp() + self.posfix)
        self.extension_size = len(self.extension)

    def set_files(self, files: list[str]):
        self._files = [os.path.abspath(f) for f in files]
        return self
    
    def set_result(self, result: str):
        self._result = result
        return self
    
    def set_percentage(self, percentage: int):
        self._result = "{}%".format(str(percentage).ljust(3, "0"))
        return self

    def get_log_full_path(self):
        return os.path.join(self._folder, self.log_file)

    def set_folder(self, folder: str):
        self._folder = os.path.join(folder, self.track_folder)
        return self
    
    # in format: YYYY-MM-DD HH:MM:SS
    def get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def get_file_history(self, file: str, file_list: list[str]):
        filename = os.path.basename(file)
        file_list = [f for f in file_list if f[self.timestamp_size:-self.extension_size] == filename]
        return sorted(file_list)

    def save_file_with_timestamp_prefix(self, timestamp: str, file: str) -> str:
        filename = os.path.basename(file)
        destination = os.path.join(self._folder, f"{timestamp}{self.posfix}{filename}{self.extension}")
        shutil.copy(file, destination)
        return destination
        

    def store(self):
        os.makedirs(self._folder, exist_ok=True)
        file_list = os.listdir(self._folder)
        file_list = [f for f in file_list if f.endswith(self.extension)]

        files_in_this_version: list[str] = []
        timestamp = self.get_timestamp()

        for file in self._files:
            saved_files = self.get_file_history(file, file_list)
            last_file = saved_files[-1] if len(saved_files) > 0 else ""
            if last_file == "":
                stored = self.save_file_with_timestamp_prefix(timestamp, file)
                files_in_this_version.append(stored)
                # print("Saved file: ", stored)
            else:
                change_time = os.path.getmtime(file)
                last_file_path = os.path.join(self._folder, last_file)
                last_time = os.path.getmtime(last_file_path)

                if change_time > last_time:
                    stored = self.save_file_with_timestamp_prefix(timestamp, file)
                    # print("Updated file: ", file)
                    files_in_this_version.append(stored)
                else:
                    files_in_this_version.append(last_file)
        

        log_file = self.get_log_full_path()
        track = Track().set_timestamp(timestamp).set_files(files_in_this_version).set_result(self._result)
        with open(log_file, encoding="utf-8", mode="a") as f:
            writer = csv.writer(f)
            writer.writerow(track.track_to_column())

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description="Track files changes.")
        parser.add_argument("files", metavar="files", type=str, nargs="+", help="files to be tracked.")
        args = parser.parse_args()
        
        tracker = Tracker().set_folder(".track").set_files(args.files)
        tracker.store()
