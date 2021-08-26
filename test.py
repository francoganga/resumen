import pdfplumber
import re
import math
import decimal

path = "/home/franco/Downloads/Resumen de Cuenta 29-07-2021.pdf"
with pdfplumber.open(path) as pdf:
    page = pdf.pages[2]
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

        # print(result)
    for k,v in result.items():
        print("[[")
        v.sort(key=sort_by_x)
        for word in v:
            print(word['text'], end=" ")
        print("]]\n")





group_closest(words)

# asd = list(map(lambda i: {'top': i['top'], 'text': i['text']}, words))
# for i in asd:
#     print(i)










# t = [
#         {'text': 'Gold', 'x0': decimal.Decimal('355.552'), 'x1': decimal.Decimal('381.368'), 'top': decimal.Decimal('28.326'), 'bottom': decimal.Decimal('42.326'), 'upright': True, 'direction': 1},
#         {'text': 'Infinity', 'x0': decimal.Decimal('314.000'), 'x1': decimal.Decimal('352.808'), 'top': decimal.Decimal('28.326'), 'bottom': decimal.Decimal('42.326'), 'upright': True, 'direction': 1}
#     ]



# print(t)
# rr = t.sort(key=sort_by_x)
# print(t)



# for i in words:
#     closest = get_closest(i['top'], lines)
#     dict[str(closest)].append(i)

# for key in dict:
#     print(f"line: {key!s}")
#     for line in dict[key]:
#         print(line['text'], end=" ")
#     print("\n")





pdf.close()
