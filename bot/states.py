from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    waiting_for_admin_id = State()


class FeedbackStates(StatesGroup):
    waiting_for_user_message = State()
    waiting_for_admin_reply = State()
    waiting_for_spam_message = State()


class UserState(StatesGroup):
    waiting_for_name = State()


class TaskState(StatesGroup):
    waiting_for_task_2_1_answer = State()
    waiting_for_task_2_2_answer = State()
    waiting_for_task_2_3_answer = State()
    waiting_for_task_2_4_answer = State()
    waiting_for_task_2_5_answer = State()
    waiting_for_task_3_1_answer = State()
    waiting_for_task_3_2_answer = State()
    waiting_for_task_3_3_answer = State()
    waiting_for_task_3_4_answer = State()
    waiting_for_task_3_5_answer = State()
    waiting_for_task_5_1_answer = State()
    waiting_for_task_5_2_answer = State()
    waiting_for_task_5_3_answer = State()
    waiting_for_task_5_4_answer = State()
    waiting_for_task_5_5_answer = State()
    waiting_for_task_6_1_answer = State()
    waiting_for_task_6_2_answer = State()
    waiting_for_task_6_3_answer = State()
    waiting_for_task_6_4_answer = State()
    waiting_for_task_6_5_answer = State()
    waiting_for_task_8_1_answer = State()
    waiting_for_task_8_2_answer = State()
    waiting_for_task_8_3_answer = State()
    waiting_for_task_8_4_answer = State()
    waiting_for_task_8_5_answer = State()
    waiting_for_task_10_1_answer = State()
    waiting_for_task_10_2_answer = State()
    waiting_for_task_10_3_answer = State()
    waiting_for_task_10_4_answer = State()
    waiting_for_task_10_5_answer = State()
    waiting_for_task_11_1_answer = State()
    waiting_for_task_11_2_answer = State()
    waiting_for_task_11_3_answer = State()
    waiting_for_task_11_4_answer = State()
    waiting_for_task_11_5_answer = State()
    waiting_for_task_15_1_answer = State()
    waiting_for_task_15_2_answer = State()
    waiting_for_task_15_3_answer = State()
    waiting_for_task_15_4_answer = State()
    waiting_for_task_15_5_answer = State()
    waiting_for_task_19_1_answer = State()
    waiting_for_task_19_2_answer = State()
    waiting_for_task_19_3_answer = State()
    waiting_for_task_19_4_answer = State()
    waiting_for_task_19_5_answer = State()
    waiting_for_task_22_1_answer = State()
    waiting_for_task_22_2_answer = State()
    waiting_for_task_22_3_answer = State()
    waiting_for_task_22_4_answer = State()
    waiting_for_task_22_5_answer = State()
    waiting_for_task_24_1_answer = State()
    waiting_for_task_24_2_answer = State()
    waiting_for_task_24_3_answer = State()
    waiting_for_task_24_4_answer = State()
    waiting_for_task_24_5_answer = State()
    waiting_for_task_25_1_answer = State()
    waiting_for_task_25_2_answer = State()
    waiting_for_task_25_3_answer = State()
    waiting_for_task_25_4_answer = State()
    waiting_for_task_25_5_answer = State()
    waiting_for_task_26_1_answer = State()
    waiting_for_task_26_2_answer = State()
    waiting_for_task_26_3_answer = State()
    waiting_for_task_26_4_answer = State()
    waiting_for_task_26_5_answer = State()
