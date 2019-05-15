from mtexplore import MtMain

# try this
def main():
    main_app = MtMain()
    main_app.connect_database('../../Desktop/MT Data/Database/')
    return main_app



main_app = main()