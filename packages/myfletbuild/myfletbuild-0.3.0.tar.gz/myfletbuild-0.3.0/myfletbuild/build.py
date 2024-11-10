import subprocess


def build():
    with open("product.txt", "r") as f:
        product = f.read()
    with open("name.txt", "r") as f:
        name = f.read()
    with open("org-domain.txt", "r") as f:
        org_domain = f.read()
    with open("flutter-deps.txt", "r") as f:
        flutter_deps = f.read()
    with open("permissions.txt", "r") as f:
        permissions = f.readlines()
    print(product)
    print(name)
    print(org_domain)
    print(flutter_deps)
    print(permissions)
    # subprocess.run(["flet"])


if __name__ == "__main__":
    build()
