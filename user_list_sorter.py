import sys
import yaml


def main(args):
    data = []
    with open(args[1], "r", encoding="utf-8") as src:
        src_data = yaml.load(src, Loader=yaml.SafeLoader)
        data = sorted(src_data, key=lambda x: x[list(src_data[0].keys())[0]])
        print(data)
    with open(args[1], "w", encoding="utf-8", newline="\n") as dst:
        yaml.dump(
            data,
            dst,
            encoding="utf-8",
            allow_unicode=True,
            default_flow_style=False,
            default_style='"',
        )


if __name__ == "__main__":
    main(sys.argv)
