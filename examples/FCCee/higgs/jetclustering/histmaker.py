
processList = {
    'wzp6_ee_mumuH_Hbb_ecm240': {'fraction': 0.1},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Optional: output directory, default is local running directory
outputDir   = f"outputs/FCCee/higgs/jetclustering/histmaker/"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 7200000.0 # 7.2 /ab


# define some binning for various histograms
bins_p_mu = (250, 0, 250)
bins_m_ll = (250, 0, 250)
bins_p_ll = (250, 0, 250)
bins_recoil = (200, 120, 140)
bins_pdgid = (51, -25.5, 25.5)
bins_dijet_m = (80, 70, 150)

import time
# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")



    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # select muons from Z decay and form Z/recoil mass
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(25)(muons_all)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Filter("muons_no >= 2")

    df = df.Define("zmumu", "ReconstructedParticle::resonanceBuilder(91)(muons)")
    df = df.Define("zmumu_m", "ReconstructedParticle::get_mass(zmumu)[0]")
    df = df.Define("zmumu_p", "ReconstructedParticle::get_p(zmumu)[0]")
    df = df.Define("zmumu_recoil", "ReconstructedParticle::recoilBuilder(240)(zmumu)")
    df = df.Define("zmumu_recoil_m", "ReconstructedParticle::get_mass(zmumu_recoil)[0]")

    # basic selection
    df = df.Filter("zmumu_m > 70 && zmumu_m < 100")
    df = df.Filter("zmumu_p > 20 && zmumu_p < 70")
    df = df.Filter("zmumu_recoil_m < 140 && zmumu_recoil_m > 120")


    # do jet clustering on all particles, except the muons
    df = df.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df = df.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons)")
    df = df.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons)")
    df = df.Define("RP_pz","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons)")
    df = df.Define("RP_e", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons)")
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")


    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets)") # 2-jet exclusive clustering

    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)") # one-to-one mapping to the input collection (rps_no_muons)
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_phi", "FCCAnalyses::JetClusteringUtils::get_phi(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    # convert jets to LorentzVectors
    df = df.Define("jets_tlv", "FCCAnalyses::makeLorentzVectors(jets_px, jets_py, jets_pz, jets_e)")
    df = df.Define("jets_truth", "FCCAnalyses::jetTruthFinder(jetconstituents, rps_no_muons, Particle, MCRecoAssociations1)") # returns best-matched PDG ID of the jets
    df = df.Define("dijet_higgs_m", "(jets_tlv[0]+jets_tlv[1]).M()")



    ############## Repeat


    # do jet clustering on all particles, except the muons
    df = df.Define("rps_no_muons_1", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df = df.Define("RP_px_1", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons_1)")
    df = df.Define("RP_py_1", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons_1)")
    df = df.Define("RP_pz_1","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons_1)")
    df = df.Define("RP_e_1", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons_1)")
    df = df.Define("pseudo_jets_1", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px_1, RP_py_1, RP_pz_1, RP_e_1)")


    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    df = df.Define("clustered_jets_1", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets_1)") # 2-jet exclusive clustering

    df = df.Define("jets_1", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets_1)")
    df = df.Define("jetconstituents_1", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets_1)") # one-to-one mapping to the input collection (rps_no_muons)
    df = df.Define("jets_e_1", "FCCAnalyses::JetClusteringUtils::get_e(jets_1)")
    df = df.Define("jets_px_1", "FCCAnalyses::JetClusteringUtils::get_px(jets_1)")
    df = df.Define("jets_py_1", "FCCAnalyses::JetClusteringUtils::get_py(jets_1)")
    df = df.Define("jets_pz_1", "FCCAnalyses::JetClusteringUtils::get_pz(jets_1)")
    df = df.Define("jets_phi_1", "FCCAnalyses::JetClusteringUtils::get_phi(jets_1)")
    df = df.Define("jets_m_1", "FCCAnalyses::JetClusteringUtils::get_m(jets_1)")

    # convert jets to LorentzVectors
    df = df.Define("jets_tlv_1", "FCCAnalyses::makeLorentzVectors(jets_px_1, jets_py_1, jets_pz_1, jets_e_1)")
    df = df.Define("jets_truth_1", "FCCAnalyses::jetTruthFinder(jetconstituents_1, rps_no_muons_1, Particle, MCRecoAssociations1)") # returns best-matched PDG ID of the jets
    df = df.Define("dijet_higgs_m_1", "(jets_tlv_1[0]+jets_tlv_1[1]).M()")

    #################



    ############## Repeat


    # do jet clustering on all particles, except the muons
    df = df.Define("rps_no_muons_2", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df = df.Define("RP_px_2", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons_2)")
    df = df.Define("RP_py_2", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons_2)")
    df = df.Define("RP_pz_2","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons_2)")
    df = df.Define("RP_e_2", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons_2)")
    df = df.Define("pseudo_jets_2", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px_2, RP_py_2, RP_pz_2, RP_e_2)")


    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    df = df.Define("clustered_jets_2", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets_2)") # 2-jet exclusive clustering

    df = df.Define("jets_2", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets_2)")
    df = df.Define("jetconstituents_2", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets_2)") # one-to-one mapping to the input collection (rps_no_muons)
    df = df.Define("jets_e_2", "FCCAnalyses::JetClusteringUtils::get_e(jets_2)")
    df = df.Define("jets_px_2", "FCCAnalyses::JetClusteringUtils::get_px(jets_2)")
    df = df.Define("jets_py_2", "FCCAnalyses::JetClusteringUtils::get_py(jets_2)")
    df = df.Define("jets_pz_2", "FCCAnalyses::JetClusteringUtils::get_pz(jets_2)")
    df = df.Define("jets_phi_2", "FCCAnalyses::JetClusteringUtils::get_phi(jets_2)")
    df = df.Define("jets_m_2", "FCCAnalyses::JetClusteringUtils::get_m(jets_2)")

    # convert jets to LorentzVectors
    df = df.Define("jets_tlv_2", "FCCAnalyses::makeLorentzVectors(jets_px_2, jets_py_2, jets_pz_2, jets_e_2)")
    df = df.Define("jets_truth_2", "FCCAnalyses::jetTruthFinder(jetconstituents_2, rps_no_muons_2, Particle, MCRecoAssociations1)") # returns best-matched PDG ID of the jets
    df = df.Define("dijet_higgs_m_2", "(jets_tlv_2[0]+jets_tlv_2[1]).M()")

    #################





    ############## Repeat


    # do jet clustering on all particles, except the muons
    df = df.Define("rps_no_muons_11", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df = df.Define("RP_px_11", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons_11)")
    df = df.Define("RP_py_11", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons_11)")
    df = df.Define("RP_pz_11","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons_11)")
    df = df.Define("RP_e_11", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons_11)")
    df = df.Define("pseudo_jets_11", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px_11, RP_py_11, RP_pz_11, RP_e_11)")


    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    df = df.Define("clustered_jets_11", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets_11)") # 2-jet exclusive clustering

    df = df.Define("jets_11", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets_11)")
    df = df.Define("jetconstituents_11", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets_11)") # one-to-one mapping to the input collection (rps_no_muons)
    df = df.Define("jets_e_11", "FCCAnalyses::JetClusteringUtils::get_e(jets_11)")
    df = df.Define("jets_px_11", "FCCAnalyses::JetClusteringUtils::get_px(jets_11)")
    df = df.Define("jets_py_11", "FCCAnalyses::JetClusteringUtils::get_py(jets_11)")
    df = df.Define("jets_pz_11", "FCCAnalyses::JetClusteringUtils::get_pz(jets_11)")
    df = df.Define("jets_phi_11", "FCCAnalyses::JetClusteringUtils::get_phi(jets_11)")
    df = df.Define("jets_m_11", "FCCAnalyses::JetClusteringUtils::get_m(jets_11)")

    # convert jets to LorentzVectors
    df = df.Define("jets_tlv_11", "FCCAnalyses::makeLorentzVectors(jets_px_11, jets_py_11, jets_pz_11, jets_e_11)")
    df = df.Define("jets_truth_11", "FCCAnalyses::jetTruthFinder(jetconstituents_11, rps_no_muons_11, Particle, MCRecoAssociations1)") # returns best-matched PDG ID of the jets
    df = df.Define("dijet_higgs_m_11", "(jets_tlv_11[0]+jets_tlv_11[1]).M()")

    #################



    ############## Repeat


    # do jet clustering on all particles, except the muons
    df = df.Define("rps_no_muons_22", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df = df.Define("RP_px_22", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons_22)")
    df = df.Define("RP_py_22", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons_22)")
    df = df.Define("RP_pz_22","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons_22)")
    df = df.Define("RP_e_22", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons_22)")
    df = df.Define("pseudo_jets_22", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px_22, RP_py_22, RP_pz_22, RP_e_22)")


    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    df = df.Define("clustered_jets_22", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets_22)") # 2-jet exclusive clustering

    df = df.Define("jets_22", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets_22)")
    df = df.Define("jetconstituents_22", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets_22)") # one-to-one mapping to the input collection (rps_no_muons)
    df = df.Define("jets_e_22", "FCCAnalyses::JetClusteringUtils::get_e(jets_22)")
    df = df.Define("jets_px_22", "FCCAnalyses::JetClusteringUtils::get_px(jets_22)")
    df = df.Define("jets_py_22", "FCCAnalyses::JetClusteringUtils::get_py(jets_22)")
    df = df.Define("jets_pz_22", "FCCAnalyses::JetClusteringUtils::get_pz(jets_22)")
    df = df.Define("jets_phi_22", "FCCAnalyses::JetClusteringUtils::get_phi(jets_22)")
    df = df.Define("jets_m_22", "FCCAnalyses::JetClusteringUtils::get_m(jets_22)")

    # convert jets to LorentzVectors
    df = df.Define("jets_tlv_22", "FCCAnalyses::makeLorentzVectors(jets_px_22, jets_py_22, jets_pz_22, jets_e_22)")
    df = df.Define("jets_truth_22", "FCCAnalyses::jetTruthFinder(jetconstituents_22, rps_no_muons_22, Particle, MCRecoAssociations1)") # returns best-matched PDG ID of the jets
    df = df.Define("dijet_higgs_m_22", "(jets_tlv_22[0]+jets_tlv_22[1]).M()")

    #################








    # define histograms
    results.append(df.Histo1D(("zmumu_m", "", *bins_m_ll), "zmumu_m"))
    results.append(df.Histo1D(("zmumu_p", "", *bins_p_ll), "zmumu_p"))
    results.append(df.Histo1D(("zmumu_recoil_m", "", *bins_recoil), "zmumu_recoil_m"))

    results.append(df.Histo1D(("jets_truth", "", *bins_pdgid), "jets_truth"))
    results.append(df.Histo1D(("dijet_higgs_m", "", *bins_dijet_m), "dijet_higgs_m"))

    results.append(df.Histo1D(("jets_truth_1", "", *bins_pdgid), "jets_truth_1"))
    results.append(df.Histo1D(("dijet_higgs_m_1", "", *bins_dijet_m), "dijet_higgs_m_1"))

    results.append(df.Histo1D(("jets_truth_2", "", *bins_pdgid), "jets_truth_2"))
    results.append(df.Histo1D(("dijet_higgs_m_2", "", *bins_dijet_m), "dijet_higgs_m_2"))

    results.append(df.Histo1D(("jets_truth_11", "", *bins_pdgid), "jets_truth_11"))
    results.append(df.Histo1D(("dijet_higgs_m_11", "", *bins_dijet_m), "dijet_higgs_m_11"))

    results.append(df.Histo1D(("jets_truth_22", "", *bins_pdgid), "jets_truth_22"))
    results.append(df.Histo1D(("dijet_higgs_m_22", "", *bins_dijet_m), "dijet_higgs_m_22"))

    return results, weightsum

    return results, weightsum

