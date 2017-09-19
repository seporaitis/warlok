import re


DuplicatedFieldMessage = "Field '{field}' occurs twice in the message.".format


def get_message_template(fields):
    message = []
    title = ""
    for field, value in fields.items():
        if field == 'title':
            title = value.strip("\n")
        else:
            message.append("{}: {}".format(field.title(), value).strip())

    return (title + "\n\n" + "\n\n\n".join(message) + "\n")


def parse_message_into_fields(message, fields):
    regex = re.compile("^(?P<field>{}):(?P<text>.*)$".format("|".join(x.title() for x in fields)))
    lines = message.split("\n")

    field_name = 'title'
    seen = set()
    field_map = {}
    result = {name: [] for name in fields}

    for idx, line in enumerate(lines):
        if 'title' not in seen:
            field_name = 'title'
            lines[idx] = line.replace("Title:", "").strip()
            seen.add('title')
        else:
            match = regex.match(line)
            if match:
                field_name = match.group('field').strip().lower()
                if field_name in seen:
                    raise ValueError(DuplicatedFieldMessage(field=field_name.title()))
                seen.add(field_name)
                lines[idx] = match.group('text').strip()

        field_map[idx] = field_name

    for idx, line in enumerate(lines):
        result[field_map[idx]].append(line)

    for field_name, content in result.items():
        result[field_name] = "\n".join(content).strip(" \n")

    return result
