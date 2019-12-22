import argparse
import time
import random


def write(data, f):
    f.write(data + "\n")
    f.flush()


def generate_msl_file(path):
    random.seed(42)
    header = [
        "Time", "SecL", "RPM/100", "MAP", "TP", "O2", "MAT", "CLT", "Engine", "Gego",
        "Gair", "Gwarm", "Gbaro", "Gammae", "TPSacc", "Gve", "PW", "Gve2", "PW2",
        "DutyCycle1", "DutyCycle2", "pulseWidth2", "veCurr22", "idleDC", "BCDuty3",
        "Spark Angle", "EGT", "Fuel Press", "Knock", "RPM", "barometer", "NOS On",
        "batt V", "porta", "portb", "portc", "portd", "Trip Meter Miles",
        "Odometer Miles", "MPH", "Power", "Torque",
    ]
    units = [
        "", "sec", "r100", "", "", "", "", "", "bits", "%", "%", "%", "%", "%", "%", "%", "ms ",
        "%", "ms", "", "", "ms", "%", "%", "%", "", "", "", "", "", "", "", "", "", "", "",
        "", "Miles", "Miles", "MPH", "HP", "lbft",
    ]
    data_formatter = "\t".join("{}" for _ in range(len(header)))
    with open(path, "w") as f:
        write('"MSnS-extra format 029q *********: MS1/Extra rev 029v  ************"', f)
        write('"Capture Date: Sat Jan 26 08:07:14 EST 2019"', f)
        # Write header
        write("\t".join(header), f)
        write("\t".join(units), f)
        trace_time = 0.0
        start_time = time.time()
        while True:
            data = [trace_time, ] + [random.randint(0, 100)
                                     for _ in range(1, len(header))]
            write(data_formatter.format(*data), f)
            trace_time = trace_time + (time.time() - start_time)
            start_time = time.time()
            time.sleep(.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    generate_msl_file(args.file)
