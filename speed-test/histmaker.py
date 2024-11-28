
processList = {
        'wzp6_ee_mumuH_Hbb_ecm240': {'fraction': 1},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Optional: output directory, default is local running directory
outputDir   = f"outputs/speed-test/histmaker/"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 7200000.0 #in /pb which is 7.2 /ab

# define some binning for various histograms
bins_p_mu = (250, 0, 250)
bins_m_ll = (250, 0, 250)
bins_p_ll = (250, 0, 250)
bins_recoil = (200, 120, 140)

# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

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


    # define histograms
    results.append(df.Histo1D(("zmumu_m", "", *bins_m_ll), "zmumu_m"))
    results.append(df.Histo1D(("zmumu_p", "", *bins_p_ll), "zmumu_p"))
    results.append(df.Histo1D(("zmumu_recoil_m", "", *bins_recoil), "zmumu_recoil_m"))

    return results, weightsum

