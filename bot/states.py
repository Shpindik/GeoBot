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
