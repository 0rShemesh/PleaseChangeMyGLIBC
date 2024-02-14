# Inject your GLIBC to ELF 
Giving the ability to patch any elf to other glibc that you've compiled.

# Requirements

* Python 3
* An linux machine with toolchain

Ubuntu:
```bash
sudo apt-get install -y build-essential
pip3 install -r requirements.txt
```


# Usage

## Compile GLIBC

Compiling:
```bash
./compile_glibc.sh
```

note: make sure you've pull GLIBC
for change the GLIBC version you may want to change the tag of `GLIBC_TAG` in `compile_glibc.sh` script


## Patch/Inject to other GLIBC version

```bash
./inject_glibc.sh my_program
```


# Example

generic c file
```c
// test.c
#include <stdio.h>


int main(void)
{
    printf("Hello World!\n");
    return 0;
}
```

## Compile

```bash
gcc -o test test.c
```

## Check current glibc  
```bash
$ ldd test
	linux-vdso.so.1 (0x00007ffdc39c3000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1588200000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f15884a3000)
```

## Inject the glibc  
```bash
./inject_glibc.sh test
```

checking the patched one:  
```bash
$ ldd patched_test 
	linux-vdso.so.1 (0x00007ffce55fd000)
	libc.so.6 => builds/glibc-2.39/libc.so.6 (0x00007effeca07000)
	/lib64/ld-linux-x86-64.so.2 (0x00007effecbf7000)
```

## running  

```bash
chmod +x ./patched_test
LD_LIBRARY_PATH="builds/glibc-2.39/elf/ld.so" ./patched_test
# print back Hello World!
```

or by the script:  
```bash
chmod +x ./patched_test
./run_binary.sh ./patched_test
```

### Permanent Bash alias
```bash
echo "alias run_binary=\"${pwd}/run_binary.sh\"" >> ~/.bashrc
```

