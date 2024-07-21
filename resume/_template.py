import yaml

template = {}

def get_template_data(template_type):
    with open(f'assets/sentences/template_{template_type}.yaml', "r") as stream:
        template = yaml.safe_load(stream)
        return template

def get_template_sentences(template_type):
    template_data = get_template_data(template_type)
    return template_data["default_sentences"]