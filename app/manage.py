from src.common.management.base import MethodCaller, ManagementParser


if __name__ == '__main__':
    MethodCaller(args=ManagementParser()())()
