def confirm_overwrite(path) -> bool:
    try:
        answer = input(path + " already exists. Overwrite? [y/N] ")
        return answer.strip().lower() == "y"
    except EOFError:
        return False
