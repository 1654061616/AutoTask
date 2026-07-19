from .step_executor import StepExecutor


def create_step_executor(variable_manager, logger):
    from .mouse import MouseOperations
    from .keyboard import KeyboardOperations
    from .image_recognition import ImageRecognition
    from .window import WindowOperations
    from .condition import ConditionEvaluator
    from .loop import LoopController
    from .excel import ExcelOperations
    from .control import FlowControl

    mouse = MouseOperations()
    keyboard = KeyboardOperations()
    image_recognition = ImageRecognition()
    window = WindowOperations()
    condition = ConditionEvaluator()
    condition.set_image_ops(image_recognition)
    condition.set_window_ops(window)
    loop = LoopController()
    excel = ExcelOperations()
    flow_control = FlowControl()

    return StepExecutor(
        mouse=mouse,
        keyboard=keyboard,
        image_recognition=image_recognition,
        window=window,
        condition=condition,
        loop=loop,
        excel=excel,
        flow_control=flow_control,
        variable_manager=variable_manager,
        logger=logger,
    )