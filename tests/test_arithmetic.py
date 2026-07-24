import sys
sys.path.insert(0, '.')
from core.variables import VariableManager

vm = VariableManager()
vm.set_variable('a', 10)
vm.set_variable('b', 3)

print("--- 测试 set_variable 算术 ---")
vm.set_variable('result', '${a} + ${b}')
print(f"a + b = {vm.get_variable('result')}")  # 13

vm.set_variable('mul', '${a} * ${b}')
print(f"a * b = {vm.get_variable('mul')}")  # 30

vm.set_variable('div', '${a} / ${b}')
print(f"a / b = {vm.get_variable('div')}")  # 3.333...

vm.set_variable('text', 'hello')
print(f"text = {vm.get_variable('text')}")  # hello

vm.set_variable('number', '42')
print(f"number = {vm.get_variable('number')}")  # 42

vm.set_variable('neg', '-${a}')
print(f"-a = {vm.get_variable('neg')}")  # -10

vm.set_variable('paren', '(${a} + ${b}) * 2')
print(f"(a+b)*2 = {vm.get_variable('paren')}")  # 26

vm.set_variable('mixed', '${a} + ${b} * 2')
print(f"a + b * 2 = {vm.get_variable('mixed')}")  # 16

print("\n全部通过!")