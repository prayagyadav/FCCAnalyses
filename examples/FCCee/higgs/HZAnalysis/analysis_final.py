
#python examples/FCCee/top/hadronic/finalSel.py
#Mandatory: List of processes

import copy

from analysis_stage1 import processList_to_compute
processList = copy.deepcopy(processList_to_compute)

###Input directory where the files produced at the pre-selection level are
inputDir   = "/eos/user/p/pryadav/ZH_HZZ/4mu/outputs/stage1/test/sel_p_0"
outputDir  = "/eos/user/p/pryadav/ZH_HZZ/4mu/outputs/final/test/sel_p_0"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"
###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = { "sel0":"fourMuons_mass < 10000000.0",
            "sel1": "fourMuons_pmin > 5",
            "sel2": "fourMuons_pmin > 5 && pmiss < 20",
            "sel3": "fourMuons_pmin > 5 && pmiss < 20 && vis_e_other_particles > 95",
            "sel4": "fourMuons_pmin > 5 && pmiss < 20 && vis_e_other_particles > 95 && non_res_Z_m < 65 && non_res_Z_m > 10",
            "sel5": "fourMuons_pmin > 5 && pmiss < 20 && vis_e_other_particles > 95 && non_res_Z_m < 65 && non_res_Z_m > 10 && fourMuons_mass < 130 && fourMuons_mass > 120",
            "sel6": "fourMuons_mass < 125.5 && fourMuons_mass > 124",
      
}

###Optinally Define new variables
#DefineList = {"selmuon_pT_0":"selected_muons_pt.at(0)"}


###Dictionary for the ouput variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "selectedmuons_p":{"name":"selected_muons_p","title":"mu_p [GeV]","bin":250,"xmin":0.0,"xmax":250.},

    "fourmuons_mass":{"name":"fourMuons_mass","title":"M_{4#mu} [GeV]","bin":50,"xmin":0.0,"xmax":250.},
    "fourmuons_pmin":{"name":"fourMuons_pmin","title":"P_{min} [GeV]","bin":20,"xmin":0.0,"xmax":100.},

    "Z_res_mass":{"name":"zll_mass","title":"On-shell M_{#mu#mu} [GeV]","bin":50,"xmin":0.0,"xmax":250.},
    "Z_non_res_mass":{"name":"non_res_Z_m","title":"Off-shell M_{#mu#mu} [GeV]","bin":50,"xmin":0.0,"xmax":250.},


    "vis_e_woMuons":{"name":"vis_e_other_particles","title":"Visible Energy excluding muons [GeV]","bin":50,"xmin":0.0,"xmax":250.},
    "iso_least_isolated_muon":{"name":"fourMuons_min_iso","title":"iso(least isolated muon)","bin":50,"xmin":0.0,"xmax":20.0},
    "missing_p":{"name":"pmiss","title":"missing p [GeV]","bin":50,"xmin":0.0,"xmax":250.},
    "cos_theta_miss":{"name":"cosTheta_miss","title":"Cos(Theta_miss)","bin":100,"xmin":0.0,"xmax":1.},

}
 
