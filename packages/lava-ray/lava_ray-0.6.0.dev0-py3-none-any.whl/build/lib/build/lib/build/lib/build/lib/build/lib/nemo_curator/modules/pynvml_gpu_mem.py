import datetime
import getopt
import os
import sys
import time

import pynvml


def get_printable_util_mem(dev_count, peak_mem):
    res = ""
    for index in range(dev_count):
        dev = pynvml.nvmlDeviceGetHandleByIndex(index)

        mem = pynvml.nvmlDeviceGetMemoryInfo(dev)
        util = pynvml.nvmlDeviceGetUtilizationRates(dev)

        used = mem.used // (1024 ** 2)
        total = mem.total // (1024 ** 2)
        peak_mem[index] = max(peak_mem[index], used)

        dev_str = str(index).rjust(2)
        util_str = str(util.gpu).rjust(3)
        used_str = str(used).rjust(5)
        total_str = str(total).rjust(5)
        peak_mem_str = str(peak_mem[index]).rjust(5)

        if res != "":
            res += "\n"
        res += "GPU #%s: %s%% | %s MB/%s MB [Peak mem: %s MB]" % (
            dev_str,
            util_str,
            used_str,
            total_str,
            peak_mem_str,
        )
    return res


def get_printable_nvlink(dev_count, nvlink_conn):
    res = ""
    for index in range(dev_count):
        dev = pynvml.nvmlDeviceGetHandleByIndex(index)

        def convert_unit(v, width):
            def float_precision(v):
                p = 0
                if v > 100:
                    p = 1
                elif v > 10:
                    p = 2
                else:
                    p = 3
                return format(v, "." + str(p) + "f")

            if v < 1024:
                return float_precision(v).rjust(width) + "  B"
            elif v < 1024 ** 2:
                return float_precision(v / 1024).rjust(width) + " KB"
            elif v < 1024 ** 3:
                return float_precision(v / (1024 ** 2)).rjust(width) + " MB"
            elif v < 1024 ** 4:
                return float_precision(v / (1024 ** 3)).rjust(width) + " GB"
            elif v < 1024 ** 5:
                return float_precision(v / (1024 ** 4)).rjust(width) + " TB"

        transfer = ""
        for i in range(nvlink_conn[index]):
            for i in range(10):
                try:
                    nvlink_counter = pynvml.nvmlDeviceGetNvLinkUtilizationCounter(
                        dev, i, 0
                    )
                    break
                except pynvml.NVMLError:
                    import time

                    time.sleep(0.1)
                    pass
            transfer += "%s:%s | " % (
                convert_unit(nvlink_counter["rx"], 5),
                convert_unit(nvlink_counter["tx"], 5),
            )

        dev_str = str(index).rjust(2)

        if res != "":
            res += "\n"
        res += "GPU #%s | %s" % (dev_str, transfer)
    return res


def get_nvlink_connections(dev_count):
    nvlink_conn = []
    for index in range(dev_count):
        dev = pynvml.nvmlDeviceGetHandleByIndex(index)
        conn = 0

        # Up to 6 NVLink connections
        for nvl in range(6):
            try:
                pynvml.nvmlDeviceGetNvLinkUtilizationCounter(dev, nvl, 0)
                conn += 1
            except pynvml.NVMLError_InvalidArgument:
                continue
        nvlink_conn.append(conn)
    return nvlink_conn


def run_loop(interval, report_nvlink=False):
    pynvml.nvmlInit()
    dev_count = pynvml.nvmlDeviceGetCount()
    peak_mem = [0] * dev_count

    if report_nvlink is True:
        nvlink_conn = get_nvlink_connections(dev_count)
        nvlink_head1 = (
            " " * 8
            + "".join(["|       Link %d      " % (i,) for i in range(max(nvlink_conn))])
            + "|"
        )
        nvlink_head2 = " " * 8 + "|       RX:TX       " * 6 + "|"

    while True:
        printable_util_mem = get_printable_util_mem(dev_count, peak_mem)

        if report_nvlink is True:
            printable_nvlink = get_printable_nvlink(dev_count, nvlink_conn)

        os.system("clear")
        print(datetime.datetime.now())
        print(printable_util_mem)

        if report_nvlink is True:
            print("\nNVLink:")
            print("-" * 129)
            print(nvlink_head1)
            print(nvlink_head2)
            print(printable_nvlink)
            print("-" * 129)

        time.sleep(interval)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:", ["interval=", "report-nvlink"])
    except getopt.GetoptError:
        print("test.py -i <interval>")
        sys.exit(2)

    report_nvlink = False
    for opt, arg in opts:
        if opt == "-h":
            print("pynvml_query_memory.py -i <interval> [--report-nvlink]")
            sys.exit()
        elif opt in ("-i", "--interval"):
            interval = float(arg)
        elif opt in ("--report-nvlink"):
            report_nvlink = True
    run_loop(interval, report_nvlink=report_nvlink)


if __name__ == "__main__":
    main(sys.argv[1:])
