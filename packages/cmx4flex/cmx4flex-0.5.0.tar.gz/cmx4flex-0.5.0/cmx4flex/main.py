# Author: Grigori Fursin

import cmind
import sys
import platform
import subprocess
import os

############################################################
def init():

    init = ''
    mode = ''
    if len(sys.argv) > 1:
        init = sys.argv[1]
    if len(sys.argv) > 2:
        mode = sys.argv[2]

    if len(sys.argv) == 1 or init != 'init':
        print ('Usage: cmx4flex init (min)')
        exit(0)

    line = '*'*55

    ############################################################

    # Check if 'git' is installed
    print (line)
    print ('Checking if git is installed ...')

    system = platform.system().lower()

    if system == 'windows':
        c1 = 'git'
        c2 = '--version'
        shell = True
    else:
        c1 = 'which'
        c2 = 'git'
        shell = False

    r = subprocess.call([c1, c2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = shell)

    if r != 0:
        print ('ERROR: git not detected - please install!')
        sys.exit(1)

    print ('')
    print ('[SUCCESS]')

    ############################################################
    cmds = ['cmx pull repo --url=git@github.com:flexaihq/cmx4flex --branch=dev']

    if mode != 'min':
        cmds.append('cmx pull repo --url=git@github.com:flexaihq/cmx4experiments --branch=dev')
        cmds.append('cmx pull repo --url=git@github.com:flexaihq/cmx4assets --branch=dev')

    for cmd in cmds:
        print (line)
        print (f'CMD: {cmd}')

        r = os.system(cmd)
        if r > 0:
            print ('ERROR: CMD failed')
            sys.exit(1)

        print ('')
        print ('[SUCCESS]')

    print (line)
    print ('cmx4flex bootstrapped successfully!')

    sys.exit(0)

###########################################################################
if __name__ == "__main__":
    init()
