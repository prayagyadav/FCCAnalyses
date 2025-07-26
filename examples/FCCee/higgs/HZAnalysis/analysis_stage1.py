processList = {
             ##'wzp6_ee_qqH_HZZ_llll_ecm240':{'fraction':1},
             ##'wzp6_ee_nunuH_HZZ_ecm240':{'fraction':1},

             ##'p8_ee_Zqq_ecm240':{'fraction':1},
             'p8_ee_ZZ_ecm240':{'fraction':0.01},
             ##'p8_ee_WW_ecm240':{'fraction':1},

             ##'wzp6_ee_tautauH_HWW_ecm240':{'fraction':1},
             ##'wzp6_ee_ccH_HWW_ecm240':{'fraction':1},
#             'wzp6_ee_eeH_HWW_ecm240':{'fraction':1},
#             'wzp6_ee_qqH_HWW_ecm240':{'fraction':1},
             ##'wzp6_ee_bbH_HWW_ecm240':{'fraction':1},
             ##'wzp6_ee_mumuH_HWW_ecm240':{'fraction':1},
#             'wzp6_ee_ssH_HWW_ecm240':{'fraction':1},
#              'wzp6_ee_nunuH_HWW_ecm240':{'fraction':1},

#**             'wzp6_ee_mumuH_Hss_ecm240':{'fraction':1},
             ##'wzp6_ee_mumuH_Hcc_ecm240':{'fraction':1},
             ##'wzp6_ee_mumuH_Hbb_ecm240':{'fraction':1},

#**             'wzp6_ee_mumuH_Htautau_ecm240':{'fraction':1},
             ##'wzp6_ee_mumuH_Hgg_ecm240':{'fraction':1},
#**             'wzp6_ee_mumuH_Hmumu_ecm240':{'fraction':1},
             ##'wzp6_ee_mumuH_HZa_ecm240':{'fraction':1},

#**             'wzp6_ee_ccH_Hmumu_ecm240':{'fraction':1},
#**             'wzp6_ee_ssH_Hmumu_ecm240':{'fraction':1},
#**             'wzp6_ee_bbH_Hmumu_ecm240':{'fraction':1},
#**             'wzp6_ee_qqH_Hmumu_ecm240':{'fraction':1},
#**             'wzp6_ee_tautauH_Hmumu_ecm240':{'fraction':1},
#                'wzp6_ee_nunuH_Hmumu_ecm240':{'fraction':1},

#                'wzp6_ee_nunuH_HZa_ecm240':{'fraction':1},
#             'wzp6_ee_ccH_HZa_ecm240':{'fraction':1},
#             'wzp6_ee_ssH_HZa_ecm240':{'fraction':1},
#**             'wzp6_ee_bbH_HZa_ecm240':{'fraction':1},
#             'wzp6_ee_qqH_HZa_ecm240':{'fraction':1},
#*             'wzp6_ee_tautauH_HZa_ecm240':{'fraction':1},
             }


processList_to_compute = processList


#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "/eos/user/p/pryadav/ZH_HZZ/4mu/outputs/stage1/test/sel_p_0/"
#includePaths = ["functions.h"]
includePaths = ["functions.h"]
#Optional
nCPUS       = 4
runBatch    = False
#runBatch    = True
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

            .Alias("Particle0", "Particle#0.index")
            .Alias("Particle1", "Particle#1.index")
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

          
            .Alias('Muon0', 'Muon#0.index')
            .Define('muons','ReconstructedParticle::get(Muon0, ReconstructedParticles)')
            .Define('muons_n','ReconstructedParticle::get_n(muons)')
            .Define('muons_p','ReconstructedParticle::get_p(muons)')
            .Define('muons_charge','ReconstructedParticle::get_charge(muons)')
          

            .Define('selected_muons','ReconstructedParticle::sel_p(2)(muons)')
            .Define('selected_muons_n','ReconstructedParticle::get_n(selected_muons)')
            .Define('selected_muons_p','ReconstructedParticle::get_p(selected_muons)')
            .Filter('selected_muons_n > 3')

            # Find muons pair with mass closest to 91.2 (On-shell Z)
            .Define("zbuilder_result", "FCCAnalyses::ZHfunctions::resonanceBuilder_mass(91.2,false)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
            .Define("zll", "Vec_rp{zbuilder_result[0]}") 
            .Define("zll_charge", 'ReconstructedParticle::get_charge(zll)') 
            .Define("zll_mass", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") 

            .Define("zll_muons", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons
            .Define('zll_muons_p','ReconstructedParticle::get_p(zll_muons)')
            .Define('zll_muons_n','ReconstructedParticle::get_n(zll_muons)')
            .Define('rest_of_muons',"ReconstructedParticle::remove(selected_muons,zll_muons)") #Remove the muon pair of the on-shell Z from the muon collection
           

            .Define("non_res_Z","FCCAnalyses::ZHfunctions::getTwoHighestPMuons(rest_of_muons)") # Find the highest p muon pair from the remaining muons (off-shell Z) 
            .Define('non_res_Z_p','ReconstructedParticle::get_p(non_res_Z)')
            .Define('non_res_Z_n','ReconstructedParticle::get_n(non_res_Z)')
            .Define('non_res_Z_px','ReconstructedParticle::get_px(non_res_Z)')
            .Define('non_res_Z_py','ReconstructedParticle::get_py(non_res_Z)')
            .Define('non_res_Z_pz','ReconstructedParticle::get_pz(non_res_Z)')
            .Define('non_res_Z_e','ReconstructedParticle::get_e(non_res_Z)')
            .Define('non_res_Z_tlv','FCCAnalyses::ZHfunctions::makeLorentzVectors(non_res_Z_px,non_res_Z_py,non_res_Z_pz,non_res_Z_e)')
            .Filter('non_res_Z_n > 0')
            .Define('non_res_Z_m','FCCAnalyses::ZHfunctions::InvariantMass(non_res_Z_tlv[0],non_res_Z_tlv[1])')      
            .Define('non_res_Z_angle','non_res_Z_tlv[0].Vect().Angle(non_res_Z_tlv[1].Vect())')
 
            .Define('fourMuons',"ReconstructedParticle::merge(zll_muons,non_res_Z)") #Merge the two muon pairs
            .Define('fourMuons_p',"ReconstructedParticle::get_p(fourMuons)") 
            .Define('fourMuons_pmin',"return *std::min_element(fourMuons_p.begin(), fourMuons_p.end());") 

            .Define('fourMuons_p4','ReconstructedParticle::get_P4vis(fourMuons)') # P4 of four muon pairs
            .Define('fourMuons_mass','fourMuons_p4.M()') # Mass of 4 muon pairs

            .Define("rest_of_particles","ReconstructedParticle::remove(ReconstructedParticles,fourMuons)")
            .Define("vis_p4_other_particles","ReconstructedParticle::get_P4vis(rest_of_particles)")
            .Define("vis_e_other_particles","vis_p4_other_particles.E()")

            .Define("Emiss","FCCAnalyses::ZHfunctions::missingEnergy(240,ReconstructedParticles)") 
            .Define("pmiss","Emiss[0].energy") 
            .Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(Emiss)")
            .Define("fourMuons_iso","FCCAnalyses::ZHfunctions::coneIsolation(0.0,0.523599)(fourMuons,rest_of_particles)")
            .Define('fourMuons_min_iso',"return *std::max_element(fourMuons_iso.begin(),fourMuons_iso.end());") 


)
        return df2

    def output():
        branchlist = [
                      "selected_muons_n",
                      "selected_muons_p",
                      "rest_of_muons",
                      "fourMuons_p",
                      "fourMuons_mass",
                      "zll_mass",
                      "non_res_Z",
                      "non_res_Z_tlv",
                      "non_res_Z_m",
                      "vis_e_other_particles",
                      "fourMuons_pmin",
                      "non_res_Z_angle",
                      "fourMuons_iso",
                      "fourMuons_min_iso",
                      "pmiss",
                      "cosTheta_miss",
                      ]
        return branchlist
