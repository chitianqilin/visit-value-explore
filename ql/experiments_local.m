clear all
do_plot = 0;
optimistic = 0;
long_horizon = 1;
long_horizon_rate = 20000/33;
deep_depth = 50;

for optimistic = [0, 1]
for long_horizon = [0, 1]
% for mdp_name = ["GridworldSparseSmall", "GridworldSparseSimple", "DeepGridworld"] 
% for mdp_name = ["GridworldSparseWall"]
% for mdp_name = ["DeepSea"]
for mdp_name = ["Taxi"]
    for trial = 1 : 20
        fprintf('%d, %d, %s, %d\n', optimistic, long_horizon, mdp_name, trial)
        for alg_name = [ ...
                 "vv_ucb", ...
                  "vv_n", ...
                "ucb1", ...
                 "random", ...
                "egreedy", ...
                 "brlsvi", ...
                "boot_thom", ...
                 "boot", ...
                 "bonus", ...
                ]
            feval(['run_ql_' char(alg_name)])
            save([setting_str '/' char(alg_name) '_' num2str(trial) '.mat'], save_list{:})
            % parsave([setting_str '/' char(alg_name) '_' num2str(trial) '.mat'], save_list)
        end
    end
end
end
end
