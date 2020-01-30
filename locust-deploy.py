from deployment_utils import ManifestMaker
import os
import argparse
import yaml
import configparser

def write_deployment(path, contents):
    f = open(path, "w")
    f.write(contents)
    f.close()

def parse_args():

    # Parse any config_file specification
    # We make this parser with add_help=False so that
    # it doesn't parse -h and print help.
    conf_parser = argparse.ArgumentParser(
        description=__doc__, # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Turn off help, so we print all options in response to -h
        add_help=False
        )
    conf_parser.add_argument("-c", "--config-file",
                        help="Specify config file", metavar="CONFIG_FILE")
    args, remaining_argv = conf_parser.parse_known_args()

    defaults = {}

    if args.config_file:
        config = configparser.ConfigParser(inline_comment_prefixes="#", converters={'list': lambda x: [i.strip() for i in x.split()]})
        config.read([args.config_file])
        for key, value in config.items("Defaults"):
            vals = config.getlist("Defaults", key);
            if len(vals) > 1:
                defaults[key] = []
                for v in vals:
                    defaults[key].append(v)
            elif value != "":
                defaults[key] = value

    # Parse rest of arguments
    # Don't suppress add_help here so it will handle -h
    parser = argparse.ArgumentParser(
        # Inherit options from config_parser
        parents=[conf_parser],
        description="Locust cluster manifest generator"
    )

    # add rest of args
    parser.add_argument("-n", "--name", required=True, help="Name of the test cluster artifacts")
    parser.add_argument("-t", "--target_host", required=True, help="Target host to run tests against")
    parser.add_argument("-e", "--env", required=True, help="Test environment")
    parser.add_argument("-S", "--services", nargs='+', required=True, help="Services to test")

    parser.add_argument("-f", "--test_file", required=True, help="The locust file to be used, relative to the github root path")
    parser.add_argument("-r", "--repo", required=True, help="Github repository containing the tests")
    parser.add_argument("-b", "--branch", required=False, help="Github branch containing the tests", default="master")
    parser.add_argument("-ns", "--namespace", required=False, help="Namespace to run the test cluster", default="test")

    parser.add_argument("-s", "--size", required=False, help="Number of workers pods to be created. Default to 3", type=int, default=3)
    parser.add_argument("-o", "--output", required=False, help="Manifest files output", default="./manifests/")

    parser.set_defaults(**defaults)
    # Reset `required` attribute when provided from config file
    for action in parser._actions:
        if action.dest in defaults:
            action.required = False

    try:
        args = parser.parse_args(remaining_argv)
    except:
        print("Missing required args...remember to set them in config file (values.yml) or pass them in yo!!!")
        exit(1)


    return args

########################################
if __name__ == '__main__':

    config = vars(parse_args())
    
    if isinstance(config['services'], list):
        config['services'] = ' '.join(config['services']) #test script only accept space separated string
    
    #print(config)  
    maker = ManifestMaker(config)

    write_deployment(os.path.join(config["output"], config["name"]+"-locust-master.yaml"), maker.master_deployment())
    write_deployment(os.path.join(config["output"], config["name"]+"-locust-master-service.yaml"), maker.master_service())
    write_deployment(os.path.join(config["output"], config["name"]+"-locust-master-service-lb.yaml"), maker.master_service_lb())
    write_deployment(os.path.join(config["output"], config["name"]+"-locust-worker.yaml"), maker.worker_deployment())
