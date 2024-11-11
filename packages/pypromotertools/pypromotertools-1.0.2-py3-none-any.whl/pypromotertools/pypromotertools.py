#! python3
# coding=utf-8
#
# Author   : BiomedicalPulsar
# Pipeline :
# Code     : pyPromoterTools
# Function : A collection of tools for acquiring gene promoter
# Example  :





#====================================================================================================
#===================================     IMPORT PACKAGE     =========================================
#====================================================================================================
# Aim: IMPORT PACKAGE
#

## Aim: os
import os

## Aim: argparse
import argparse
from optparse import OptionParser

## Aim: pandas
import pandas as pd

## Aim: numpy
import numpy as np

## Aim: re
import re

## Aim: Bio
from Bio import SeqIO





#====================================================================================================
#==================================      GET CHROM SIZES     ========================================
#====================================================================================================
# Aim: GET CHROM SIZES
#

## Aim: 获取染色体长度，从FASTA文件获取
def get_chrom_sizes_from_fa(parms_paths_fa):
    data = []  ### 用于存储染色体名称和长度的列表
    for record in SeqIO.parse(parms_paths_fa, "fasta"):
        chrom_name = record.id
        chrom_length = len(record.seq)
        data.append({"chr": chrom_name, "length": chrom_length})  ### 将数据添加到列表中

    ## Aim: 创建DataFrame
    df_chrom_sizes = pd.DataFrame(data)

    ## Aim: 返回
    return df_chrom_sizes



## Aim: 获取染色体长度，从chrom.sizes文件获取
def get_chrom_sizes_from_tsv(parms_paths_tsv):

    ## Aim: 读取chrom.sizes文件
    df_chrom_sizes = pd.read_csv(parms_paths_tsv, sep='\t', comment='#', header=None)

    ## Aim: 设置列名
    df_chrom_sizes.columns = ['chr', 'length']

    ## Aim: 返回
    return df_chrom_sizes





#====================================================================================================
#====================================      GET GENE INFOR     =======================================
#====================================================================================================
# Aim: GET GENE INFOR
#

## Aim: 根据需求，获取基因信息
def get_gene_infor(parms_paths_gtf, parms_chr=None, parms_feature=None, parms_strand=None, parms_gene_id=None, parms_gene_name=None, parms_gene_type=None):

    ## Aim: 读取GTF文件
    frame_gtf = pd.read_csv(parms_paths_gtf, sep='\t', comment='#', header=None)

    ## Aim: 设置列名
    frame_gtf.columns = ['chr', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute']



    ## Aim: 基于attributes列，提取指定内容
    def extract_attributes(attribute_str):

        ## Aim: Use regex to find key-value pairs
        attributes = dict(re.findall(r'(\S+)\s+"([^"]+)"', attribute_str))
        return attributes.get('gene_id'), attributes.get('gene_name'), attributes.get('gene_type'), attributes.get('gene'), attributes.get('gene_biotype'), attributes.get('product')

    ## Aim: 创建新列
    frame_gtf[['gene_id', 'gene_name', 'gene_type', 'gene', 'gene_biotype', 'product']] = frame_gtf['attribute'].apply(lambda x: pd.Series(extract_attributes(x)))

    ## Aim: 去掉列中"."号后的内容
    for col in ['gene_id']:
        frame_gtf[col] = frame_gtf[col].str.split('.').str[0]  ### 只保留"."前面的部分



    ## Aim: 将注释列插入到表格中
    frame_gtf.insert(frame_gtf.columns.get_loc('attribute'), 'gene_id', frame_gtf.pop('gene_id'))
    frame_gtf.insert(frame_gtf.columns.get_loc('attribute'), 'gene_name', frame_gtf.pop('gene_name'))
    frame_gtf.insert(frame_gtf.columns.get_loc('attribute'), 'gene_type', frame_gtf.pop('gene_type'))
    frame_gtf.insert(frame_gtf.columns.get_loc('attribute'), 'gene', frame_gtf.pop('gene'))
    frame_gtf.insert(frame_gtf.columns.get_loc('attribute'), 'gene_biotype', frame_gtf.pop('gene_biotype'))
    frame_gtf.insert(frame_gtf.columns.get_loc('attribute'), 'product', frame_gtf.pop('product'))

    ## Aim: 判断gene_name是否存在值，若无值，则使用gene列的值；若gene也无值，则使用product列的值
    frame_gtf['gene_name'] = np.where(
        frame_gtf['gene_name'].notnull(),   ### 如果 gene_name 存在值
        frame_gtf['gene_name'],             ### 使用 gene_name 的值
        np.where(
            frame_gtf['gene'].notnull(),    ### 如果 gene_name 不存在值，但 gene 存在值
            frame_gtf['gene'],              ### 使用 gene 的值
            frame_gtf['product']            ### 如果 gene 也没有值，则使用 product 的值
        )
    )

    ## Aim: 判断gene_type是否存在值，若无值，则使用gene_biotype列的值
    frame_gtf['gene_type'] = np.where(frame_gtf['gene_type'].notnull(), frame_gtf['gene_type'], frame_gtf['gene_biotype'])



    ## Aim: 根据strand列添加新列first
    frame_gtf['first'] = frame_gtf.apply(lambda row: row['start'] if row['strand'] == '+' else row['end'], axis=1)

    ## Aim: 将first列插入到frame列后面
    frame_gtf.insert(frame_gtf.columns.get_loc('frame') + 1, 'first', frame_gtf.pop('first'))



    ## Aim: 根据参数过滤表格
    if parms_chr:
        frame_gtf = frame_gtf[frame_gtf['chr'] == parms_chr]
    if parms_feature:
        frame_gtf = frame_gtf[frame_gtf['feature'] == parms_feature]
    if parms_strand:
        frame_gtf = frame_gtf[frame_gtf['strand'] == parms_strand]
    if parms_gene_id:
        frame_gtf = frame_gtf[frame_gtf['gene_id'] == parms_gene_id]
    if parms_gene_name:
        frame_gtf = frame_gtf[frame_gtf['gene_name'] == parms_gene_name]
    if parms_gene_type:
        frame_gtf = frame_gtf[frame_gtf['gene_type'] == parms_gene_type]



    ## Aim: Drop the 'attribute' column
    frame_gtf = frame_gtf.drop(columns=['attribute'])

    ## Aim: 返回
    return frame_gtf






#====================================================================================================
#====================================      GET PROMOTER     =========================================
#====================================================================================================
# Aim: GET PROMOTER
#

## Aim: 获取启动子区域
def get_promoter(parms_paths_fa, parms_gene_infor, parms_model=None, parms_up=None, parms_down=None, parms_chrom_sizes=None, parms_seq_strand=None, parms_output=None):

    ## Aim: 当输出文件是TSS格式时
    if parms_model == "tss2tsv":

        ## Aim: 设置tss_start和tss_end
        parms_gene_infor['tss'] = parms_gene_infor['first']

        ## Aim: 调整新表的顺序
        frame_promoter = parms_gene_infor[['chr', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'tss', 'gene_id', 'gene_name', 'gene_type']]

        ## Aim: 输出结果
        frame_promoter.to_csv(parms_output, sep='\t', index=False, header=False)



    ## Aim: 当输出文件是TSS格式时
    if parms_model == "tss2bed":

        ## Aim: 设置tss_start和tss_end
        parms_gene_infor['tss_start'] = parms_gene_infor['first']
        parms_gene_infor['tss_end']   = parms_gene_infor['first']

        ## Aim: 调整新表的顺序
        frame_promoter = parms_gene_infor[['chr', 'tss_start', 'tss_end', 'gene_id', 'score', 'strand', 'gene_name', 'gene_type']]

        ## Aim: 输出结果
        frame_promoter.to_csv(parms_output, sep='\t', index=False, header=False)



    ## Aim: 当输出文件是TSV格式时
    elif parms_model == "promoter2tsv":

        ## Aim: 获取染色体长度
        dicts_chrom_sizes = parms_chrom_sizes.set_index('chr')['length'].to_dict()

        ## Aim: 根据strand的值计算promoter_start和promoter_end
        parms_gene_infor['promoter_start'] = parms_gene_infor.apply(
            lambda row: max(0, row['first'] - parms_up) if row['strand'] == '+'
            else max(0, row['first'] - parms_down) if row['strand'] == '-' else None, axis=1)

        parms_gene_infor['promoter_end'] = parms_gene_infor.apply(
            lambda row: min(dicts_chrom_sizes.get(row['chr'], float('inf')), row['first'] + parms_down) if row['strand'] == '+'
            else min(dicts_chrom_sizes.get(row['chr'], float('inf')), row['first'] + parms_up) if row['strand'] == '-' else None, axis=1)

        ## Aim: 调整新表的顺序
        frame_promoter = parms_gene_infor[['chr', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'promoter_start', 'promoter_end', 'gene_id', 'gene_name', 'gene_type']]

        ## Aim: 输出结果
        frame_promoter.to_csv(parms_output, sep='\t', index=False, header=False)



    ## Aim: 当输出文件是BED格式时
    elif parms_model == "promoter2bed":

        ## Aim: 获取染色体长度
        dicts_chrom_sizes = parms_chrom_sizes.set_index('chr')['length'].to_dict()

        ## Aim: 根据strand的值计算promoter_start和promoter_end
        parms_gene_infor['promoter_start'] = parms_gene_infor.apply(
            lambda row: max(0, row['first'] - parms_up -1) if row['strand'] == '+' 
            else max(0, row['first'] - parms_down) if row['strand'] == '-' else None, axis=1)

        parms_gene_infor['promoter_end'] = parms_gene_infor.apply(
            lambda row: min(dicts_chrom_sizes.get(row['chr'], float('inf')), row['first'] + parms_down - 1) if row['strand'] == '+'
            else min(dicts_chrom_sizes.get(row['chr'], float('inf')), row['first'] + parms_up) if row['strand'] == '-' else None, axis=1)

        ## Aim: 调整新表的顺序
        frame_promoter = parms_gene_infor[['chr', 'promoter_start', 'promoter_end', 'gene_id', 'score', 'strand', 'gene_name', 'gene_type']]

        ## Aim: 输出结果
        frame_promoter.to_csv(parms_output, sep='\t', index=False, header=False)



    ## Aim: 当输出文件是fa格式时
    elif parms_model == "promoter2fa":

        ## Aim: pybedtools
        from pybedtools import BedTool

        ## Aim: 获取染色体长度
        dicts_chrom_sizes = parms_chrom_sizes.set_index('chr')['length'].to_dict()

        ## Aim: 根据strand的值计算promoter_start和promoter_end
        parms_gene_infor['promoter_start'] = parms_gene_infor.apply(
            lambda row: max(0, row['first'] - parms_up -1) if row['strand'] == '+' 
            else max(0, row['first'] - parms_down) if row['strand'] == '-' else None, axis=1)

        parms_gene_infor['promoter_end'] = parms_gene_infor.apply(
            lambda row: min(dicts_chrom_sizes.get(row['chr'], float('inf')), row['first'] + parms_down - 1) if row['strand'] == '+'
            else min(dicts_chrom_sizes.get(row['chr'], float('inf')), row['first'] + parms_up) if row['strand'] == '-' else None, axis=1)

        ## Aim: 调整新表的顺序
        frame_promoter = parms_gene_infor[['chr', 'promoter_start', 'promoter_end', 'gene_id', 'score', 'strand', 'gene_name', 'gene_type']]

        ## Aim: 将 DataFrame 转换为 BED 格式的 BedTool 对象
        bedtool_promoter = BedTool.from_dataframe(frame_promoter)

        ## Aim: 使用 fetch 方法来从基因组中提取对应的序列
        frame_promoter = bedtool_promoter.sequence(fi=parms_paths_fa, fo=parms_output, name=True, s = parms_seq_strand)



    ## Aim: 返回
    return frame_promoter





#====================================================================================================
#=======================================      MAIN     ==============================================
#====================================================================================================
# Aim: MAIN
#

## Aim: 主程序
def main():

    ## Aim: 命令行函数
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--fa',         required=True,  type=str, default=None,   help="File path of FASTA or chrom.sizes")
    parser.add_argument('-g', '--gtf',        required=True,  type=str, default=None,   help="GTF file path")
    parser.add_argument('-m', '--mode',       required=True,  type=str, default=None,   help="Program mode", choices=['promoter2tsv', 'promoter2bed', 'promoter2fa','tss2tsv','tss2bed'])
    parser.add_argument('-u', '--up',         required=False, type=int, default=2000,   help="The upstream regulatory region of TSS")
    parser.add_argument('-d', '--down',       required=False, type=int, default=1000,   help="The downstream regulatory region of TSS")
    parser.add_argument('-s', '--seq_strand', required=False, type=str, default=False,  help="In the context of using the '-m promoter2fa', the sequence is extracted based on the transcription direction of the gene", choices=['True', 'False'])
    parser.add_argument('--feature',          required=False, type=str, default='gene', help="Filter the GTF feature. It is recommended to set it as 'gene'")
    parser.add_argument('--chr',              required=False, type=str, default=None,   help="Filter the chromosome")
    parser.add_argument('--strand',           required=False, type=str, default=None,   help="Filter genes based on the transcription direction, and distinguish this from the parameter '-s, --seq_strand'", choices=['+', '-'])
    parser.add_argument('--gene_id',          required=False, type=str, default=None,   help="Filter by gene ID")
    parser.add_argument('--gene_name',        required=False, type=str, default=None,   help="Filter by gene name")
    parser.add_argument('--gene_type',        required=False, type=str, default=None,   help="Filter by gene type")
    parser.add_argument('-o', '--output',     required=True,  type=str, default=None,   help="Output file path")

    ## Aim: 命令行参数
    args = parser.parse_args()



    ## Aim: 获取文件的扩展名
    file_extension = os.path.splitext(args.fa)[1]

    ## Aim: 根据文件格式调用不同的函数
    if file_extension == '.fa':
        frame_chrom_sizes = get_chrom_sizes_from_fa(args.fa)
    elif file_extension == '.sizes':
        frame_chrom_sizes = get_chrom_sizes_from_tsv(args.fa)
    else:
        raise ValueError("Unsupported file format. Please use a .fa or .chrom.sizes file.")

    ## Aim: 将参数args.seq_strand设置为布尔类型
    if args.seq_strand == 'True':
        seq_strand = bool(True)
    elif args.seq_strand == 'False':
        seq_strand = bool(False)
    else:
        seq_strand = bool(False)



    ## Aim: 筛选基因信息
    frame_gene_infor = get_gene_infor(parms_paths_gtf=args.gtf, parms_feature=args.feature, parms_chr=args.chr, parms_strand=args.strand, parms_gene_id=args.gene_id, parms_gene_name=args.gene_name, parms_gene_type=args.gene_type)

    ## Aim: 获取启动子
    files_get_promoter = get_promoter(parms_paths_fa = args.fa, parms_gene_infor = frame_gene_infor, parms_model = args.mode, parms_up = args.up, parms_down = args.down, parms_chrom_sizes = frame_chrom_sizes, parms_seq_strand=seq_strand, parms_output = args.output)





if __name__ == "__main__":
    main()




