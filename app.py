from MYLIB.modules.controller import controller
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()  # needed if ever packaged as .exe
    controller()