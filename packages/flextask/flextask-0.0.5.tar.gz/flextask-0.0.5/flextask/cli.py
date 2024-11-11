# Flex Task CLI
#
# Written by Grigori Fursin

import cmind
import sys

############################################################
def run_flex_task(argv = None):
    """
    """

    # Access CM
    from cmind.core import CM

    cm = CM()

    if argv is None:
        argv = sys.argv[1:]

    r = cm.x(['run', 'flex.task'] + argv, out='con')

    if r['return']>0 and (cm.output is None or cm.output == 'con'):
        cm.errorx(r)

    sys.exit(r['return'])

###########################################################################
if __name__ == "__main__":
    run_flex_task()
