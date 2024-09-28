from src.database import Database
from src.gui.app import App


GLOBAL_DATABASE = Database('database.tmp.json', default_data={
    'players': [],
    'tournaments': [],
    'settings': {},
})


def main():
    app = App(GLOBAL_DATABASE)

    app.mainloop()


if __name__ == '__main__':
    main()
