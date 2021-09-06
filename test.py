import pdfplumber
import re
import math
import decimal
import pandas as pd
from collections import namedtuple

path = "/home/franco/Downloads/Resumen de Cuenta 29-07-2021.pdf"
with pdfplumber.open(path) as pdf:
    page = pdf.pages[1]
    text = page.extract_text()
    words = page.extract_words()

line_height = decimal.Decimal(36)

dict = {}
lines = []
for i in range(28, math.floor(page.height), 36):
    dict[str(i)] = []
    lines.append(i)


def sort_by_x(e):
    return e['x0']

def get_closest(value, lista):
    closest = 0
    cd = 0

    floored_value = math.floor(value)

    for i in lista:
        diff = abs(i - floored_value)
        # print(f"floored_value:{floored_value!s} diff: {diff!s} i: {i!s}")
        if cd == 0:
            cd = diff
            closest = i
        if diff < cd:
            # print(f"diff: {diff!s} cd: {cd!s} ---- {diff!s} < {cd!s}")
            cd = diff
            closest = i
    print(closest)
    return closest


def group_closest(lista):
    offset = 10

    current_key = 0

    result = {}

    print(f"len: {len(lista) - 1}")

    for k, v in enumerate(lista):
        if k < len(lista) - 1:
            value = v['top']
            next_value = lista[k + 1]['top']
            diff = abs(value - next_value)
            text = v['text']

            # print(f"---text: {text} ---")
            if current_key == 0:
                # print("ck == 0 inicializando valor")
                current_key = str(value)

            elif diff <= offset:
                # print(f"diff es menor que offset")
                # print(f"ck: {current_key}, val_text: {text}")
                if not current_key in result:
                    # print(f"key no existe, creando")
                    result[current_key] = []
                result[current_key].append(v)
                # print(f"haciendo append de {text} en result[{current_key}]")
            elif diff > offset:
                current_key = str(value)
                # print(f"diff > offset, cambiando current_key por: {current_key}")
                result[current_key] = []
                result[current_key].append(v)
                # print(f"haciendo append de {text} en result[{current_key}]")

        # print("-------------\n\n")

    for k,v in result.items():
        v.sort(key=sort_by_x)
        # for word in v:
        #     print({'x': word['x0'], 't': word['text'], 'y': word['top']})
        # print("----\n\n")
    return result


def sort_by_xy(arr):
    for _ in range(0, len(arr) -1):
        for j in range(0, len(arr) -1):
            if arr[j]['x0'] > arr[j + 1]['x0']:
                arr[j], arr[j+1] = arr[j+1], arr[j]
            if arr[j]['top'] > arr[j + 1]['top']:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr


result = group_closest(words)






t = result['721.853']
for i in t:
    v = {}

# lines = []
# print(result['721.853'])

# res = sort_by_xy(result['721.853'])
# for i in res:
#     print({'x': i['x0'], 'y': i['top']})


# for line in lines:
#     print(line, end="\n\n")

# for k,words in result.items():
#     for word in words:
#         print({'x': word['x0'], 'y': word['top']})
#     print("----\n\n")









# descripcion = re.compile(r'(?:\s\d{4}\s)?[-a-zA-Z_ \*.]{3,}(?:[0-9]{4}\s)?')

# consumo = re.compile(r'-?\$[0-9 ,.]+')

# Consumo = namedtuple('Consumo', 'descripcion consumo')

# lines = []
# for k,v in result.items():
#     line = []
#     for word in v:
#         line.append(word['text'])
#     lines.append(" ".join(line))


# descripciones = []
# consumos = []

# for line in lines:

#     desc = descripcion.search(line)
#     cons = consumo.search(line)

#     if desc:
#         descripciones.append(desc.group())

#     if cons:
#         consumos.append(cons.group())







pdf.close()
