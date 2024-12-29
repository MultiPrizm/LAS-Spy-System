import os, json

if not os.path.isfile("../.env"):

        with open("../.env", 'w') as file:
            file.write('')


def save_to_env(key, value, env_file='.env'):

    try:
        with open(env_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f'{key}='):
            lines[i] = f'{key}={value}\n'
            updated = True
            break

    if not updated:
        lines.append(f'{key}={value}\n')

    with open(env_file, 'w') as file:
        file.writelines(lines)