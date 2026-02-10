import re

# Leer el archivo
with open('c:\\Users\\india\\Documents\\GitHub\\Refaccionaria-Oviedo\\REFACCIONARIA\\app\\static\\cajas_cierre.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Contar llaves
open_braces = content.count('{')
close_braces = content.count('}')

# Contar paréntesis
open_parens = content.count('(')
close_parens = content.count(')')

# Contar corchetes
open_brackets = content.count('[')
close_brackets = content.count(']')

print(f'Llaves: {open_braces} vs {close_braces} - {"OK" if open_braces == close_braces else "ERROR"}')
print(f'Paréntesis: {open_parens} vs {close_parens} - {"OK" if open_parens == close_parens else "ERROR"}')
print(f'Corchetes: {open_brackets} vs {close_brackets} - {"OK" if open_brackets == close_brackets else "ERROR"}')

# Encontrar líneas problemáticas
lines = content.split('\n')
print(f'\nTotal de líneas: {len(lines)}')

# Ver últimas 10 líneas
print('\nÚltimas 10 líneas:')
for i, line in enumerate(lines[-10:], start=len(lines)-9):
    print(f'{i}: {line}')
