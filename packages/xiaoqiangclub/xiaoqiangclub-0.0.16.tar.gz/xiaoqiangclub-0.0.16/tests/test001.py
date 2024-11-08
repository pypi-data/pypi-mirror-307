def my_decorator(func):
    print("装饰器开始执行")  # 装饰器的内容
    def wrapper():
        print("函数被调用")
        return func()
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# 结果：
# 装饰器开始执行
# say_hello 函数在被定义时就已经执行了装饰器中的 print
