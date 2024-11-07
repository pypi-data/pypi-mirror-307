import importlib.resources
import json
from typing import Any

import webview

from .btype import Null


def show(
    itemList: Any,
    *,
    title: str = '标题',
    width: int = 500,
    height: int = 400,
    labelWidth: int = 160,
    resizable: bool = False,
    debug: bool = False,
):
    '''
    bform.show([
        bform.InputItem('用户名', 'username', placeholder='Enter your username'),
        bform.PasswordItem('密码', 'password', placeholder='Enter your password'),
        bform.CheckboxItem('记住我', 'remember'),
    ])
    '''

    with importlib.resources.path('beni.resources.web-form', 'index.html') as file:

        # test start
        # file = './beni/resources/web-form/index.html'
        # test end

        result = Null

        class Api():

            def done(self, value: Any):
                nonlocal result
                result = value
                window.destroy()

        def init():
            value = json.dumps({
                'labelWidth': f'{labelWidth}px',
                'itemList': itemList,
            })
            window.evaluate_js('window.__show( JSON.parse(`' + value + '`) );')

        window = webview.create_window(
            title,
            str(file),
            js_api=Api(),
            width=width,
            height=height,
            resizable=resizable,
        )
        webview.start(init, debug=debug)

        return result


# ----------------------------------------


def InputItem(
    name: str,
    key: str = '',
    *,
    value: str = '',
    placeholder: str = '',
    autofocus: bool = False,
):
    return {'type': 'InputItem', **locals()}


def PasswordItem(
    name: str,
    key: str = '',
    *,
    value: str = '',
    placeholder: str = '',
    autofocus: bool = False,
):
    return {'type': 'PasswordItem', **locals()}


def TextareaItem(
    name: str,
    key: str = '',
    *,
    value: list[str] = [],
    placeholder: str = '',
    autofocus: bool = False,
    rows: int = 3,
):
    return {'type': 'TextareaItem', **locals()}


def CheckboxItem(
    name: str,
    key: str = '',
    *,
    value: bool = False,
    text: str = '',
):
    return {'type': 'CheckboxItem', **locals()}


def TextItem(
    name: str,
    key: str = '',
    *,
    text: str = '',
):
    return {'type': 'TextItem', **locals()}


def RadioGroupItem(
    name: str,
    key: str = '',
    *,
    value: Any = None,
    options: list[tuple[str, Any]] = [],
):
    return {'type': 'RadioGroupItem', **locals()}
