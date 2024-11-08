import requests


def get_req(url):
    req = requests.get(url)
    ok = req.status_code == requests.codes.ok
    available = 'Available' if ok == False else 'Not Available'
    return available, req.status_code, ok


def get_status_package(p_name: str):
    url = f"https://pypi.org/project/{p_name}/"

    return get_req(url)


def get_status_package_cli_multi(p_names):
    p_names = [x for x in p_names if x.strip()]
    for name in p_names:
        get_status_package_cli(name)
    return True

def get_status_package_cli(p_name: str):
    if ',' in p_name:
        return get_status_package_cli_multi(p_name.split(','))
    r, a, ok = get_status_package(p_name)
    if ok:
        template = print(f"\n  ❌ `{p_name}` is already taken.")
    else:
        template = print(f"\n. 🎉 Wow! `{p_name}` is available!")
    print(template)
    return r, a, ok
