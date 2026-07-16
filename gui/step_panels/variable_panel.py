from . import StepConfigPanel


class SetVariablePanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.var_name_edit = self.add_lineedit("变量名", placeholder="输入变量名称")

        self.var_value_edit = self.add_lineedit("变量值", placeholder="支持表达式和变量引用，如 ${var_name}")

        self.value_type_combo = self.add_combobox("值类型", ["字符串", "数字", "布尔值", "列表", "字典"])

        self.add_separator()
        self.add_delay_section()

    def get_config(self):
        type_map = ["string", "number", "boolean", "list", "dict"]
        return {
            "var_name": self.var_name_edit.text(),
            "var_value": self.var_value_edit.text(),
            "value_type": type_map[self.value_type_combo.currentIndex()],
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        self.var_name_edit.setText(config.get("var_name", ""))
        self.var_value_edit.setText(config.get("var_value", ""))

        type_map = {"string": 0, "number": 1, "boolean": 2, "list": 3, "dict": 4}
        self.value_type_combo.setCurrentIndex(type_map.get(config.get("value_type", "string"), 0))

        self.delay_spin.setValue(config.get("delay", 0))


class GetVariablePanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.var_name_edit = self.add_lineedit("变量名", placeholder="输入要获取的变量名称")

        self.output_mode_combo = self.add_combobox("输出方式", ["输出日志", "弹窗显示", "复制到剪贴板"])

        self.add_separator()
        self.add_delay_section()

    def get_config(self):
        output_map = ["log", "popup", "clipboard"]
        return {
            "var_name": self.var_name_edit.text(),
            "output_mode": output_map[self.output_mode_combo.currentIndex()],
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        self.var_name_edit.setText(config.get("var_name", ""))

        output_map = {"log": 0, "popup": 1, "clipboard": 2}
        self.output_mode_combo.setCurrentIndex(output_map.get(config.get("output_mode", "log"), 0))

        self.delay_spin.setValue(config.get("delay", 0))