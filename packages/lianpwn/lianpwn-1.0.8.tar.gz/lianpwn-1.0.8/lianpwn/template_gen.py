# template_gen.py
import os
from pwncli import *
from lianpwn import lg_err, lg_suc, lg_inf
import subprocess


def generate_template():
    if os.path.exists("exp.py"):
        lg_err("File 'exp.py' already exists.")
        subprocess.run(["mv", "exp.py", "exp.py.bak"])
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   expBy : @eastXueLian
#   Debug : ./exp.py debug  ./pwn -t -b b+0xabcd
#   Remote: ./exp.py remote ./pwn ip:port

from lianpwn import *

cli_script()
set_remote_libc("libc.so.6")

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

ia()
"""

    with open("exp.py", "w") as f:
        f.write(content)

    os.chmod("exp.py", 0o755)

    lg_inf("Template 'exp.py' created successfully!")


def generate_template_nocli():
    if os.path.exists("exp_nocli.py"):
        lg_err("File 'exp_nocli.py' already exists.")
        subprocess.run(["mv", "exp_nocli.py", "exp_nocli.py.bak"])
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   expBy : @eastXueLian

from lianpwn import *
import sys

context.log_level = "debug"
context.arch = "amd64"
context.terminal = ["tmux", "sp", "-h", "-l", "120"]

LOCAL = 1
filename = "./pwn"
if LOCAL:
    io = process(filename)
else:
    remote_service = ""
    remote_service = remote_service.strip().split(":")
    io = remote(remote_service[0], int(remote_service[1]))
elf = ELF(filename, checksec=False)
libc = ELF(elf.libc.path, checksec=False)


def ru(a, drop=False):
    return io.recvuntil(a, drop)


rl = lambda a=False: io.recvline(a)
rn = lambda x: io.recvn(x)
s = lambda x: io.send(x)
sl = lambda x: io.sendline(x)
sa = lambda a, b: io.sendafter(a, b)
sla = lambda a, b: io.sendlineafter(a, b)
ia = lambda: io.interactive()
dbg = lambda text=None: gdb.attach(io, text)
i2b = lambda c: str(c).encode()
u32_ex = lambda data: u32(data.ljust(4, b"\\x00"))
u64_ex = lambda data: u64(data.ljust(8, b"\\x00"))


'''
while True:
    try:

        ia()
    except:
        io.close()
        if LOCAL:
            io = process(filename)
        else:
            io = remote(remote_service[0], int(remote_service[1]))
'''
"""

    with open("exp_nocli.py", "w") as f:
        f.write(content)

    os.chmod("exp_nocli.py", 0o755)

    lg_inf("Template 'exp_nocli.py' created successfully!")


def kernel_upload_template():
    if os.path.exists("upload.py"):
        lg_err("File 'upload.py' already exists.")
        subprocess.run(["mv", "upload.py", "upload.py.bak"])
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   expBy : @eastXueLian
#   Remote: ./upload.py remote ip:port -nl

import subprocess
from lianpwn import *
from base64 import b64encode, b64decode

cli_script()

io: tube = gift.io

ia()

commands = []

# lg_inf("compiling exp.c")
# if subprocess.run("musl-gcc -static -o exp.bin exp.c", shell=True).returncode:
#     lg_err("compile error")
# lg_suc("compile finished")

exp_data_list = []
SPLIT_LENGTH = 0x400
with open("./exp.bin", "rb") as f_exp:
    exp_data = b64encode(f_exp.read()).decode()
lg_inf("Data length: " + str(len(exp_data)))
for i in range(len(exp_data) // SPLIT_LENGTH):
    exp_data_list.append(exp_data[i * SPLIT_LENGTH : (i + 1) * SPLIT_LENGTH])
if not len(exp_data) % SPLIT_LENGTH:
    exp_data_list.append(exp_data[(len(exp_data) // SPLIT_LENGTH) :])


commands.append("cd /tmp; touch ./exp.b64")
for i in exp_data_list:
    commands.append("echo -n '" + i + "'>> ./exp.b64")
commands.append("base64 -d ./exp.b64 > ./exp; chmod +x ./exp; ./exp")
commands.append("cat /flag")

for i in commands:
    sl(i)

lg_suc(str(len(commands)) + " commands sent.")
ia()
"""

    with open("upload.py", "w") as f:
        f.write(content)

    os.chmod("upload.py", 0o755)

    lg_inf("Template 'upload.py' created successfully!")
