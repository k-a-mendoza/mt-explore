from mtexplore import Mt_Ex_Main

# try this
def main():
    main_app = Mt_Ex_Main()
    main_app.connect_database('../../Desktop/MT Data/Database/')
    return main_app




if __name__=='__main__':
    main_app = main()