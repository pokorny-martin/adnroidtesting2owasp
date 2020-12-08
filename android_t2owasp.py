import argparse
import android_testing2owasp.framework_coverage as framework_coverage

parser = argparse.ArgumentParser(description="")
parser.add_argument("-aw", type=str, help="Path to Androwarn output")
parser.add_argument("-ap", type=str, help="Path to AndroPyTool output")
parser.add_argument("-ab", type=str, help="Path to Androbugs output")
parser.add_argument("-sf", type=str, help="Path to MobSF output")
parser.add_argument("-o", type=str, help="Path to output directory")

args = parser.parse_args()
frameworks = []
for key, value in args.__dict__.items():
    if value is None:
        continue
    if key == "aw":
        try:
            frameworks.append(framework_coverage.FrameworkCoverage(value))
            frameworks[-1].parse("Androwarn")
        except FileNotFoundError:
            print("Invalid path to Androwarn output was given")
    elif key == "ap":
        try:
            frameworks.append(framework_coverage.FrameworkCoverage(value))
            frameworks[-1].parse("AndroPyTool")
        except FileNotFoundError:
            print("Invalid path to AndroPyTool output was given")
    elif key == "ab":
        try:
            frameworks.append(framework_coverage.FrameworkCoverage(value))
            frameworks[-1].parse("AndroBugs")
        except FileNotFoundError:
            print("Invalid path to AndroBugs output was given")
    elif key == "sf":
        try:
            frameworks.append(framework_coverage.FrameworkCoverage(value))
            frameworks[-1].parse("MobSF")
        except FileNotFoundError:
            print("Invalid path to MobSF output was given")


final = framework_coverage.FrameworkCoverage()
for framework in frameworks:
    final.combine(framework)

try:
    with open(args.o+"/out.json", "w+") as f:
        f.write(final.to_json())
except Exception as e:
    if isinstance(e, TypeError):
        with open("out.json", "w+") as f:
            f.write(final.to_json())
    else:
        print("Cannot create output file, please check output directory")

