from mtexplore import Main

# try this
def main():
    main_app = Main(debug=False)
    main_app.connect_database('../../Desktop/MT Data/Database/')
    return main_app



main_app = main()