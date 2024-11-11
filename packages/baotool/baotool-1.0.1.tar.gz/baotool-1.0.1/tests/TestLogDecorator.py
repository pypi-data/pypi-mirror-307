import random
import time
import unittest

from baotool.decorator import log


# 基本用法
@log
def print_user_info(name, age):
    # 随机休眠1到3秒
    time.sleep(random.randint(1, 3))
    if age is None:
        raise ValueError('方法执行异常: age is None')
    if age < 0:
        raise ValueError('方法执行异常: age < 0')
    print(name, age)
    return f'{name} 有 {age} 岁了!'


# 自定义日志输出
@log(logfn=lambda i: print(i.msg, '------------------'))
def print_user_info_1(name, age):
    pass


# 制定部分入参打印日志, 不打印出参
@log(ins=(0,), inskw=('height',))
def print_user_info_2(name, age, height):
    return f'{name} 有 {age} 岁了! 身高 {height}'


@log(out=False)
def print_user_info_3(name, age, height):
    return f'{name} 有 {age} 岁了! 身高 {height}'


class TestLogDecorator(unittest.TestCase):
    def setUp(self):
        # 可以在这里初始化一些共享资源
        self.data = [('张飞', 123, 179), ('李逵', None, 154), ('丽萨', -1, 180)]

    def test_1(self):
        for name, age in self.data:
            with self.subTest(f'name={name},age={age}', name=name, age=age):
                ex = None
                try:
                    print_user_info(name, age)
                except Exception as e:
                    ex = e
                # if age is None or age < 0:
                #     self.assertIsNone(ex)

    def test_2(self):
        for name, age in self.data:
            with self.subTest(f'name={name},age={age}', name=name, age=age):
                print_user_info_1(name, age)

    def test_3(self):
        for d in self.data:
            with self.subTest(f'{d}', data=d):
                print_user_info_2(d[0], d[1], height=d[2])

    def test_4(self):
        for d in self.data:
            with self.subTest(f'{d}', data=d):
                print_user_info_3(d[0], d[1], height=d[2])


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=False)
