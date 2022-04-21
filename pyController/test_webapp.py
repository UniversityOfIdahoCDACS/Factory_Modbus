
from time import sleep
import webapp.webadmin as webadmin


def main():
    """ Main program """
    print("Starting Webapp")
    
    webadmin.start_webapp()
    print("Webapp continuted")

    while True:
        print("tick")
        try:
            sleep(5)
        except KeyboardInterrupt:
            print("main exiting from keyboard interrupt")
            webadmin.stop_webapp()
            exit()


if __name__ == "__main__":
    main()
