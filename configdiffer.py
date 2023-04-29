#!/usr/bin/python3

import subprocess
import sys
import tempfile
import os

def get_pkgname(filename):
    output = subprocess.run(["/usr/bin/dpkg","-S",filename], capture_output=True, env={"LC_ALL":"C.UTF-8"})
    if output.returncode != 0:
        raise NameError("Unable to find associated package from {}.".format(filename))
    return output.stdout.decode("utf-8").split(":")[0]

def get_pkgversion(pkgname):
    output = subprocess.run(["/usr/bin/dpkg","-s",pkgname], capture_output=True, env={"LC_ALL":"C.UTF-8"})
    if output.returncode != 0:
        raise NameError("Unable to find version of package {}".format(pkgname))
    lines=output.stdout.decode("utf-8").split("\n")
    for line in lines:
        if line.startswith("Version"):
            tokens = line.split(":")
            return ":".join(tokens[1:]).strip()
    raise NameError("Unable to find version of package {}".format(pkgname))

def download_pkg(name, version, dirname):
    print("Downloading package...", end=" ")
    output = subprocess.run(["/usr/bin/apt","download","{}={}".format(name, version)], capture_output=True, cwd=dirname, env={"LC_ALL":"C.UTF-8"})
    if output.returncode != 0:
        raise RuntimeError("Unable to download package, is package too old?")
    files = os.listdir(dirname)
    if len(files) != 1:
        raise RuntimeError("Expecting only 1 file.")
    filename = files[0]
    print("Done.\nFile saved to {}/{}".format(dirname, filename))
    return filename

def extract_pkg(filename, dirname):
    filepath = os.path.join(dirname, filename)
    output = subprocess.run(["/usr/bin/dpkg","--extract", filepath, dirname], capture_output=True, env={"LC_ALL":"C.UTF-8"})
    output.check_returncode()

def show_diff(input_path, dirname):
    # input_path is absolute path
    extracted_path = os.path.join(dirname, input_path[1:])
    print("diff below:")
    output = subprocess.run(["/usr/bin/diff", input_path, extracted_path], capture_output=True, env={"LC_ALL":"C.UTF-8"})
    output.check_returncode()
    print(output.stdout.decode("utf-8"))

def main():
    if len(sys.argv) < 2:
        print("Usage: ./configdiffer.py /path/to/config/file")
        return
    filename = os.path.abspath(sys.argv[1])
    pkgname = get_pkgname(filename)
    version = get_pkgversion(pkgname)
    print ("File {} is associated with package {}, installed version {}".format(filename, pkgname, version))
    with tempfile.TemporaryDirectory() as dirname:
        pkg_filename = download_pkg(pkgname, version, dirname)
        extract_pkg(pkg_filename, dirname)
        show_diff(filename, dirname)

main()
