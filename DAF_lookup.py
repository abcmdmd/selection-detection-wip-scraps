"""
Calculate derived allele frequency for one SNP directly from the original dataset VCFs

How to use:
    python DAF_lookup.py {SNP} {chromosome} {optional: inputfile.tsv}
    ex: 
        python DAF_lookup.py 1229984 4 
        or
        python DAF_lookup.py rs1229984 chr4 
        or 
        python DAF_lookup.py rs1229984 chr 4 --input new_inputfile.tsv

Output:
    /{wherever_you_run_the_script}/rs{snp}_chr{chromosome}_original_vcf_DAF.csv

Example usage: 
    python /scratch/myang_shared/lab/Aine/Relate_CLUES2_pipeline/scripts/DAF_lookup.py rs1229984 chr4

    """

import argparse
import csv
import os
import re
from collections import defaultdict


from pipeline_settings import (
    open_maybe_gzip,
    normalize_snp_id,
    get_orientation_from_vcf_parts,
    count_vcf_derived_alleles,
)


default_input_megafile= "/scratch/myang_shared/lab/selection/data_references/worldwide_populations_inputfile.tsv"

dataset_dict = {
    "DGP": {
        "dataset_names": {"DGP", "929"},
        "metadata": "/scratch/myang_shared/data/929_WGS/hgdp_wgs.20190516.metadata.txt",
        "vcf_template": "/scratch/myang_shared/data/929_WGS/hg19_929_best/929_phased_hg19_addAA.{chrom}.vcf.gz",
        "sample_col": "sample",
        "label_cols": ["population", "region"],
    },
    "KGP": {
        "dataset_names": {"KGP", "1KG"},
        "metadata": "/scratch/myang_shared/data/1KG/integrated_call_samples_v3.20130502.ALL.panel",
        "vcf_template": "/scratch/myang_shared/data/1KG/addAA/ALL.chr{chrom}.addAA.vcf.gz",
        "sample_col": "sample",
        "label_cols": ["pop", "super_pop"],
    },
    "GAP": {
        "dataset_names": {"GAP", "GA100K"},
        "metadata": "/scratch/myang_shared/lab/Aine/alcohol/Relate/GA100Ksubset_metadata2.txt",
        "vcf_template": "/scratch/myang_shared/data/GA100K/phased_eagle/addAA/GA100K_addAA_chr{chrom}_mm1_maf0.1_eagle.vcf.gz",
        "sample_col": "GA_sample_ID",
        "label_cols": [
            "Population",
            "Population(abbr)",
            "Region",
            "Region(abbr)",
            "Country_of_origin",
        ],
    },
}


names_in_original_dataset = {
    name: original
    for original, cfg in dataset_dict.items()
    for name in cfg["dataset_names"]
}


output_cols = [
    "dataset",
    "group_name",
    "region",
    "involved_groups",
    "matched_groups",
    "unmatched_groups",
    "snp",
    "chromosome",
    "reference_allele",
    "alternative_allele",
    "ancestral_allele",
    "derived_allele",
    "derived_count",
    "ancestral_count",
    "total_allele_count",
    "DAF",
    "status"
]




def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate per-population DAF for one SNP from the original DGP/KGP/GAP VCFs."
    )
    parser.add_argument(
        "snp",
        help="SNP ID! Either '1229984' or 'rs1229984' works.",
    )
    parser.add_argument(
        "chrom",
        help="Chromosome number! Either '4' or 'chr4' works.",
    )
    parser.add_argument(
        "--input_megafile",
        default=default_input_megafile,
        help=f"Path to the big population input TSV. Default: {default_input_megafile}",
    )
    return parser.parse_args()


def normalize_chromosome(chrom):
    chrom = str(chrom).strip()
    chrom = re.sub(r"^chr", "", chrom, flags=re.IGNORECASE)

    if not chrom:
        raise ValueError("Don't forget to input the chromosome associated with your SNP.")

    return chrom


def clean_header_name(name):
    return str(name).strip()


def clean_value(value):
    if value is None:
        return ""
    value = str(value).strip()
    if value.lower() in {"", "na", "n/a", "nan", "none", "."}:
        return ""
    return value


def loose_key(value):
    # normalizing labels to match little formatting differences like Buryat_Xhalxh & BuryatXhalxh
    return re.sub(r"[^A-Za-z0-9]", "", clean_value(value)).lower()


def split_group_values(value):
    # split csv/tsv cells with lists in them
    value = clean_value(value)

    if not value:
        return []

    value = value.strip("[]")
    value = value.replace("'", "").replace('"', "")

    return [x.strip() for x in re.split(r"[;,|]+", value) if clean_value(x)]


def split_excluded_individuals(value):
    value = clean_value(value)

    if not value:
        return set()

    value = value.strip("[]")
    value = value.replace("'", "").replace('"', "")

    return {x.strip() for x in re.split(r"[,;|\s]+", value) if clean_value(x)}


def original_dataset_name(dataset):
    dataset = clean_value(dataset)
    return names_in_original_dataset.get(dataset, dataset)


def read_input_megafile(input_megafile):
    if not os.path.exists(input_megafile):
        raise FileNotFoundError(f"Input megafile not found: {input_megafile}")

    records_by_dataset = defaultdict(list)

    with open(input_megafile, "r", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")

        if reader.fieldnames is None:
            raise ValueError(f"Input megafile appears to have no header: {input_megafile}")

        reader.fieldnames = [clean_header_name(x) for x in reader.fieldnames]

        required = {"dataset", "group_name", "involved_groups"}
        missing = required - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Input megafile is missing required columns {sorted(missing)}. "
                f"Found columns: {reader.fieldnames}"
            )

        for raw_row in reader:
            row = {clean_header_name(k): clean_value(v) for k, v in raw_row.items()}
            dataset = original_dataset_name(row.get("dataset", ""))

            if dataset not in dataset_dict:
                continue

            row["dataset"] = dataset
            records_by_dataset[dataset].append(row)

    return records_by_dataset


def read_metadata_maps(dataset):
    cfg = dataset_dict[dataset]
    metadata_path = cfg["metadata"]

    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found for {dataset}: {metadata_path}")

    exact_label_to_samples = defaultdict(set)
    loose_label_to_samples = defaultdict(set)

    with open(metadata_path, "r", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")

        if reader.fieldnames is None:
            raise ValueError(f"Metadata file appears to have no header: {metadata_path}")

        reader.fieldnames = [clean_header_name(x) for x in reader.fieldnames]
        sample_col = cfg["sample_col"]

        if sample_col not in reader.fieldnames:
            raise ValueError(
                f"Metadata file for {dataset} does not contain sample column '{sample_col}'. "
                f"Found columns: {reader.fieldnames}"
            )

        for raw_row in reader:
            row = {clean_header_name(k): clean_value(v) for k, v in raw_row.items()}
            sample_id = clean_value(row.get(sample_col))

            if not sample_id:
                continue

            for col in cfg["label_cols"]:
                label = clean_value(row.get(col))

                if not label:
                    continue

                exact_label_to_samples[label].add(sample_id)
                loose_label_to_samples[loose_key(label)].add(sample_id)

    return exact_label_to_samples, loose_label_to_samples


def get_samples_for_group(group_record, exact_label_to_samples, loose_label_to_samples):
    group_name = clean_value(group_record.get("group_name"))
    involved_groups = split_group_values(group_record.get("involved_groups"))

    if not involved_groups:
        involved_groups = [group_name]

    samples = set()
    matched_groups = []
    unmatched_groups = []

    for group_label in involved_groups:
        exact_matches = exact_label_to_samples.get(group_label, set())
        loose_matches = loose_label_to_samples.get(loose_key(group_label), set())

        group_samples = set(exact_matches) | set(loose_matches)

        if group_samples:
            samples.update(group_samples)
            matched_groups.append(group_label)
        else:
            unmatched_groups.append(group_label)

    excluded = split_excluded_individuals(group_record.get("inds_to_exclude"))
    samples -= excluded

    return samples, matched_groups, unmatched_groups, excluded


def find_target_vcf_row_and_samples(vcf_path, target_snp):
    # note: returns vcf_sample_ids, target_parts
    # target_parts is None if no SNP present

    if not os.path.exists(vcf_path):
        raise FileNotFoundError(f"VCF file not found:( Expected at: {vcf_path}")

    vcf_sample_ids = None
    target_parts = None

    with open_maybe_gzip(vcf_path) as vcf:
        for line in vcf:
            if line.startswith("##"):
                continue

            if line.startswith("#CHROM"):
                header_parts = line.rstrip("\n").split()
                vcf_sample_ids = header_parts[9:]
                continue

            if line.startswith("#"):
                continue

            parts = line.rstrip("\n").split()

            if len(parts) < 10:
                continue

            if parts[2] == target_snp:
                target_parts = parts
                break

    if vcf_sample_ids is None:
        raise ValueError(f"Could not find #CHROM header in VCF: {vcf_path}")

    return vcf_sample_ids, target_parts

# FIX next 3 functions
def count_called_individuals(sample_fields):
    called = 0

    for sample_field in sample_fields:
        genotype = sample_field.split(":", 1)[0]
        codes = genotype.replace("|", "/").split("/")

        if any(code in {"0", "1"} for code in codes):
            called += 1

    return called

def blank_result_row(dataset, group_record, target_snp, chrom, vcf_path, status):
    return {
        "dataset": dataset,
        "group_name": group_record.get("group_name", ""),
        "region": group_record.get("region", ""),
        "involved_groups": group_record.get("involved_groups", ""),
        "matched_groups": "",
        "unmatched_groups": "",
        "snp": target_snp,
        "chromosome": chrom,
        "reference_allele": "",
        "alternative_allele": "",
        "ancestral_allele": "",
        "derived_allele": "",
        "derived_count": "",
        "ancestral_count": "",
        "total_allele_count": "",
        "DAF": "",
        "status": status
    }


def calculate_dataset_rows(dataset, group_records, target_snp, chrom):
    cfg = dataset_dict[dataset]
    vcf_path = cfg["vcf_template"].format(chrom=chrom)

    print(f"\nSearching {dataset} VCF for {target_snp}: {vcf_path}", flush=True)

    rows = []

    try:
        vcf_sample_ids, target_parts = find_target_vcf_row_and_samples(vcf_path, target_snp)

    except Exception as e:
        print(f"ERROR: Could not search {dataset} VCF: {e}", flush=True)

        for group_record in group_records:
            rows.append(
                blank_result_row(
                    dataset,
                    group_record,
                    target_snp,
                    chrom,
                    vcf_path,
                    "VCF_SEARCH_ERROR",
                )
            )

        return rows, False

    if target_parts is None:
        print(f"{target_snp} was NOT found in {dataset} VCF.", flush=True)

        for group_record in group_records:
            rows.append(
                blank_result_row(
                    dataset,
                    group_record,
                    target_snp,
                    chrom,
                    vcf_path,
                    "SNP_NOT_FOUND_IN_DATASET_VCF",
                )
            )

        return rows, False

    print(f"{target_snp} found in {dataset} VCF.", flush=True)

    try:
        ancestral, derived, ref, alt, aa = get_orientation_from_vcf_parts(target_parts)

    except Exception as e:
        print(
            f"ERROR: {target_snp} was found in {dataset}, "
            f"but allele orientation could not be determined: {e}",
            flush=True,
        )

        for group_record in group_records:
            row = blank_result_row(
                dataset,
                group_record,
                target_snp,
                chrom,
                vcf_path,
                "ALLELE_ORIENTATION_ERROR",
            )
            row.update(
                {
                    "reference_allele": target_parts[3],
                    "alternative_allele": target_parts[4],
                }
            )
            rows.append(row)

        return rows, True


    exact_label_to_samples, loose_label_to_samples = read_metadata_maps(dataset)

    sample_index = {sample_id: i for i, sample_id in enumerate(vcf_sample_ids)}
    vcf_sample_set = set(sample_index)
    all_sample_fields = target_parts[9:]

    for group_record in group_records:
        group_name = group_record.get("group_name", "")

        group_samples, matched_groups, unmatched_groups, excluded = get_samples_for_group(
            group_record,
            exact_label_to_samples,
            loose_label_to_samples,
        )

        vcf_samples = sorted(
            group_samples & vcf_sample_set,
            key=lambda sample_id: sample_index[sample_id],
        )

        group_sample_fields = [
            all_sample_fields[sample_index[sample_id]]
            for sample_id in vcf_samples
        ]

        status = "OK"
        D = A = T = daf = ""
        n_called_individuals = ""

        if not group_samples:
            status = "NO_METADATA_SAMPLES_FOR_GROUP"

        elif not vcf_samples:
            status = "NO_GROUP_SAMPLES_PRESENT_IN_VCF"

        else:
            D_int, T_int = count_vcf_derived_alleles(
                group_sample_fields,
                ref,
                alt,
                derived,
            )

            n_called_individuals = count_called_individuals(group_sample_fields)

            if T_int == 0:
                status = "NO_ALLELES_FOR_GROUP"
                D = 0
                A = 0
                T = 0

            else:
                A_int = T_int - D_int
                daf_float = D_int / T_int

                D = D_int
                A = A_int
                T = T_int
                daf = daf_float

        rows.append({
            "dataset": dataset,
            "group_name": group_name,
            "region": group_record.get("region", ""),
            "involved_groups": group_record.get("involved_groups", ""),
            "matched_groups": ";".join(matched_groups),
            "unmatched_groups": ";".join(unmatched_groups),
            "snp": target_snp,
            "chromosome": chrom,
            "reference_allele": ref,
            "alternative_allele": alt,
            "ancestral_allele": ancestral,
            "derived_allele": derived,
            "derived_count": D,
            "ancestral_count": A,
            "total_allele_count": T,
            "DAF": daf,
            "status": status,
        })

        if status == "OK":
            print(
                f"{dataset} {group_name}: "
                f"D={D}, A={A}, T={T}, DAF={daf}, "
                f"REF={ref}, ALT={alt}, "
                f"ancestral={ancestral}, derived={derived}",
                flush=True,
            )

        else:
            print(f"{dataset} {group_name}: {status}", flush=True)

    return rows, True

def write_csv(rows, out_csv):
    with open(out_csv, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=output_cols)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def main():
    args = parse_args()

    target_snp = normalize_snp_id(args.snp)
    chrom = normalize_chromosome(args.chrom)

    records_by_dataset = read_input_megafile(args.input_megafile)

    all_rows = []
    found_in_any_dataset = False

    for dataset in ["DGP", "KGP", "GAP"]:
        group_records = records_by_dataset.get(dataset, [])

        if not group_records:
            print(f"No rows for {args.snp} found for the populations listed in the input file.", flush=True)
            print(f"Skipping {dataset}", flush=True)
            continue

        dataset_rows, dataset_found = calculate_dataset_rows(
            dataset,
            group_records,
            target_snp,
            chrom,
        )

        all_rows.extend(dataset_rows)
        found_in_any_dataset = found_in_any_dataset or dataset_found

    out_csv = f"{target_snp}_chr{chrom}_original_vcf_DAF.csv"
    write_csv(all_rows, out_csv)

    print(f"Wrote {args.snp} DAF info to: {out_csv}", flush=True)

    if not found_in_any_dataset:
        print(f"{target_snp} was not found in any of the searched VCFs (DGP, KGP, GAP) ",flush=True)


if __name__ == "__main__":
    main()
