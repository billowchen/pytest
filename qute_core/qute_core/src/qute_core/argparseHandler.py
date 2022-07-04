import argparse


class ArgparseHandler(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='设置运行参数')

    def get_args(self):
        self.parser.add_argument('--testcase', type=str, default='')
        self.parser.add_argument('--env', type=str, default='test')
        self.parser.add_argument('--mark', type=str, default=None)
        self.parser.add_argument('--report', type=bool, default=False)
        self.parser.add_argument('--db', type=str, default='false')
        args = self.parser.parse_args()
        return args.testcase, args.env, args.mark, args.report, args.db
