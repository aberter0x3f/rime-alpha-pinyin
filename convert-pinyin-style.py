#!/usr/bin/env python3

import sys
import pypinyin
from multiprocessing import Pool, cpu_count

# 将自定义词典定义为全局变量，方便子进程加载
CUSTOM_PHRASES = {
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


def init_worker():
    """
    子进程初始化函数，每个进程只调用一次
    """
    pypinyin.load_phrases_dict(CUSTOM_PHRASES)


def process_line(line):
    """
    单行处理逻辑
    """
    line = line.strip()
    if not line:
        return ""

    w = line.split("\t")

    if len(w) < 2:
        return line

    # 转换拼音
    py_list = pypinyin.lazy_pinyin(w[0], style=pypinyin.TONE3, neutral_tone_with_five=True)
    py_str = " ".join(py_list)

    if len(w) > 2:
        return f"{w[0]}\t{py_str}\t" + "\t".join(w[2:])
    else:
        return f"{w[0]}\t{py_str}"


def process_chunk(lines):
    """
    处理一组行）
    """
    return [process_line(line) for line in lines]


def chunk_generator(file_path, chunk_size=1000):
    """
    生成器：将文件内容按块读取
    """
    with open(file_path, "r", encoding="utf-8") as f:
        chunk = []
        for line in f:
            chunk.append(line)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


def main(input_path, output_path):
    num_workers = cpu_count()
    chunk_size = 2000

    with Pool(processes=num_workers, initializer=init_worker) as pool:
        # 使用 imap 保持顺序并节省内存
        chunks = chunk_generator(input_path, chunk_size)

        with open(output_path, "w", encoding="utf-8") as f_out:
            for result_chunk in pool.imap(process_chunk, chunks):
                for line in result_chunk:
                    f_out.write(line + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 script.py input.yaml output.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
