import subprocess


class SubprocessHandler(object):

    def popen(self, cmd):
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output
