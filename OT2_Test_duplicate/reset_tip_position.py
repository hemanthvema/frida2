from Minerva_Lite import Configuration
if __name__ =='__main__':
    Configuration.load_configuration()
    ot2 = Configuration.OpentronsOT2["ot2"]
    ot2.reset_tipracks_and_tippositions()
    Configuration.save_configuration()