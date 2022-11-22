import os

for env in ['Taxi']: # ['GridworldSparseWall', 'GridworldSparseSimple', 'GridworldSparseSmall', 'Taxi', 'DeepGridworld', 'DeepSea50']:
    for var in ['VC_history', 'J_history']:
        text = 'python plot_env.py --env=' + env + ' --var=' + var
        os.system(text)
