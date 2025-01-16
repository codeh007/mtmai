import yaml
def load_yaml_file(filename, label='config file', loader=yaml.Loader):
    """Load a yaml config file.
    """
    try:
        with open(filename, "r") as file:
            res = yaml.load(file.read(), Loader=loader) or {}
            if not isinstance(res, dict):
                msg = f"Please ensure that {label} consists of key value pairs."
                raise ValueError(f"Invalid {label}: {filename}", msg)
            return res

    except yaml.YAMLError as err:
        if hasattr(err, 'problem_mark'):
            mark = getattr(err, 'problem_mark')
            problem = getattr(err, 'problem')
            message = f"Could not read {label} {filename}:"
            message += "\n filename: {filename}, mark line: {mark.line}, column: {mark.column} {problem}"
        elif hasattr(err, 'problem'):
            problem = getattr(err, 'problem')
            message = f"Could not read {label} {filename}: {problem}"
        else:
            message = f"Could not read {label} {filename}: YAML Error"

        suggestion = f"There is a syntax error in your {label} - please fix it and try again."

        raise ValueError(message, suggestion)

    except OSError as err:
        msg = "Please ensure the file exists and you have the required access privileges."
        raise ValueError(f"Could not open {label} {filename}: {err.strerror}", msg)



def save_dict_to_yaml(dict_value: dict, save_path: str):
    """dict保存为yaml"""
    with open(save_path, 'w') as file:
        # logger.info(f"保存clash yaml 配置文件")
        file.write(yaml.dump(dict_value, allow_unicode=True))
