import os
from qute_core.argparseHandler import ArgparseHandler
from qute_core.run import run


if __name__ == '__main__':
    cur_path = os.getcwd()
    testcase, env, mark, report, db = ArgparseHandler().get_args()

    run(cur_path, testcase, 'qa', mark, True, 'true')
