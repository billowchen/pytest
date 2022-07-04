import random


class RandomHandler(object):

    base_data = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9']

    def random_base(self, num=2):
        return format(random.random(), '.{}f'.format(num))

    def random_uniform(self, max, min=0, num=2):
        return format(random.uniform(min, max), '.{}f'.format(num))

    def random_randint(self, min, max):
        return random.randint(min, max)

    def random_choices(self, *args):
        return random.choices(*args)[0]

    def random_sample(self, num, *args):
        return random.sample(*args, num)

    def random_shuffle(self, *args):
        random.shuffle(*args)
        return args[0]

    def random_string(self, num):
        return ''.join(self.random_sample(num, self.base_data))
