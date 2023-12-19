import subprocess, sys, os, argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "jarPath",
    nargs="?",
    type=str,
    help="Specify the path to the server core file",
)

parser.add_argument(
    "-javaPath",
    dest="java_path",
    type=str,
    help="Specify the path to the java executable",
)

parser.add_argument(
    "-jarArgs",
    dest="jar_args",
    type=str,
    help="Specify the arguments to be passed to the server core file",
)

args = parser.parse_args()

assert args.jar_path and os.path.isfile(args.jar_path), "Invalid jar path"

java_path = args.java_path or "java"
jar_args = args.jar_args or ""

result = False
server_process = subprocess.Popen(
    f"{java_path} -jar {args.jar_path} {jar_args} nogui",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
print("[OMCS] 🚀 Starting server...")

for line in server_process.stdout:
    print(line, end="")
    if 'For help, type "help" or "?"' in line:
        result = True
        server_process.send_signal(3)

server_process.wait()
if not result:
    print("[OMCS] ❌ Server compatability failed")
    sys.exit(1)
else:
    print("[OMCS] ✅ Server compatability verified")
    sys.exit(0)
