import subprocess


def create():
    product = "Example App"  # can be written in uppercase
    # if " " in product:
    #    name = product.replace(" ", "_").lower()
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
        f.writelines(flutter_deps)
    with open("permissions.txt", "w") as f:
        f.writelines(permissions)


if __name__ == "__main__":
    create()
