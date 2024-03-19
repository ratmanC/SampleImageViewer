# スタックの仕組み
class Stack:

    def __init__(self):
        self.stack = []
        self._pointer = 0

    @property
    def pointer(self):
        return self._pointer

    def push(self, item):
        if len(self.stack) > self._pointer:
            for i in range(self._pointer, len(self.stack)):
                del self.stack[self._pointer]

        # スタックが10件以上溜まっているなら、古いものから破棄する処理
        if len(self.stack) >= 10:
            del self.stack[0]

        self.stack.append(item)
        if self._pointer < 10:
            self._pointer += 1

        print("len{},pointer{}".format(len(self.stack), self._pointer))

    def undoPop(self):
        if len(self.stack) == 1 or self._pointer == 1:
            return

        pop_obj = self.stack[self._pointer - 2]
        self._pointer -= 1
        print("len{},pointer{}".format(len(self.stack), self._pointer))
        return pop_obj

    def redoPop(self):
        if len(self.stack) == 0 or len(self.stack) <= self._pointer:
            return

        print("viewpoint{}".format(self._pointer))
        pop_obj = self.stack[self._pointer]
        self._pointer += 1
        print("len{},pointer{}".format(len(self.stack), self._pointer))
        return pop_obj
