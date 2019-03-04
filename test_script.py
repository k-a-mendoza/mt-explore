from mtexplore import Main

# try this
def main():
    main_app = Main()
    main_app.connect_database('../../Desktop/MT Data/Earthscope')
    return main_app


if __name__=='__main__':
    main()
