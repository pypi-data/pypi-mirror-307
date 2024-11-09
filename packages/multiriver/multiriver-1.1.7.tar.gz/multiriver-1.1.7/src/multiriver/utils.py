import datetime
import re
import collections

PATTERNS_MAPPING = {
    "MM": "(?P<MM>[0-5]?\d)",
    "hh": "(?P<hh>[0-1]?[0-9]|2[0-3])",
    "h": "(?P<hh>[0]?[0-9]|1[0-2])",
    "AM": "(?P<AMPM>AM|PM)",
    "PM": "(?P<AMPM>AM|PM)",
    "dd": "(?P<dd>3[0-1]|[1-2][0-9]|0[1-9])",
    "d": "(?P<dd>3[0-1]|[1-2][0-9]|0?[1-9])",
    "mm": "(?P<mm>0[1-9]|1[0-2])",
    "m": "(?P<mm>[0-1]?[0-2])",
    "mon": "(?P<mm>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
    "month": "(?P<mm>(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|"
             "Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)",
    "yyyy": "(?P<yyyy>[12]\d{3})",
    "yy": "(?P<yyyy>\d{2}(\d{2})?)",
    "ee": "(?P<ee>\d{13})",
    "e": "(?P<e>\d{10})",
    "entity_name": "(?P<entity_name>.+)"
}

def liberal_format(format_this, *args, **kwargs):
    """loose implementation of string.format().
    perform replacements without enforcing keys (i.e. replace what you can,
    do not raise an error on missing key)"""

    ptrn = re.compile('.*?(\{.*?\}).*?') # noqa
    formatted = format_this
    to_replace = [item for item in re.findall(ptrn, format_this)]
    for item in to_replace:
        if kwargs.get(item[1:-1]) is not None:
            formatted = formatted.replace(item, str(kwargs.get(item[1:-1])))
    return formatted

def make_template_groups(literal_prefix, template):
    """ Making the template groups, so it takes the literal predfix and template,
        and return the group of the template objects in the literal prefix.

        i.e: {yyyy}-{mm}-{dd}/10938/{yyyy}{mm}{dd}
              prefix: 2017-12-01/10938/20171201

        returns: {"{yyyy}": "2017", "{mm}": "12", "{dd}": "01"}
    """

    formatted_template = liberal_format(template, **PATTERNS_MAPPING)
    try:
        tmp_groups = re.match(formatted_template, literal_prefix, re.IGNORECASE)
        if tmp_groups:
            return tmp_groups.groupdict()
        else:
            return {}
    except Exception:
        return {}


def recursive_update(source, overrides, overwrite_nones=False):
    """Update a nested dictionary or similar mapping.

    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if value is not None and not overwrite_nones or (overwrite_nones is True):
            if isinstance(value, collections.Mapping):
                returned = recursive_update(source.get(key, {}), value)
                source[key] = returned
            else:
                source[key] = overrides[key]
    return source

def convert_template_to_regex(template):
    return liberal_format(template, **PATTERNS_MAPPING)


def generate_rivers_template(user_template, file_names):
    result = []
    for file_name in file_names:
        template_group = make_template_groups(file_name, user_template)
        entity_name = template_group.get('entity_name')
        if not entity_name:
            continue
        result.append(
            {
                'template': liberal_format(user_template, **{'entity_name': entity_name}),
                'entity_name': entity_name
            }
        )
    return result

if __name__ == '__main__':

    file_name = 'oleks/another_entity_123-2023-06.csv'
    user_template = 'oleks/{entity_name}.csv'
    template_group = make_template_groups(file_name, user_template)
    entity_name = template_group.get('entity_name')
    result_template = liberal_format('{entity_name}-{yy}-{mm}', **{'entity_name': entity_name})
    pass


def process_data(data_to_process: dict, convert_to_oi: list=None,
                 to_delete: list=None, to_date: list = None, to_replace: dict = None):

    if convert_to_oi is None:
        convert_to_oi = []
    if to_delete is None:
        to_delete = []
    if to_date is None:
        to_date = []
    if to_replace is None:
        to_replace = {}

    def recursive_process(data):
        if isinstance(data, dict):
            keys_to_process = list(data.keys())
            for key in keys_to_process:
                # Delete the key if it's in the to_delete list
                if key in to_delete:
                    del data[key]
                # Wrap the value if the key is in the convert_to_oi list
                elif key in convert_to_oi and data[key]:
                    data[key] = {"$oid": str(data[key])}
                # Recurse for nested dictionaries
                elif key in to_date and isinstance(data[key], str):
                    try:
                        timestamp = int(datetime.datetime.fromisoformat(data[key].replace("Z", "+00:00")).timestamp() * 1000)
                        data[key] = {"$date": timestamp}
                    except ValueError:
                        pass  # Skip if the value isn't in a valid date format
                elif key in to_replace:
                    data[key] = to_replace[key]

                else:
                    recursive_process(data[key])
        elif isinstance(data, list):
            for item in data:
                recursive_process(item)

    recursive_process(data_to_process)
    return data_to_process
