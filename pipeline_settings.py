"""
pipeline_settings.py

This script contains functions to be imported into the other scripts within the pipeline.

There are [4? # FIX - confirm] scripts that you SHOULD edit: 
    1. general_comparison_groupings()
    2. timebins() 
    3. flat_log_of_runs() - optional, if you want to combine results across runs
    4. renaming_popns() - optional, if you want to rename populations in resulting figures
Examples of these functions are given below.

This script ALSO contains a number of scripts that you SHOULD NOT edit!!! 
Anything under the "DO NOT TOUCH THESE" comment should be left as-is. 
"""
import ast
import fcntl
import json
import tempfile
import pandas as pd
import os
from PIL import Image
import argparse
import sys
import tempfile
import shutil
from filelock import FileLock, Timeout
import numpy as np
from typing import List, Tuple
import math

############# Edit these functions!
def general_comparison_groupings():
    plot_tgt_groupings_dict = {'NativeAmerican': ['PEL', 'PUR', 'MXL', 'CLM'],
 'CentralEastSouthAsia': ['Jamatia_Mog_Chakma_Toto',
  'Halba_Oraon_Munda_Muria_Abujmaria_Tanti_Dorla_BisonHornMaria',
  'Birhor_HillKorwa_Kamar_KondaReddy_Dhurwa',
  'Agharia_Chamar_Lambada_Nababuddha_Mahar',
  'BEB'],
 'MongolianSteppe': ['Han', 'Hazara', 'Russian', 'Uygur', 'Yakut'],
 'Iberian': ['GBR', 'IBS', 'Basque', 'French_Orcadian'],
 'MiddleEast': ['Mozabite', 'Druze', 'Palestinian', 'Bedouin'],
 'NortheastEurope': ['Adygei', 'Russian', 'FIN', 'CEU'],
 'BeninKingdom': ['ESN', 'YRI', 'Mandenka_Yoruba'],
 'SouthwestChina': ['Han', 'Naxi_Yi_Tu', 'CHS', 'Miao_She_Tujia'],
 'PapuanOceanian': ['Bougainville', 'PapuanSepik', 'PapuanHighlands'],
 'WesternAfrica': ['MSL', 'YRI', 'GWD', 'LWK', 'Bantu'],
 'Mediterranean': ['IBS', 'Sardinian', 'BergamoItalian_Tuscan', 'TSI'],
 'AdmixedAfricanAmerican ': ['ASW', 'ACB'],
 'NortheastAsia': ['CHB',
  'Korean',
  'Japanese',
  'JPT',
  'Han_NorthernHan',
  'Korean_Japanese'],
 'SouthAsia': ['SouthAsia1',
  'Onge_Jarwa',
  'Urban',
  'GIH',
  'BEB',
  'ITU',
  'STU',
  'Westbengalbrahmin_Rajput_Saryuparibrahmin'],
 'Siberia': ['Yakut',
  'Daur_Hezhen_Oroqen_Xibo',
  'Han_NorthernHan',
  'Buryat_Xhalxh',
  'Buryat'],
 'Mende': ['GWD', 'MSL'],
 'IslandOceania': ['Aeta', 'Austronesian_Ati_Flores', 'Flores'],
 'NigerCongo': ['YRI', 'MSL', 'GWD'],
 'BantuExpansion': ['Bantu', 'LWK'],
 'NortheastIndia': ['Jamatia_Mog_Chakma_Toto', 'RanaTharu_Manipuri', 'BEB'],
 'SouthernIndia': ['Birhor_HillKorwa_Kamar_KondaReddy_Dhurwa',
  'SouthAsia2',
  'Urban'],
 'Oceania': ['Austronesian_Ati_Flores',
  'Aeta',
  'PapuanHighlands',
  'PapuanSepik',
  'Bougainville',
  'Flores'],
 'KGPEastAsia': ['JPT', 'KHV', 'CHS', 'CDX', 'CHB'],
 'SouthernChina': ['CDX', 'Dai_Cambodian_Lahu', 'CHB', 'CHS', 'Han', 'Dai'],
 'PygmyForestHunterGatherers': ['Biaka_Mbuti'],
 'NorthWestSouthAsia': ['SouthAsia1',
  'Gujjar_Khatri_Brahui_Pathan',
  'Sindhi_Pathan_Burusho',
  'PJL',
  'Hazara',
  'Kalash',
  'Makrani_Balochi_Brahui'],
 'SoutheastAsia': ['CHS',
  'CHB',
  'KHV',
  'Cambodian_Lahu',
  'Dai',
  'Dai_Cambodian_Lahu']}
    return plot_tgt_groupings_dict

def timebins():
    return {
        "1epoch": ["XXX"], # keep "XXX" here for 1-epoch models
        "2epoch_150": ["150"],
        "2epoch_300": ["300"],
        "2epoch_450": ["450"],
        "3epoch_300_450": ["300", "450"],
        "3epoch_150_450": ["150", "450"],
        "3epoch_150_300": ["150", "300"],
        "4epoch_150_300_450": ["150", "300", "450"],
        "2epoch_75": ["75"],
        "3epoch_75_150": ["75", "150"],
        "3epoch_75_300": ["75", "300"],
        "3epoch_75_450": ["75", "450"],
        "4epoch_75_150_300": ["75", "150", "300"],
        "4epoch_75_300_450": ["75", "300", "450"],
        "4epoch_75_150_450": ["75", "150", "450"],
        "5epoch_75_150_300_450": ["75", "150", "300", "450"]
    }

def flat_log_of_runs():
    # example of how to list runs vs the populations they include:
    # "input_nickname" : ["population1 - as seen in data", "population2 - as seen in data"]
    logging_runs_dict = {
        "august": ["SAS2_BEB_7","SAS2_STU_7","SAS2_ITU_7","SAS2_PJL_7","SAS2_GIH_7","SouthAsia_GIH","SouthAsiaSTUAll","SouthAsiaSTU","SouthAsia_PJL","Biaka_Mbuti","Bantu_LWK","extraline"],
        "redo_4": ["Kalash_4","Uygur_4","Sindhi_Pathan_Burusho_4","Makrani_Balochi_Brahui_4","Hazara_4","Bougainville_4","PapuanSepik_4","PapuanHighlands_4","Druze_4","Bedouin_4","Palestinian_4","Mozabite_4","Adygei_4","Basque_4","BergamoItalian_Tuscan_4","French_Orcadian_4","Russian_4","Bantu_4","Mandenka_Yoruba_4","Biaka_San_Mbuti_4","Cambodian_Lahu_4","Dai_4","Daur_Hezhen_Oroqen_Xibo_4","Han_NorthernHan_4","Japanese_4","Miao_She_Tujia_4","Naxi_Yi_Tu_4","Yakut_4","Aeta_4","BuryatXhalxh_4","KoreanJapanese_4","AustronesianAtiFlores_4","AustronesianAti_4","Korean_4","Buryat_4","GujjarKhatriBrahuiPathan_PJL_4","SAS2_PJL_4","BirhorHillkorwaKamarKondareddyDhurwa_PJL_4","OngeJarwa_PJL_4","JamatiaMogChakmaToto_PJL_4","RanaharManipuri_PJL_4","HalbaOraonMundaMuriaAbujmariaTantiDorlaBisonhornmaria_PJL_4","AghariaChamarLambadaNababuddhaMahar_PJL_4","WestbengalbrahminRajputSaryuparibrahmin_PJL_4","Urban_PJL_4","GujjarKhatriBrahuiPathan_GIH_4","SAS2_GIH_4","BirhorHillkorwaKamarKondareddyDhurwa_GIH_4","OngeJarwa_GIH_4","JamatiaMogChakmaToto_GIH_4","RanaharManipuri_GIH_4","HalbaOraonMundaMuriaAbujmariaTantiDorlaBisonhornmaria_GIH_4","AghariaChamarLambadaNababuddhaMahar_GIH_4","WestbengalbrahminRajputSaryuparibrahmin_GIH_4","Urban_GIH_4","ACB_4","ASW_4","BEB_4","CEU_4","CHS_4","CLM_4","ESN_4","FIN_4","GBR_4","GIH_4","GWD_4","IBS_4","ITU_4","LWK_4","MSL_4","MXL_4","PEL_4","PJL_4","STU_4","TSI_4","CDX_C_2d_4","CHS_C_2d_4","KHV_C_2d_4"],
        "redo_5": ["Han_NorthernHan_5","CDX_C_2d_5","CHS_C_2d_5","KHV_C_2d_5","CDX_5","KHV_5","JPT_5","PUR_5","CHB_CHB","CHB_CHS","CHB_CDX","CHB_KHV","CHB_JPT","CHB_ASW","CHB_YRI","CHB_GBR","CHB_CEU","CHB_IBS","CHB_TSI","CHB_PUR"],
        "redo_6": ["Han_NorthernHan_CDX_6","Han_NorthernHan_CHB_6","Han_CDX_6","Han_CHB_6","Miao_She_Tujia_6","Cambodian_Lahu_6","Dai_Cambodian_Lahu_6","Yakut_6","AustronesianAtiFlores_KHV_6","Flores_KHV_6","Flores_CHS_6","AustronesianAti_KHV_6","Austronesian_KHV_6","Austronesian_CHS_6","Druze_6","Palestinian_6","Dai_4"]
    }

    # flatten list for mapping
    run_log = {pop: tag for tag, pops in logging_runs_dict.items() for pop in pops}
    return run_log

def renaming_popns():
    # example of how to list old names + new names
    # "old_name": "new_name"
    popn_renaming_dict = {
        "Adygei_4":"Adygei",
        "Bantu_4":"Bantu",
        "Basque_4":"Basque",
        "Bedouin_4":"Bedouin",
        "BergamoItalian_Tuscan_4":"BergamoItalian_Tuscan",
        "Biaka_San_Mbuti_4":"Biaka_San_Mbuti",
        "Bougainville_4":"Bougainville",
        "Cambodian_Lahu_6":"Cambodian_Lahu",
        "Dai_4":"Dai",
        "Dai_Cambodian_Lahu_6":"Dai_Cambodian_Lahu",
        "Daur_Hezhen_Oroqen_Xibo_4":"Daur_Hezhen_Oroqen_Xibo",
        "Druze_6":"Druze",
        "French_Orcadian_4":"French_Orcadian",
        "Han_CDX_6":"Han_CDX",
        "Han_CHB_6":"Han_CHB",
        "Han_NorthernHan_CHB_6":"Han_NorthernHan_CHB",
        "Hazara_4":"Hazara",
        "Japanese_4":"Japanese",
        "Kalash_4":"Kalash",
        "Makrani_Balochi_Brahui_4":"Makrani_Balochi_Brahui",
        "Mandenka_Yoruba_4":"Mandenka_Yoruba",
        "Miao_She_Tujia_6":"Miao_She_Tujia",
        "Mozabite_4":"Mozabite",
        "Naxi_Yi_Tu_4":"Naxi_Yi_Tu",
        "Palestinian_6":"Palestinian",
        "PapuanHighlands_4":"PapuanHighlands",
        "PapuanSepik_4":"PapuanSepik",
        "Russian_4":"Russian",
        "Sardinian_4":"Sardinian",
        "Sindhi_Pathan_Burusho_4":"Sindhi_Pathan_Burusho",
        "Uygur_4":"Uygur",
        "Yakut_6":"Yakut",
        "Aeta_4":"Aeta",
        "AghariaChamarLambadaNababuddhaMahar_PJL_4":"AghariaChamarLambadaNababuddhaMahar_PJL",
        "Austronesian_CHS_6":"Austronesian_CHS",
        "Austronesian_KHV_6":"Austronesian_KHV",
        "AustronesianAti_4":"AustronesianAti",
        "AustronesianAti_KHV_6":"AustronesianAti_KHV",
        "AustronesianAtiFlores_4":"AustronesianAtiFlores",
        "AustronesianAtiFlores_KHV_6":"AustronesianAtiFlores",
        "BirhorHillkorwaKamarKondareddyDhurwa_GIH_4":"BirhorHillkorwaKamarKondareddyDhurwa_GIH_",
        "Buryat_4":"Buryat",
        "BuryatXhalxh_4":"BuryatXhalxh",
        "Flores_CHS_6":"Flores_CHS",
        "Flores_KHV_6":"Flores_KHV",
        "GujjarKhatriBrahuiPathan_GIH_4":"GujjarKhatriBrahuiPathan_GIH",
        "GujjarKhatriBrahuiPathan_PJL_4":"GujjarKhatriBrahuiPathan_PJL",
        "HalbaOraonMundaMuriaAbujmariaTantiDorlaBisonhornmaria_GIH_4":"HalbaOraonMundaMuriaAbujmariaTantiDorlaBisonhornmaria_GIH",
        "JamatiaMogChakmaToto_GIH_4":"JamatiaMogChakmaToto_GIH",
        "Korean_4":"Korean",
        "KoreanJapanese_4":"KoreanJapanese",
        "OngeJarwa_GIH_4":"OngeJarwa_GIH",
        "RanaharManipuri_GIH_4":"RanaharManipuri_GIH",
        "SAS2_GIH_4":"SAS2_GIH",
        "SouthAsia_GIH":"SouthAsia_GIH",
        "SouthAsia_PJL":"SouthAsia_PJL",
        "SouthAsia_STUAll":"SouthAsia_STUAll",
        "SouthAsia_STU":"SouthAsia_STU",
        "SAS2_BEB_7":"SAS2_BEB",
        "SAS2_STU_7":"SAS2_STU",
        "SAS2_ITU_7":"SAS2_ITU",
        "SAS2_PJL_7":"SAS2_PJL",
        "SAS2_GIH_7":"SAS2_GIH",
        "Urban_GIH_4":"Urban_GIH",
        "WestbengalbrahminRajputSaryuparibrahmin_GIH_4":"WestbengalbrahminRajputSaryuparibrahmin_GIH",
        "ACB_4":"ACB",
        "ASW_4":"ASW",
        "BEB_4":"BEB",
        "CDX_5":"CDX",
        "CDX_C_2d_5":"CDX_C_2d",
        "CEU_4":"CEU",
        "CHB_ASW":"CHB_ASW",
        "CHB_CDX":"CHB_CDX",
        "CHB_CEU":"CHB_CEU",
        "CHB_CHB":"CHB_CHB",
        "CHB_CHS":"CHB_CHS",
        "CHB_GBR":"CHB_GBR",
        "CHB_IBS":"CHB_IBS",
        "CHB_JPT":"CHB_JPT",
        "CHB_KHV":"CHB_KHV",
        "CHB_PUR":"CHB_PUR",
        "CHB_TSI":"CHB_TSI",
        "CHB_YRI":"CHB_YRI",
        "CHS_4":"CHS",
        "CHS_C_2d_5":"CHS_C_2d",
        "CLM_4":"CLM",
        "ESN_4":"ESN",
        "FIN_4":"FIN",
        "GBR_4":"GBR",
        "GIH_4":"GIH",
        "GWD_4":"GWD",
        "IBS_4":"IBS",
        "ITU_4":"ITU",
        "JPT_5":"JPT",
        "KHV_5":"KHV",
        "KHV_C_2d_5":"KHV_C_2d_5",
        "LWK_4":"LWK",
        "MSL_4":"MSL",
        "MXL_4":"MXL",
        "PEL_4":"PEL",
        "PJL_4":"PJL",
        "PUR_5":"PUR",
        "STU_4":"STU",
        "TSI_4":"TSI",
        "YRI_4":"YRI"
    }
    return popn_renaming_dict

def populations_to_exclude_from_multiple_testing_corrections(snp):
    rs_snp = f"rs{snp}"

    dict = {
        "SNP": ["population1, population2, population3"], 
        "rs1229984": [
            "KGP,ACB", "KGP,ASW", "KGP,CLM", "KGP,MXL", "KGP,PEL", "KGP,PUR", 
            "GAP,Korean_Japanese", "DGP,Dai", "GAP,Cambodian_Lahu",
            "GAP,Buryat", "GAP,Flores", "DGP,Han_NorthernHan"
            ],
        "rs2066702": [
            "fill this out",
            ],

    }
    return dict.get(str(rs_snp), [])

populations_missing_snps = {
    "rs2066702": [
        "DGP,Adygei",
        "DGP,Basque",
        "GAP,Aeta",
        "GAP,Agharia_Chamar_Lambada_Nababuddha_Mahar",
        "DGP,BergamoItalian_Tuscan",
        "GAP,Austronesian_Ati_Flores",
        "GAP,Birhor_HillKorwa_Kamar_KondaReddy_Dhurwa",
        "DGP,Bougainville",
        "DGP,Cambodian_Lahu",
        "GAP,Buryat",
        "KGP,BEB",
        "DGP,Dai_Cambodian_Lahu",
        "GAP,Buryat_Xhalxh",
        "DGP,Dai",
        "KGP,CDX",
        "DGP,Daur_Hezhen_Oroqen_Xibo",
        "GAP,Flores",
        "DGP,Druze",
        "GAP,Gujjar_Khatri_Brahui_Pathan",
        "KGP,CEU",
        "DGP,French_Orcadian",
        "GAP,Halba_Oraon_Munda_Muria_Abujmaria_Tanti_Dorla_BisonHornMaria",
        "DGP,Han",
        "KGP,CHB",
        "GAP,Jamatia_Mog_Chakma_Toto",
        "DGP,Han_NorthernHan",
        "GAP,Korean",
        "KGP,CHS",
        "DGP,Japanese",
        "GAP,Korean_Japanese",
        "DGP,Makrani_Balochi_Brahui",
        "GAP,Onge_Jarwa",
        "GAP,RanaTharu_Manipuri",
        "GAP,Central_SouthAsia",
        "DGP,Miao_She_Tujia",
        "KGP,FIN",
        "GAP,Southern_SouthAsia",
        "DGP,Mozabite",
        "GAP,Urban",
        "DGP,Naxi_Yi_Tu",
        "KGP,GBR",
        "GAP,Westbengalbrahmin_Rajput_Saryuparibrahmin",
        "DGP,Palestinian",
        "DGP,PapuanHighlands",
        "KGP,GIH",
        "DGP,PapuanSepik",
        "DGP,Russian",
        "DGP,Sardinian",
        "KGP,IBS",
        "DGP,Uygur",
        "DGP,Yakut",
        "KGP,ITU",
        "KGP,JPT",
        "KGP,KHV",
        "KGP,PJL",
        "KGP,STU",
        "KGP,TSI"
    ],
    "snp": [
        "dataset1,population1",
        "dataset2,population2",
        "dataset3,population3"
    ]
}

populations_not_mapping_snps = {
    "rs1229984": [
        "DGP,Adygei",
        "KGP,ACB",
        "KGP,BEB",
        "DGP,Basque",
        "DGP,BergamoItalian_Tuscan",
        "DGP,Dai_Cambodian_Lahu",
        "KGP,CEU",
        "DGP,Druze",
        "DGP,Mozabite",
        "KGP,CLM",
        "DGP,Naxi_Yi_Tu",
        "DGP,Palestinian",
        "DGP,Russian",
        "DGP,Sardinian",
        "DGP,Uygur",
        "KGP,PEL",
        "KGP,PUR"
    ],
    "snp": [
        "dataset1,population1",
        "dataset2,population2",
        "dataset3,population3"
    ]
}
############ DO NOT TOUCH THESE.
SNP_DAF_ZERO_MESSAGE = "SNP DAF = 0"
SNP_NOT_MAPPING_MESSAGE = "SNP is_not_mapping = 1"

def normalize_snp_id(snp):
    snp_string = str(snp).strip()
    return f"rs{snp_string.removeprefix('rs')}"

def record_population_missing_snp(working_directory, snp, dataset_name, group):
    """
    Persistently record that a dataset/group should be excluded downstream
    because the SNP has DAF = 0 or is absent from the relevant haps output.

    This updates the populations_missing_snps dictionary inside:
        {working_directory}/scripts/pipeline_settings.py

    Example output:
        populations_missing_snps = {
            "rs1229984": [
                "DGP,Bantu",
                "KGP,YRI"
            ]
        }
    """

    snp_key = normalize_snp_id(snp)
    entry = f"{dataset_name},{group}"

    settings_path = os.path.join(
        os.path.normpath(working_directory),
        "scripts",
        "pipeline_settings.py"
    )

    if not os.path.exists(settings_path):
        # Fallback to the currently imported file.
        settings_path = os.path.abspath(__file__)

    lock_path = settings_path + ".lock"

    with open(lock_path, "w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)

        with open(settings_path, "r") as file:
            source = file.read()

        lines = source.splitlines(keepends=True)

        assignment_start = None
        assignment_end = None
        current_dict = {}

        try:
            tree = ast.parse(source)

            for node in tree.body:
                is_target_assignment = (
                    isinstance(node, ast.Assign)
                    and any(
                        isinstance(target, ast.Name)
                        and target.id == "populations_missing_snps"
                        for target in node.targets
                    )
                )

                if is_target_assignment:
                    assignment_start = node.lineno - 1
                    assignment_end = node.end_lineno
                    current_dict = ast.literal_eval(node.value)
                    break

        except Exception:
            current_dict = globals().get("populations_missing_snps", {})

        if not isinstance(current_dict, dict):
            current_dict = {}

        current_dict.setdefault(snp_key, [])

        if entry not in current_dict[snp_key]:
            current_dict[snp_key].append(entry)

        rendered_assignment = (
            "populations_missing_snps = "
            + json.dumps(current_dict, indent=4, sort_keys=True)
            + "\n"
        )

        if assignment_start is not None and assignment_end is not None:
            lines[assignment_start:assignment_end] = [rendered_assignment]
        else:
            if lines and not lines[-1].endswith("\n"):
                lines[-1] += "\n"

            lines.extend([
                "\n",
                "# Populations where the SNP has DAF = 0 or is missing from haps.\n",
                rendered_assignment
            ])

        new_source = "".join(lines)

        fd, temp_path = tempfile.mkstemp(
            dir=os.path.dirname(settings_path),
            prefix=".pipeline_settings.",
            suffix=".tmp"
        )

        try:
            with os.fdopen(fd, "w") as temp_file:
                temp_file.write(new_source)

            os.replace(temp_path, settings_path)

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        globals()["populations_missing_snps"] = current_dict

        fcntl.flock(lock_file, fcntl.LOCK_UN)

    return current_dict

def population_missing_snp(snp, dataset_name, group):
    """
    Check whether a dataset/group has already been recorded as missing this SNP.
    """

    snp_key = normalize_snp_id(snp)
    entry = f"{dataset_name},{group}"

    return entry in populations_missing_snps.get(snp_key, [])

########################### 260608

def record_population_not_mapping_snp(working_directory, snp, dataset_name, group):
    """
    Persistently record that a dataset/group should be excluded downstream
    because the SNP is marked is_not_mapping=1 in the _popsize_resample.mut file.

    This updates the populations_not_mapping_snps dictionary inside:
        {working_directory}/scripts/pipeline_settings.py

    Example output:
        populations_not_mapping_snps = {
            "rs1229984": [
                "DGP,Druze",
                "KGP,CHB"
            ]
        }
    """

    snp_key = normalize_snp_id(snp)
    entry = f"{dataset_name},{group}"

    settings_path = os.path.join(
        os.path.normpath(working_directory),
        "scripts",
        "pipeline_settings.py"
    )

    if not os.path.exists(settings_path):
        # Fallback to the currently imported file.
        settings_path = os.path.abspath(__file__)

    lock_path = settings_path + ".lock"

    with open(lock_path, "w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)

        with open(settings_path, "r") as file:
            source = file.read()

        lines = source.splitlines(keepends=True)

        assignment_start = None
        assignment_end = None
        current_dict = {}

        try:
            tree = ast.parse(source)

            for node in tree.body:
                is_target_assignment = (
                    isinstance(node, ast.Assign)
                    and any(
                        isinstance(target, ast.Name)
                        and target.id == "populations_not_mapping_snps"
                        for target in node.targets
                    )
                )

                if is_target_assignment:
                    assignment_start = node.lineno - 1
                    assignment_end = node.end_lineno
                    current_dict = ast.literal_eval(node.value)
                    break

        except Exception:
            current_dict = globals().get("populations_not_mapping_snps", {})

        if not isinstance(current_dict, dict):
            current_dict = {}

        current_dict.setdefault(snp_key, [])

        if entry not in current_dict[snp_key]:
            current_dict[snp_key].append(entry)

        rendered_assignment = (
            "populations_not_mapping_snps = "
            + json.dumps(current_dict, indent=4, sort_keys=True)
            + "\n"
        )

        if assignment_start is not None and assignment_end is not None:
            lines[assignment_start:assignment_end] = [rendered_assignment]
        else:
            if lines and not lines[-1].endswith("\n"):
                lines[-1] += "\n"

            lines.extend([
                "\n",
                "# Populations where the SNP is marked is_not_mapping=1 in _popsize_resample.mut.\n",
                rendered_assignment
            ])

        new_source = "".join(lines)

        fd, temp_path = tempfile.mkstemp(
            dir=os.path.dirname(settings_path),
            prefix=".pipeline_settings.",
            suffix=".tmp"
        )

        try:
            with os.fdopen(fd, "w") as temp_file:
                temp_file.write(new_source)

            os.replace(temp_path, settings_path)

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        globals()["populations_not_mapping_snps"] = current_dict

        fcntl.flock(lock_file, fcntl.LOCK_UN)

    return current_dict

def population_not_mapping_snp(snp, dataset_name, group):
    """
    Check whether a dataset/group has already been recorded as having
    is_not_mapping=1 for this SNP in the _popsize_resample.mut file.
    """

    snp_key = normalize_snp_id(snp)
    entry = f"{dataset_name},{group}"

    return entry in populations_not_mapping_snps.get(snp_key, [])


def load_dataset_map(tsv_path):
    """
    Reads worldwide_populations_inputfile.tsv and returns
    a dict mapping generic population names → dataset source (1KG, 929, GA100K)
    """

    if tsv_path is None:
        tsv_path = "/scratch/myang_shared/lab/Aine/Relate_CLUES2_pipeline/input_files/worldwide_populations_inputfile.tsv" # FIX: have this defined in master pipeline
    if not os.path.exists(tsv_path):
        raise FileNotFoundError(f"Missing dataset map TSV: {tsv_path}")
    
    df = pd.read_csv(tsv_path, sep="\t")
    df = df[df["dataset"].notna() & df["group_name"].notna()]
    dataset_map = dict(zip(df["group_name"], df["dataset"]))
    return dataset_map

def str_to_bool(value):
    if isinstance(value, bool):
        return value

    value = str(value).strip().lower()

    if value in ["true", "t", "yes", "y", "1"]:
        return True
    elif value in ["false", "f", "no", "n", "0"]:
        return False
    else:
        raise argparse.ArgumentTypeError(f"Expected boolean, got: {value}")

def display_or_na(value):
    if value is None:
        return "NA"
    value = str(value).strip()
    if value == "" or value.lower() in {"na", "nan", "none"}:
        return "NA"
    return value

def combine_pngs_to_pdf(png_paths, output_pdf):
    if not png_paths:
        return
    try:
        images = [Image.open(p).convert("RGB") for p in png_paths]
        first, rest = images[0], images[1:]
        first.save(output_pdf, save_all=True, append_images=rest)
        print(f"📄 Combined {len(png_paths)} plots → {output_pdf}")
    finally:
        for im in images:
            im.close()
    for p in png_paths:
        if os.path.exists(p):
            try:
                os.remove(p)
            except OSError as e:
                print(f"⚠️ Could not delete {p}: {e}")

def update_meta_tsv(working_directory, input_nickname, dataset_name, group, step_name, mark):
    input_megafile_logdir = os.path.join(working_directory, "input_files", f"{input_nickname}_logs")
    input_megafile_logtsv = os.path.join(input_megafile_logdir, f"{input_nickname}_progresslog.tsv")
    lock_path = input_megafile_logtsv + ".lock"
 
    # Ensure log directory exists
    os.makedirs(input_megafile_logdir, exist_ok=True)

    lock = FileLock(lock_path, timeout=10)  # wait max 10 sec
    try:
        with lock:
            if not os.path.exists(input_megafile_logtsv):
                raise FileNotFoundError(f"Log file '{input_megafile_logtsv}' does not exist!")

            with open(input_megafile_logtsv, 'r') as infile:
                lines = infile.readlines()

            if not lines:
                raise ValueError(f"Log file '{input_megafile_logtsv}' is empty!")

            header = lines[0].strip().split('\t')
            header_dict = {col: idx for idx, col in enumerate(header)}
            step_index = header_dict.get(step_name)

            if step_index is None:
                raise ValueError(
                    f"Step '{step_name}' not found in header. "
                    f"Available steps: {list(header_dict.keys())}"
                )

            # Write to a temp file
            fd, temp_path = tempfile.mkstemp()
            with os.fdopen(fd, 'w') as tmpfile:
                tmpfile.write('\t'.join(header) + '\n')
                for line in lines[1:]:
                    lineparts = line.strip().split('\t')
                    if len(lineparts) < 2:
                        tmpfile.write(line)
                        continue
                    if lineparts[0] == dataset_name and lineparts[1] == group:
                        while len(lineparts) <= step_index:
                            lineparts.append('')
                        lineparts[step_index] = mark
                    tmpfile.write('\t'.join(lineparts) + '\n')

            shutil.move(temp_path, input_megafile_logtsv)

    except Timeout:
        print(f"❌ Could not acquire lock on {lock_path}. Another process may be stuck.")
        sys.exit(1)

def initialize_meta_tsv(working_directory, input_nickname,  input_megafile):
    input_megafile_logdir= os.path.join(working_directory, "input_files", f"{input_nickname}_logs")
    os.makedirs(input_megafile_logdir, exist_ok=True)

    # initialize input_megafile_logcsv
    input_megafile_logtsv = os.path.join(input_megafile_logdir, f"{input_nickname}_progresslog.tsv")
    with open(input_megafile, 'r') as template, open(input_megafile_logtsv, 'w') as csv:
        header = [
            "dataset", "group_name", "involved_groups", "recomb_map", "region", "inds_to_exclude", "n", "DAF",
            "CLUES2_4",
            "CLUES2_3",
            "CLUES2_2",
            "CLUES2_1",
            "Relate_4",
            "Relate_3",
            "Relate_2",
            "Relate_1",
            "iHS",
            "initialization_6",
            "initialization_5",
            "initialization_4",
            "initialization_3",
            "initialization_2",
        ] 

        csv.write('\t'.join(header) + '\n')
        for line in template:
            lineparts = line.strip().split('\t')
            if lineparts[0] != "dataset": 
                while len(lineparts) < len(header):
                    lineparts.append('')
                csv.write('\t'.join(lineparts) + '\n')
        csv.flush()
        os.fsync(csv.fileno())

def calculate_daf(
    working_directory,
    dataset_name,
    group,
    snp,
    gene_name,
    defined_derived=None,
    defined_ancestral=None,
):
    """
    Calculate derived allele frequency from the group VCF.

    This function no longer assumes ALT = derived.
    It uses user-defined derived/ancestral alleles if provided.
    Otherwise, it infers ancestral from INFO/AA and derived as the other REF/ALT allele.
    """
    vcf_directory = os.path.join(working_directory, f"Relate_{dataset_name}", group)
    vcf_file = f"{group}_{gene_name}_{dataset_name}_{snp}.vcf"
    vcf_path = os.path.join(vcf_directory, vcf_file)

    if not os.path.exists(vcf_path):
        print(f"Error: VCF file not found: {vcf_path}")
        return None

    parts = find_target_vcf_parts(vcf_path, snp)

    if parts is None:
        print(f"Warning: rs{snp} not found in VCF: {vcf_path}")
        return None

    try:
        ancestral, derived, ref, alt, aa = get_orientation_from_vcf_parts(
            parts,
            defined_derived=defined_derived,
            defined_ancestral=defined_ancestral,
        )
    except ValueError as e:
        print(f"Error determining allele orientation for rs{snp}: {e}")
        return None

    sample_fields = parts[9:]
    D, T = count_vcf_derived_alleles(sample_fields, ref, alt, derived)

    if T == 0:
        print(f"Warning: No allele counts found for rs{snp} in {vcf_path}")
        return None

    DAF = D / T

    print(
        f"VCF DAF for rs{snp}: D={D}, T={T}, DAF={DAF}; "
        f"REF={ref}, ALT={alt}, AA={aa}, ancestral={ancestral}, derived={derived}"
    )

    return DAF

def calculate_vcf_stats(
    working_directory,
    dataset_name,
    group,
    snp,
    gene_name,
    vcf_path,
    defined_derived=None,
    defined_ancestral=None,
):
    """
    Calculate VCF-derived SNP stats.

    Returns:
      [D, A, T, DAF, num_individuals]

    D = derived allele count
    A = ancestral/non-derived allele count
    T = total counted alleles
    DAF = D / T

    Note: A used to be labeled as "Alt allele" in older code, but that is misleading
    when ALT is ancestral. Here A is the non-derived/ancestral count.
    """
    if not os.path.exists(vcf_path):
        print(f"Error: VCF file not found: {vcf_path}")
        return None

    parts = find_target_vcf_parts(vcf_path, snp)

    if parts is None:
        print(f"Warning: rs{snp} not found in VCF: {vcf_path}")
        return None

    try:
        ancestral, derived, ref, alt, aa = get_orientation_from_vcf_parts(
            parts,
            defined_derived=defined_derived,
            defined_ancestral=defined_ancestral,
        )
    except ValueError as e:
        print(f"Error determining allele orientation for rs{snp}: {e}")
        return None

    sample_fields = parts[9:]
    num_individuals = len(sample_fields)

    D, T = count_vcf_derived_alleles(sample_fields, ref, alt, derived)

    if T == 0:
        print(f"Warning: No allele counts found for rs{snp} in {vcf_path}")
        return None

    A = T - D
    DAF = D / T

    print(
        f"VCF stats for rs{snp}: D={D}, A={A}, T={T}, DAF={DAF}, n={num_individuals}; "
        f"REF={ref}, ALT={alt}, AA={aa}, ancestral={ancestral}, derived={derived}"
    )

    return [D, A, T, DAF, num_individuals]

def calculate_haps(
    working_directory,
    vcfs_directory,
    dataset_name,
    chr,
    group,
    snp,
    gene_name,
    defined_derived=None,
    defined_ancestral=None,
    debug=False
):
    """
    Calculate derived allele frequency from .haps.

    Important fix:
    This does NOT decide flipping from AA == ALT.
    Instead, it checks the actual .haps allele columns:

      if allele0 == ancestral and allele1 == derived:
          DAF = count(1) / total

      if allele0 == derived and allele1 == ancestral:
          DAF = count(0) / total

    This makes it robust to cases where REF/ALT != ancestral/derived.
    """

    def dbg(msg):
        if debug:
            print(f"[calculate_haps DEBUG] {msg}", flush=True)

    def fail(msg):
        print(f"[calculate_haps ERROR] {msg}", flush=True)
        return None

    tolerance = 0.1
    
    target_snp = f"rs{str(snp).removeprefix('rs')}"

    

    def mark_snp_daf_zero(reason):
        print(
            f"[calculate_haps INFO] SNP DAF = 0 for "
            f"{dataset_name} {group} {target_snp}: {reason}",
            flush=True
        )

        record_population_missing_snp(
            working_directory=vcfs_directory,
            snp=snp,
            dataset_name=dataset_name,
            group=group
        )

        return SNP_DAF_ZERO_MESSAGE




    last_folder = os.path.basename(os.path.normpath(working_directory))

    vcf_directory = os.path.join(vcfs_directory, f"Relate_{dataset_name}", group)
    vcf_file = f"{group}_{gene_name}_{dataset_name}_{snp}.vcf"
    vcf_path = os.path.join(vcf_directory, vcf_file)

    if not os.path.exists(vcf_path):
        print(f"Error: VCF file not found: {vcf_path}")
        return fail(f"VCF file not found: {vcf_path}")
        return None # ts 260607

    vcf_parts = find_target_vcf_parts(vcf_path, snp)

    if vcf_parts is None:
        return mark_snp_daf_zero(
            f"{target_snp} not found in VCF: {vcf_path}"
        )

    try:
        ancestral, derived, ref, alt, aa = get_orientation_from_vcf_parts(
            vcf_parts,
            defined_derived=defined_derived,
            defined_ancestral=defined_ancestral,
        )
        dbg(
            f"Orientation from VCF: ancestral={ancestral}, derived={derived}, "
            f"REF={ref}, ALT={alt}, AA={aa}"
        )
        dbg(f"VCF row preview: {' '.join(vcf_parts[:12])}")

    except ValueError as e:
        print(f"Error determining allele orientation for rs{snp}: {e}")
        # return None ts 260607
        return fail(f"Error determining allele orientation for {target_snp}: {e}")

    vcf_daf = calculate_daf(
        vcfs_directory,
        dataset_name,
        group,
        snp,
        gene_name,
        defined_derived=defined_derived,
        defined_ancestral=defined_ancestral,
    )

    if vcf_daf is None:
        return fail(
            f"calculate_daf() returned None for {dataset_name} {group} {target_snp}; "
            f"vcf_path={vcf_path}; ancestral={ancestral}; derived={derived}; "
            f"REF={ref}; ALT={alt}; AA={aa}"
        )
    
    try:
        vcf_daf_float = float(vcf_daf)
    except (TypeError, ValueError):
        return fail(
            f"calculate_daf() returned non-numeric DAF for "
            f"{dataset_name} {group} {target_snp}: {vcf_daf}"
        )

    if vcf_daf_float == 0.0:
        return mark_snp_daf_zero(
            f"VCF DAF is 0; vcf_path={vcf_path}"
        )

    group_haps_path = os.path.join(
        working_directory,
        f"{dataset_name}_chr{chr}_{group}.haps"
    )

    clues2_haps_path = os.path.join(
        working_directory,
        f"{dataset_name}_chr{chr}_{group}_{snp}.haps"
    )

    haps_daf = None
    haps_path = None

    if last_folder == group:
        haps_path = group_haps_path

        """if not os.path.isfile(haps_path):
            print(f"Missing group haps file: {haps_path}")
            return None"""
        
        dbg(f"Using group haps path: {haps_path}")
        dbg(f"group_haps_exists={os.path.isfile(haps_path)}")

        if not os.path.isfile(haps_path):
            return fail(f"Missing group haps file: {haps_path}")

        rows_seen = 0
        malformed_rows = 0
        candidate_rows = []

        with open(haps_path, "r") as haps_file:
            for line in haps_file:
                rows_seen += 1
                parts = line.strip().split()

                if len(parts) < 6:
                    malformed_rows += 1
                    continue

                if rows_seen <= 5:
                    candidate_rows.append(" ".join(parts[:5]))

                if target_snp in parts[:5] or str(snp) in parts[:5]:
                    dbg(f"Found target SNP in haps at row {rows_seen}")
                    dbg(f"haps target row first 15 fields: {' '.join(parts[:15])}")
                    dbg(f"haps allele columns: allele0={parts[3]}, allele1={parts[4]}")
                    dbg(f"haps token count after allele columns: {len(parts[5:])}")

                    try:
                        haps_daf = count_haps_derived_from_full_row(
                            parts,
                            ancestral=ancestral,
                            derived=derived,
                            debug=debug,
                            context=f"{dataset_name} {group} {target_snp} haps_path={haps_path}"
                        )
                    except ValueError as e:
                        return fail(f"Error calculating haps DAF for {target_snp}: {e}")
                    break

        dbg(f"Finished scanning haps file: rows_seen={rows_seen}, malformed_rows={malformed_rows}")
        dbg(f"First few haps row headers: {candidate_rows}")

        if haps_daf is None:
            preview = []

            with open(haps_path, "r") as haps_file:
                for i, line in enumerate(haps_file):
                    if i >= 10:
                        break

                    p = line.strip().split()

                    if len(p) >= 5:
                        preview.append(" ".join(p[:5]))

            if vcf_daf_float == 0.0:
                return mark_snp_daf_zero(
                    f"{target_snp} missing from haps file and VCF DAF is 0; "
                    f"haps_path={haps_path}; first_10_haps_row_headers={preview}"
                )

            return fail(
                f"{target_snp} missing from haps file, but VCF DAF is not 0. "
                f"This may indicate a real haps/VCF mismatch. "
                f"VCF_DAF={vcf_daf}; haps_path={haps_path}; "
                f"first_10_haps_row_headers={preview}"
            )

    elif last_folder.startswith("clues2_"):
        haps_path = clues2_haps_path

        if not os.path.isfile(haps_path):
            return fail(f"Missing CLUES2 one-SNP haps file: {haps_path}")
            #return None

        with open(haps_path, "r") as haps_file:
            lines = [line.strip().split() for line in haps_file if line.strip()]

        if not lines:
            return fail(f"Empty CLUES2 haps file: {haps_path}")
            #return None

        # Case 1: CLUES2 haps file still has full .haps-style row.
        full_row = None
        for parts in lines:
            if len(parts) >= 6 and (target_snp in parts[:5] or str(snp) in parts[:5]):
                full_row = parts
                break

        if full_row is not None:
            try:
                haps_daf = count_haps_derived_from_full_row(
                    full_row,
                    ancestral=ancestral,
                    derived=derived,
                    debug=True,
                    context=f"{dataset_name} {group} rs{snp} CLUES2 haps_path={haps_path}"
                )
            except ValueError as e:
                return fail(f"Error calculating CLUES2 haps DAF for rs{snp}: {e}")
                return None

        # Case 2: CLUES2 haps file is just 0/1 allele states.
        else:
            allele_tokens = []
            for parts in lines:
                allele_tokens.extend(parts)

            valid_tokens = [x for x in allele_tokens if x in {"0", "1"}]
            total = len(valid_tokens)

            if total == 0:
                return fail(f"No 0/1 alleles found in CLUES2 haps file: {haps_path}")
                return None

            # This assumes CLUES2 one-SNP haps was created from correctly oriented haps,
            # where 1 = derived.
            haps_daf = valid_tokens.count("1") / total

    else:
        print("Take a look at the working dir/.haps file structure.")
        return dbg(
            f"Got working_directory={working_directory}. "
            f"Expected either group folder ending in {group}, or clues2_* folder."
        )
        return None

    if haps_daf is None:
        return fail(f"Could not calculate haps DAF from: {haps_path}")
        return None

    if abs(float(vcf_daf) - float(haps_daf)) <= tolerance:
        return haps_daf

    
    diff = abs(float(vcf_daf) - float(haps_daf))
    dbg(f"DAF comparison: vcf_daf={vcf_daf}, haps_daf={haps_daf}, diff={diff}, tolerance={tolerance}")

    if diff <= tolerance:
        dbg(f"PASS: haps DAF ({haps_daf}) == VCF ({vcf_daf}) DAF for {dataset_name} {group} {target_snp}")
        return haps_daf

    return fail(
        f"VCF DAF and haps DAF differ beyond tolerance for {dataset_name} {group} {target_snp}. "
        f"VCF_DAF={vcf_daf}, HAPS_DAF={haps_daf}, diff={diff}, tolerance={tolerance}; "
        f"ancestral={ancestral}, derived={derived}, REF={ref}, ALT={alt}, AA={aa}; "
        f"haps_path={haps_path}; vcf_path={vcf_path}. "
        "Not auto-flipping based on AA==ALT."
    )

    return None
    
def count_haps_derived_from_full_row(parts, ancestral, derived, debug=False, context=""):
    """
    Count derived allele frequency from a standard Relate .haps row.

    Expected .haps columns:
      chrom rsid position allele0 allele1 hap0 hap1 ...

    Correct orientation:
      allele0 = ancestral
      allele1 = derived
      derived count = count("1")

    Reversed orientation:
      allele0 = derived
      allele1 = ancestral
      derived count = count("0")
    """

    def dbg(msg):
        if debug:
            prefix = f"[count_haps_derived_from_full_row DEBUG]"
            if context:
                prefix += f" [{context}]"
            print(f"{prefix} {msg}", flush=True)

    if len(parts) < 6:
        raise ValueError(
            f"Malformed haps row: expected at least 6 columns, got {len(parts)}. "
            f"context={context}; row_preview={' '.join(parts[:10])}"
        )

    raw_allele0 = parts[3]
    raw_allele1 = parts[4]

    allele0 = normalize_allele(raw_allele0)
    allele1 = normalize_allele(raw_allele1)
    haps = parts[5:]

    count_0 = haps.count("0")
    count_1 = haps.count("1")
    total = count_0 + count_1

    invalid_tokens = sorted(set(x for x in haps if x not in {"0", "1"}))

    dbg(f"row first 10 fields: {' '.join(parts[:10])}")
    dbg(f"raw haps alleles: allele0={raw_allele0}, allele1={raw_allele1}")
    dbg(f"normalized haps alleles: allele0={allele0}, allele1={allele1}")
    dbg(f"hap token counts: count_0={count_0}, count_1={count_1}, total_valid={total}, total_tokens={len(haps)}")
    dbg(f"invalid hap tokens: {invalid_tokens if invalid_tokens else 'None'}")

    if total == 0:
        raise ValueError(
            f"No valid 0/1 hap tokens found in haps row. "
            f"context={context}; "
            f"allele0={allele0}, allele1={allele1}; "
            f"total_tokens={len(haps)}; "
            f"invalid_tokens={invalid_tokens}; "
            f"row_preview={' '.join(parts[:15])}"
        )

    raw_ancestral = ancestral
    raw_derived = derived

    ancestral = normalize_allele(ancestral)
    derived = normalize_allele(derived)

    dbg(f"raw expected alleles: ancestral={raw_ancestral}, derived={raw_derived}")
    dbg(f"normalized expected alleles: ancestral={ancestral}, derived={derived}")

    if allele0 == ancestral and allele1 == derived:
        daf = count_1 / total
        dbg(f"orientation=normal: allele0=ancestral, allele1=derived; DAF=count_1/total={daf}")
        return daf

    if allele0 == derived and allele1 == ancestral:
        daf = count_0 / total
        dbg(f"orientation=reversed: allele0=derived, allele1=ancestral; DAF=count_0/total={daf}")
        return daf

    raise ValueError(
        f"HAPS alleles do not match expected ancestral/derived alleles. "
        f"context={context}; "
        f"haps_alleles={allele0}/{allele1}; "
        f"expected_ancestral={ancestral}; "
        f"expected_derived={derived}; "
        f"raw_haps_alleles={raw_allele0}/{raw_allele1}; "
        f"raw_expected_ancestral={raw_ancestral}; "
        f"raw_expected_derived={raw_derived}; "
        f"count_0={count_0}; count_1={count_1}; total={total}; "
        f"invalid_tokens={invalid_tokens if invalid_tokens else 'None'}; "
        f"row_preview={' '.join(parts[:15])}"
    )

def calculate_haps_daf_from_row(parts, ancestral_allele=None, derived_allele=None):
    #FIX: consolidate between calculate_haps_daf_from_row
     
    allele0 = parts[3].upper()
    allele1 = parts[4].upper()
    haps = parts[5:]

    count_0 = haps.count("0")
    count_1 = haps.count("1")
    total = count_0 + count_1

    if total == 0:
        print(f"No 0/1 alleles found")
        return None

    if ancestral_allele:
        ancestral_allele = ancestral_allele.upper()
    if derived_allele:
        derived_allele = derived_allele.upper()

    if ancestral_allele and derived_allele:
        if allele0 == ancestral_allele and allele1 == derived_allele:
            return count_1 / total
        elif allele0 == derived_allele and allele1 == ancestral_allele:
            return count_0 / total
        else:
            raise ValueError(
                f"HAPS alleles {allele0}/{allele1} do not match "
                f"ancestral={ancestral_allele}, derived={derived_allele}"
            )

    # Fallback only if you trust haps is already ancestral-oriented.
    return count_1 / total





def generate_group_dict(dataset_name, input_megafile):
    dataset_group_mapping = {dataset_name: []}

    with open(input_megafile) as f:
        for line in f:
            lineparts = line.strip().split("\t")
            if len(lineparts) < 2:
                continue  # skip malformed lines
            dataset = lineparts[0]
            grouping_name = lineparts[1]
            if dataset == dataset_name:
                if grouping_name not in dataset_group_mapping[dataset_name]:
                    dataset_group_mapping[dataset_name].append(grouping_name)

    return dataset_group_mapping

# from s_avg_bins:

def format_timepoint(x):
    x = float(x)
    if x.is_integer():
        return str(int(x))
    return str(x).replace(".", "p")

def determine_timebins(min_time, max_time):
    timebin_dict = timebins()
    bins_set = {float(min_time), float(max_time)}
    for title in timebin_dict:
        for timepoint in timebin_dict[title]:
            if str(timepoint).upper() == "XXX": continue
            bins_set.add(float(timepoint))
    return sorted(bins_set)

def make_s_columns(min_time,max_time):
    bins_list = determine_timebins(min_time,max_time)
    s_columns_list = []
    for left, right in zip(bins_list[:-1], bins_list[1:]):
        left_str = format_timepoint(left)
        right_str = format_timepoint(right)
        s_columns_list.append(f"s{left_str}_{right_str}")
    return s_columns_list

def find_timebins_midpoint(min_time,max_time):
    bins_list = determine_timebins(min_time,max_time)
    list_of_midpoints = []
    for left, right in zip(bins_list[:-1], bins_list[1:]):
        midpoint = (left + right) / 2
        list_of_midpoints.append(midpoint)
    return list_of_midpoints

def parse_args():
    ap = argparse.ArgumentParser(description="Average CLUES2 s across fixed time bins with model weighting.")
    ap.add_argument("--aicfile", required=True, help="Path to AIChighlighted_table.tsv")
    ap.add_argument("--sep", default="auto", choices=["auto", "csv", "tsv"], help="File separator if needed")
    ap.add_argument("--model_criteria", default="TopAIC", choices=["TopAIC", "LowestParameterSpace"],
                    help="Which models to include per group")

    ap.add_argument("--out", help="Output CSV path: averaged_s_by_group.csv")
    ap.add_argument("--min_time", type=float, default=0)
    ap.add_argument("--max_time", type=float, default=600)
    return ap.parse_args()

def read_table(path: str, sep_mode: str) -> pd.DataFrame:
    if sep_mode == "csv":
        return pd.read_csv(path)
    if sep_mode == "tsv":
        return pd.read_csv(path, sep="\t")
    if path.lower().endswith(".tsv"):
        return pd.read_csv(path, sep="\t")
    return pd.read_csv(path)

def parse_timebins(tb: str, min_time, max_time) -> List[float]:
    min_time = float(min_time)
    max_time = float(max_time)
    if pd.isna(tb) or not isinstance(tb, str):
        return []
    tb = tb.strip()
    if "=" not in tb:
        return []
    _, right = tb.split("=", 1)
    right = right.strip()
    if not right:
        return []
    cuts = [int(x) for x in right.split("+") if x.strip()]
    cuts = sorted([c for c in cuts if 0 < c < 600])
    return cuts

def epoch_edges_from_cuts(cuts: List[float], min_time, max_time) -> List[float]:
    return [float(min_time)] + cuts + [float(max_time)]

def get_epoch_count(tb: str) -> int:
    """
    '1' -> 1, '2=150' -> 2, '3=075+150' -> 3
    """
    if pd.isna(tb):
        return 0
    tb = str(tb).strip()
    if "=" in tb:
        left = tb.split("=", 1)[0].strip()
        return int(left) if left.isdigit() else 0
    return int(tb) if tb.isdigit() else 0

def overlap(a0, a1, b0, b1):
    return max(0, min(a1, b1) - max(a0, b0))

def model_epoch_s_values(row: pd.Series, epochs_n: int) -> List[float]:
    """
    Use s1..s{epochs_n}. Return [] if any required s_k is missing or '*'.
    """
    out = []
    for k in range(1, epochs_n + 1):
        col = f"s{k}"
        if col not in row or pd.isna(row[col]):
            return []
        v = row[col]
        if isinstance(v, str) and v.strip() == "*":
            return []
        try:
            out.append(float(v))
        except Exception:
            return []
    return out

def map_model_to_standard_bins(edges: List[float], s_vals: List[float], timebin_options: List[float]) -> List[float]:
    assert len(edges) >= 2 and len(s_vals) == len(edges) - 1, "edges/s mismatch"
    out = []
    model_epochs: List[Tuple[float, float, float]] = [
        (edges[i], edges[i + 1], s_vals[i])
        for i in range(len(s_vals))
    ]

    for b0, b1 in zip(timebin_options[:-1], timebin_options[1:]):
        num, den = 0.0, 0.0
        for e0, e1, s in model_epochs:
            ol = overlap(e0, e1, b0, b1)
            if ol > 0:
                num += s * ol
                den += ol
        out.append(num / den if den > 0 else float("nan"))

    return out

def akaike_weights(df: pd.DataFrame) -> pd.Series:
    if "AIC_difference" in df.columns:
        d = pd.to_numeric(df["AIC_difference"], errors="coerce")
        if d.notna().any():
            w = (-(0.5) * d).apply(math.exp)
            s = w.sum()
            return w / s if s > 0 else pd.Series([1.0/len(df)]*len(df), index=df.index)
    return pd.Series([1.0/len(df)]*len(df), index=df.index)

def select_models(group_df: pd.DataFrame, model_criteria: str) -> pd.DataFrame:
    """
    automatically filters out any models that aren't statistically significant
    """

    df = group_df.copy()
    if "AIC_difference" in df.columns:
        df["AIC_difference"] = pd.to_numeric(df["AIC_difference"], errors="coerce")

    if model_criteria  in {"TopAIC"}:
        if "Best_Model" in df.columns:
            keep = df[
                (df["Best_Model"].astype(str) != "NotStatSig") &
                (df["AIC_difference"] <= 2)
            ].copy()
            if len(keep) > 0:
                return keep
        return df
    
    elif model_criteria == "LowestParameterSpace":
        return df[df["Best_Model"].astype(str).str.contains("LowestParameterSpace", case=False)]

    # trying to not use this one anymore...
    elif model_criteria in {"best3", "best5"}:
        n = 3 if model_criteria == "best3" else 5
        if "AIC" in df.columns and df["AIC"].notna().any():
            return df.sort_values("AIC", ascending=True).head(n)
        if "logLR" in df.columns and df["logLR"].notna().any():
            return df.sort_values("logLR", ascending=False).head(n)
        return df.head(n)

    elif model_criteria in {"bestX", "TopAIC"}:
        if "Best_Model" in df.columns:
            sig = df[df["Best_Model"].astype(str) != "NotStatSig"].copy()
            if not sig.empty:
                df = sig
        if "AIC_difference" in df.columns and df["AIC_difference"].notna().any():
            return df.sort_values("AIC_difference", ascending=True)
        if "AIC" in df.columns and df["AIC"].notna().any():
            return df.sort_values("AIC", ascending=True)
        if "logLR" in df.columns and df["logLR"].notna().any():
            return df.sort_values("logLR", ascending=False)
        return df

    return df

def process(aic_df: pd.DataFrame, model_criteria: str, min_time=0, max_time=600) -> pd.DataFrame:
    timebin_options = determine_timebins(min_time, max_time)
    ultimate_timebins = make_s_columns(min_time, max_time)

    if "group" not in aic_df.columns:
        raise ValueError("Input needs a 'group' column.")
    if "timebins" not in aic_df.columns:
        raise ValueError("Input needs a 'timebins' column with patterns like '3=150+450'.")
    out_rows = []
    for group, gdf in aic_df.groupby("group"):
        gsel = select_models(gdf, model_criteria)
        if gsel.empty:
            continue

        # compute weights (your akaike_weights; if you changed it to dAIC-only, that applies here)
        w = akaike_weights(gsel)
        gsel = gsel.assign(_w=w)

        mapped = []
        models_included_ct = 0

        # ----- Portet (2020) rule: if any model has weight > 0.9, use ONLY that model -----
        if w.max() > 0.9:
            idx = w.idxmax()
            row = gsel.loc[idx]
            
            epochs_n = get_epoch_count(row["timebins"])
            cuts = parse_timebins(str(row["timebins"]), min_time, max_time)
            edges = epoch_edges_from_cuts(cuts, min_time, max_time)
            s_vals = model_epoch_s_values(row, epochs_n)
            if len(s_vals) != len(edges) - 1:
                continue
            s_std = map_model_to_standard_bins(edges, s_vals, timebin_options)
            mapped = [(1.0, s_std)]
            models_included_ct = 1
        else:
            # normal model-averaging across all selected models
            for _, row in gsel.iterrows():
                epochs_n = get_epoch_count(row["timebins"])
                cuts = parse_timebins(str(row["timebins"]), min_time, max_time)
                edges = epoch_edges_from_cuts(cuts, min_time, max_time)
                s_vals = model_epoch_s_values(row, epochs_n)
                if len(s_vals) != len(edges) - 1:
                    continue
                s_std = map_model_to_standard_bins(edges, s_vals, timebin_options)
                mapped.append((row["_w"], s_std))
            models_included_ct = len(mapped)

        if not mapped:
            continue

        # aggregate (single-model or weighted multi-model)
        num = [0.0] * len(ultimate_timebins)
        den = 0.0
        for w_i, s_std in mapped:
            for j, v in enumerate(s_std):
                if not math.isnan(v):
                    num[j] += w_i * v
            den += w_i
        s_avg = [v / den if den > 0 else float("nan") for v in num]

        row_out = {"groupname": group, "models_included_ct": models_included_ct}
        row_out.update({label: s_avg[i] for i, label in enumerate(ultimate_timebins)})
        out_rows.append(row_out)

    return pd.DataFrame(out_rows)

def standard_error(aic_df: pd.DataFrame, model_criteria: str, min_time=0, max_time=600) -> pd.DataFrame:
    """
    Compute weighted standard error of selection coefficients across models per group.
    Similar to model averaging, but stores standard errors (SE) rather than averages.

    Output: one row per group, columns are standard error for each standard timebin.
    """

    timebin_options = determine_timebins(min_time, max_time)
    ultimate_timebins = make_s_columns(min_time, max_time)

    if "group" not in aic_df.columns:
        raise ValueError("Input needs a 'group' column.")
    if "timebins" not in aic_df.columns:
        raise ValueError("Input needs a 'timebins' column with patterns like '3=150+450'.")

    out_rows = []

    for group, gdf in aic_df.groupby("group"):
        gsel = select_models(gdf, model_criteria)
        if gsel.empty:
            continue

        # Compute Akaike weights (same as before)
        w = akaike_weights(gsel)
        gsel = gsel.assign(_w=w)

        mapped = []

        # ---- Case 1: if one model dominates (>0.9 weight) ----
        if w.max() > 0.9:
            idx = w.idxmax()
            row = gsel.loc[idx]
            epochs_n = get_epoch_count(row["timebins"])
            cuts = parse_timebins(str(row["timebins"]), min_time, max_time)
            edges = epoch_edges_from_cuts(cuts, min_time, max_time)
            s_vals = model_epoch_s_values(row, epochs_n)
            if len(s_vals) != len(edges) - 1:
                continue
            s_std = map_model_to_standard_bins(edges, s_vals, timebin_options)
            # if only one model, SE = 0
            s_se = [0.0 for _ in s_std]
            models_included_ct = 1

        # ---- Case 2: multiple models → weighted SE ----
        else:
            model_matrix = []
            weights = []

            for _, row in gsel.iterrows():
                epochs_n = get_epoch_count(row["timebins"])
                cuts = parse_timebins(str(row["timebins"]), min_time, max_time)
                edges = epoch_edges_from_cuts(cuts, min_time, max_time)
                s_vals = model_epoch_s_values(row, epochs_n)
                if len(s_vals) != len(edges) - 1:
                    continue
                s_std = map_model_to_standard_bins(edges, s_vals, timebin_options)
                model_matrix.append(s_std)
                weights.append(row["_w"])

            if not model_matrix:
                continue

            models_included_ct = len(model_matrix)
            weights = np.array(weights)
            weights /= weights.sum()

            model_matrix = np.array(model_matrix)  # shape: (n_models, n_bins)
            mean_per_bin = np.average(model_matrix, axis=0, weights=weights)

            # weighted variance formula
            var_per_bin = np.average((model_matrix - mean_per_bin) ** 2, axis=0, weights=weights)

            # standard error = sqrt(variance / effective sample size)
            # effective n approximated as number of models
            s_se = np.sqrt(var_per_bin / models_included_ct)

        # --- Prepare output row ---
        row_out = {"groupname": group, "models_included_ct": models_included_ct}
        row_out.update({label: s_se[i] for i, label in enumerate(ultimate_timebins)})
        out_rows.append(row_out)

    return pd.DataFrame(out_rows)


import os
import gzip


def open_maybe_gzip(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")

def normalize_allele(allele):
    if allele is None:
        return None
    allele = str(allele).strip().upper()
    return allele if allele else None

def get_aa_from_info(info):
    for field in info.split(";"):
        if field.startswith("AA="):
            aa = field.split("=", 1)[1].strip().upper()
            return aa[0] if aa else None
    return None

def get_orientation_from_vcf_parts(parts, defined_derived=None, defined_ancestral=None):
    """
    Determine ancestral and derived alleles for a VCF row.

    User-defined alleles override REF/ALT/AA interpretation.
    Otherwise:
      - AA is ancestral
      - derived is the other allele among REF/ALT

    Returns:
      ancestral, derived, ref, alt, aa
    """
    ref = normalize_allele(parts[3])
    alt = normalize_allele(parts[4].split(",")[0])
    info = parts[7]
    aa = get_aa_from_info(info)

    defined_derived = normalize_allele(defined_derived)
    defined_ancestral = normalize_allele(defined_ancestral)

    if defined_derived or defined_ancestral:
        if not defined_derived or not defined_ancestral:
            raise ValueError(
                "If using user-defined alleles, provide BOTH defined_derived and defined_ancestral."
            )

        if defined_derived == defined_ancestral:
            raise ValueError(
                f"defined_derived and defined_ancestral cannot be the same: {defined_derived}"
            )

        if defined_derived not in {ref, alt}:
            raise ValueError(
                f"User-defined derived allele {defined_derived} is not REF/ALT ({ref}/{alt})"
            )

        if defined_ancestral not in {ref, alt}:
            raise ValueError(
                f"User-defined ancestral allele {defined_ancestral} is not REF/ALT ({ref}/{alt})"
            )

        if aa and aa != defined_ancestral:
            print(
                f"WARNING: VCF AA={aa} does not match user-defined ancestral={defined_ancestral}. "
                "Using user-defined orientation."
            )

        return defined_ancestral, defined_derived, ref, alt, aa

    if not aa:
        raise ValueError("No INFO/AA field found and no user-defined alleles were provided.")

    if aa == ref:
        ancestral = ref
        derived = alt
    elif aa == alt:
        ancestral = alt
        derived = ref
    else:
        raise ValueError(
            f"AA={aa} is neither REF={ref} nor ALT={alt}. "
            "Provide defined_derived and defined_ancestral."
        )

    return ancestral, derived, ref, alt, aa

def count_vcf_derived_alleles(sample_fields, ref, alt, derived):
    """
    0 = REF
    1 = ALT

    If derived == REF, genotype code 0 is derived.
    If derived == ALT, genotype code 1 is derived.
    """
    D = 0
    T = 0

    code_to_allele = {
        "0": ref,
        "1": alt,
    }

    for sample_field in sample_fields:
        genotype = sample_field.split(":")[0]

        for code in genotype.replace("|", "/").split("/"):
            if code not in code_to_allele:
                continue

            allele = code_to_allele[code]
            T += 1

            if allele == derived:
                D += 1

    return D, T

def find_target_vcf_parts(vcf_path, snp):
    target = f"rs{str(snp).removeprefix('rs')}"

    with open_maybe_gzip(vcf_path) as vcf:
        for line in vcf:
            if line.startswith("#"):
                continue

            parts = line.strip().split()
            if len(parts) < 10:
                continue

            if parts[2] == target:
                return parts

    return None


# OLD ONES
def calculate_vcf_stats_old(working_directory, dataset_name, group, snp, gene_name, vcf_path):
    """
    Run as: python /scratch/myang_shared/lab/Aine/alcohol/clues2/pyfiles/DAF_calc.py

    Calculate Derived Allele Frequency (DAF) for a given population in a dataset.

    Parameters:
    - vcf_directory (str): Path to the directory containing VCF files
    - dataset_name (str): Name of the dataset (e.g., '1KG')
    - population_name (str): Name of the population (e.g., 'Han')
    - snp (str): SNP ID without 'rs' prefix (e.g., '1229984')

    Returns:
    - list of D, A, T, DAF, and num_individuals
    """
    if not os.path.exists(vcf_path):
        print(f"Error: VCF file not found: {vcf_path}")
        return None

    D = 0  # Derived allele count
    A = 0 # Alt allele
    T = 0  # Total allele count
    num_individuals = None

    with open(vcf_path, 'r') as vcf:
        for line in vcf:
            if line.startswith("#"):
                continue

            parts = line.strip().split()
            if len(parts) < 10:
                continue

            if parts[2] != f"rs{snp}":
                continue

            reference_allele_id = parts[3]
            alternate_allele_id = parts[4]
            info = parts[7]

            ancestral_allele = None
            for field in info.split(";"):
                if field.startswith("AA="):
                    ancestral_allele = field.split("=")[1]
                    break

            if not ancestral_allele:
                print(f"Warning: No ancestral allele found in INFO for rs{snp}")
                return None

            alleles = parts[9:]
            num_individuals = len(alleles)

            for sample_field in alleles:
                genotype = sample_field.split(":")[0]  
                for a in genotype.replace("|", "/").split("/"):
                    if reference_allele_id == ancestral_allele:
                        if a == "1":
                            D += 1
                        if a == "0":
                            A += 1
                        if a in ["0", "1"]:
                            T += 1
                    elif alternate_allele_id == ancestral_allele:
                        if a == "0":
                            D += 1
                        if a == "1":
                            A += 1
                        if a in ["0", "1"]:
                            T += 1

            break  # Stop after finding the SNP

    if T == 0:
        print(f"Warning: No allele counts found for rs{snp} in {vcf_path}")
        DAF = None
    else:
        DAF = D / T

    return ([D, A, T, DAF, num_individuals])
        
def calculate_daf_old(working_directory, dataset_name, group, snp, gene_name):
    """
    Run as: python /scratch/myang_shared/lab/Aine/alcohol/clues2/pyfiles/DAF_calc.py

    Calculate Derived Allele Frequency (DAF) for a given population in a dataset.

    Parameters:
    - vcf_directory (str): Path to the directory containing VCF files
    - dataset_name (str): Name of the dataset (e.g., '1KG')
    - population_name (str): Name of the population (e.g., 'Han')
    - snp (str): SNP ID without 'rs' prefix (e.g., '1229984')

    Returns DAF only
    """
    vcf_directory = os.path.join(working_directory, f"Relate_{dataset_name}", group)

    vcf_file = f"{group}_{gene_name}_{dataset_name}_{snp}.vcf"

    vcf_path = os.path.join(vcf_directory, vcf_file)
    if not os.path.exists(vcf_path):
        print(f"Error: VCF file not found: {vcf_path}")
        return None

    D = 0  # Derived allele count
    A = 0  # Alt allele ct
    T = 0  # Total allele count
    num_individuals = None

    with open(vcf_path, 'r') as vcf:
        for line in vcf:
            if line.startswith("#"):
                continue

            parts = line.strip().split()
            if len(parts) < 10:
                continue

            if parts[2] != f"rs{snp}":
                continue

            reference_allele_id = parts[3]
            alternate_allele_id = parts[4]
            info = parts[7]

            ancestral_allele = None
            for field in info.split(";"):
                if field.startswith("AA="):
                    ancestral_allele = field.split("=")[1]
                    break

            if not ancestral_allele:
                print(f"Warning: No ancestral allele found in INFO for rs{snp}")
                return None

            alleles = parts[9:]
            num_individuals = len(alleles)

            for sample_field in alleles:
                genotype = sample_field.split(":")[0]  
                for a in genotype.replace("|", "/").split("/"):
                    if reference_allele_id == ancestral_allele:
                        if a == "1":
                            D += 1
                        if a in ["0", "1"]:
                            T += 1
                    elif alternate_allele_id == ancestral_allele:
                        if a == "0":
                            D += 1
                        if a in ["0", "1"]:
                            T += 1

            break  # Stop after finding the SNP

    if T == 0:
        print(f"Warning: No allele counts found for rs{snp} in {vcf_path}")
        DAF = None
    else:
        DAF = D / T

    return DAF

def calculate_haps_old(working_directory, vcfs_directory, dataset_name, chr, group, snp, gene_name):

    target_snp = f"rs{snp}"
    snp_found = False
    
    last_folder = os.path.basename(os.path.normpath(working_directory))
    
    count_0 = 0
    count_1 = 0

    group_haps_path = os.path.join(working_directory, f"{dataset_name}_chr{chr}_{group}.haps")
    clues2_haps_path = os.path.join(working_directory,f"{dataset_name}_chr{chr}_{group}_{snp}.haps")

    if last_folder == group:

        with open(group_haps_path, 'r') as haps_file:
            for line in haps_file:
                parts = line.strip().split()
                if len(parts) < 6: continue

                snp_id = parts[2]
                if target_snp in parts[:5]:
                    snp_found = True
                    alleles = parts[5:]
                    count_0 += alleles.count("0")
                    count_1 += alleles.count("1")

        if not snp_found:
            print(f"SNP {snp} missing from haps file: {group_haps_path}")
            return None


    elif last_folder.startswith("clues2_"):
        with open(clues2_haps_path, 'r') as haps_file:
            for allele in haps_file:
                count_0 += allele.count('0')
                count_1 += allele.count('1')

        
    elif not os.path.isfile(group_haps_path) and not os.path.isfile(clues2_haps_path):
        print("Missing haps file.")
        return None
    
    else:
        print(f"Take a look at the working dir/.haps file structure... and edit calculate_haps_proportions.py accordingly.")
        print (f"Expecting: working_dir of: {working_directory}, vcf_dir of {vcfs_directory}, and .haps file format of {dataset_name}_chr{chr}_{group}.haps (for group folder) or {dataset_name}_chr{chr}_{group}_{snp}.haps (for clues2 folder)")
        return None

    total = count_0 + count_1

    original_haps_freq = count_1 / total if total > 0 else 0.0
    daf = calculate_daf(vcfs_directory, dataset_name, group, snp, gene_name)

    # if haps file and vcf file have the same DAFs, just use that haps_freq + call it a day
    if abs(float(daf) - float(original_haps_freq)) <= 0.1:
        # VCF files have matching DAFs for {group}")
        return original_haps_freq

    else: # IF AA=alt allele, flipping 0's and 1's in .haps file to align with .vcf's DAF (hopefully...?)
        # Determine ancestral allele from corresponding VCF
        vcf_directory = os.path.join(vcfs_directory, f"Relate_{dataset_name}", group)
        vcf_file = f"{group}_{gene_name}_{dataset_name}_{snp}.vcf"
        vcf_path = os.path.join(vcf_directory, vcf_file)

        if not os.path.exists(vcf_path):
            print(f"Error: VCF file not found: {vcf_path}")
            return None

        ancestral_allele = None
        # in case u need it someday: ref_allele = None
        alt_allele = None

        with open(vcf_path, 'r') as vcf:
            for line in vcf:
                if line.startswith("#"):
                    continue
                parts = line.strip().split()

                if len(parts) < 8 or target_snp not in parts[:5]: continue

                # note: ref_allele = parts[3]
                alt_allele = parts[4]
                info = parts[7]

                for field in info.split(";"):
                    if field.startswith("AA="):
                        ancestral_allele = field.split("=")[1]
                        break
                break  # Stop after finding the relevant SNP

        if not ancestral_allele:
            print(f"Warning: No ancestral allele found in INFO for rs{snp}")
            return None

        # Determine whether to flip haplotype alleles
        flip_alleles = (ancestral_allele == alt_allele)

        # Process haps file
        updated_lines = []
        count_0 = 0
        count_1 = 0

        if last_folder == group:
            group_haps_path = os.path.join(working_directory, f"{dataset_name}_chr{chr}_{group}.haps")
            with open(group_haps_path, 'r') as haps_file:
                for line in haps_file:
                    parts = line.strip().split()
                    if len(parts) < 6: continue

                    if f"rs{snp}" not in parts[:5]:
                        updated_lines.append(line)
                        continue

                    alleles = parts[5:]
                    if flip_alleles:
                        alleles = [('1' if a == '0' else '0') if a in ('0', '1') else a for a in alleles]

                    count_0 += alleles.count('0')
                    count_1 += alleles.count('1')

        elif last_folder.startswith("clues2_"):
            clues2_haps_path = os.path.join(working_directory, f"{dataset_name}_chr{chr}_{group}_{snp}.haps")
            with open(clues2_haps_path, 'r') as haps_file:
                for line in haps_file:
                    alleles = line.strip().split()
                    if flip_alleles:
                        alleles = [('1' if a == '0' else '0') if a in ('0', '1') else a for a in alleles]

                    count_0 += alleles.count('0')
                    count_1 += alleles.count('1')

        total = count_0 + count_1

        if total > 0:
            proportion_1 = count_1 / total 
        else:
            proportion_1 = 0.0 

        return proportion_1
    

