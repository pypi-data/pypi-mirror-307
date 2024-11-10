import subprocess


def create():
    product = "Example App"  # can be written in uppercase
    if " " in product:
        name = product.replace(" ", "_").lower()
    name = product.lower()
    org_domain = "com.example"
    flutter_deps = [""]
    permissions = [""]
    with open("product.txt", "w") as f:
        f.write(product)
    with open("name.txt", "w") as f:
        f.write(name)
    with open("org-domain.txt", "w") as f:
        f.write(org_domain)
    with open("flutter-deps.txt", "w") as f:
        f.write(flutter_deps)
    with open("permissions.txt", "w") as f:
        for permission in permissions:
            f.writelines(permission)


def build():
    with open("product.txt", "r") as f:
        product=f.read()
    with open("name.txt", "r") as f:
        name=f.read()
    with open("org-domain.txt", "r") as f:
        org_domain=f.read()
    with open("flutter-deps.txt", "r") as f:
        flutter_deps=f.read()
    with open("permissions.txt", "r") as f:
        permissions=f.readlines()
    print(product)
    print(name)
    print(org_domain)
    print(flutter_deps)
    print(permissions)
    #subprocess.run(["flet"])
