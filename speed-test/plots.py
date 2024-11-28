import ROOT

# global parameters
intLumi        = 1. # histograms already scaled
intLumiLabel   = "L = 7.2 ab^{-1}"
ana_tex        = 'e^{+}e^{-} #rightarrow Z(#mu^{+}#mu^{-})H(b#bar{b})'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = f"outputs/speed-test/histmaker/"
formats        = ['png','pdf']
outdir         = f"outputs/speed-test/plots/"
plotStatUnc    = True

colors = {}
colors['ZH'] = ROOT.kRed

procs = {}
procs['signal'] = {'ZH':['wzp6_ee_mumuH_Hbb_ecm240']}
procs['backgrounds'] = {}

legend = {}
legend['ZH'] = 'ZH'

hists = {}


hists["zmumu_recoil_m"] = {
    "output":   "zmumu_recoil_m",
    "logy":     False,
    "stack":    True,
    "rebin":    1,
    "xmin":     120,
    "xmax":     140,
    "ymin":     0,
    "ymax":     2000,
    "xtitle":   "Recoil (GeV)",
    "ytitle":   "Events",
}

hists["zmumu_p"] = {
    "output":   "zmumu_p",
    "logy":     False,
    "stack":    True,
    "rebin":    1,
    "xmin":     20,
    "xmax":     70,
    "ymin":     0,
    "ymax":     5000,
    "xtitle":   "p(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events",
}

hists["zmumu_m"] = {
    "output":   "zmumu_m",
    "logy":     False,
    "stack":    True,
    "rebin":    1,
    "xmin":     70,
    "xmax":     110,
    "ymin":     0,
    "ymax":     7000,
    "xtitle":   "m(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events",
}

