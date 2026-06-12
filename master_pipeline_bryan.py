"""
Master Pipeline copy for Bryan
Last updated: Jun 11 2026 4:55 PM

# ---------------------------------------------- Purpose: -----------------------------------------------
This is the .py file meant to run all of the scripts in the selection detection pipeline.

# ---------------------------------------------- Instructions: ------------------------------------------
 1. Look into this file and adjust all of the settings marked under headings ending in "Edit this." 
    and all of the settings in the "your_run" dictionary.
    See "run_template" for an example.

 2. Copy "pipeline_settings.py" into a new folder (inside of the one where your version of 
    master_pipeline.py is) called /scripts

 3. Look into (your version of) /scripts/pipeline_settings.py and change whatever you'd like there.
    These settings become relevant in during/after iHS.py. 

 4. When satisfied with your choices, change the "script" option to "initialization_1.py" to begin!
    To see all of the script options, ctrl+F for "command_settings".
    They're written in the order in which you should logically run them.

 5. Run this script in your terminal as: "python {master_pipeline}.py"

    If you want, you can use: 
        /usr/bin/time -v python {master_pipeline}.py 
    to see how much computational room/energy/etc the command is taking.

# ----------------------------------------------- Notes: ------------------------------------------------
1. Anything marked as "# FIX" is a note for Aine to go back and fix later.

"""

import subprocess
import os
import re

# ------------------- CLUSTER SETTINGS. Edit this. 
processes = []
account = "am8ht" # use "bnam" here
partition= "yang2" # which node do you want to use for bigger jobs?
path_to_clues2 = "/scratch/myang_shared/lab/Aine/CLUES2/" # leave these as-is until Aine provides info to download clues2 + relate
path_to_relate="/usr/local/sw/relate/" # leave these as-is until Aine provides info to download clues2 + relate
# FIX -- provide info to download clues2 + relate
receive_emails = False # if True; don't forget to check your spam
email = "aine.macdermott@richmond.edu" if receive_emails else None
base_dir = "/scratch/myang_shared/lab/Aine/Relate_CLUES2_pipeline" # where did you download the package?

# ------------------- RUN-SPECIFIC SETTINGS. Edit this. 
# feel free to keep more than one here -- just make sure to set run = [the run you want]

run_template = {
    # ----------------------------------- PROJECT SPECIFICATIONS:
    "gene_name": "ADH1B", 
    "input_nickname": "2026_ADH1B", # the name you want to use as an identifier for this project.
    "input_megafile": "2026_ADH1B_inputfile.tsv", # name of the input file you downloaded earlier. 
     # keep this in a folder called {base_dir}/input_files/ 

    "datasets_list": ["KGP", "GAP", "DGP"], # we're using 3 datasets here. these are all 3 options.

    # -------------------------------------- GENE SPECIFICATIONS:
    "chr": "4", # chromosome number only
    "snp": "1229984", # don't include the "rs" here
    "position": "100239319",  # on the GrCh37 build

    "defined_ancestral": "C", # this is optional, for if you want to make sure that you're forcing a particular ancestral/derived allele pair
    "defined_derived": "T", # this is optional, for if you want to make sure that you're forcing a particular ancestral/derived allele pair

    # -------------------------------------- DAF_barplot SETTINGS:
    "show_DAF_value": "True", # whether to write out the DAF on top of each bar in plot

    # -------------------------------------- iHS and Relate significance calculation SETTINGS:
    "p_value": 0.05,
    "rerun_multiple_testing_corrections": "True", # option to JUST redo MTC, not calculating ihs again
    
    # -------------------------------------- Relate_4 SETTINGS:
    "create_relate_table": "True", # option to create the Relate results summary table (precursor for combined table)
    "create_combined_ihs_relate_table": "True", # option to create the iHS + Relate results summary table 

    # --------------------------------------CLUES2 SETTINGS:
    "generation_time": "28", # how many years are in a generation?
    "num_samples": "1000",
    "pad_bp": "10", # optional; default = 0
    "max_workers": "5", # how many groups your script tries to submit at the same time

    # --------------------------------------CLUES2 GRAPHING SETTINGS:
    "total_epochs": "5", # how many different timebins did you use?
    "graph_prefix": "260602", # what special name do you want to use to distinguish this graph?
    "allele_frequency_graphing_setting": "LowestParameterSpace", # options: "TopAIC", "LowestParameterSpace"
    "confidence_interval": ".99", # note: this is relevant for the plotting modes with confidence intervals
    "allele_frequency_graph_type": "SmoothedConfidence", 
        # options: 
        # MultipleModels
        # ConfidenceIntervals
        # Heatmap
        # SmoothedConfidence
    "x_axis_metric": "gen", # options: "gen" for generations or "kya" for thousand years BP
    "use_groupings": "True",  # do you want to use the groupings defined in pipeline_settings.py?
    "multiple_inputfiles": "False", # do you want to overlay CLUES2 results from different inputfiles? if so, define them in pipeline_settings.py
    "renaming": "False", # do you want to rename any of your groupings as defined in pipeline_settings.py?
    "selection_coefficient_graphing_setting": "LowestParameterSpace", 
        # options: "TopAIC", "LowestParameterSpace" # FIX, add to documentation
        # if you leaave "confidence_interval" blank, then no error shading will be applied
    "min_time": "0", # x axis lower limit
    "max_time": "600", # x axis upper limit
    "create_new_avg_tables": "True", # for CLUES2_6.py (while generating selection coefficient trajectory graphs)

    # ----------------------------------- RUN SPECIFICATIONS:
    "script_file": "CLUES2_3.py", # which script are you running? just give the filename itself, no need for path.
} 

your_run = {
    # ----------------------------------- PROJECT SPECIFICATIONS:
    "gene_name": "ADH1B", 
    "input_nickname": "2026_ADH1B", # the name you want to use as an identifier for this project.
    "input_megafile": "2026_ADH1B_inputfile.tsv", # name of the input file you downloaded earlier. 
     # keep this in a folder called {base_dir}/input_files/ 

    "datasets_list": ["KGP", "GAP", "DGP"], # we're using 3 datasets here. these are all 3 options.

    # -------------------------------------- GENE SPECIFICATIONS:
    "chr": "4", # chromosome number only
    "snp": "1229984", # don't include the "rs" here
    "position": "100239319",  # on the GrCh37 build

    "defined_ancestral": "C", # this is optional, for if you want to make sure that you're forcing a particular ancestral/derived allele pair
    "defined_derived": "T", # this is optional, for if you want to make sure that you're forcing a particular ancestral/derived allele pair

    # -------------------------------------- DAF_barplot SETTINGS:
    "show_DAF_value": "True", # whether to write out the DAF on top of each bar in plot

    # -------------------------------------- iHS and Relate significance calculation SETTINGS:
    "p_value": 0.05,
    "rerun_multiple_testing_corrections": "True", # option to JUST redo MTC, not calculating ihs again
    
    # -------------------------------------- Relate_4 SETTINGS:
    "create_relate_table": "True", # option to create the Relate results summary table (precursor for combined table)
    "create_combined_ihs_relate_table": "True", # option to create the iHS + Relate results summary table 

    # --------------------------------------CLUES2 SETTINGS:
    "generation_time": "28", # how many years are in a generation?
    "num_samples": "1000",
    "pad_bp": "10", # optional; default = 0
    "max_workers": "5", # how many groups your script tries to submit at the same time

    # --------------------------------------CLUES2 GRAPHING SETTINGS:
    "total_epochs": "5", # how many different timebins did you use?
    "graph_prefix": "260602", # what special name do you want to use to distinguish this graph?
    "allele_frequency_graphing_setting": "LowestParameterSpace", # options: "TopAIC", "LowestParameterSpace"
    "confidence_interval": ".99", # note: this is relevant for the plotting modes with confidence intervals
    "allele_frequency_graph_type": "SmoothedConfidence", 
        # options: 
        # MultipleModels
        # ConfidenceIntervals
        # Heatmap
        # SmoothedConfidence
    "x_axis_metric": "gen", # options: "gen" for generations or "kya" for thousand years BP
    "use_groupings": "True",  # do you want to use the groupings defined in pipeline_settings.py?
    "multiple_inputfiles": "False", # do you want to overlay CLUES2 results from different inputfiles? if so, define them in pipeline_settings.py
    "renaming": "False", # do you want to rename any of your groupings as defined in pipeline_settings.py?
    "selection_coefficient_graphing_setting": "LowestParameterSpace", 
        # options: "TopAIC", "LowestParameterSpace" # FIX, add to documentation
        # if you leaave "confidence_interval" blank, then no error shading will be applied
    "min_time": "0", # x axis lower limit
    "max_time": "600", # x axis upper limit
    "create_new_avg_tables": "True", # for CLUES2_6.py (while generating selection coefficient trajectory graphs)

    # ----------------------------------- RUN SPECIFICATIONS:
    "script_file": "initialization_1.py", # which script are you running? just give the filename itself, no need for path.
} 


# ------------------Don't forget to define WHICH run you're looking at here. Edit this. 
run = your_run

"""
Attention!!! Attention!!! Attention!!! Attention!!! Attention!!! Attention!!! Attention!!!

Do not edit anything below this line.

"""

# ------------------- PATHS. DO NOT edit this. 
#script_dir = os.path.join(base_dir, "scripts") # FIX for final ver w github import
script_dir = os.path.join("/scratch/myang_shared/lab/Aine/Relate_CLUES2_pipeline", "scripts")
input_dir = os.path.join(base_dir, "input_files")
logs_dir = os.path.join(base_dir, "logs")

working_directory = base_dir + "/"
logs_directory = logs_dir + "/"

script_name = run["script_file"] # filename only
script = os.path.join(script_dir, script_name) # full path to script

# timebins_dictionary ="/scratch/myang_shared/lab/Aine/Relate_CLUES2_pipeline/scripts/timebins.py" # FIX: migrate to pipeline settings
ancestral_path = f'/scratch/myang_shared/data/1KG/ancestral_alignments/GrCh37_readable/human_ancestor_{run["chr"]}.fa' # FIX: make this generalizable somehow...
ancestral_manifest = "/scratch/myang_shared/data/1KG/ancestral_alignments/GrCh37_readable/manifest.mf"
recombmap_base_directory = f'/scratch/myang_shared/data/RecombinationRates/pyrho_hg19'

# ------------------- DEFINING COMMANDS PER SCRIPT
command_settings = {
    # initialization steps
    "initialization_1.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory", "metadata_file", "input_nickname", "logs_directory"]},

    "initialization_2.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","metadata_file", "input_nickname"]},

    "initialization_3.sh": {
        "runner": "sbatch",
        "log_subdir": "3_initialize_vcf",
        "args": ["dataset_name", "chr", "vcf_directory","vcf_name_nosuffix", "working_directory", "snp", "path_to_relate"]},

    "initialization_4.sh": {
        "runner": "sbatch",
        "log_subdir": "4_initialize_haps",
        "args": ["dataset_name", "input_megafile", "vcf_directory","vcf_name_nosuffix", "chr", "ancestral_path","working_directory", "input_nickname", "path_to_relate", "snp", "position", "defined_derived", "defined_ancestral"]},
        #"optional_args": {"defined_derived": "--defined_ancestral"}},
        
    "initialization_5.sh": {
        "runner": "sbatch",
        "log_subdir": "5_initialize_haps",
        "args": ["dataset_name", "input_megafile", "working_directory","metadata_file", "logs_directory", "ancestral_path","chr", "input_nickname", "path_to_relate"]},
       
    "initialization_6.sh": {
        "runner": "sbatch",
        "log_subdir": "6_initialize_haps",
        "args": ["dataset_name", "input_megafile", "vcf_directory","vcf_name", "chr", "ancestral_manifest","working_directory", "gene_name", "snp","position", "input_nickname"],
        "optional_args": {"defined_derived" : "--defined_derived", "defined_ancestral" :  "--defined_ancestral", "email": "--email"}},

    # iHS/DAF
    "ihs.py": {
        "runner": "python",
        "args": ["datasets_list", "input_megafile", "working_directory","metadata_file", "chr", "snp", "logs_directory","gene_name", "input_nickname", "p_value"],
        "optional_args": {"defined_derived" : "--defined_derived", "defined_ancestral" :  "--defined_ancestral", "rerun_multiple_testing_corrections" : "--rerun_multiple_testing_corrections"}},
      

    "DAF_barplot.py": {
        "runner": "python",
        "args": ["datasets_list", "input_megafile", "working_directory","chr", "snp", "logs_directory", "gene_name", "input_nickname"],
        "optional_args": {"defined_derived" : "--defined_derived", "defined_ancestral" :  "--defined_ancestral", "show_DAF_value": "--show_DAF_value"}},
    
    # Relate
    "Relate_1.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","metadata_file", "chr", "snp", "vcf_directory","vcf_name", "logs_directory", "gene_name", "input_nickname", "account", "partition", "recombmap_base_directory", "path_to_relate"],
        "optional_args": {"email": "--email", "defined_derived" : "--defined_derived", "defined_ancestral" :  "--defined_ancestral"}},
      
    "Relate_2.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","chr", "logs_directory", "gene_name", "input_nickname","account", "partition", "path_to_relate", "snp"],
        "optional_args": {"email": "--email"}},

    "Relate_3.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","chr", "snp", "position", "generation_time", "logs_directory","gene_name", "input_nickname","account", "partition", "path_to_relate"],
        "optional_args": {"email": "--email"}},


    "Relate_4.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","chr", "snp", "position", "logs_directory","gene_name", "input_nickname", "generation_time", "p_value"],
        "optional_args": {"create_relate_table": "--create_relate_table","create_combined_ihs_relate_table": "--create_combined_ihs_relate_table", "defined_derived" : "--defined_derived", "defined_ancestral" :  "--defined_ancestral", "rerun_multiple_testing_corrections" : "--rerun_multiple_testing_corrections"}},
 
    # CLUES2 
    "CLUES2_1.sh": {
        "runner": "sbatch",
        "log_subdir": "CLUES2_1",
        "args": ["dataset_name", "input_megafile", "chr","working_directory", "snp", "gene_name","position", "logs_directory", "input_nickname", "path_to_relate", "num_samples", "pad_bp"],},

    "CLUES2_2.sh": {
        "runner": "sbatch",
        "log_subdir": "CLUES2_2",
        "args": ["dataset_name", "input_megafile", "chr","working_directory", "snp", "gene_name","logs_directory", "input_nickname", "path_to_clues2"]},
 

    "CLUES2_3.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","metadata_file", "chr", "snp", "vcf_directory","vcf_name", "logs_directory", "gene_name", "input_nickname", "max_time", "account", "partition", "path_to_clues2"],
        "optional_args": {
            "email": "--email",
            "max_workers": "--max_workers"},},


    "CLUES2_4.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","chr", "snp", "vcf_directory", "vcf_name","logs_directory", "gene_name", "total_epochs", "input_nickname"]},


    "CLUES2_5.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","chr", "snp", "vcf_directory", "vcf_name","logs_directory", "gene_name", "total_epochs", "generation_time", "input_nickname"],
        "optional_args": {
            "graph_prefix": "--graph_prefix",
            "allele_frequency_graphing_setting": "--allele_frequency_graphing_setting",
            "confidence_interval": "--confidence_interval",
            "allele_frequency_graph_type": "--allele_frequency_graph_type",
            "x_axis_metric": "--x_axis_metric",
            "use_groupings": "--use_groupings",
            "multiple_inputfiles": "--multiple_inputfiles",
            "renaming": "--renaming"},},

    "CLUES2_6.py": {
        "runner": "python",
        "args": ["dataset_name", "input_megafile", "working_directory","chr", "snp", "vcf_directory", "vcf_name","logs_directory", "gene_name", "total_epochs", "generation_time", "input_nickname",],
        "optional_args": {
            "graph_prefix": "--graph_prefix",
            "confidence_interval": "--confidence_interval",
            "x_axis_metric": "--x_axis_metric",
            "use_groupings": "--use_groupings",
            "multiple_inputfiles": "--multiple_inputfiles",
            "renaming": "--renaming",
            "selection_coefficient_graphing_setting": "--selection_coefficient_graphing_setting",
            "min_time":"--min_time",
            "max_time":"--max_time",
            "create_new_avg_tables": "--create_new_avg_tables"},},
}


def build_command(script_name, context):
    if script_name not in command_settings:
        raise ValueError(f"No command template found for script: {script_name}")

    spec = command_settings[script_name]
    runner = spec["runner"]

    def stringify_arg(value):
        if isinstance(value, list):
            return ",".join(str(item) for item in value)
        return str(value)

    script_args = [stringify_arg(context[name]) for name in spec["args"]]

    optional_args = []
    for context_key, flag in spec.get("optional_args", {}).items():
        value = context.get(context_key)
        if value is None: 
            continue
        optional_args.extend([flag, stringify_arg(value)])

    if runner == "python":
        return ["python", context["script"], *script_args, *optional_args]

    elif runner == "bash":
        return ["bash", context["script"], *script_args, *optional_args]

    elif runner == "sbatch":
        log_subdir = spec["log_subdir"]
        log_dir = os.path.join(context["logs_directory"],context["input_nickname"],log_subdir)
        os.makedirs(log_dir, exist_ok=True)

        return [
            "sbatch",
            f"--output={log_dir}/{context['dataset_name']}_%x_%j.out",
            f"--error={log_dir}/{context['dataset_name']}_%x_%j.err",
            f"--account={context['account']}",
            f"--partition={context['partition']}",
            context["script"],
            *script_args,
            *optional_args
            ]

    else:
        raise ValueError(f"Unsupported runner: {runner}")

# make certain scripts only run once...
scripts_to_run_only_once = {
    "initialization_1.py",
    "ihs.py",
    "CLUES2_5.py",
    "CLUES2_6.py",
    "DAF_barplot.py",
}

if script_name in scripts_to_run_only_once:
    datasets_to_run = [run["datasets_list"][0]]
else:
    datasets_to_run = run["datasets_list"]

for dataset_name in datasets_to_run:
    chr = run["chr"]

    # Customize per dataset
    if dataset_name in ["GA100K", "GAP"]:
        metadata_file = "/scratch/myang_shared/lab/selection/data_references/GA100Ksubset_metadata2.txt"
        vcf_directory = "/scratch/myang_shared/data/GA100K/phased_eagle/addAA/"
        vcf_name = f"GA100K_addAA_chr{chr}_mm1_maf0.1_eagle.vcf.gz"
        vcf_name_nosuffix = f"GA100K_addAA_chr{chr}_mm1_maf0.1_eagle"

    elif dataset_name in ["1KG", "KGP"]:
        metadata_file = "/scratch/myang_shared/data/1KG/integrated_call_samples_v3.20130502.ALL.panel"
        vcf_directory = "/scratch/myang_shared/data/1KG/addAA/"
        vcf_name = f"ALL.chr{chr}.addAA.vcf.gz"
        vcf_name_nosuffix= f"ALL.chr{chr}.addAA"

    elif dataset_name in ["929", "DGP"]:
        metadata_file = "/scratch/myang_shared/data/929_WGS/hgdp_wgs.20190516.metadata.txt"
        vcf_directory = "/scratch/myang_shared/data/929_WGS/hg19_929_best/"
        vcf_name = f"929_phased_hg19_addAA.{chr}.vcf.gz"
        vcf_name_nosuffix= f"929_phased_hg19_addAA.{chr}"

    else:
        raise ValueError(f"Unknown dataset_name: {dataset_name}")

    context = {
        "base_dir": base_dir,
        "script": script,
        "script_name": script_name,
        "account": account,
        "partition": partition,
        "email": email,
        "dataset_name": dataset_name,
        "datasets_list": run["datasets_list"],
        "input_megafile": os.path.join(input_dir, run["input_megafile"]),
        "working_directory": working_directory,
        "metadata_file": metadata_file,
        "chr": run["chr"],
        "vcf_directory": vcf_directory,
        "vcf_name": vcf_name,
        "vcf_name_nosuffix": vcf_name_nosuffix,
        "logs_directory": logs_directory,
        "snp": run["snp"],
        "gene_name": run["gene_name"],
        "position": run["position"],
        "p_value": run["p_value"],
        "ancestral_path": ancestral_path,
        "ancestral_manifest": ancestral_manifest,
        "recombmap_base_directory": recombmap_base_directory,
        #"timebins_dictionary": timebins_dictionary,
        "total_epochs": run["total_epochs"],
        "input_nickname": run["input_nickname"],
        "generation_time": run["generation_time"], 
        "graph_prefix": run["graph_prefix"], 
        "allele_frequency_graphing_setting": run["allele_frequency_graphing_setting"], 
        "confidence_interval": run["confidence_interval"], 
        "allele_frequency_graph_type": run["allele_frequency_graph_type"], 
        "x_axis_metric": run["x_axis_metric"], 
        "use_groupings": run["use_groupings"], 
        "multiple_inputfiles": run["multiple_inputfiles"], 
        "renaming": run["renaming"], 
        "selection_coefficient_graphing_setting": run["selection_coefficient_graphing_setting"], 
        "min_time": run["min_time"],
        "max_time": run["max_time"],
        "create_new_avg_tables": run["create_new_avg_tables"],
        "create_combined_ihs_relate_table": run["create_combined_ihs_relate_table"],
        "create_relate_table": run["create_relate_table"],
        "rerun_multiple_testing_corrections": run["rerun_multiple_testing_corrections"],
        "show_DAF_value": run["show_DAF_value"],
        "num_samples": run["num_samples"],
        "pad_bp": run["pad_bp"],
        "path_to_relate": path_to_relate,
        "path_to_clues2": path_to_clues2,
        "max_workers": run["max_workers"],
        "defined_derived": run["defined_derived"],
        "defined_ancestral": run["defined_ancestral"],
    }

    command = build_command(script_name, context)

    if script_name in scripts_to_run_only_once:
        print(f"\n🟡 Running {script_name} command: {' '.join(command)}\n")
    else:
        print(f"\n🟡 Running {script_name} command for {dataset_name}: {' '.join(command)}\n")

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append((dataset_name, p))

# Here, you're actually running everything!!!
for dataset_name, process in processes:
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        job_match = re.search(r"Submitted batch job (\d+)", stdout)

        if job_match:
            job_id = job_match.group(1)
            print(f"✅ {dataset_name} submitted successfully with job submission number {job_id}.")
        else:
            print(f"✅ {dataset_name} finished successfully.")

        if stdout.strip():
            print(f"--- STDOUT ({dataset_name}) ---\n{stdout.strip()}")
    else:
        print(f"❌ {dataset_name} failed with return code {process.returncode}.")
        print(f"--- STDERR ({dataset_name}) ---\n{stderr.strip()}")
   
