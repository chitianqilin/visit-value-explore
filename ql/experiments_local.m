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
        for alg_name = [ ...
               "vv_ucb", ...
                 "vv_n", ...
                "egreedy", ...
                "brlsvi", ...
                "boot", ...
                "bonus", ...
                "random", ...
                "ucb1", ...
                "boot_thom", ...
                ]
            fprintf('optimistic=%d, long_horizon=%d, mdp_name=%s, trial=%d, alg_name=%s\n', ...
                optimistic, long_horizon, mdp_name, trial,alg_name)
            feval(['run_ql_' char(alg_name)])
            save([setting_str '/' char(alg_name) '_' num2str(trial) '.mat'], save_list{:})
            % parsave([setting_str '/' char(alg_name) '_' num2str(trial) '.mat'], save_list)
            %parsave(setting_str, alg_name,gamma_vv, trial, save_list)
        end
%           alg_name = "vv_ucb"
%           run_ql_vv_ucb
%           parsave(setting_str, alg_name,gamma_vv, trial, save_list)
    end
end
end
end

% function parsave(setting_str, alg_name, trial, save_list)
%    save([setting_str '/' char(alg_name) '_' num2str(trial) '.mat'], save_list{:})
% end