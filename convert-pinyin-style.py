#!/usr/bin/env python3

import sys
import pypinyin


pypinyin.load_phrases_dict(
    {
        "重复": [["chóng"], ["fù"]],
        "换行": [["huàn"], ["háng"]],
        "最美的": [["zuì"], ["meǐ"], ["de"]],
        "相似": [["xiāng"], ["sì"]],
        "重庆": [["chóng"], ["qìng"]],
        "最长": [["zuì"], ["cháng"]],
        "重载": [["chóng"], ["zǎi"]],
        "重画": [["chóng"], ["huà"]],
        "长整": [["cháng"], ["zhěng"]],
        "字长": [["zì"], ["cháng"]],
        "超长": [["chāo"], ["cháng"]],
        "模长": [["mó"], ["cháng"]],
        "线长": [["xiàn"], ["cháng"]],
        "可重": [["kě"], ["chóng"]],
        "去重": [["qù"], ["chóng"]],
        "沃尔什": [["wò"], ["ěr"], ["shí"]],
        "吖丙啶": [["ā"], ["bǐng"], ["dìng"]],
        "吖丁啶": [["ā"], ["dīng"], ["dìng"]],
        "吖啶橙": [["ā"], ["dìng"], ["chéng"]],
        "吖啶黄": [["ā"], ["dìng"], ["huáng"]],
        "吖啶酮": [["ā"], ["dìng"], ["tóng"]],
        "吖啶": [["ā"], ["dìng"]],
        "吖庚环": [["ā"], ["gēng"], ["huán"]],
        "吖唑": [["ā"], ["zuò"]],
        "重传": [["chóng"], ["chuán"]],
        "重读": [["chóng"], ["dú"]],
        "重发": [["chóng"], ["fā"]],
        "重写": [["chóng"], ["xiě"]],
        "重做": [["chóng"], ["zuò"]],
        "调整图层": [["tiáo"], ["zhěng"], ["tú"], ["céng"]],
        "行数": [["háng"], ["shù"]],
        "行高": [["háng"], ["gāo"]],
        "串行": [["chuàn"], ["xíng"]],
        "勒文海姆": [["lè"], ["wén"], ["hǎi"], ["mǔ"]],
        "多行": [["duō"], ["háng"]],
        "标识": [["biāo"], ["shí"]],
    }
)


def process_rime_file(input_path, output_path):
    output_lines = []
    with open(input_path, "r", encoding="utf-8") as f_in:
        for line in f_in:
            line = line.strip()

            w = line.strip().split("\t")

            if len(w) < 2:
                output_lines.append(line + "\n")
                continue

            py = pypinyin.lazy_pinyin(w[0], style=pypinyin.TONE3, neutral_tone_with_five=True)
            if len(w) > 2:
                output_line = f"{w[0]}\t" + " ".join(py) + "\t" + "\t".join(w[2:]) + "\n"
            else:
                output_line = f"{w[0]}\t" + " ".join(py) + "\n"
            output_lines.append(output_line)

    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write("".join(output_lines))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 script.py input.yaml output.txt")
        sys.exit(1)
    process_rime_file(sys.argv[1], sys.argv[2])
