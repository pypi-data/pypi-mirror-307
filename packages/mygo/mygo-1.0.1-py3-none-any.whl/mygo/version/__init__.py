from typing import Optional


class SimpleVersion(str):
    def __init__(self, version):
        self.version: str = version
        self.version_resolved: tuple = self.resolver()
        self.version_number: Optional[int] = None

    def resolver(self) -> tuple:
        # 将版本字符串转换为元组
        return tuple(map(int, (self.version.split("."))))

    # 版本大小比较的运算符重载方法
    # 大于
    def __gt__(self, other: 'SimpleVersion'):
        # 类型检查
        if not isinstance(other, SimpleVersion):
            raise TypeError("比较对象不是SimpleVersion类型")
        if self.version_number:
            return self.version_number > other.version_number
        else:
            # 按位比较 self.version_resolved 和 other.version_resolved
            for i in range(len(self.version_resolved)):
                if self.version_resolved[i] > other.version_resolved[i]:
                    return True
                elif self.version_resolved[i] < other.version_resolved[i]:
                    return False
            return False

    # 小于
    def __lt__(self, other: 'SimpleVersion'):
        if not isinstance(other, SimpleVersion):
            raise TypeError("比较对象不是SimpleVersion类型")
        if self.version_number:
            return self.version_number < other.version_number
        else:
            for i in range(len(self.version_resolved)):
                if self.version_resolved[i] < other.version_resolved[i]:
                    return True
                elif self.version_resolved[i] > other.version_resolved[i]:
                    return False
            return False
