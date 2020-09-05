import subprocess

class Exporter(object):
    def __init__(self, path):
        self.path = path

    def export_obj(self, root):
        with open(self.path, 'w') as o:
            o.write(root.dump_xcsg())

        process = subprocess.Popen(['xcsg', '--obj', self.path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
