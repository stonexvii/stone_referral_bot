from aiogram.utils.keyboard import InlineKeyboardBuilder

from collections import namedtuple

# from database.tables import QuestionsTable
from .callback_data import UserMainMenu, BackButton
import config
from classes.inline_buttons import UserMainMenuButton

Button = namedtuple('Button', ['text', 'callback'])


def ikb_user_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        UserMainMenuButton('Зачем нужна реферальная ссылка?', button='about_referral'),
        UserMainMenuButton('Твои рефералы', button='my_referrals'),
        UserMainMenuButton('Кто такой Стоун?', url=config.CHANNEL_URL),
        UserMainMenuButton('Связь со Стоуном', button='contact_stone'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())

    keyboard.adjust(1, 2, 1)
    return keyboard.as_markup()


def ikb_back(user_name: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Назад',
        callback_data=BackButton(
            user_name=user_name,
        )
    )
    return keyboard.as_markup()


# def ikb_question_menu(question_id: int):
#     keyboard = InlineKeyboardBuilder()
#     buttons = [
#         Button('Отправить', 'send'),
#         Button('Сколько?', 'amount'),
#         Button('Результаты', 'results'),
#         Button('Удалить', 'delete'),
#         Button('Сбросить', 'reset'),
#         Button('Назад', 'back'),
#     ]
#     for button in buttons:
#         keyboard.button(
#             text=button.text,
#             callback_data=QuestionNavigate(
#                 button=button.callback,
#                 question_id=question_id,
#             ),
#         )
#     keyboard.adjust(3, 2)
#     return keyboard.as_markup()


def ikb_show_answer(answers: list[tuple[int, int, int]], answers_text: dict[int, str]):
    keyboard = InlineKeyboardBuilder()
    if answers:
        for position, answer_id, answer_amount in answers:
            keyboard.button(
                text=answers_text[answer_id],
                callback_data=ShowAnswer(
                    button='target',
                    position=position,
                    target_answer=answer_id,
                    answer_amount=answer_amount,
                ),
            )
    else:
        keyboard.button(
            text='Очистить',
            callback_data=ShowAnswer(
                button='reset',
                position=0,
                target_answer=0,
                answer_amount=0,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
