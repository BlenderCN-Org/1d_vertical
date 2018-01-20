# 1d_vertical

**Проверка**

Для показа работы весь код представлен в виде аддона.

Для проверки скачать код:
Clone or download - download ZIP - открыть Blender - установить аддон обычным образом (Install add-on From File)

В Т-панели, вкладка Vertical:

Две кнопки - две версии алгоритма:
- Vertical Test 0 - проверяется длина максимальной проекции ребра полигона на ось Z
- Vertical Test 1 - проверяется максимальная проекция полигона на ось Z (соответствует ТЗ)

На тестовой сцене оба алгоритма выдают одинаковый результат.

**Встраивание**

Для включения в другой проект необходм только модуль vertical.py

После регистрации данного модуля в Blender API стандартным способом (вызов функции register) для вызова доступен оператор:

    bpy.ops.vertical.select()

У оператора есть один параметр algorithm, дефолтное значение = 1, что соответсвует вызову алгоритма 1 (соответствует в ТЗ)

Для вызова оператора с версией алгоритма 0, нужно передать указание в параметре:

    bpy.ops.vertical.select(algorithm=0)

Version history:
-
**v.0.0.0.**
- Dev start