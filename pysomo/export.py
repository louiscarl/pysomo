import subprocess
from pathlib import Path


class Exporter(object):
    def __init__(self, path):
        self.path = Path.cwd() / path

    def export(self, root, file_type):
        with open('temp.xcsg', 'w') as o:
            o.write(root.dump_xcsg())

        process = subprocess.Popen(
            ['xcsg', f'--{file_type}', 'temp.xcsg'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        if self.path.exists():
            self.path.unlink()

        p = Path.cwd() / f'temp.{file_type}'
        stdout, stderr = process.communicate()

        if not p.exists():
            raise Exception(
                'The exported file was not generated.',
                {
                    'stdout': stdout,
                    'stderr': stderr
                })

        p.rename(self.path)

    def export_obj(self, root):
        self.export(root, 'obj')
