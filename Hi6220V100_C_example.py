import soc

Hi6220V100_path = "./data/soc/hikey/Hi6220V100.json"
output_name = "Hi6220V100.h"


def main():
    # load modules path
    loader = soc.Loader()
    # load SoC memmap and modules data
    hi6220v100 = loader.load(Hi6220V100_path)

    soc_header = ""

    # include
    soc_header += "#include <stdint.h>\n"
    soc_header += "\n"

    # output register structure
    for k, v in hi6220v100["modules"].items():
        soc_header +=  "typedef struct {\n"
        addrp = 0
        reserve_count = 0
        for kk, vv in sorted(v["register"].items(), key=lambda x:x[1]["offset"]):
            offset = int(vv["offset"], 16)
            if addrp != offset:
                # fill unused memory
                soc_header += "    volatile uint8_t  RESERVED{count}[{size}];\n".format(count=reserve_count, size=(offset - addrp))
                reserve_count = reserve_count + 1
                addrp = offset
            if int(vv["size"], 16) == 4:
                soc_header +=  "    volatile uint32_t {name};\n".format(name=kk)
            else:
                soc_header += "    volatile uint32_t {name}[{size}];\n".format(name=kk, size=int(int(vv["size"], 16)/4))
            addrp = addrp + int(vv["size"], 16)
        soc_header +=  "}} {name}_Type;\n".format(name=v["name"])
        soc_header += "\n"

    # output memmap
    soc_header += "// memmap\n"
    for k, v in hi6220v100["memmap"].items():
        tname = hi6220v100["modules"][v["module"]]["name"]
        soc_header += "#define {name} ({tname}_Type *)({addr})\n".format(
            name=k, tname=tname, addr=v["address"])

    soc_header += "\n"
    soc_header += "\n"

    with open(output_name, "w") as f:
        f.write(soc_header)


if __name__ == "__main__":
    main()
